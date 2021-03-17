package com.example.rasbandroid;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Handler;
import android.widget.ImageView;
import android.widget.Button;
import android.view.View;

public class MainActivity extends AppCompatActivity {
//    private static TextView t;
    private static ImageView frameView;
    private static Button connectBtn;
    private static Handler handler=new Handler();
    private static Bitmap currentFrame;
    private Intent serviceIntent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
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
        currentFrame=frame;
        handler.post(RefreshFrame);
    }

    private static Runnable RefreshFrame=new Runnable() {
        @Override
        public void run() {
            frameView.setImageBitmap(currentFrame);
        }
    };

    @Override
    protected void onDestroy(){
        super.onDestroy();
        stopService(serviceIntent);
    }
}
