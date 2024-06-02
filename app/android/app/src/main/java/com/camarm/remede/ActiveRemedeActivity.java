package com.camarm.remede;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;

public class ActiveRemedeActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        CharSequence text = getIntent().getCharSequenceExtra(Intent.EXTRA_PROCESS_TEXT);
        Intent definitionIntent = new Intent(this, MainActivity.class)
                .setData(Uri.parse(getResources().getString(R.string.custom_url_scheme) + "://dictionnaire/" + text))
                .setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED);
        startActivity(definitionIntent);
    }

}

