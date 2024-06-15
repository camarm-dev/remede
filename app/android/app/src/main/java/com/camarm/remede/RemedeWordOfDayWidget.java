package com.camarm.remede;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.StrictMode;
import android.widget.RemoteViews;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

/**
 * Implementation of App Widget functionality.
 */
public class RemedeWordOfDayWidget extends AppWidgetProvider {

    public static String CLICK_ACTION = "com.camarm.remede.action.OPEN_WORD_OF_DAY";
    public static String DEFAULT_WORD_JSON = "{}";

    private static JSONObject getJsonResponse(URL url) throws JSONException, IOException {
        String plain = getPlainResponse(url);
        return new JSONObject(plain);
    }

    private static String getPlainResponse(URL url) throws IOException {
        String inline = "";
        Scanner scanner = new Scanner(url.openStream());
        while (scanner.hasNext()) {
            inline += scanner.nextLine();
        }
        return inline;
    }

    public static JSONObject getWordDocument(String word) throws JSONException, IOException {
        URL getDocumentUrl = new URL("https://api-remede.camarm.fr/word/" + word);
        return getJsonResponse(getDocumentUrl);
    }

    public static String getWordOfDay() throws IOException, JSONException {
        URL getWordUrl = new URL("https://api-remede.camarm.fr/word-of-day");

        HttpURLConnection wordConnection = (HttpURLConnection) getWordUrl.openConnection();
        wordConnection.setRequestMethod("GET");
        wordConnection.connect();

        if (wordConnection.getResponseCode() == 200) {
            return getPlainResponse(getWordUrl);
        } else {
            throw new IOException();
        }
    }


    static void updateAppWidget(Context context, AppWidgetManager appWidgetManager,
                                int appWidgetId) {

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();

        StrictMode.setThreadPolicy(policy);

        // Construct the RemoteViews object
        RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.remede_word_of_day_widget);

        // Get word of day
        String word;
        try {
            word = getWordOfDay().replaceAll("\"", "");
        } catch (JSONException | IOException e) {
            word = "remède";
        }

        JSONObject wordDocument;

        String nature;
        String phoneme;
        String definition;
        try {
            wordDocument = getWordDocument(word);
            nature = wordDocument.getJSONArray("definitions").getJSONObject(0).getString("classe");
            phoneme = wordDocument.getString("ipa");
            definition = wordDocument.getJSONArray("definitions").getJSONObject(0).getJSONObject("explications").getString("1");
            definition = definition.replaceAll("<[^>]*>", "");
            if (definition.length() > 100) {
                definition = definition.substring(0, 90) + "...";
            }
        } catch (JSONException | IOException e) {
            nature = "Nom propre";
            phoneme = "/ʁəmɛd/";
            definition = "(Informatique) Dictionnaire français, open source et gratuit qui a pour objectif de remplacer Antidote.";
        }

        // Update text on widget
        String capitalizedWord = word.substring(0, 1).toUpperCase() + word.substring(1);
        views.setTextViewText(R.id.wodwidget_word, capitalizedWord);
        views.setTextViewText(R.id.wodwidget_nature, nature);
        views.setTextViewText(R.id.wodwidget_phoneme, phoneme);
        views.setTextViewText(R.id.wodwidget_definition, definition);

        // Handle clicks
        Intent intent = new Intent(context, RemedeWordOfDayWidget.class).setAction(CLICK_ACTION).setData(Uri.parse(context.getResources().getString(R.string.custom_url_scheme) + "://dictionnaire/" + word));
        PendingIntent pendingIntent = PendingIntent.getBroadcast(context, 0, intent, PendingIntent.FLAG_IMMUTABLE);
        views.setOnClickPendingIntent(R.id.container, pendingIntent);

        // Instruct the widget manager to update the widget
        appWidgetManager.updateAppWidget(appWidgetId, views);
    }

    @Override
    public void onUpdate(Context context, AppWidgetManager appWidgetManager, int[] appWidgetIds) {
        // There may be multiple widgets active, so update all of them
        for (int appWidgetId : appWidgetIds) {
            updateAppWidget(context, appWidgetManager, appWidgetId);
        }
    }

    @Override
    public void onEnabled(Context context) {
        // Enter relevant functionality for when the first widget is created
    }

    @Override
    public void onDisabled(Context context) {
        // Enter relevant functionality for when the last widget is disabled
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        super.onReceive(context, intent);
        if (CLICK_ACTION.equals(intent.getAction())) {
            Intent searchbarIntent = new Intent(context, MainActivity.class)
                    .setData(intent.getData())
                    .setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            context.startActivity(searchbarIntent);
        }
    }
}