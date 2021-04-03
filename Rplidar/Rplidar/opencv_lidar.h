#include <iostream>
#include <cmath>

#include <opencv2\opencv.hpp>
#include <highgui.hpp> 
#include "opencv2/imgproc/imgproc_c.h"

#include "rplidar.h" //RPLIDAR standard sdk

using namespace std;


//����opencv��ʾ�����С��rplidar��Զ������12m�����Է�����㣬����ȡ12�ı���
static int RadarImageWdith = 600;
static int RadarImageHeight = 600;
static int halfWidth = RadarImageWdith / 2;
static int halfHeight = RadarImageHeight / 2;

//ʵ�ʾ�������ڵ�
struct scanDot {
    _u16  angle;
    _u32  dist;
    _u8   quality;
};
//�״�����ϵ��ͼ�ڵ�
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

    vector<scanDot> scan_data; //����ÿɨ��һ�ܵ��״�ʵ������
    vector<drawDot> draw_data; //������OPENCV����ϵ�Ľڵ�����

    void DataConversion(rplidar_response_measurement_node_hq_t *buffer, size_t count);
    void Draw(cv::Mat& RadarImage);
    bool IS_Near(const drawDot &former, const drawDot &latter);
};
