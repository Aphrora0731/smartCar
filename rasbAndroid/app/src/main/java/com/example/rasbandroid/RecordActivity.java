package com.example.rasbandroid;

import android.content.Context;
import android.os.Bundle;

import com.bumptech.glide.Glide;
import com.bumptech.glide.request.FutureTarget;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.View;

import java.io.File;
import java.lang.annotation.Target;
import java.util.ArrayList;
import java.util.List;

public class RecordActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private List<BaseMultiBean> multiDataList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_record);
        recyclerViewInit();
    }

    private void recyclerViewInit(){
        recyclerView=(RecyclerView)findViewById(R.id.recycler);
        LinearLayoutManager manager=new LinearLayoutManager(this);
        manager.setOrientation(LinearLayoutManager.VERTICAL);
        recyclerView.setLayoutManager(manager);
        multiDataList=new ArrayList<>();
        multiDataList.add(new TitleBean("2021-04-06"));
        new Thread(new Runnable() {
            @Override
            public void run() {
                try{
                    final Context cxt=getApplicationContext();
                    FutureTarget<File> target1=Glide.with(cxt).load(R.drawable.ic_camera_pressed).
                            downloadOnly(100,100);
                    FutureTarget<File> target2=Glide.with(cxt).load(R.drawable.ic_record_pressed).
                            downloadOnly(100,100);
                    FutureTarget<File> target3=Glide.with(cxt).load(R.drawable.ic_more_pressed).
                            downloadOnly(100,100);
                    multiDataList.add(new ItemBean(target1.get(),target1.get(),target1.get()));
                    multiDataList.add(new TitleBean("2021-04-03"));
                    multiDataList.add(new ItemBean(target2.get(),target2.get(),target2.get()));
                    multiDataList.add(new TitleBean("2021-04-01"));
                    multiDataList.add(new ItemBean(target3.get(),target3.get(),target3.get()));
                    final RecyclerViewAdapter adapter=new RecyclerViewAdapter(RecordActivity.this,
                            multiDataList);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            recyclerView.setAdapter(adapter);
                        }
                    });
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        }).start();

    }

    private void readFile(){

    }
    @Override
    public void onStop(){
        super.onStop();
        new Thread(new Runnable() {
            @Override
            public void run() {
                Glide.get(getApplication()).clearDiskCache();
                Glide.get(getApplication()).clearMemory();
            }
        });
    }
}
