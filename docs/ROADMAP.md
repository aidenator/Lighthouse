# Roadmap

What's planned for the 3DS port after v1.0. Plans change; this is a list of intentions, not
promises.

## Next release (v1.1)

### Done so far

* **60 frames per second on the New 3DS.** Frame interpolation is back on, and Freezeezy Peak, the
  heaviest level, holds about 60. The renderer records each frame and a second thread on core 2
  sends it to the GPU, and the per-draw and per-triangle costs in libultraship's citro3d backend
  were cut until a heavy frame takes about 9 ms of the 16.6 ms budget.
* **More cores in use.** On a New 3DS:

  | Core | Work |
  |---|---|
  | 0 | Renderer and main loop |
  | 1 | The game's audio thread (the app borrows 80% of this core's time) |
  | 2 | Game logic, and sending recorded frames to the GPU |
  | 3 | Building in-between frames, when the system grants the core |

* **A loading screen and a stats screen** on the bottom screen. While the game starts, a progress
  bar, the step under way and the latest log line, with errors kept up in red. During play, the
  current level's notes, Jiggies, honeycombs and time, the game's totals and the frame rate.
* **Faster startup**: about 2.5 seconds, down from about 5 (and sometimes over 10). Settings are no
  longer rewritten to the SD card when nothing changed, and SDL no longer looks for a romfs the app
  doesn't have.

### Still to do

* **A clear error when `bk.o2r` is missing or broken.** If `bk.o2r` isn't in
  `sdmc:/3ds/lighthouse/`, was made by a different Lighthouse version, or can't be read, show a
  plain message on screen saying what's wrong and how to fix it, instead of exiting or hanging.
  The loading screen already keeps errors up in red; the rest is saying what to do about them.
* Check that the core layout falls back sensibly on an Old 3DS (cores 0 and 1 only).

## Later

### Make `bk.o2r` on the 3DS

Today players make `bk.o2r` on a PC first. Instead, put the ROM in `sdmc:/3ds/lighthouse/` and
have the 3DS build `bk.o2r` itself on the first start, with a progress screen.

* This means building Lighthouse's asset extractor (Torch) into the 3DS app.
* Memory is the main risk: the extractor would have to work through the ROM a piece at a time to
  fit, especially on an Old 3DS.
* Extraction will take a while on a 3DS CPU, but only once.

### Stereoscopic 3D

Use the top screen's 3D, controlled by the console's 3D slider: draw the scene once for each eye,
with each eye's view shifted by a different amount depending on depth, and the HUD at a depth of
its own.

* Drawing twice must not double the CPU cost: record a frame's draws once and replay them for the
  second eye with only the eye's shift changed.
* Settings for depth and convergence, and a way to keep close-ups from popping too far out of the
  screen.
* Lighthouse on PC has no 3D, so this is new work for the port.

### A CIA build

Build a `.cia` alongside the `.3dsx`, so the game can be installed and started from the HOME Menu
as well as the Homebrew Launcher.

* This matters most on an Old 3DS: a CIA declares its own memory and CPU needs, so it can ask for
  the larger memory mode and more of core 1's time, instead of making do with what the Homebrew
  Launcher leaves over.
* Needs a banner, an icon and a title ID, and `makerom` in the build and in CI.

### A better bottom screen

The bottom screen is a text console with the loading bar, the current level's stats, the game's
totals and the frame rate. Make it more useful during play, for example:

* **More stats**: Mumbo tokens, empty honeycombs and Jinjos per world, like the pause menu's totals.
* **An overhead map** of the current world with Banjo's position. The game has no maps of its own,
  so they would have to be drawn from each level's geometry, either ahead of time into images in
  `bk.o2r` or live as a cheap top-down render.
* A settings menu, for options such as draw distance and controls.

Drawing the bottom screen with the GPU instead of the text console costs some renderer time, so it
has to fit beside 60 fps.

### Lighthouse features

Bring back the PC version's features where they fit on the 3DS, for example:

* The randomizer
* Mods. The 3DS can't load code at runtime, so mods would have to be built into the app.

### Known issues

The [known issues](../README.md#known-issues) in the README: the particle effects that read back
the screen, the grayscale and noise effects, the intro waterfall's edge, and the pause when a level
loads.
