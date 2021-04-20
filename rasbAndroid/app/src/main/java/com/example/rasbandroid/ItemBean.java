package com.example.rasbandroid;

import android.graphics.drawable.Drawable;

import java.io.File;
import java.util.ArrayList;

public class ItemBean extends BaseMultiBean {
    private ArrayList<File> images;
    private int imageNum;

    public ItemBean(ArrayList<File> imageList){
        this.images=imageList;
        this.type=TYPE_ITEM;
        this.imageNum=imageList.size();
    }
    public File getImage(int num){
        if(num>imageNum)return null;
        else
            return images.get(num-1);
    }
    public int getNum(){
        return imageNum;
    }
    public void setImage(File image,int num) {
        if(num>imageNum)return;
        else
            this.images.set(num-1,image);

    }
}
