import cv2
import os
import detect
import code_reader as cr


def interval(codes: list) -> tuple:
    l = ans_l = ans_r = 0
    max_len = 0
    cur = 1
    for r in range(len(codes)):
        if r > 0 and codes[r] != codes[r - 1] + 1:
            # 不连续
            cur = 0
            l = r

        cur += 1
        if cur > max_len:
            ans_l, ans_r = l, r
            max_len = cur

    return ans_l, ans_r


names = os.listdir(os.getcwd() + r"\numbers")  # 遍历numbers文件夹下所有

with open("result.txt", 'w') as result:
    for name in names:
        print(name, end=' ')
        target_img = cv2.imread("numbers/" + name)

        # 读取右侧数字
        num_r = detect.code_reader(result, target_img)

        # 读取左侧条码
        code_l = cr.code_reader(target_img)
        # 考虑到底下其他试卷的条码也会露出来，我要检测最长连续条码
        # 这些连续的条码很有可能就是我们想要的
        l, r = interval(code_l)
        code_l = code_l[l:r+1]
        print(code_l)
        print(code_l, file=result)
