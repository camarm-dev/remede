package dev.camarm.remede;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

public class ActiveRemedeActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        CharSequence text = getIntent().getCharSequenceExtra(Intent.EXTRA_PROCESS_TEXT);
        Boolean readonly = getIntent().getBooleanExtra(Intent.EXTRA_PROCESS_TEXT_READONLY, false);

        String readonlyArg;

        if (readonly) {
            readonlyArg = "true";
        } else {
            readonlyArg = "false";
        }

        Uri page;
        boolean endProcess;
        if (text.toString().contains(" ") && text.charAt(0) != 'à') {
            page = Uri.parse(getResources().getString(R.string.custom_url_scheme) + "://correction?data=" + text.toString().replaceAll("\n", "<newline>") + "&readonly=" + readonlyArg);
            endProcess = false;
        } else {
            page = Uri.parse(getResources().getString(R.string.custom_url_scheme) + "://dictionary/" + text.toString().toLowerCase() + "?close=true");
            endProcess = true;
        }

        Intent definitionIntent = new Intent(this, MainActivity.class)
                .setData(page);
        startActivityForResult(definitionIntent, 1);
        if (endProcess) {
            setResult(Activity.RESULT_OK);
            finish();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (resultCode == RESULT_OK) {
            String result = data.getStringExtra("dev.camarm.remede.ACTIVE_REMEDE_RESULT");
            Log.w("Active Remede", result);
            Intent outgoingIntent = new Intent().putExtra(Intent.EXTRA_PROCESS_TEXT, result);
            setResult(Activity.RESULT_OK, outgoingIntent);
            finish();
        }
    }

}

