import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_rectangle_elem(depth_colormap_dim, *rect):
    center_x, center_y = depth_colormap_dim[1]//2, depth_colormap_dim[0]//2
    rect_width, rect_height = rect[0], rect[1]
    x1 = center_x - rect_width // 2
    y1 = center_y - rect_height // 2
    x2 = center_x + rect_width // 2
    y2 = center_y + rect_height // 2

    return x1, x2, y1, y2

def get_hist(data):
    hist, bins = np.histogram(data, bins=10)

# プロット
    plt.hist(data, bins=10)

    # プロットしたグラフを画像データとして取得
    fig = plt.gcf()
    fig.canvas.draw()

    # 画像データをndarray形式に変換
    img = np.array(fig.canvas.renderer._renderer)

    # ウィンドウを閉じる
    plt.close()
    # imgの形状を(height, width, channels)に変換
    return img[:, :, :3]
    