package com.example.rasbandroid;

public abstract class BaseMultiBean {
    public static final int TYPE_TITLE=0;
    public static final int TYPE_ITEM=1;
    protected int type;

    public int getType() {
        return type;
    }

    public void setType(int type) {
        this.type = type;
    }
}
