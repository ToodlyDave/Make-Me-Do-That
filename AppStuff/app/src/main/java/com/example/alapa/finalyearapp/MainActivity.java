package com.example.alapa.finalyearapp;

import android.app.ProgressDialog;
import android.app.VoiceInteractor;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v4.content.FileProvider;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;

import static android.os.Environment.getExternalStoragePublicDirectory;

public class MainActivity extends AppCompatActivity {

    public static final String EXTRA_MESSAGE = "com.example.finalyearapp.MESSAGE";
    public static int count = 1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final RequestQueue queue = Volley.newRequestQueue(this);
        Button btn = (Button) findViewById(R.id.button);
        Button send = (Button) findViewById(R.id.button2);

        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getApplicationContext(), "Pushed the button", Toast.LENGTH_SHORT).show();

                connectServer(queue);
            }
        });

        send.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getApplicationContext(), "Camera", Toast.LENGTH_SHORT).show();
                camera();
                //example();
            }
        });

    }

    static final int REQUEST_TAKE_PHOTO = 1;
    Uri photoURI;

    private void example()
    {
        EditText something = findViewById(R.id.editText);
        Intent intent = new Intent(this, theCamera.class);

        String text = something.getText().toString();

        intent.putExtra(EXTRA_MESSAGE, text);
        startActivity(intent);

    }

    String path;

    private File filer(){
        String imageFileName = "Image" + count;

        File storageFile = getExternalFilesDir(Environment.DIRECTORY_PICTURES + "/yoloy/");
        Toast.makeText(getApplicationContext(), "testing now", Toast.LENGTH_SHORT).show();
        Toast.makeText(getApplicationContext(), storageFile.toString(), Toast.LENGTH_SHORT).show();

        if(!storageFile.exists())
        {
            storageFile.mkdirs();
        }

        try {
            return File.createTempFile(imageFileName, ".jpg", storageFile);
        }

        catch (IOException e)
        {
            Toast.makeText(getApplicationContext(), e.toString(), Toast.LENGTH_SHORT).show();
            Log.e("oops", e.toString());
        }

        return null;
    }

    private void camera()
    {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {

            File photoFile = filer();
            //filer();
            //Toast.makeText(getApplicationContext(), "Couldn't get the file thing working", Toast.LENGTH_SHORT).show();

            if(photoFile != null)
            {
                Toast.makeText(getApplicationContext(), "Working?", Toast.LENGTH_SHORT).show();

                Toast.makeText(getApplicationContext(), photoFile.getPath(), Toast.LENGTH_SHORT).show();

                photoURI = FileProvider.getUriForFile(getApplicationContext(),
                        "com.example.android.fileprovider",
                        photoFile);
                takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                startActivityForResult(takePictureIntent, REQUEST_TAKE_PHOTO);
            }

            /*Intent mediaScanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
            File f = new File(photoFile.getAbsolutePath());
            Uri contentUri = Uri.fromFile(f);
            mediaScanIntent.setData(contentUri);
            this.sendBroadcast(mediaScanIntent);*/

        }
    }

    public void connectServer(RequestQueue queue)
    {
        String url = "http://192.168.43.246:5000/";

        JSONObject testText = new JSONObject();
        Toast.makeText(getApplicationContext(), "trying to contact server", Toast.LENGTH_SHORT).show();

        try
        {
            testText.put("status", "This is the app trying to talk to the server. Can you hear me?");

            Bitmap bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), photoURI);
            ByteArrayOutputStream bytearray = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, bytearray);
            byte[] imagebytes = bytearray.toByteArray();
            String image = Base64.encodeToString(imagebytes, Base64.DEFAULT);

            testText.put("payload", image);

        }
        catch(JSONException e)
        {
            Toast.makeText(getApplicationContext(), "cant send data to server", Toast.LENGTH_SHORT).show();
        }
        catch (IOException e)
        {
            Toast.makeText(getApplicationContext(), "cant make image", Toast.LENGTH_SHORT).show();
        }

        final JsonObjectRequest getRequest = new JsonObjectRequest(Request.Method.POST, url, testText, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                //Toast.makeText(getApplicationContext(), response.toString(), Toast.LENGTH_LONG).show();

                try
                {
                    String str = response.getString("payload");
                    Toast.makeText(getApplicationContext(), str, Toast.LENGTH_SHORT).show();
                }

                catch(JSONException e)
                {
                    Toast.makeText(getApplicationContext(), "ERROR", Toast.LENGTH_SHORT).show();
                }

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(getApplicationContext(), error.toString(), Toast.LENGTH_LONG).show();
                Log.d("Error.response", error.toString());
            }
        })
        {

        };

        queue.add(getRequest);

    }
}
