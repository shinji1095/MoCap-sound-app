# -*- coding: utf-8 -*-
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty


import os
import csv
import cv2
import numpy as np
import pyrealsense2 as rs
import matplotlib.pyplot as plt
import utils.MotiveControll as motive
from utils.utils import get_rectangle_elem, get_hist
from datetime import datetime

class DepthPreview(Image):
    hist_mean = NumericProperty(0)
    def __init__(self, **kwargs):
        super(DepthPreview, self).__init__(**kwargs)

        # /*-----------------------------------------------
        #    Initialize Depth Camera
        # ------------------------------------------------*/
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)
        while not self.pipeline.wait_for_frames(): 
            pass

        align_to = rs.stream.color
        self.align = rs.align(align_to)

        # /*-----------------------------------------------
        #    Filename
        # ------------------------------------------------*/
        self.baseDir = ''

        # 更新スケジュールとコールバックの指定
        Clock.schedule_interval(self.update, 1.0/30.0)

    def update(self, dt):
        # 基本的にここでOpenCV周りの処理を行なってtextureを更新する
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        
        aligned_frames = self.align.process(frames)
        depth_frame =  aligned_frames.get_depth_frame()
        # /*-----------------------------------------------
        #    フィルタリング
        # ------------------------------------------------*/
        # decimarion_filterのパラメータ
        decimate = rs.decimation_filter()
        decimate.set_option(rs.option.filter_magnitude, 1)
        # spatial_filterのパラメータ
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.filter_magnitude, 1)
        spatial.set_option(rs.option.filter_smooth_alpha, 0.25)
        spatial.set_option(rs.option.filter_smooth_delta, 50)
        # hole_filling_filterのパラメータ
        hole_filling = rs.hole_filling_filter()
        # disparity
        depth_to_disparity = rs.disparity_transform(True)
        disparity_to_depth = rs.disparity_transform(False)

        # 省略(フレーム取得処理)

        # filterをかける
        filter_frame = decimate.process(depth_frame)
        filter_frame = depth_to_disparity.process(filter_frame)
        filter_frame = spatial.process(filter_frame)
        filter_frame = disparity_to_depth.process(filter_frame)
        filter_frame = hole_filling.process(filter_frame)
        depth_frame = filter_frame.as_depth_frame()

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        depth_colormap_dim = depth_colormap.shape

        # /*-----------------------------------------------
        #    距離情報を取得
        # ------------------------------------------------*/
        dist = depth_frame.get_distance(depth_colormap_dim[1]//2, depth_colormap_dim[0]//2)

        # /*-----------------------------------------------
        #    距離の描画
        # ------------------------------------------------*/
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.0
        font_thickness = 2
        cv2.putText(depth_colormap, str(np.round(dist, 2)), 
                    (depth_colormap_dim[1]//2, depth_colormap_dim[0]//2), font, font_scale, (0, 0, 255), font_thickness, cv2.LINE_AA)


        # /*-----------------------------------------------
        #    矩形の描画
        # ------------------------------------------------*/
        x1, x2, y1, y2 = get_rectangle_elem(depth_colormap_dim, 100, 150)
        cv2.rectangle(depth_colormap, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # /*-----------------------------------------------
        #    ヒストグラムの描画
        # ------------------------------------------------*/
        # プロット
        hist_data = np.ravel(depth_colormap[x1:x2, y1:y2])
        hist = get_hist(hist_data*100)
        hist = cv2.resize(hist, (depth_colormap_dim[1], depth_colormap_dim[0]))

        # /*-----------------------------------------------
        #    画像の表示
        # ------------------------------------------------*/
        img = np.hstack((depth_colormap, hist))
        # img = cv2.resize(img, (depth_colormap_dim[1], depth_colormap_dim[0]))
        # self.ids.hist_label.text = str(np.mean(hist_data))
        print(dist)

        img = cv2.flip(img, 0)
        texture1 = Texture.create(size=(depth_colormap_dim[1]*2, depth_colormap_dim[0]), colorfmt='bgr')
        texture1.blit_buffer(img.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture1
