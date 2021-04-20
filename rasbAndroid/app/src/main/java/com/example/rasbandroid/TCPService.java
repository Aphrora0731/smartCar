package com.example.rasbandroid;

import android.app.Service;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Binder;
import android.os.Environment;
import android.os.IBinder;
import android.util.Log;


import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.SocketTimeoutException;
import java.net.Socket;
import java.util.Date;
import java.text.DateFormat;

import static androidx.constraintlayout.widget.Constraints.TAG;


public class TCPService extends Service {
    private InetAddress hostIP;
    private int port=8000;
    private Socket client=null;
    private TCPBinder mBinder=new TCPBinder();
    class TCPBinder extends Binder {
    }
    public TCPService() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        Log.d( "onBind","binded");
        hostIP=(InetAddress) intent.getSerializableExtra("IP");
        Log.d("in bind",hostIP.toString());
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
        new Thread() {
            @Override
            public void run() {
                super.run();
                try{
                    client=new Socket();
                    Log.d("in connect",hostIP.toString());
                    client.connect(new InetSocketAddress(hostIP,port),6000);
                    Log.d("in connect", "conneted");
                    byte[] data=new byte[65536];
                    while(client!=null){
                        try{
                            BufferedInputStream in=new BufferedInputStream(client.getInputStream());
                            int dataLength;
                            Bitmap bitmap;
                            if((dataLength=in.read(data))!=-1) {
                                bitmap = BitmapFactory.decodeByteArray(data, 0, dataLength);
                                Log.d("in recv","recved");
                                System.out.println(dataLength);
                                storeBitmap(bitmap);
                            }
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
        }.start();

    }
    protected void storeBitmap(Bitmap bitmap){
        DateFormat dateFormat= DateFormat.getDateInstance();
        String date=dateFormat.format(new Date());
        int picNum=0;
        if(Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED)) {
            File appExternalPicDir=this.getExternalFilesDir(Environment.DIRECTORY_PICTURES);
            File pictureDateDir=new File(appExternalPicDir,date);
            if(pictureDateDir.exists()){
                picNum=pictureDateDir.list().length;
                if(picNum>=3)return;
            }
            else pictureDateDir.mkdir();

            File newImage=new File(pictureDateDir,"image"+Integer.toString(picNum));
            try {
                FileOutputStream fos = new FileOutputStream(newImage);
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, fos);
                fos.flush();
                fos.close();
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

}
