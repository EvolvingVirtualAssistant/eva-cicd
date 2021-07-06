package io.jenkins.plugins.branch;

import org.jvnet.localizer.Localizable;
import org.jvnet.localizer.ResourceBundleHolder;

public class DescriptorMessages {

    private static final ResourceBundleHolder holder = ResourceBundleHolder.get(
        DescriptorMessages.class);

    public static String My_ProjectRecognizer_DisplayName() {
        return holder.format("ProjectRecognizer.DisplayName", new Object[0]);
    }

    public static Localizable _My_ProjectRecognizer_DisplayName() {
        return new Localizable(holder, "ProjectRecognizer.DisplayName", new Object[0]);
    }
}
