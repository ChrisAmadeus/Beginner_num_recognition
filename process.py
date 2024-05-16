import cv2
# 预处理


def pre_process(original, erosion=False) -> tuple:
    """输入图片->灰度化->二值化->轮廓->最小外接"""
    p1 = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)  # =蓝绿红 to gray
    p2 = cv2.threshold(p1, 120, 255, cv2.THRESH_BINARY_INV)[1]  # 为什么不INV就会出错？怪了

    if erosion:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))  # 侵蚀
        # 5*5太大了，4*4又擦不干净
        p2 = cv2.erode(p2, kernel, iterations=1)
        p2 = cv2.dilate(p2, kernel, iterations=1)

    p3 = cv2.findContours(p2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    return p2, [cv2.boundingRect(i) for i in p3]
