import os
import re

# 匹配选项组。
strinfo1 = re.compile(r".*\\task.*\n\s+.*\n\s+.*\n\s+.*")

# 匹配单个选项。
strinfo2 = re.compile(r"\s+\\task\s+")

# 匹配答案。
strinfo3 = re.compile(r"A|B|C|D")

# 答案临时存储列表。
aws_list = list()


# 处理阅读理解。
def deal_read(etype, years):
    for i in range(1, 5):
        f1 = open(f"{etype}/{years}/read/options{i}.tex",
                  "r+", encoding="utf-8")
        f1_read = f1.read()
        f2 = open(f"{etype}/{years}/read/read{i}_answer.tex",
                  "r+", encoding="utf-8")
        deal_aws(f2, "r")
        new_f = re.sub(strinfo1, deal_options, f1_read)
        deal_aws(f2, "w")
        f1.seek(0)
        f1.write(new_f)
        f1.close()
        f2.close()


# 处理完型填空。
def deal_cloze(etype, years):
    f1 = open(f"{etype}/{years}/cloze/options.tex", "r+", encoding="utf-8")
    f1_read = f1.read()
    f2 = open(f"{etype}/{years}/cloze/answer.tex", "r+", encoding="utf-8")
    deal_aws(f2, "r")
    new_f = re.sub(strinfo1, deal_options, f1_read)
    deal_aws(f2, "w")
    f1.seek(0)
    f1.write(new_f)
    f1.close()
    f2.close()


# 提取原答案或写入新答案。
def deal_aws(f, mode_):
    global aws_list
    f.seek(0)
    f_read = f.read()
    if mode_ == "r":
        res = re.findall(strinfo3, f_read)
        aws_list += res
    elif mode_ == "w":
        res = re.sub(strinfo3, lambda _: aws_list.pop(0), f_read)
        print(res)
        f.seek(0)
        f.write(res)


# 处理选项，打乱选项，并将记录新答案。
def deal_options(matched):
    global aws_list
    res = re.split(strinfo2, matched.group())
    # del res[0]
    c_res_num = ord(aws_list.pop(0))-64
    c_res = res.pop(c_res_num)
    new_res = list()
    a = get_random()
    for ii in a:
        new_res.append(res[ii+1])
    right_res_num = ord(os.urandom(1)) % 4
    new_res.insert(right_res_num, c_res)
    aws_list.append(chr(right_res_num+65))
    nr = ""
    for iii in new_res:
        nr = nr + "\t\\task " + iii + "\n"
    return nr[:-1]


# 获得随机数。
def get_random():
    res = set()
    res_ = list()
    while len(res) < 3:
        i = ord(os.urandom(1)) % 3
        if i in res:
            pass
        else:
            res.add(i)
            res_.append(i)
    return res_


def run_201(years=2005):
    if years == 2024:
        return
    deal_cloze(201, years)
    deal_read(201, years)
    return run_201(years+1)


def run_204(years=2010):
    if years == 2024:
        return
    deal_cloze(204, years)
    deal_read(204, years)
    return run_204(years+1)


if __name__ == "__main__":
    # run_201(2023)
    # run_204(2023)
    run_201()
    run_204()
    print("完成")
