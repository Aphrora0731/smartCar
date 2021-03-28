//package com.example.rasbandroid.ui.view;
//
//import androidx.lifecycle.ViewModelProviders;
//import androidx.lifecycle.Observer;
//
//
//import android.content.ComponentName;
//import android.content.Intent;
//import android.content.ServiceConnection;
//import android.content.pm.ActivityInfo;
//import android.content.res.Configuration;
//import android.graphics.Bitmap;
//import android.os.Bundle;
//
//import androidx.annotation.NonNull;
//import androidx.annotation.Nullable;
//import androidx.fragment.app.Fragment;
//
//
//import android.os.Handler;
//import android.os.IBinder;
//import android.view.LayoutInflater;
//import android.view.View;
//import android.view.ViewGroup;
//import android.view.Window;
//import android.view.WindowManager;
//import android.widget.ImageView;
//import android.widget.TextView;
//
//import com.example.rasbandroid.R;
//import com.example.rasbandroid.UDPService;
//import com.google.android.material.bottomnavigation.BottomNavigationView;
//
//import androidx.appcompat.app.AppCompatActivity;
//
//
//
//public class ViewFragment extends Fragment {
//
//    private ViewViewModel viewViewModel;
//    private ImageView frameView;
//    private static Handler handler=new Handler();
//    private Bitmap currentFrame;
//    public static Fragment frag;
//
//    private Intent serviceIntent;
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
//
//    public View onCreateView(@NonNull LayoutInflater inflater,
//                             ViewGroup container, Bundle savedInstanceState) {
//        viewViewModel =
//                ViewModelProviders.of(this).get(ViewViewModel.class);
//        View root = inflater.inflate(R.layout.fragment_view, container, false);
//        final TextView textView = root.findViewById(R.id.text_view);
//        viewViewModel.getText().observe(this, new Observer<String>() {
//            @Override
//            public void onChanged(@Nullable String s) {
//                textView.setText(s);
//            }
//        });
//        frameView=root.findViewById(R.id.imageView);
//        frag=this;
//        return root;
//    }
//
//    public static void updateFrame(Bitmap frame){
//        ((ViewFragment)frag).currentFrame=frame;
//        handler.post(RefreshFrame);
//    }
//
//    private static Runnable RefreshFrame=new Runnable() {
//        @Override
//        public void run() {
//            ((ViewFragment)frag).frameView.setImageBitmap(((ViewFragment)frag).currentFrame);
//        }
//    };
//
//    @Override
//    public void onStart(){
//        super.onStart();
//        serviceIntent=new Intent(getActivity(),UDPService.class);
//        getActivity().bindService(serviceIntent,conn,getActivity().BIND_AUTO_CREATE);
//        if(getActivity().getResources().getConfiguration().orientation == Configuration.ORIENTATION_PORTRAIT){
//            getActivity().setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
//        }
//        ((AppCompatActivity)getActivity()).getSupportActionBar().hide();
////        getActivity().getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
//        getActivity().getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
//                WindowManager.LayoutParams.FLAG_FULLSCREEN);
//        getActivity().findViewById(R.id.nav_view).setVisibility(View.GONE);
//    }
//
//    @Override
//    public void onStop(){
//        super.onStop();
//        getActivity().unbindService(conn);
//        getActivity().findViewById(R.id.nav_view).setVisibility(View.VISIBLE);
//        getActivity().getWindow().clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
//        ((AppCompatActivity)getActivity()).getSupportActionBar().show();
//        getActivity().setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
//    }
//
//}
