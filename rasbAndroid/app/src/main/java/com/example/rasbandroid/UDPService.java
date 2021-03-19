package com.example.rasbandroid;

import android.app.Service;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Binder;
import android.os.IBinder;
import android.util.Log;

import java.io.*;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.*;
import java.net.SocketTimeoutException;

public class UDPService extends Service {

    private int port=8080;
    private DatagramSocket socket=null;
    private NoticeBinder mBinder=new NoticeBinder();
    class NoticeBinder extends Binder {
    }
    public UDPService() {
    }

//    @Override
//    public int onStartCommand(Intent intent, int flags, int startId) {
//        Log.d("in","serviceStart");
////        startReceiveThread();
//        return super.onStartCommand(intent, flags, startId);
//    }
    @Override
    public IBinder onBind(Intent intent) {
        startReceiveThread();
        return mBinder;
    }

    @Override
    public boolean onUnbind(Intent intent) {
        if(socket!=null){
            socket.close();
            socket=null;
            MainActivity.updateFrame(null);
        }
        return true;
    }
    /**
     * Start the frame receive thread
     */
    private void startReceiveThread(){
        new Thread(){
            @Override
            public void run() {
                super.run();
                try{
                    socket=new DatagramSocket(port);
                    socket.setSoTimeout(10000);
                    byte[] data=new byte[65536];
                    DatagramPacket packet=new DatagramPacket(data,data.length);
                    Log.d("inRecv","initsucess");
                    while(socket!=null){
                        try{
//                            Log.d("inRecvLoop","beforerecv");
                            socket.receive(packet);
                            Log.d("inRecvLoop","inrecv");
                        }catch (SocketTimeoutException timeoute){
                            Log.d("inRecvLoop",timeoute.getMessage());
                            continue;
                        }catch (IOException ioe){
                            Log.d("inRecvLoop","ioe");
                            throw ioe;
                        }
                        Bitmap bitmap= BitmapFactory.decodeByteArray(data,0,packet.getLength());
                        MainActivity.updateFrame(bitmap);
                    }
                }catch (IOException e){
                    e.printStackTrace();
                }
            }
        }.start();
    }

    @Override
    public void onDestroy(){
        super.onDestroy();
    }
}

