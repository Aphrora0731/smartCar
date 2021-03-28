package com.example.rasbandroid.ui.condition;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class ConditionViewModel extends ViewModel {

    private MutableLiveData<String> mText;

    public ConditionViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is condition fragment");
    }

    public LiveData<String> getText() {
        return mText;
    }
}