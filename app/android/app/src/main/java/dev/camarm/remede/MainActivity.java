package dev.camarm.remede;

import android.os.Bundle;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(SetResult.class);
        super.onCreate(savedInstanceState);
    }
}
