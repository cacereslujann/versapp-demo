package com.versapp.demo;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

public class MainActivity extends Activity {
    private int count;
    private TextView counter;

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        count = savedInstanceState == null ? 0 : savedInstanceState.getInt("count", 0);
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(Color.rgb(241, 245, 249));
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(Gravity.CENTER);
        int pad = (int) (28 * getResources().getDisplayMetrics().density);
        layout.setPadding(pad, pad, pad, pad);
        layout.addView(text("Versapp Demo", 30));
        layout.addView(text("Aplicación Android de prueba", 18));
        layout.addView(text("Versión: " + BuildConfig.VERSION_NAME + "\nBuild: " + BuildConfig.VERSION_CODE + "\nEntorno: " + BuildConfig.ENTORNO.toUpperCase(java.util.Locale.ROOT), 18));
        counter = text("", 24);
        updateCounter();
        layout.addView(counter);
        Button increment = new Button(this);
        increment.setText("Probar contador");
        increment.setOnClickListener(v -> { count++; updateCounter(); });
        layout.addView(increment);
        Button reset = new Button(this);
        reset.setText("Reiniciar");
        reset.setOnClickListener(v -> { count = 0; updateCounter(); });
        layout.addView(reset);
        layout.addView(text("Si podés instalar esta app y usar el contador, el APK de prueba funciona.\nNo requiere cuenta ni conexión a Internet.", 15));
        scroll.addView(layout);
        setContentView(scroll);
    }

    private TextView text(String value, int size) {
        TextView view = new TextView(this);
        view.setText(value);
        view.setTextSize(size);
        view.setTextColor(Color.rgb(30, 41, 59));
        view.setGravity(Gravity.CENTER);
        view.setPadding(0, 16, 0, 16);
        return view;
    }
    private void updateCounter() { counter.setText("Pruebas: " + count); }
    @Override protected void onSaveInstanceState(Bundle out) {
        out.putInt("count", count);
        super.onSaveInstanceState(out);
    }
}
