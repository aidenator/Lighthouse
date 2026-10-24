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
* **Clear errors when `bk.o2r` is missing or broken.** If `lighthouse.o2r` or `bk.o2r` is missing,
  `bk.o2r` can't be read (damaged or only partly copied), or it was made by another Lighthouse
  version, the bottom screen says so and how to fix it, and waits for START before exiting. A
  damaged `bk.o2r` used to hang startup.
* **Stereoscopic 3D at 60 fps on the New 3DS**, with the 3D slider. Each eye's view shifts by
  depth, with Banjo about at the screen's depth. The HUD and pause menu have a depth of their own,
  and the jigsaw transition comes out of the screen as its pieces fly at the camera. With the
  slider down, the game draws one image, at no extra cost. Textures now live in VRAM, and the GPU
  starts on the left eye while the right one is built. Details in
  [3DS-PERFORMANCE.md](3DS-PERFORMANCE.md#stereoscopic-3d).
* **Old 3DS check.** On an Old 3DS (two cores), the game logic and the work of sending frames to
  the GPU fall back to core 0 beside the renderer. Tested in the Azahar emulator in Old 3DS mode
  (boots, and fits in an Old 3DS's memory) and on a New 3DS made to act like an Old one (268 MHz,
  no L2 cache, cores 0 and 1 only): no crashes or freezes, but far too slow to play. See
  [Old 3DS speed](#old-3ds-speed).

## Later

### Old 3DS speed

On a simulated Old 3DS the game runs at about 10 frames a second, and the game itself slows to
about 10 updates a second instead of 30, so everything moves in slow motion. The CPU work measured
per frame (about 46 ms) would allow about 20 frames a second, but every slow frame takes exactly
98 ms, which points at a wait that runs into a timeout rather than a CPU that is too slow: the game
logic and the renderer seem to wait on each other each frame. Places to look: the threads that now
share core 0 at the same priority (a 3DS thread does not give way to another of equal priority
until it blocks), and the audio thread's share of core 1, where the system's graphics service
also runs.

To test without an Old 3DS, configure with `-DLH_3DS_SIMULATE_OLD=ON` (and
`-DLH_3DS_OLD_INTERPOLATION=ON` to also draw in-between frames). The log's `game:` line shows the
game's own update rate.

### Make `bk.o2r` on the 3DS

Today players make `bk.o2r` on a PC first. Instead, put the ROM in `sdmc:/3ds/lighthouse/` and
have the 3DS build `bk.o2r` itself on the first start, with a progress screen.

* This means building Lighthouse's asset extractor (Torch) into the 3DS app.
* Memory is the main risk: the extractor would have to work through the ROM a piece at a time to
  fit, especially on an Old 3DS.
* Extraction will take a while on a 3DS CPU, but only once.

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
* A settings menu, for options such as draw distance and controls, and the 3D's convergence and
  HUD depth, which today are fixed (with a hidden SELECT + tap control for testing).

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
