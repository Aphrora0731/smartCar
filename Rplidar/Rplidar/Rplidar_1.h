#include <stdio.h>
#include <stdlib.h>

//#include "rplidar.h" //RPLIDAR standard sdk, all-in-one header
#include "opencv_lidar.h"
#include <iostream>
#include <cmath>
#include "io.h"
//#include <boost/python.hpp>

#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

using namespace rp::standalone::rplidar;


bool checkRPLIDARHealth(RPlidarDriver* drv);
bool Rplidar_connect(RPlidarDriver* drv);
cv::Mat Rplidar_getImage(LidarImage& lidarImage, RPlidarDriver* drv);
char preDetection(LidarImage& lidarImage);
