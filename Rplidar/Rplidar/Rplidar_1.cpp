
#include"Rplidar_1.h"



bool checkRPLIDARHealth(RPlidarDriver* drv)
{
    u_result     op_result;
    rplidar_response_device_health_t healthinfo;

    op_result = drv->getHealth(healthinfo);
    if (IS_OK(op_result)) { // the macro IS_OK is the preperred way to judge whether the operation is succeed.
        printf("雷达健康状态 : %d\n", healthinfo.status);
        if (healthinfo.status == RPLIDAR_STATUS_ERROR) {
            fprintf(stderr, "错误雷达中心受损请重启设备.\n");
            // enable the following code if you want rplidar to be reboot by software
            //drv->reset();
            return false;
        }
        else {
            return true;
        }

    }
    else {
        fprintf(stderr, "Error, cannot retrieve the lidar health code: %x\n", op_result);
        return false;
    }
}


    
bool Rplidar_connect(RPlidarDriver* drv)
{
    //drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
    if (!drv) {
        fprintf(stderr, "insufficent memory, exit\n");
        exit(-2);
    }

    //make connection
    if (IS_FAIL(drv->connect("\\\\.\\com3", 115200))) {
        fprintf(stderr, "Error, cannot bind to the specified serial port %s.\n"
            , "\\\\.\\com3");
        RPlidarDriver::DisposeDriver(drv);
        return false;
    }
    cout << "debug" << endl;
    drv->startMotor();

    // check health
    if (!checkRPLIDARHealth(drv)) {
        RPlidarDriver::DisposeDriver(drv);
        return false;
    }
    return true;
}
    


cv::Mat Rplidar_getImage(LidarImage &lidarImage, RPlidarDriver* drv) {
    u_result     op_result;

    //creat opencv image
    cv::Mat RadarImage(RadarImageWdith, RadarImageHeight, CV_8UC3);

    // start typical scan
    RplidarScanMode scanMode;
    drv->startScan(false,true,0,&scanMode);


    rplidar_response_measurement_node_hq_t nodes[720];
    size_t   count = _countof(nodes);
    op_result = drv->grabScanDataHq(nodes, count);
    drv->ascendScanData(nodes, count);

    if (IS_OK(op_result)) {
        //变为纯黑背景
        RadarImage.setTo(0);
        //中间画一个点
        circle(RadarImage, cv::Point(halfWidth, halfHeight), 7, cv::Scalar(255, 255, 255), -1, CV_AA);

        lidarImage.DataConversion(nodes, count);
        lidarImage.Draw(RadarImage);
        return RadarImage;
    }
} 