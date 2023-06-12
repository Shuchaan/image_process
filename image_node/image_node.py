import rclpy  # ROS2のPythonモジュールをインポート
from rclpy.node import Node 
from std_msgs.msg import String ,Bool
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import Image
from std_msgs.msg import Int64
from cv_bridge import CvBridge, CvBridgeError
import math
import sys
import cv2

import time
sys.path.append("/home/suke/toms_ws/src/image_node/image_node")
from realsense_setup import Realsense_Module
from utils import Coordinate_Transformation,Maturity_Judgment
from instanse_seg  import Segmantation_Model

class Image_Processing(Node):  
    def __init__(self):
        super().__init__('image_node') 
        timer_period = 0.01 
        self.create_timer(timer_period , self.node_callback)
        self.realsense_module=Realsense_Module()
        self.R = self.realsense_module.obtain_camera_prame()
        self.seg=Segmantation_Model()
        self.transform=Coordinate_Transformation(self.R)
        self.mature_juge=Maturity_Judgment()
        
    
    def node_callback(self):
        color_image,depth_image,img_flag=self.realsense_module.obtain_cam_image()
        outputs,box_result,bool_array = self.seg.detact(color_image) 
        #zも入れたい box result1の中に
        #self.transform.transformation(box_result)
        if img_flag :
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', outputs)
            cv2.waitKey(1)
            #map関数かけてもいいかも
            #self.detect(color_image,depth_image)
            #self.transform.transformation()
            #self.mature_juge.judgment()
            

    def detect(self,color_image,depth_image):
        detect_flag = False
        return detect_flag
            

def main():
    rclpy.init() 
    node=Image_Processing() 
    try :
        rclpy.spin(node) 
        print("image_node")
        # 制御周期
        
    except KeyboardInterrupt :
        print("Ctrl+Cが入力されました")  
        print("プログラム終了")  
    rclpy.shutdown() # rclpyモジュールの終了処理   



if __name__ == '__main__':
    main()
