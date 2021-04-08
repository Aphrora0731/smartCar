#include"Rplidar_1.h"
#include<iostream>
#include<vector>
#include <Winsock2.h>
#include <stdio.h>
#pragma warning(disable:4996)
#pragma comment(lib,"ws2_32.lib")
using namespace std;
using namespace rp::standalone::rplidar;


int main()
{
	RPlidarDriver* drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
	Rplidar_connect(drv);
	LidarImage lidarImage;

	//加载套接字库
	WORD wVersionRequested;
	WSADATA wsaData;
	int err;

	wVersionRequested = MAKEWORD(1, 1);

	err = WSAStartup(wVersionRequested, &wsaData);
	if (err != 0)
	{
		return 0;
	}

	if (LOBYTE(wsaData.wVersion) != 1 ||     //低字节为主版本
		HIBYTE(wsaData.wVersion) != 1)      //高字节为副版本
	{
		WSACleanup();
		return 0;
	}

	printf("Client is operating!\n\n");
	//创建用于监听的套接字
	SOCKET sockSrv = socket(AF_INET, SOCK_DGRAM, 0);

	sockaddr_in  addrSrv;
	addrSrv.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");//输入你想通信  ，的她（此处是本机内部）
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(8088);

	int len = sizeof(SOCKADDR);

	// start typical scan
	RplidarScanMode scanMode;
	drv->startScan(false, true, 0, &scanMode);

	while (1) {
		cv::Mat image = Rplidar_getImage(lidarImage, drv);
		vector<uchar>data_encode;
		imencode(".jpg", image, data_encode);
		string str_encode(data_encode.begin(), data_encode.end());

		//
		char pre_detection = preDetection(lidarImage);
		str_encode += pre_detection;

		const char* sendBuf = str_encode.c_str();
		int toSendNum = str_encode.size();

		sendto(sockSrv, sendBuf, toSendNum + 1, 0, (SOCKADDR*)&addrSrv, len);
	}
	closesocket(sockSrv);
	WSACleanup();

}