import numpy as np
from datetime import datetime

def cali_money(target, base_liu, base_li, ex_out_liu, ex_out_li):
    # 分配比例加权参数
    ALPHA = 0.4
    BETA = 0.7
    # 初始化参数列表
    cur_liu = base_liu
    cur_li = base_li
    money_liu_list, money_li_list = [], []
    out_liu_list, out_li_list = [], []
    money_liu_list.append(cur_liu)
    money_li_list.append(cur_li)
    
    # 第一次分配
    k1 = cur_liu / (cur_liu + cur_li) # 分配比例系数
    k1 = np.clip(k1, 0.25, 0.75) # 限制比例系数范围

    out_liu = target * ALPHA * k1
    out_li = target * ALPHA * (1 - k1)
    cur_liu = cur_liu - ex_out_liu # 第一次分配后扣除额外支出
    cur_li = cur_li - ex_out_li # 第一次分配后扣除额外支出
    money_liu_list.append(cur_liu)
    money_li_list.append(cur_li)
    cur_liu = cur_liu - out_liu
    cur_li = cur_li - out_li
    money_liu_list.append(cur_liu)
    money_li_list.append(cur_li)
    out_liu_list.append(out_liu)
    out_li_list.append(out_li)

    # 第二次分配
    k2 = cur_liu / (cur_liu + cur_li) # 分配比例系数
    k2 = (np.clip(k2, 0.25, 0.75) * BETA) + (k1 * (1-BETA)) # 限制比例系数范围

    out_liu = target * (1-ALPHA) * k2
    out_li = target * (1-ALPHA) * (1 - k2)
    cur_liu = cur_liu - out_liu
    cur_li = cur_li - out_li
    money_liu_list.append(cur_liu)
    money_li_list.append(cur_li)
    out_liu_list.append(out_liu)
    out_li_list.append(out_li)
    

    total_out_liu = sum(out_liu_list) 
    total_out_li = sum(out_li_list)

    k_out_list = []
    for i in range(len(out_liu_list)):
        k_out = out_liu_list[i] / out_li_list[i]
        k_out_list.append(k_out)
    k_out_list.append(total_out_liu / total_out_li)

    return {"param": {"分配权重系数 ALPHA": ALPHA, "比例加权系数 BETA": BETA}, 
            "money_liu_list": money_liu_list, "money_li_list": money_li_list,
            "out_liu_list": out_liu_list, "out_li_list": out_li_list,
            "total_out_liu": total_out_liu, "total_out_li": total_out_li,
            "k_out_list": k_out_list}

def save_to_txt(data):
    today = datetime.today()
    filename = f"money_dispatch_{today.year}_{today.month:02d}_{today.day:02d}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for k,v in data.items():
            file.write(f"{k}: {v}\n")
    print(f"数据已成功保存到 {filename} 文件")
if __name__ == "__main__":
    target = 6000
    base_liu = 20000
    base_li = 8000
    ex_out_liu = 2000 +12000
    ex_out_li = 1500
    
    res = cali_money(target=target, 
               base_liu=base_liu, ex_out_liu=ex_out_liu, 
               base_li=base_li, ex_out_li=ex_out_li)
    print(res)
    # 保存为txt文件
    save_to_txt(res)

    
    