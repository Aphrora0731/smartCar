#pragma once
#include "opencv_lidar.h"
#define PI 3.141592653
#define scale  25
LidarImage::LidarImage(void)
{
}

LidarImage::~LidarImage(void)
{
}

//判断两点是否逼近以画直线
bool LidarImage::IS_Near(const drawDot &last, const drawDot &current)
{
    int x, y, zz;
    x = last.x-current.x;
    y = last.y-current.y;
    zz = x * x + y * y;
    if (zz < 640000/(scale*scale))
        return true;
    return false;
}
//将扫面的原始数据转化为实际距离和角度
//将实际距离与角度转化为雷达坐标系的点坐标
void LidarImage::DataConversion(rplidar_response_measurement_node_hq_t* buffer, size_t count)
{
    scan_data.clear();
    draw_data.clear();
    for (int pos = 0; pos < (int)count; ++pos) {
        scanDot sdot;
        //为画图准备 无效点则不放入scan_data
        if (!buffer[pos].dist_mm_q2) continue;

        sdot.quality = buffer[pos].quality   ;
        sdot.angle = (buffer[pos].angle_z_q14 * 90.f / (1 << 14));
        sdot.dist = buffer[pos].dist_mm_q2/4.0f;
        scan_data.push_back(sdot);

    
        drawDot ddot;

        double theta, rho;
        theta = sdot.angle * PI / 180;
        rho = sdot.dist;

        ddot.x = (int)(rho * sin(theta) / scale) + halfWidth;
        ddot.y = (int)(-rho * cos(theta)/scale)+ halfHeight;
        draw_data.push_back(ddot);
    }
}
//将扫描点映射到画布上

void LidarImage::Draw(cv::Mat& RadarImage) {

    int x, y;
    for (int i = 0; i < draw_data.size(); i++)
    {
        x = draw_data[i].x;
        y = draw_data[i].y;

        cv::Scalar s; 
        //5米以外 绿色显示 
        if (scan_data[i].dist > 5000) 
             s=cv::Scalar(0, 255, 0);
        //5米以内 红色显示
        else
             s=cv::Scalar(255, 0, 0);


        int thickth;
        if (scan_data[i].quality > 100)
            thickth = 3;
        else
            thickth = 1;

        circle(RadarImage, cv::Point(x, y), 1, s, thickth,CV_AA);

        //判断是否需要画直线
        int ilast = (i + draw_data.size() - 1) % draw_data.size();
        if (IS_Near(draw_data[ilast], draw_data[i]))
        {
            int xlast = draw_data[ilast].x;
            int ylast = draw_data[ilast].y;
            line(RadarImage, cv::Point(xlast, ylast), cv::Point(x, y), s, thickth, CV_AA);
        }

    }
}