import cv2
import numpy as np


def pre_process(original) -> list:
    """输入图片->灰度化->二值化->轮廓->最小外接"""
    p1 = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)  # =蓝绿红 to gray
    p2 = cv2.threshold(p1, 100, 255, cv2.THRESH_BINARY_INV)[1]  # 为什么不INV就会出错？怪了
    p3 = cv2.findContours(p2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    return p2, [cv2.boundingRect(i) for i in p3]


nums_img = cv2.imread("numbers/nums.png", -1)
bin_num, nums = pre_process(nums_img)
nums.sort(key=lambda x: x[0])
digits = {}
for i, num in enumerate(nums):
    x, y, w, h = num
    region = bin_num[y:y + h, x:x + w]
    digits[i] = cv2.resize(region, (50, 50))

target_img = cv2.imread("test_pic1.jpg")
zone = target_img[100:800, 3500:]
bin_zone, target = pre_process(zone)
target.sort(key=lambda x: x[0])


def match_num(roi) -> tuple:
    global digits
    scores: list = []
    for i in digits:
        ans = cv2.matchTemplate(roi, digits[i], cv2.TM_CCOEFF_NORMED)
        ans = cv2.minMaxLoc(ans)[1]
        scores.append((ans, i))
    return max(scores)


roi = []  # region of interest

for rect in target:
    x, y, w, h = rect
    # 注意！这是相对于切片的坐标，不是整个照片的坐标！！！
    LW = rect[2] / float(rect[3])
    if LW > 0.82 or LW < 0.28:  # 看形状，太离谱的肯定不是数字
        continue
    cv2.rectangle(zone, (x, y), (x + w, y + h), (0, 0, 255), 10)
    region = bin_zone[y:y + h, x:x + w]
    ans = match_num(cv2.resize(region, (50, 50)))
    if ans[0] > 0.5:
        roi.append(ans[1])

print(roi)

cv2.imshow("cont", zone)
cv2.waitKey()
