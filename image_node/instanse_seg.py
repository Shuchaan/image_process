import cv2
import json
import numpy as np
import os
import random
import cv2
from detectron2 import model_zoo
from detectron2.utils.visualizer import ColorMode
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.engine import DefaultTrainer
from detectron2.structures import BoxMode
from detectron2.utils.visualizer import Visualizer
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader


class Segmantation_Model:
    def __init__(self, xyxy=(0.0, 0.0, 0.0, 0.0), name='', conf=0.0):
        # self.cfg = get_cfg()
        # self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  #クラス数
        # self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")) #model選択
        # self.cfg.MODEL.WEIGHTS = "/home/suke/toms_ws/instanse_seg_tools/output/model_final.pth"
        # self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.2
        # self.cfg.MODEL.DEVICE = "cuda" #cpu or cuda
        # self.predictor = DefaultPredictor(self.cfg)

        #サンプルデータ
        self.cfg = get_cfg()
        self.cfg.MODEL.DEVICE = "cuda"
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        self.predictor = DefaultPredictor(self.cfg)

    def detact(self,img):
        outputs = self.predictor(img)
        box_result=self.obj_box(outputs)
        bool_array = outputs["instances"]._fields["pred_masks"]
        v = Visualizer(img[:, :, ::-1],MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.0)
        outputs = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        #objects = outputs["instances"]._fields["pred_classes"].tensor.cpu().numpy():
        return outputs.get_image(),box_result,bool_array
       



    def obj_box(self,outputs):
        bounding_boxes = outputs["instances"]._fields["pred_boxes"].tensor.cpu().numpy()
        box_result=[]
        for i in range(len(bounding_boxes)):
            # 左上座標
            center_x = (bounding_boxes[i][0]+bounding_boxes[i][2])/2
            # 右下座標
            center_y = (bounding_boxes[i][1]+bounding_boxes[i][3])/2
            box_result.append([center_x,center_y])
        
        return box_result

def main():
    seg=Segmantation_Model()
    device_id = 0
    cap = cv2.VideoCapture(device_id)
    while True:
        # 1フレームずつ取得する。
        ret, frame = cap.read()
        if not ret:
            break  # 取得に失敗した場合
        seg.detact(frame)

if __name__ == '__main__':
    main()
