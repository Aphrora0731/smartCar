package com.example.rasbandroid;

import androidx.appcompat.app.AppCompatActivity;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.ActivityInfo;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.widget.ImageView;
import android.widget.Button;
import android.view.*;


public class MainActivity extends AppCompatActivity {
//    private static TextView t;
    private ImageView frameView;
    private Button connectBtn;
    private Button disconnectBtn;
    private static Handler handler=new Handler();
    private Bitmap currentFrame;
    private Intent serviceIntent;
    public static Context context;
    private UDPService.NoticeBinder binder;
    private ServiceConnection conn=new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            binder=(UDPService.NoticeBinder)service;
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
        }
    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        context=this;
        frameView=(ImageView)findViewById(R.id.imageView);
        connectBtn=(Button)findViewById(R.id.connect);
        disconnectBtn=(Button)findViewById(R.id.disconnect);
        serviceIntent=new Intent(this,UDPService.class);
        connectBtn.setOnClickListener(new Button.OnClickListener(){
            public void onClick(View view){
                bindService(serviceIntent,conn,BIND_AUTO_CREATE);
            }
        });
        disconnectBtn.setOnClickListener(new Button.OnClickListener(){
            public void onClick(View view){
                unbindService(conn);
            }
        });
    }

    public static void updateFrame(Bitmap frame){
        ((MainActivity)context).currentFrame=frame;
        handler.post(RefreshFrame);
    }

    private static Runnable RefreshFrame=new Runnable() {
        @Override
        public void run() {
            ((MainActivity)context).frameView.setImageBitmap(((MainActivity)context).currentFrame);
        }
    };

    @Override
    protected void onDestroy(){
        super.onDestroy();
    }
}
