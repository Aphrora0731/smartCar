package com.example.rasbandroid;


public class TitleBean extends BaseMultiBean {
    private String title;
    public TitleBean(String title){
        this.title=title;
        this.type=TYPE_TITLE;
    }

    public String getTitle() {
        return title;
    }
}
