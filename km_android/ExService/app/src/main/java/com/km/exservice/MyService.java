package com.km.exservice;

import android.app.Service;
import android.content.Intent;
import android.media.MediaPlayer;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.util.Log;
import android.widget.Toast;

public class MyService extends Service {
	private static final String TAG = "MyService";
	MediaPlayer myPlayer;
	@Nullable
	@Override
	public IBinder onBind(Intent intent) {
		return null;
	}
	@Override
	public void onCreate() {
		Log.d(TAG, "onCreate: ");
		Toast.makeText(this, "Service Created", Toast.LENGTH_LONG).show();

		myPlayer = MediaPlayer.create(this, R.raw.rex_tremendae);
		myPlayer.setLooping(false); // Set looping
	}
	@Override
	public int onStartCommand(Intent intent, int flags, int startid) {
		Log.d(TAG, "onStartCommand: ");
		Toast.makeText(this, "Service Started", Toast.LENGTH_LONG).show();
		myPlayer.start();
		Log.d(TAG, "onStartCommand: hit return.");
		return START_NOT_STICKY;
	}
	@Override
	public void onDestroy() {
		Log.d(TAG, "onDestroy: ");
		Toast.makeText(this, "Service Stopped", Toast.LENGTH_LONG).show();
		myPlayer.stop();
	}
}