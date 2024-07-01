package com.camarm.remede;

import android.app.Activity;
import android.content.Intent;

import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "SetResult")
public class SetResult extends Plugin {

    @PluginMethod()
    public void sendActiveRemedeResult(PluginCall call) {
        String value = call.getString("value");

        Intent returnIntent = new Intent().putExtra("com.camarm.remede.ACTIVE_REMEDE_RESULT", value).putExtra(Intent.EXTRA_PROCESS_TEXT, value);
        getActivity().setResult(Activity.RESULT_OK, returnIntent);
        getActivity().finish();
    }
}
