import pyrealsense2 as rs
import numpy as np
import cv2


class Realsense_Module():
    WIDTH = 640
    HEIGHT = 480
    FPS = 30
    def __init__(self) :
        #RGBとdepthの初期設定
        self.conf = rs.config()
        #解像度はいくつか選択できる
        self.conf.enable_stream(rs.stream.color, self.WIDTH, self.HEIGHT, rs.format.bgr8, self.FPS)
        self.conf.enable_stream(rs.stream.depth, self.WIDTH, self.HEIGHT, rs.format.z16, self.FPS)
        #stream開始
        self.pipe = rs.pipeline()
        self.profile = self.pipe.start(self.conf)
        #Alignオブジェクト生成(位置合わせのオブジェクト)
        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)
        self.depth_intrinsics = rs.video_stream_profile(self.profile.get_stream(rs.stream.depth)).get_intrinsics()
        self.color_intrinsics = rs.video_stream_profile(self.profile.get_stream(rs.stream.color)).get_intrinsics()

    def obtain_camera_prame(self):
        R=[self.color_intrinsics.fx,
           self.color_intrinsics.fy,
           self.WIDTH/2,
           self.HEIGHT/2
           ]
        return R

    def obtain_cam_image(self) :
        try :
            #フレーム待ち(これがないとデータの取得にエラーが出ることがあるらしい）
            frames = self.pipe.wait_for_frames()
            # frameデータを取得
            aligned_frames = self.align.process(frames)
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()
            depth_frame = self.depth_filter(depth_frame)
            if not depth_frame or not color_frame:
                return
            #dataがunit16の形で入っているのでnumpy配列に変更
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            img_flag=True
            return color_image,depth_image,img_flag
        except Exception as e :
            print(e)
            color_image=None
            depth_image=None
            img_flag=False
            return color_image,depth_image,img_flag

    def depth_filter(self,depth_frame):
        #TODO recursive median filterを入れる
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
        # filterをかける
        filter_frame = decimate.process(depth_frame)
        filter_frame = depth_to_disparity.process(filter_frame)
        filter_frame = spatial.process(filter_frame)
        filter_frame = disparity_to_depth.process(filter_frame)
        filter_frame = hole_filling.process(filter_frame)
        result_frame = filter_frame.as_depth_frame()
        return result_frame

    def limit_area(self,color_image,depth_image):
        left=0
        right=600
        top=0
        bottom=500
        lim_colorimage=color_image[left:right,top:bottom,:]
        lim_depth_image=depth_image[left:right,top:bottom]
        return lim_colorimage,lim_depth_image

    def shutdown(self):
        self.pipe.stop()

    def save_data():  
        #画像を保存用(ある周期ごとにdataを保存したい)
        pass

