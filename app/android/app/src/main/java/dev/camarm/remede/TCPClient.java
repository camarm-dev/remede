package dev.camarm.remede;

import android.util.Log;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.PluginResult;
import com.getcapacitor.annotation.CapacitorPlugin;

import org.json.JSONException;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@CapacitorPlugin(name = "TCPClient")
public class TCPClient extends Plugin {

    @PluginMethod()
    public void request(PluginCall call) throws JSONException, IOException {
        String host = call.getString("host", "");
        Integer port = call.getInt("port", 2628);
        JSArray messages = call.getArray("messages", new JSArray());
        Log.i("TCPClient", "Starting communication with " + host + ":" + port + ". Sending " + messages);

        List<String> responses = new ArrayList<>();
        String response = "";

        try {
            Socket socket = new Socket(host, port.intValue());

            // Open stream to the server
            PrintWriter bufferOut = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

            // Open stream from the server
            BufferedReader bufferIn = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            List<String> commands = messages.toList();
            commands.add("QUIT"); // Add a command to close the connection
            for (String command: commands) {  // Send the commands one by one
                sendTcpMessage(bufferOut, command);
            }

            while ((response = bufferIn.readLine()) != null) {
                responses.add(response);
                Log.i("TCPClient", "Received : " + response);
            }

            socket.close();
            bufferOut.flush();
            bufferOut.close();
            bufferIn.close();

        } catch (Exception e) {
            call.reject(e.toString());
        }

        call.resolve(new JSObject().put("responses", new JSArray(responses)));
    }

    void sendTcpMessage(PrintWriter buffer, String message) {
        if (!buffer.checkError()) {
            Log.i("TCPClient", "Sending : "  + message);
            buffer.println(message);
            buffer.flush();
        }
    }
}
