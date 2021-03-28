package com.example.rasbandroid.ui.route;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class RouteViewModel extends ViewModel {

    private MutableLiveData<String> mText;

    public RouteViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is route fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }
}