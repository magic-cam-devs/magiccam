package nahuy.fithcmus.magiccam.presentation.uis;

import android.app.Application;

import nahuy.fithcmus.magiccam.presentation.uis.customs.tools.PreferenceUtil;

public class App extends Application {
    private static App mInstance;

    public static synchronized App getInstance() {
        return mInstance;
    }

    public PreferenceUtil getPreferencesUtility() {
        return PreferenceUtil.getInstance();
    }

    @Override
    public void onCreate() {
        super.onCreate();
        mInstance = this;
    }

    @Override
    public void onTerminate() {
        super.onTerminate();
    }
}
