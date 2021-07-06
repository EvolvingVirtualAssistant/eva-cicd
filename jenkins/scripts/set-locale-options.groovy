import hudson.plugins.locale.PluginImpl

PluginImpl localePlugin = Jenkins.getInstance().getPlugin("locale")
localePlugin.setSystemLocale("en-US")
localePlugin.setIgnoreAcceptLanguage(true)

return String.format("Jenkins system language successfully changed to %s", Jenkins.getInstance().getPlugin("locale").getSystemLocale())
