package com.example.rasbandroid;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;


import java.io.IOException;
import java.io.InputStream;
import java.net.InetSocketAddress;
import java.net.SocketTimeoutException;
import java.net.Socket;




public class TCPService extends Service {
    private String host="localhost";
    private int port=8080;
    private Socket client=null;
    private TCPBinder mBinder=new TCPBinder();
    class TCPBinder extends Binder {
    }
    public TCPService() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        startReceiveThread();
        return mBinder;
    }

    @Override
    public boolean onUnbind(Intent intent) {
        if(client!=null){
            try{
                client.close();
            }catch(IOException e){
                e.printStackTrace();
            }

            client=null;
        }
        return true;
    }
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        startReceiveThread();
        return super.onStartCommand(intent, flags, startId);
    }
    protected void startReceiveThread(){
        new Thread(new Runnable() {
            @Override
            public void run() {
                try{
                    client=new Socket();
                    client.connect(new InetSocketAddress(host,port),6000);
                    byte[] data=new byte[65536];
                    while(client!=null){
                        try{
                            InputStream in=client.getInputStream();
                            if(in.read(data)!=-1)
                                phraseString(new String(data));
                        }catch (SocketTimeoutException timeoute){
                            continue;
                        }catch(IOException ioe){
                            throw ioe;
                        }
                    }

                }catch (IOException e){
                    client=null;
                    e.printStackTrace();
                }
            }
        }).start();

    }

    protected void phraseString(String s){
//        MainActivity.updateFrame(s);
    }

}
