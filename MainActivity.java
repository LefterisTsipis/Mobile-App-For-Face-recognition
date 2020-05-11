package com.example.uploaddemo;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;


public class MainActivity extends AppCompatActivity implements View.OnClickListener{


    private Button UploadBtn,ChooseBtn;
    private EditText NAME;
    private ImageView imgView;
    private final int IMG_REQUEST=1;
    private Bitmap bitmap;
    private String uploadUrl="http://195.251.166.153:80/imageUploadApp/index.php";
    //private String uploadUrl=" http://10.0.2.2:8080/imageUploadDownload/index.php";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        UploadBtn=(Button)findViewById(R.id.UploadBtn);
        ChooseBtn=(Button)findViewById(R.id.ChooseBtn);
        imgView=(ImageView)findViewById(R.id.imgView);
        NAME=(EditText) findViewById(R.id.name);
        UploadBtn.setOnClickListener(this);
        ChooseBtn.setOnClickListener(this);
    }



    @Override
    public void onClick(View v) {


        switch (v.getId())
        {
            case R.id.ChooseBtn:
                selectImage();
                break;

            case R.id.UploadBtn:
                uploadImage();
                break;



        }

    }


    private void selectImage(){
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(intent,IMG_REQUEST);




    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
      //  Uri path=data.getData();

        if(requestCode==IMG_REQUEST && resultCode==RESULT_OK && data!=null){
            Uri path=data.getData();

            try{

                bitmap= MediaStore.Images.Media.getBitmap(getContentResolver(),path);
                imgView.setImageBitmap(bitmap);
                imgView.setVisibility(View.VISIBLE);
                NAME.setVisibility(View.VISIBLE);




            }catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }


        }
    }


    public void uploadImage()
    {
        StringRequest stringRequest= new StringRequest(Request.Method.POST, uploadUrl, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                try {
                    JSONObject jsonObject=new JSONObject(response);
                    String Response=jsonObject.getString("response");
                    Toast.makeText(MainActivity.this,Response,Toast.LENGTH_SHORT).show();
                    imgView.setImageResource(0);
                    imgView.setVisibility(View.GONE);
                    NAME.setText("");
                    NAME.setVisibility(View.GONE);


                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(MainActivity.this,error.getMessage(),Toast.LENGTH_SHORT).show();

            }
        }){
            @Override
            protected Map<String,String> getParams() throws AuthFailureError{
                Map<String,String> params=new HashMap<>();
                params.put("name",NAME.getText().toString().trim());
                params.put("image",imageToString(bitmap));


                return params;

            }

        };

        MySingleton.getInstance(MainActivity.this).addToRequestQue(stringRequest);




    }



    private String imageToString(Bitmap bitmap){
        ByteArrayOutputStream byteArrayOutputStream=new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG,100,byteArrayOutputStream);
        byte[] imgBytes=byteArrayOutputStream.toByteArray();
        return Base64.encodeToString(imgBytes,Base64.DEFAULT);





    }
}
