package com.km.exlooperhandler;

import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.util.Log;

public class ExampleLooperThread extends Thread {
    private static final String TAG = "ExampleLooperThread";

    public Looper looper;
    public Handler handler;

    @Override
    public void run() {
        Looper.prepare();

        looper = Looper.myLooper();
        Log.d(TAG, "sleeping in looper...");
        SystemClock.sleep(1000);

        handler = new ExampleHandler();

        Looper.loop();

        Log.d(TAG, "End of run()");
    }
}