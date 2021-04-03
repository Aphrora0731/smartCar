#include"Rplidar_1.h"
#include<iostream>
#include <windows.h>
#include <ctime>
#include<vector>
#include <stdio.h>

using namespace std;
using namespace rp::standalone::rplidar;


int main()
{
	RPlidarDriver* drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
	Rplidar_connect(drv);
	LidarImage lidarImage;
	cout << "debug1" << endl;
	HANDLE hPipe = CreateNamedPipe(L"\\\\.\\Pipe\\mypipe", PIPE_ACCESS_DUPLEX, PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT
		, PIPE_UNLIMITED_INSTANCES, 0, 0, NMPWAIT_WAIT_FOREVER, 0);

	if (ConnectNamedPipe(hPipe, NULL) != NULL)
	{
		printf("连接成功，开始发送数据\n");
		while (1) {
			cv::Mat image = Rplidar_getImage(lidarImage, drv);
			vector<uchar>data_encode;
			imencode(".jpg", image, data_encode);
			string str_encode(data_encode.begin(), data_encode.end());

			const char* sendBuf = str_encode.c_str();
			int toSendNum = str_encode.size();
			DWORD    dwWrite;

			if (!WriteFile(hPipe, sendBuf, toSendNum, &dwWrite, NULL))
			{
				cout << "write failed..." << endl << endl;
				return 0;
			}
		}
		//cout << "sent data: " << endl << pStr << endl << endl;
	}

	DisconnectNamedPipe(hPipe);
	CloseHandle(hPipe);//关闭管道
	printf("关闭管道\n");
}
