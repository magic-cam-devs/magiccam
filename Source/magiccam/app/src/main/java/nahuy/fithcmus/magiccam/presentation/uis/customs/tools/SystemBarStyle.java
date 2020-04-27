package nahuy.fithcmus.magiccam.presentation.uis.customs.tools;

import android.app.Activity;
import android.content.res.Configuration;
import android.graphics.Color;
import android.os.Build;
import android.view.View;
import android.view.WindowManager;

import androidx.appcompat.app.AppCompatDelegate;
import androidx.core.content.ContextCompat;
import androidx.core.content.res.ResourcesCompat;
import androidx.core.view.WindowCompat;


import java.lang.ref.WeakReference;
import java.util.ArrayList;

import nahuy.fithcmus.magiccam.R;

public class SystemBarStyle {
    private ArrayList<Boolean> mStyleList = new ArrayList<>();
    private Activity mActivity;
    public static void init(Activity activity, boolean initLight) {
        sInstance = new SystemBarStyle();
        sInstance.mActivity = activity;
        sInstance.push(initLight);
    }

    public static void destroy() {
        if(sInstance!=null)
        sInstance.mActivity = null;
        sInstance = null;
    }

    public static void pushTheme(boolean light) {
        if(sInstance!=null)
        sInstance.push(light);
    }

    public void push(boolean light) {
        mStyleList.add(light);
        setSystemComponentStyle(light);
    }

    public void pop() {
        if(!mStyleList.isEmpty()) {
            boolean old = mStyleList.remove(mStyleList.size()-1);
            if(!mStyleList.isEmpty()&&mStyleList.get(mStyleList.size()-1)!=old) setSystemComponentStyle(!old);
        }
    }

    public static void popTheme() {
        if(sInstance!=null)
            sInstance.pop();
    }

    /**
     * Cài đặt style các thanh hệ thống
     *
     * @param lightStyle
     */
    private void setSystemComponentStyle(boolean lightStyle) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M&&mActivity!=null) {

            /*  Giao diện sáng, nghĩa là các icon system bar màu tối */
            if (lightStyle) {

                   mActivity.getWindow().getDecorView().setSystemUiVisibility(
                                      View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                         //           | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                                    | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
                                    | View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
                                    | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                   );

                /**
                 * Trên Android O (8.0, API Level 26) mới hỗ trợ icon navigation màu đen (light navigation bar)
                 * Dưới Android O, ta buộc phải để dải màu navigation color màu tối
                 */
                int navBarBackColor = (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) ?
                        Color.TRANSPARENT :
                        ContextCompat.getColor(mActivity, android.R.color.black);
                mActivity.getWindow().setNavigationBarColor(navBarBackColor);

            } else {
                    /*
                Giao diện theme tối, nghĩa là các icon system bar màu sáng
                 */

                mActivity.getWindow().getDecorView().setSystemUiVisibility(
                        View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);

                //mActivity.getWindow().setNavigationBarColor(mActivity.getResources().getColor(R.color.backColorDark, mActivity.getTheme()));

            }
        }

    }
    private static SystemBarStyle sInstance;

    public static boolean applySystemTheme(Activity activity) {
        int themeOption = AppCompatDelegate.getDefaultNightMode();
        switch (themeOption) {
            case AppCompatDelegate.MODE_NIGHT_YES:
                activity.setTheme(R.style.ThemeDark);
                return false;

            case AppCompatDelegate.MODE_NIGHT_NO:
                activity.setTheme(R.style.ThemeLight);
                return true;

            case AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM:
            default:
                int themeMode = activity.getResources().getConfiguration().uiMode &
                        Configuration.UI_MODE_NIGHT_MASK;
                switch (themeMode) {
                    case Configuration.UI_MODE_NIGHT_YES:
                        activity.setTheme(R.style.ThemeDark);
                        return false;

                    case Configuration.UI_MODE_NIGHT_NO:
                    case Configuration.UI_MODE_NIGHT_UNDEFINED:
                    default:
                        activity.setTheme(R.style.ThemeLight);
                        return true;
                }
        }
    }
}