from pathlib import Path

game_lines = [
    "2026-11-01 08:00:00 [INFO] server started",
    "2026-11-01 08:15:30 [INFO] player Alice login",
    "2026-11-01 08:47:12 [WARNING] inventory almost full: Alice",
    "2026-11-01 09:05:00 [ERROR] save failed: disk full",
    "this line is broken",
    "2026-11-01 09:30:41 [INFO] player Bob login",
    "2026-11-01 10:02:19 [ERROR] save failed: timeout",
]
shop_lines = [
    "2026-11-01 07:59:59 [INFO] shop warming up",
    "2026-11-01 08:30:00 [INFO] shop opened",
    "2026-11-01 08:59:59 [WARNING] potion stock low",
    "2026-11-01 25:10:00 [ERROR] clock glitch",
    "2026-11-01 09:45:10 [INFO] Alice bought potion x3",
    "2026-11-01 10:00:00 [CRITICAL] payment service down",
    "2026-11-01 11:20:00 [ERROR] payment retry failed",
]

logs_dir = Path("logs")
(logs_dir / "archive").mkdir(parents=True, exist_ok=True)
(logs_dir / "game_2026-11-01.log").write_text("\n".join(game_lines) + "\n", encoding="utf-8")
(logs_dir / "shop_2026-11-01.log").write_text("\n".join(shop_lines) + "\n", encoding="utf-8")
(logs_dir / "notes.txt").write_text("2026-11-01 09:10:00 [INFO] not a log file\n", encoding="utf-8")
(logs_dir / "archive" / "old.log").write_text("2026-11-01 09:00:00 [ERROR] archived, should be ignored\n", encoding="utf-8")
print("sample logs ready")
