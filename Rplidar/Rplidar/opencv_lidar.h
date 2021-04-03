#include <iostream>
#include <cmath>

#include <opencv2\opencv.hpp>
#include <highgui.hpp> 
#include "opencv2/imgproc/imgproc_c.h"

#include "rplidar.h" //RPLIDAR standard sdk

using namespace std;


//定义opencv显示界面大小，rplidar最远距离是12m，所以方便计算，画布取12的倍数
static int RadarImageWdith = 600;
static int RadarImageHeight = 600;
static int halfWidth = RadarImageWdith / 2;
static int halfHeight = RadarImageHeight / 2;

//实际距离测量节点
struct scanDot {
    _u16  angle;
    _u32  dist;
    _u8   quality;
};
//雷达坐标系绘图节点
struct drawDot {
    int  x;
    int  y;
    _u8  quality;
};

class LidarImage
{
public:
    LidarImage(void);
    ~LidarImage(void);

    vector<scanDot> scan_data; //保存每扫描一周的雷达实际数据
    vector<drawDot> draw_data; //保存在OPENCV坐标系的节点数据

    void DataConversion(rplidar_response_measurement_node_hq_t *buffer, size_t count);
    void Draw(cv::Mat& RadarImage);
    bool IS_Near(const drawDot &former, const drawDot &latter);
};
