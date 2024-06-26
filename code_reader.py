import cv2
import pyzbar.pyzbar as zb


def code_reader(target_img):
    y1 = int(target_img.shape[0] / 3)
    x1 = int(target_img.shape[1] * 2 / 3)
    zone = target_img[y1:, 200:x1]

    # 排除光照影响
    zone = cv2.boxFilter(zone, -1, (5, 5), normalize=True)
    # cv2.imshow("grey", zone[500:])
    # cv2.waitKey()

    # 识别
    codes = zb.decode(zone)

    # print(file_name + ":", file=result, end=' ')
    # print(file_name + ":", end=' ')
    ans = []
    for code in codes:
        code_info = code.data.decode("utf-8")
        if len(code_info) < 15:  # 不要最上边15位的长条码
            ans.append(int(code_info))
    ans.sort()
    return ans
