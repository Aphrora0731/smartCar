package com.example.rasbandroid;

import android.graphics.drawable.Drawable;

import java.io.File;

public class ItemBean extends BaseMultiBean {
    private File image1;
    private File image2;
    private File image3;

    public ItemBean(File image1, File image2, File image3){
        this.image1=image1;
        this.image2=image2;
        this.image3=image3;
        this.type=TYPE_ITEM;
    }

    public File getImage(int num){
        if(num==1)
            return image1;
        else if(num==2)
            return image2;
        else
            return image3;
    }

    public void setImage(File image,int num) {
        if(num==1)
            this.image1=image;
        else if(num==2)
            this.image2=image;
        else
            this.image3=image;

    }
}
