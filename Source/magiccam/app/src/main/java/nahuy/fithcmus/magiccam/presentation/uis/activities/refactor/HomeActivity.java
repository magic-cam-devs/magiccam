package nahuy.fithcmus.magiccam.presentation.uis.activities.refactor;

import android.app.Activity;
import android.content.res.Configuration;
import android.graphics.Rect;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.core.content.ContextCompat;
import androidx.core.view.WindowInsetsCompat;

import nahuy.fithcmus.magiccam.R;
import nahuy.fithcmus.magiccam.presentation.uis.App;
import nahuy.fithcmus.magiccam.presentation.uis.customs.tools.AppUtil;
import nahuy.fithcmus.magiccam.presentation.uis.customs.tools.SystemBarStyle;

public class HomeActivity extends AppCompatActivity {
    private static final String TAG = "HomeActivity";
    private boolean useDynamicTheme = true;
    private View mRoot;

   @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
       SystemBarStyle.init(this, SystemBarStyle.applySystemTheme(this));

       super.onCreate(savedInstanceState);
        setContentView(R.layout.home_activity_layout);
        mRoot = findViewById(R.id.root);
        //applyInsets();
    }

    private void applyInsets() {
        AppUtil.doOnApplyWindowInset(mRoot, (view, insets, padding) -> {
            view.setPadding(padding.left + insets.getSystemWindowInsetLeft(),
                    view.getPaddingTop(),
                    padding.right + insets.getSystemWindowInsetRight(),
                    view.getPaddingBottom());
            return insets.replaceSystemWindowInsets(new Rect(0, insets.getSystemWindowInsetTop(), 0, insets.getSystemWindowInsetBottom()));
        });
    }

    private void postShowWallpaper() {
        mRoot.post(new Runnable() {
            @Override
            public void run() {
                if(useDynamicTheme) {
                    mRoot.postDelayed(() -> {
                        getWindow().setFlags(WindowManager.LayoutParams.FLAG_SHOW_WALLPAPER, WindowManager.LayoutParams.FLAG_SHOW_WALLPAPER);
                        Log.d(TAG, "set flag FLAG_SHOW_WALLPAPER");
                    }, 2500);
                }
            }
        });
    }
}
