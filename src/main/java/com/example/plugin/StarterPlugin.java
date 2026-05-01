package com.example.plugin;

import org.bukkit.plugin.java.JavaPlugin;

public final class StarterPlugin extends JavaPlugin {
    @Override
    public void onEnable() {
        getLogger().info("StarterPlugin enabled.");
    }

    @Override
    public void onDisable() {
        getLogger().info("StarterPlugin disabled.");
    }
}
