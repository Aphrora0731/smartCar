package com.example.rasbandroid.ui.home;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;

import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.annotation.NonNull;
import androidx.appcompat.widget.Toolbar;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProviders;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;
import mehdi.sakout.fancybuttons.FancyButton;


import com.example.rasbandroid.CameraActivity;
import com.example.rasbandroid.R;

public class HomeFragment extends Fragment {

    private HomeViewModel homeViewModel;
    private FancyButton fancyButton;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        homeViewModel =
                ViewModelProviders.of(this).get(HomeViewModel.class);
        View root = inflater.inflate(R.layout.fragment_home, container, false);
        final TextView textView = root.findViewById(R.id.text_home);
//        homeViewModel.getText().observe(this, new Observer<String>() {
//            @Override
//            public void onChanged(@Nullable String s) {
//                textView.setText(s);
//            }
//        });
        fancyButton=(FancyButton) root.findViewById(R.id.btn_camera);
        fancyButton.setOnClickListener(new OnClickListener(){
            @Override
            public void onClick(View v) {
                Intent intent=new Intent(getActivity(), CameraActivity.class);
                startActivity(intent);
            }

        });
        return root;
    }
}