package com.example.runningtest;

import org.bukkit.Location;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public final class RunningTestPlugin extends JavaPlugin {
    private final Map<UUID, Location> startPoints = new HashMap<>();
    private final Map<UUID, Long> startTimes = new HashMap<>();

    @Override
    public void onEnable() {
        getLogger().info("RunningTestPlugin enabled.");
    }

    @Override
    public void onDisable() {
        getLogger().info("RunningTestPlugin disabled.");
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (!command.getName().equalsIgnoreCase("run")) {
            return false;
        }

        if (!(sender instanceof Player player)) {
            sender.sendMessage("플레이어만 사용할 수 있는 명령어입니다.");
            return true;
        }

        if (args.length != 1) {
            sender.sendMessage("사용법: /run <start|end>");
            return true;
        }

        switch (args[0].toLowerCase()) {
            case "start" -> handleStart(player);
            case "end" -> handleEnd(player);
            default -> sender.sendMessage("사용법: /run <start|end>");
        }

        return true;
    }

    private void handleStart(Player player) {
        UUID uuid = player.getUniqueId();
        startPoints.put(uuid, player.getLocation());
        startTimes.put(uuid, System.currentTimeMillis());
        player.sendMessage("출발 지점을 기록했습니다. 도착 지점에서 /run end를 입력하세요.");
    }

    private void handleEnd(Player player) {
        UUID uuid = player.getUniqueId();
        Location start = startPoints.get(uuid);
        Long startTime = startTimes.get(uuid);

        if (start == null || startTime == null) {
            player.sendMessage("먼저 /run start를 입력하세요.");
            return;
        }

        Location end = player.getLocation();
        if (!start.getWorld().equals(end.getWorld())) {
            player.sendMessage("출발/도착 월드가 달라 측정할 수 없습니다.");
            return;
        }

        double distance = start.distance(end);
        double elapsedSeconds = (System.currentTimeMillis() - startTime) / 1000.0;
        if (elapsedSeconds <= 0.0) {
            player.sendMessage("측정 시간이 너무 짧습니다. 다시 시도하세요.");
            return;
        }

        double speed = distance / elapsedSeconds;
        player.sendMessage(String.format("거리: %.2f 블록", distance));
        player.sendMessage(String.format("시간: %.2f 초", elapsedSeconds));
        player.sendMessage(String.format("속도: %.2f 블록/초", speed));
    }
}
