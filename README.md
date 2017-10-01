## 1.项目简介
* 实现目标：对桥上过往的车辆能够实时监控(用bounding box标记出来），如果有车辆在桥上停下来，那么对其进行计时，超过一定时间，则自动报警。
* 核心方法：考虑到实时性，这个项目没有使用深度学习的方法，而是使用了传统的帧差法，发现效果还不错，能够满足要求，但是如果要对车辆进行唯一的id标记并识别的话，
那么这个方法得到效果并不是很好。

## 2.运行环境
* ubuntu 14.04 或是 windows下都可以。
* 最好安装GPU和安转CUDA，CPU下也可以运行，但是比较慢。
* 编程语言是Python3,python推荐安装Anaconda,需要安装的python库：
    * opencv
    * numpy

## 3.使用方式

* 将项目clone到你的本地：`git clone https://github.com/Lihit/VehicleDetection.git`
* 到下载后的文件夹`：cd VehicleDetection`。
* 打开终端，运行`python main.py`,即可看到效果。

## 4.运行结果
![image](https://github.com/Lihit/VehicleDetection/blob/master/resource/frame_003.png)<br>
![image](https://github.com/Lihit/VehicleDetection/blob/master/resource/frame_004.png)<br>
![image](https://github.com/Lihit/VehicleDetection/blob/master/resource/frame_005.png)<br>
![image](https://github.com/Lihit/VehicleDetection/blob/master/resource/frame_006.png)<br>
![image](https://github.com/Lihit/VehicleDetection/blob/master/resource/frame_007.png)<br>

## 5.文件结构
>`VehicleDetection`：项目根路径<br>
  >>`FindBackFrame/`:找寻背景帧的算法<br>
  >>`MotionDetection/`:图像处理算法和帧差法等<br>
  >>`test/`:测试用，不用看<br>
  >>`resource/`:一些外部的资源，包括视频样本，报警音频等<br>
  >>`main.py`：程序入口<br>
