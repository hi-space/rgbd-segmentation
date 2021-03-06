import enum
import subprocess
import os


class CameraConfig:
    class CameraMode(enum.Enum):
        WEBCAM = 0
        REALSENSE = 1
        RGBTOF = 2
        
    camera_mode = CameraMode.REALSENSE

class SegConfig:
    # segmentation
    NYU_RGB_NO_PRETRAIN = "segmentation/models/nyu_rgb_no_pretrain"
    NYU_RGB_IMAGENET_PRETRAIN = "segmentation/models/nyu_rgb_imagenet_pretrain"
    NYU_RGB_SCENENET_PRETRAIN = "segmentation/models/nyu_rgb_scenenet_pretrain"
    NYU_RGBD_NO_PRETRAIN = "segmentation/models/nyu_rgbd_no_pretrain"
    NYU_RGBD_SCENENET_PRETRAIN = "segmentation/models/nyu_rgbd_scenenet_pretrain"

    SUN_RGB_NO_PRETRAIN = "segmentation/models/sun_rgb_no_pretrain"
    SUN_RGB_IMAGENET_PRETRAIN = "segmentation/models/sun_rgb_imagenet_pretrain"
    SUN_RGB_SCENENET_PRETRAIN = "segmentation/models/sun_rgb_scenenet_pretrain"
    SUN_RGBD_NO_PRETRAIN = "segmentation/models/sun_rgbd_no_pretrain"
    SUN_RGBD_SCENENET_PRETRAIN = "segmentation/models/sun_rgbd_scenenet_pretrain"

    on_gpu = True
    eval_mode = True


class TrackingConfig:
    on_gpu = True
    # config_detection = "tracking/configs/yolov3_tiny.yaml"
    # config_detection = "tracking/configs/yolov3.yaml"
    config_detection = "tracking/configs/yolov3-beammice.yaml"
    config_deepsort = "tracking/configs/deep_sort.yaml"

class RedisConfig:

    @property
    def conf(self):
        class Config:
            topic_for_visualizer = "3d-vis"
        return Config
