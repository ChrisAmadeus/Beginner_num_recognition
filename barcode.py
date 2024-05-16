import cv2
import numpy as np
import zxing as zx

# 读取目标文件名
with open("input.txt", 'r') as f:
    names = f.readlines()


def find_code(zone) -> list:
    gray = cv2.cvtColor(zone, cv2.COLOR_BGR2GRAY)
    black = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = np.ones((5, 3))
    eroded = cv2.erode(black, kernel, iterations=1)
    kernel = np.ones((10, 20))
    dilated = cv2.dilate(eroded, kernel, iterations=1)

    cv2.imshow("1", dilated)
    cv2.waitKey()

    contours = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    return [cv2.boundingRect(i) for i in contours]


# 结果写进res里
with open("result.txt", 'w') as res:
    reader = zx.BarCodeReader()
    for name in names:
        target_img = cv2.imread("numbers/" + name[:-1] + ".jpg")
        y1 = int(target_img.shape[0] / 2)
        x1 = int(target_img.shape[1] /2)
        zone = target_img[y1:, 200:x1]
        zone1 = zone.copy()

        # 找条码
        rects = find_code(zone)
        rects.sort(key=lambda x: x[0])
        # 保存条码
        bars = 0
        for rect in rects:
            x, y, w, h = rect
            if 100 < h < 400 and w > 300 and x > 2 and x + w + 2 < zone.shape[1] and y > 2 and y + h + 2 < zone.shape[0]:
                cv2.rectangle(zone1, (x, y), (x + w, y + h), (0, 0, 255), 2)

                cv2.imwrite("./zones/zone" + str(bars) + ".png", zone[y - 2:y + h + 2, x - 2:x + w + 2])
                bars += 1

        cv2.imshow("bar", zone1)
        cv2.waitKey(4)

        # 读写
        for i in range(bars):
            result = reader.decode("./zones/zone" + str(i) + ".png")
            print(result.raw, file=res, end=' ')
        print(name, file=res)
