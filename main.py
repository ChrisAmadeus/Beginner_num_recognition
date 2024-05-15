import cv2
from process import pre_process


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

name = input()
target_img = cv2.imread("numbers/" + name + ".jpg")
zone = target_img[100:800, 3300:]

bin_zone, target = pre_process(zone, True)
target.sort(key=lambda x: x[0])

roi = []  # region of interest
cv2.imshow("bin", bin_zone)
for rect in target:
    x, y, w, h = rect
    # 注意！这是相对于切片的坐标，不是整个照片的坐标！！！

    LW = rect[2] / float(rect[3])  # 形状，太离谱的肯定不是数字
    if rect[2] < 10 or rect[3] < 10 or LW > 0.82 or LW < 0.28:  # 检查大小、形状
        continue

    cv2.rectangle(zone, (x, y), (x + w, y + h), (0, 0, 255), 10)
    region = bin_zone[y:y + h, x:x + w]
    ans = match_num(cv2.resize(region, (50, 50)))
    if ans[0] > 0.5:
        roi.append(ans[1])

print(roi)

cv2.imshow("cont", zone)
cv2.waitKey()
