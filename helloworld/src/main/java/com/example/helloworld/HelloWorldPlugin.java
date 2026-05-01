package com.example.helloworld;

import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.plugin.java.JavaPlugin;

public final class HelloWorldPlugin extends JavaPlugin {
    @Override
    public void onEnable() {
        getLogger().info("HelloWorldPlugin enabled.");
    }

    @Override
    public void onDisable() {
        getLogger().info("HelloWorldPlugin disabled.");
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (command.getName().equalsIgnoreCase("hello")) {
            sender.sendMessage("세계에 오신걸 환영해요!");
            return true;
        }
        return false;
    }
}
