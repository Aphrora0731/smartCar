//package com.example.rasbandroid;
//
//import android.app.Service;
//import android.content.Intent;
//import android.os.IBinder;
//import android.graphics.Bitmap;
//import android.graphics.BitmapFactory;
//import android.os.Message;
//
//
//import java.io.IOException;
//import java.io.InputStream;
//import java.net.InetSocketAddress;
//import java.net.SocketTimeoutException;
//import java.net.Socket;
//
//
//
//
//public class TCPService extends Service {
//    private String host="localhost";
//    private int port=8080;
//    private boolean stopFlag=false;
//    private Socket client=null;
//    public TCPService() {
//    }
//
//    @Override
//    public int onStartCommand(Intent intent, int flags, int startId) {
//        startReceiveThread();
//        return super.onStartCommand(intent, flags, startId);
//    }
//    protected void startReceiveThread(){
//        new Thread(new Runnable() {
//            @Override
//            public void run() {
//                try{
//                    client=new Socket();
//                    client.connect(new InetSocketAddress(host,port),6000);
//                    byte[] data=new byte[65536];
//                    while(!stopFlag){
//                        try{
//                            InputStream in=client.getInputStream();
//                            if(in.read(data)!=-1)
//                                sendString(new String(data));
//                        }catch (SocketTimeoutException timeoute){
//                            continue;
//                        }catch(IOException ioe){
//                            throw ioe;
//                        }
//                    }
//
//                }catch (IOException e){
//                    client=null;
//                    e.printStackTrace();
//                }
//            }
//        }).start();
//
//    }
//
//    protected void sendString(String s){
//        MainActivity.updateFrame(s);
//    }
//
//    @Override
//    public void onDestroy(){
//        super.onDestroy();
//        if(client!=null){
//            try{
//                client.close();
//                client=null;
//            }catch (IOException e){
//                e.printStackTrace();
//            }
//        }
//    }
//
//    @Override
//    public IBinder onBind(Intent intent) {
//        // TODO: Return the communication channel to the service.
//        throw new UnsupportedOperationException("Not yet implemented");
//    }
//}
