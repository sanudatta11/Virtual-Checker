package com.company.kone.kone;

import android.app.Activity;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.CountDownTimer;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.WindowManager;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;



public class MainActivity extends AppCompatActivity {
    static int counter = 0;
    CountDownTimer count,prevcount;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_main);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {

        final int number = event.getPointerCount();
        final TextView tv = (TextView)findViewById(R.id.textid);
        final TextView text_msg = (TextView)findViewById(R.id.textid2);

        switch (event.getActionMasked())
        {
            case MotionEvent.ACTION_DOWN: return true;
            case MotionEvent.ACTION_UP: if(counter == number)
                                            tv.setText(String.valueOf(0));
                                        return true;
        }

        tv.setText(String.valueOf(number));
        if(counter == number)
            return super.onTouchEvent(event);
        if(prevcount!=null)
            prevcount.cancel();
        final boolean[] flag_var = {false};
        count = new CountDownTimer(3000, 1000) {


            public void onTick(long millisUntilFinished) {
                text_msg.setText("Seconds remaining: " + millisUntilFinished / 1000);
            }

            public void onFinish() {
                text_msg.setText("Posting!");
                tv.setText(String.valueOf(0));
                flag_var[0] = true;

                if(isConnected())
                {
                    //TODO Make the JSON DATA SEND

                }
                else{
                    Context context = getApplicationContext();
                    Toast.makeText(context, "Sorry Network not connected", Toast.LENGTH_SHORT).show();
                }
            }

        };

        if(flag_var[0])
        {
            flag_var[0] = false;
            return false;
        }
        prevcount = count;
        count.start();
        counter = number;
        Log.d("value", String.valueOf(number));

        return super.onTouchEvent(event);

    }

    public static String getMD5(String input) {
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] messageDigest = md.digest(input.getBytes());
            BigInteger number = new BigInteger(1, messageDigest);
            String hashtext = number.toString(16);
            // Now we need to zero pad it if you actually want the full 32 chars.
            while (hashtext.length() < 32) {
                hashtext = "0" + hashtext;
            }
            return hashtext;
        }
        catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }


    public boolean isConnected(){
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        if (networkInfo != null && networkInfo.isConnected())
            return true;
        else
            return false;
    }


        // Create GetText Metod
        public  void  Sendit(int newdata)  throws UnsupportedEncodingException
        {

        }
}
