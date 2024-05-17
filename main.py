import cv2
from process import pre_process
import os


def match_num(roi) -> tuple:
    global digits
    scores: list = []
    for i in digits:
        ans = cv2.matchTemplate(roi, digits[i], cv2.TM_CCOEFF_NORMED)
        ans = cv2.minMaxLoc(ans)[1]
        scores.append((ans, i))
    return max(scores)


nums_img = cv2.imread("nums.png", -1)
bin_num, nums = pre_process(nums_img)
nums.sort(key=lambda x: x[0])
digits = {}
for i, num in enumerate(nums):
    x, y, w, h = num
    region = bin_num[y:y + h, x:x + w]
    digits[i] = cv2.resize(region, (50, 50))

names = os.listdir(os.getcwd()+r"\numbers")  # 遍历numbers文件夹下所有

with open("result.txt", 'w') as result:
    for name in names:
        print(name, end=' ')
        target_img = cv2.imread("numbers/" + name)
        y1, y2 = int(target_img.shape[0] / 20), int(target_img.shape[0] / 2)
        x1 = int(target_img.shape[1] * 3 / 4)
        zone = target_img[y1:y2, x1:]

        bin_zone, target = pre_process(zone, True)
        target.sort(key=lambda x: x[0])

        roi = []  # region of interest

        for rect in target:
            x, y, w, h = rect
            # 注意！这是相对于切片的坐标，不是整个照片的坐标！！！

            LW = w / float(h)  # 形状，太离谱的肯定不是数字
            if w < 20 or w > 80 or h < 60 or h > 90 or LW > 0.82 or LW < 0.28:  # 检查大小、形状
                # 需要排除的：密封条上的小斑点-太小
                # 黑色背景-一般比较大
                continue

            region = bin_zone[y:y + h, x:x + w]
            ans = match_num(cv2.resize(region, (50, 50)))
            if ans[0] > 0.5:
                roi.append(ans[1])

        print(roi)  # 这个版本没有调试语句，detect.py是用来调试的
        print(name[:-4], roi, file=result)  # 输出时删去后缀
