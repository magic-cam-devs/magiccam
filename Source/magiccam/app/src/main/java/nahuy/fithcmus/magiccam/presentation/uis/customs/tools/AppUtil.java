package nahuy.fithcmus.magiccam.presentation.uis.customs.tools;

import android.graphics.Rect;
import android.view.View;

import androidx.core.view.OnApplyWindowInsetsListener;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class AppUtil {
    public static Rect recordInitialPaddingForView(View view) {
        return new Rect(view.getPaddingLeft(), view.getPaddingTop(), view.getPaddingRight(), view.getPaddingBottom());
    }
    public interface WindowInsetsBlockCallback {
        WindowInsetsCompat onCalled(View view, WindowInsetsCompat insets, Rect padding);
    }

    public static void addSystemTopPadding(View view) {
        View targetView = view;
        final boolean isConsumed = false;
        doOnApplyWindowInset(view, (v, insets, initialPadding) -> {
            targetView.setPadding(targetView.getPaddingLeft(), initialPadding.top + insets.getSystemWindowInsetTop(), targetView.getPaddingRight(), targetView.getPaddingBottom());
        if(isConsumed) {
            return insets.replaceSystemWindowInsets(new Rect(insets.getSystemWindowInsetLeft(),0,insets.getSystemWindowInsetRight(), insets.getSystemWindowInsetBottom()));
        } else return insets;
        });
    }

    public static void doOnApplyWindowInset(View view, WindowInsetsBlockCallback block) {
        final Rect initialPadding = recordInitialPaddingForView(view);
        ViewCompat.setOnApplyWindowInsetsListener(view, new OnApplyWindowInsetsListener() {
            @Override
            public WindowInsetsCompat onApplyWindowInsets(View v, WindowInsetsCompat insets) {
                return block.onCalled(v, insets, initialPadding);
            }
        });
        requestApplyInsetsWhenAttached(view);
    }

    private static void requestApplyInsetsWhenAttached(View view) {
        if(view.isAttachedToWindow()) {
            ViewCompat.requestApplyInsets(view);
        } else {
            view.addOnAttachStateChangeListener(new View.OnAttachStateChangeListener() {
                @Override
                public void onViewAttachedToWindow(View v) {
                    v.removeOnAttachStateChangeListener(this);
                    ViewCompat.requestApplyInsets(v);
                }

                @Override
                public void onViewDetachedFromWindow(View v) {}
            });
        }
    }
}
