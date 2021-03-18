package com.example.rasbandroid;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Handler;
import android.widget.ImageView;
import android.widget.Button;
import android.view.View;

public class MainActivity extends AppCompatActivity {
//    private static TextView t;
    private ImageView frameView;
    private Button connectBtn;
    private static Handler handler=new Handler();
    private Bitmap currentFrame;
    private Intent serviceIntent;
    public static Context context;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        context=this;
        frameView=(ImageView)findViewById(R.id.imageView);
        connectBtn=(Button)findViewById(R.id.connect);
        serviceIntent=new Intent(this,UDPService.class);
        connectBtn.setOnClickListener(new Button.OnClickListener(){
            public void onClick(View view){
                startService(serviceIntent);

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
        stopService(serviceIntent);
    }
}
