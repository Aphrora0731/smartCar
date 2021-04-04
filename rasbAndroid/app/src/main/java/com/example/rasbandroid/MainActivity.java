package com.example.rasbandroid;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

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
import android.util.Log;
import android.widget.ImageView;
import android.widget.Button;
import android.view.*;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.navigation.NavigationView;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;
import java.util.Enumeration;


public class MainActivity extends AppCompatActivity {
//    private static TextView t;
//    private ImageView frameView;
//    private Button connectBtn;
//    private Button disconnectBtn;
//    private static Handler handler=new Handler();
//    private Bitmap currentFrame;
//    private Intent serviceIntent;
      private DatagramSocket socket;
//    public static Context context;
//
//    private UDPService.UDPBinder binder;
//    private ServiceConnection conn=new ServiceConnection() {
//        @Override
//        public void onServiceConnected(ComponentName name, IBinder service) {
//            binder=(UDPService.UDPBinder)service;
//        }
//
//        @Override
//        public void onServiceDisconnected(ComponentName name) {
//        }
//    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        BottomNavigationView navView = findViewById(R.id.nav_view);
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        AppBarConfiguration appBarConfiguration;appBarConfiguration = new AppBarConfiguration.Builder(
                R.id.navigation_home, R.id.navigation_route, R.id.navigation_condition)
                .build();
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        NavController navController = Navigation.findNavController(this,R.id.nav_host_fragment);
        NavigationUI.setupWithNavController(toolbar, navController, appBarConfiguration);
        NavigationUI.setupWithNavController(navView, navController);
        socketInit();

    }

    private void socketInit(){
        new Thread(){
            @Override
            public void run() {
                super.run();
                try {
                    socket = new DatagramSocket();
                    socket.setBroadcast(true);
                    socket.setSoTimeout(10);
                    byte[] b ="udp server".getBytes(StandardCharsets.UTF_8);
                    DatagramPacket dpSend = new DatagramPacket(b, b.length,
                            InetAddress.getByName("192.168.212.255"),8080);
                    for(int i=0;i<=13333;i++){
                        socket.send(dpSend);
//                        Log.d("inSendLoop","in");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }finally {
                    if(socket!=null){
                        socket.close();
                    }
                }
            }
        }.start();
    }

    private static String getIP(){

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

    @Override
    public void onConfigurationChanged (Configuration newConfig){
        super.onConfigurationChanged(newConfig);
    }
//    @Override
//    protected void onStart(){
//        super.onStart();
//        serviceIntent=new Intent(this,UDPService.class);
//        bindService(serviceIntent,conn,BIND_AUTO_CREATE);
//    }
//
//    @Override
//    protected void onStop(){
//        super.onStop();
//        unbindService(conn);
//    }
//    public static void updateFrame(Bitmap frame){
//        ((MainActivity)context).currentFrame=frame;
//        handler.post(RefreshFrame);
//    }
//
//    private static Runnable RefreshFrame=new Runnable() {
//        @Override
//        public void run() {
//            ((MainActivity)context).frameView.setImageBitmap(((MainActivity)context).currentFrame);
//        }
//    };
}
