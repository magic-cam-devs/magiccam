package nahuy.fithcmus.magiccam.presentation.uis.customs.tools;

import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;

import androidx.annotation.NonNull;

import nahuy.fithcmus.magiccam.presentation.uis.App;

public class PreferenceUtil {
    private static PreferenceUtil sInstance;

    public boolean isFirstTime() {
        return isFirstTime;
    }

    public void setFirstTime(boolean firstTime) {
        isFirstTime = firstTime;
    }

    private boolean isFirstTime = true;

    private final SharedPreferences mPreferences;

    private PreferenceUtil(@NonNull final Context context) {
        mPreferences = PreferenceManager.getDefaultSharedPreferences(context);
    }

    public static PreferenceUtil getInstance() {
        if (sInstance == null) {
            sInstance = new PreferenceUtil(App.getInstance().getApplicationContext());
        }
        return sInstance;
    }
}
