import cv2
# 预处理


def pre_process(original, erosion=False) -> tuple:
    """输入图片->灰度化->二值化->轮廓->最小外接"""
    p1 = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)  # =蓝绿红 to gray

    # 因findContours 检测黑底白字的物体，所以要选择反转的二值化THRESH_BINARY_INV
    p2 = cv2.threshold(p1, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]  # OTSU均值化
    # OTSU会把所有的灰度画成统计图，统计图会有两个高峰（黑&白），算法会在中间找到合适的阈值

    if erosion:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))  # 侵蚀
        # 5*5太大了，4*4又擦不干净
        p2 = cv2.erode(p2, kernel, iterations=1)
        p2 = cv2.dilate(p2, kernel, iterations=1)

    p3 = cv2.findContours(p2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    return p2, [cv2.boundingRect(i) for i in p3]
