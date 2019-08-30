package com.km.exviewmodel;

import android.app.Application;

import android.arch.lifecycle.AndroidViewModel;
import android.arch.lifecycle.LiveData;

import androidx.annotation.NonNull;

import java.util.List;

public class MyViewModel extends AndroidViewModel {

	private LiveData<List<String>> users;

	private MyViewModel(@NonNull Application application){
		super(application);
//		repository
		//make new repository
		//get all notes
	}

//	public LiveData<List<User>> getUsers() {
//		if (users == null) {
//			users = new MutableLiveData<List<User>>();
//			loadUsers();
//		}
//		return users;
//	}

	private void loadUsers() {
		// perform an asynchronous operation to fetch users.
	}
}