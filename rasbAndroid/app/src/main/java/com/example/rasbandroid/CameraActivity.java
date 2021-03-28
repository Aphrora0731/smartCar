package com.example.rasbandroid;

import androidx.lifecycle.ViewModelProviders;
import androidx.lifecycle.Observer;


import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.ActivityInfo;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.os.Bundle;



import android.os.Handler;
import android.os.IBinder;
import android.view.View;
import android.view.WindowManager;
import android.widget.ImageButton;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;



public class CameraActivity extends AppCompatActivity {

    private ImageView frameView;
    private static Handler handler=new Handler();
    private Bitmap currentFrame;
    public static Context context;

    private Intent serviceIntent;
    private UDPService.UDPBinder binder;
    private ImageButton imgBtn;
    private ServiceConnection conn=new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            binder=(UDPService.UDPBinder)service;
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);
        frameView=findViewById(R.id.imageView);
        imgBtn=findViewById(R.id.img_button);
        context=this;
        imgBtn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                finish();
            }

        });
    }

    public static void updateFrame(Bitmap frame){
        ((CameraActivity)context).currentFrame=frame;
        handler.post(RefreshFrame);
    }

    private static Runnable RefreshFrame=new Runnable() {
        @Override
        public void run() {
            ((CameraActivity)context).frameView.setImageBitmap(((CameraActivity)context).currentFrame);
        }
    };

    @Override
    public void onStart(){
        super.onStart();
        serviceIntent=new Intent(context,UDPService.class);
        bindService(serviceIntent,conn,BIND_AUTO_CREATE);
        if(getResources().getConfiguration().orientation == Configuration.ORIENTATION_PORTRAIT){
            setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
        }
//        getSupportActionBar().hide();
//        getActivity().getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
//        findViewById(R.id.nav_view).setVisibility(View.GONE);
    }

    @Override
    public void onStop(){
        super.onStop();
        unbindService(conn);
//        findViewById(R.id.nav_view).setVisibility(View.VISIBLE);
        getWindow().clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
//        getSupportActionBar().show();
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
    }

}
