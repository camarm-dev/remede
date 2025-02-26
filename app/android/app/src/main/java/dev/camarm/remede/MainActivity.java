package dev.camarm.remede;

import android.net.Uri;
import android.os.Bundle;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(SetResult.class);
        registerPlugin(TCPClient.class);
        super.onCreate(savedInstanceState);
    }
}
