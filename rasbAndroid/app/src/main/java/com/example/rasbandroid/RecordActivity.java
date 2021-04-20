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

import android.os.Environment;
import android.view.View;

import java.io.File;
import java.lang.annotation.Target;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class RecordActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private ArrayList<BaseMultiBean> multiDataList;
    private ArrayList<ImageDateSet> imageDateSets;

    public class ImageDateSet{
        private String dateString;
        private ArrayList<File> fileList;
        public ImageDateSet(String date,ArrayList<File> files){
            dateString=date;
            fileList=files;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_record);
//        readFiles();
        recyclerViewInit();
    }

    private void recyclerViewInit(){
        recyclerView=(RecyclerView)findViewById(R.id.recycler);
        LinearLayoutManager manager=new LinearLayoutManager(this);
        manager.setOrientation(LinearLayoutManager.VERTICAL);
        recyclerView.setLayoutManager(manager);
        multiDataList=new ArrayList<>();

//        for(ImageDateSet i : imageDateSets) {
//            multiDataList.add(new TitleBean(i.dateString));
//            multiDataList.add(new ItemBean(i.fileList));
//        }

        multiDataList.add(new TitleBean("2021-04-15"));
        new Thread(new Runnable() {
            @Override
            public void run() {
                try{
                    final Context cxt=getApplicationContext();
                    FutureTarget<File> target1=Glide.with(cxt).load(R.drawable.test_car).
                            downloadOnly(100,100);
                    FutureTarget<File> target2=Glide.with(cxt).load(R.drawable.test_car2).
                            downloadOnly(100,100);
                    FutureTarget<File> target3=Glide.with(cxt).load(R.drawable.test_moto).
                            downloadOnly(100,100);
                    FutureTarget<File> target4=Glide.with(cxt).load(R.drawable.test_moto2).
                            downloadOnly(100,100);
                    ArrayList<File> imageList1=new ArrayList<File>();
                    imageList1.add(target1.get());imageList1.add(target2.get());imageList1.add(target3.get());
                    multiDataList.add(new ItemBean(imageList1));
                    multiDataList.add(new TitleBean("2021-04-14"));
                    ArrayList<File> imageList2=new ArrayList<File>();
                    imageList1.add(target2.get());imageList1.add(target3.get());imageList1.add(target3.get());
                    multiDataList.add(new ItemBean(imageList2));
                    multiDataList.add(new TitleBean("2021-04-13"));
                    ArrayList<File> imageList3=new ArrayList<File>();
                    imageList1.add(target3.get());imageList1.add(target1.get());imageList1.add(target4.get());
                    multiDataList.add(new ItemBean(imageList3));
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

    private void readFiles(){
        imageDateSets=new ArrayList<ImageDateSet>();
        if(Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED)) {
            File appExternalPicDir=this.getExternalFilesDir(Environment.DIRECTORY_PICTURES);
            for(File i : appExternalPicDir.listFiles()){
                String fileName=i.getName();
                ArrayList<File> imageList= new ArrayList<File>(Arrays.asList(i.listFiles()));
                ImageDateSet dataItem=new ImageDateSet(fileName,imageList);
                imageDateSets.add(dataItem);
            }

        }
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
