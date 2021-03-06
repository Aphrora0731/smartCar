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
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;
import java.util.Enumeration;

import static androidx.constraintlayout.widget.Constraints.TAG;


public class MainActivity extends AppCompatActivity {
//    private static TextView t;
//    private ImageView frameView;
//    private Button connectBtn;
//    private Button disconnectBtn;
//    private static Handler handler=new Handler();
//    private Bitmap currentFrame;
      private InetAddress centerIP;
      private Intent serviceIntent;
      private DatagramSocket sendSocket;
      private DatagramSocket recvSocket;
    //    public static Context context;
//
    private TCPService.TCPBinder binder;

    private ServiceConnection conn=new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            binder=(TCPService.TCPBinder)service;
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
        }
    };


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
                    sendSocket = new DatagramSocket();
                    sendSocket.setBroadcast(true);
                    recvSocket=new DatagramSocket(8081);
                    recvSocket.setSoTimeout(1000);
                    byte[] b ="udp server".getBytes(StandardCharsets.UTF_8);
                    System.out.println("broadcastip:"+getBroadcastIP());
                    DatagramPacket dpSend = new DatagramPacket(b, b.length,
                            InetAddress.getByName(getBroadcastIP()),8080);
                    byte[] c=new byte[1024];
                    DatagramPacket dpRecv=new DatagramPacket(c,c.length);
                    for(int i=0;i<=13333;i++){
                        sendSocket.send(dpSend);
                        try {
                            recvSocket.receive(dpRecv);
                            String answer = new String(c,"utf-8").trim();
                            Log.d("Recved", answer);
                            if (answer.contains("udp client")) {
                                centerIP = dpRecv.getAddress();
                                Log.d("inSendLoop", "recv ip");
                                startTCPService();
                                break;
                            }
                        }
                        catch (SocketTimeoutException timeoute){
                            Log.d("inRSendLoop",timeoute.getMessage());
                            continue;
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }finally {
                    if(sendSocket!=null){
                        sendSocket.close();
                    }
                    if(recvSocket!=null){
                        recvSocket.close();
                    }
                }
            }
        }.start();
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

    private  String getBroadcastIP(){
        String myIP=getIP();
        int dotIndex=myIP.lastIndexOf('.');
        String subIP=myIP.substring(0,dotIndex);
        return subIP.concat(".255");
    }

    private void startTCPService(){
        serviceIntent=new Intent(this,TCPService.class);
        Bundle data=new Bundle();
        Log.d("onStart",centerIP.toString());
        data.putSerializable("IP",centerIP);
        serviceIntent.putExtras(data);
        bindService(serviceIntent,conn,BIND_AUTO_CREATE);
    }

    @Override
    public void onConfigurationChanged (Configuration newConfig){
        super.onConfigurationChanged(newConfig);
    }
    @Override
    protected void onDestroy(){
        super.onDestroy();
        if(centerIP !=null)
            unbindService(conn);
    }
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
