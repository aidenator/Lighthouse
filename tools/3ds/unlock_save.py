#!/usr/bin/env python3
"""Make an "access only" Banjo-Kazooie save from a Lighthouse save file.

Every move learned; every world, note door, lair obstacle, water switch and cauldron opened the way the game's own
Treasure Trove Cove sandcastle codes do it (castle.c). Collectibles are left as they are, and
the banned-code counter stays at 0, so the sandcastle's save-erasing penalty never applies.

Usage: unlock_save.py <in.json> <out.json>
"""
import json
import sys

# What each puzzle code writes besides its own flag: (puzzle pieces placed, world open flag)
PUZZLES = {
    "CC": 5, "BGS": 7, "FP": 8, "GV": 9, "MMM": 10, "RBB": 12, "CCW": 15,
}
# Not covered by any code, set the same way
EXTRA_PUZZLES = {"MM": 1, "TTC": 2}


def main(src, dst):
    save = json.load(open(src))

    for table in ("learned", "used"):
        for move in save["abilities"][table]:
            save["abilities"][table][move] = 1

    cheats = save["cheats"]
    for name in cheats:
        if name.startswith("SANDCASTLE_"):
            cheats[name] = 1
    cheats["CHEAT_ENTERED"] = 1
    cheats["BANNED_CHEATCODES_ENTERED"] = 0

    lair = save["worlds"]["LAIR"]["progress"]
    for world, pieces in {**EXTRA_PUZZLES, **PUZZLES}.items():
        lair[f"{world}_PUZZLE_PIECES_PLACED"] = pieces
        lair[f"{world}_OPEN"] = 1
    # The CCW podium code also presses and activates the podium
    lair["CCW_PUZZLE_PODIUM_SWITCH_PRESSED"] = 1
    lair["CCW_PUZZLE_PODIUM_ACTIVE"] = 1
    for name in lair:
        if name.startswith("NOTE_DOOR_") and name.endswith("_OPEN"):
            lair[name] = 1
    # Not covered by any code: the first two water switches pressed, raising the water to Rusty
    # Bucket Bay's entrance, and every cauldron teleport the game uses. The third switch only
    # raises the water for 30 seconds on an hourglass (quiz/game.c), so it stays off.
    for i in (1, 2):
        lair[f"WATER_SWITCH_{i}_PRESSED"] = 1
        lair[f"LAIR_WATER_LEVEL_{i}"] = 1
    for colour in ("PINK", "GREEN", "RED", "YELLOW"):
        for i in (1, 2):
            lair[f"{colour}_CAULDRON_{i}_ACTIVE"] = 1

    missing = [k for k in [f"{w}_PUZZLE_PIECES_PLACED" for w in {**EXTRA_PUZZLES, **PUZZLES}]
               if k not in save["worlds"]["LAIR"]["progress"]]
    if missing:
        sys.exit(f"unexpected save layout, missing: {missing}")

    with open(dst, "w") as f:
        json.dump(save, f, indent=4)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
