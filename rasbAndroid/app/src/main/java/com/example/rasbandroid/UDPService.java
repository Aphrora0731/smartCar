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
import java.net.InetSocketAddress;
import java.net.SocketTimeoutException;
import java.net.InetAddress;
import java.net.Inet4Address;
import java.net.NetworkInterface;
import java.util.Enumeration;



public class UDPService extends Service {

    private int framePort=8081;
    private int radarPort=8082;
    private DatagramSocket frameSocket=null;
    private DatagramSocket radarSocket=null;
    private UDPBinder mBinder=new UDPBinder();
    public class UDPBinder extends Binder {
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
        Log.d("on Bind","in");
        return mBinder;
    }

    @Override
    public boolean onUnbind(Intent intent) {
        if(frameSocket!=null){
            frameSocket.close();
            frameSocket=null;
            CameraActivity.updateFrame(null);
        }
        if(radarSocket!=null){
            radarSocket.close();
            radarSocket=null;
            CameraActivity.updateRadar(null);
        }
        return true;
    }
    private String getIP(){

        try {
            for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements();) {
                NetworkInterface intf = en.nextElement();
                for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();)
                {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress() && (inetAddress instanceof Inet4Address))
                    {
                        return inetAddress.getHostAddress().toString();
                    }
                }
            }
        }
        catch (Exception ex){
            ex.printStackTrace();
        }
        return null;
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
                    Log.d("inRecv","initPort");
                    if(frameSocket==null){
                        frameSocket = new DatagramSocket(null);
                        frameSocket.setReuseAddress(true);
                        frameSocket.bind(new InetSocketAddress(framePort));
                    }
//                    socket=new DatagramSocket(port);
                    Log.d("inRecv","after initPort");
                    frameSocket.setSoTimeout(10000);
                    byte[] data=new byte[65536];
                    DatagramPacket packet=new DatagramPacket(data,data.length);
                    Log.d("inRecv","initsucess");

                    System.out.println("Local HostAddress: "+getIP());
                    while(frameSocket!=null){
                        try{
//                            Log.d("inRecvLoop","beforerecv");
                            frameSocket.receive(packet);
                            Log.d("inRecvLoop","inrecv");
                        }catch (SocketTimeoutException timeoute){
                            Log.d("inRecvLoop",timeoute.getMessage());
                            continue;
                        }catch (IOException ioe){
                            Log.d("inRecvLoop","ioe");
                            throw ioe;
                        }
                        Bitmap bitmap= BitmapFactory.decodeByteArray(data,0,packet.getLength());
                        CameraActivity.updateFrame(bitmap);
                    }
                }catch (IOException e){
                    e.printStackTrace();
                }
            }
        }.start();

        new Thread(){
            @Override
            public void run() {
                super.run();
                try{
                    Log.d("inRecv","initPort");
                    if(radarSocket==null){
                        radarSocket = new DatagramSocket(null);
                        radarSocket.setReuseAddress(true);
                        radarSocket.bind(new InetSocketAddress(radarPort));
                    }
//                    socket=new DatagramSocket(port);
                    Log.d("inRecv","after initPort");
                    radarSocket.setSoTimeout(10000);
                    byte[] data=new byte[65536];
                    DatagramPacket packet=new DatagramPacket(data,data.length);
                    Log.d("inRecv","initsucess");

                    System.out.println("Local HostAddress: "+getIP());
                    while(radarSocket!=null){
                        try{
//                            Log.d("inRecvLoop","beforerecv");
                            radarSocket.receive(packet);
                            Log.d("inRecvLoop","inrecv");
                        }catch (SocketTimeoutException timeoute){
                            Log.d("inRecvLoop",timeoute.getMessage());
                            continue;
                        }catch (IOException ioe){
                            Log.d("inRecvLoop","ioe");
                            throw ioe;
                        }
                        Bitmap bitmap= BitmapFactory.decodeByteArray(data,0,packet.getLength());
                        CameraActivity.updateRadar(bitmap);
                    }
                }catch (IOException e){
                    e.printStackTrace();
                }
            }
        }.start();
    }
}

