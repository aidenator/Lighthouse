# Roadmap

What's planned for the 3DS port after v1.0. Plans change; this is a list of intentions, not
promises.

## Next release (v1.1)

### 60 frames per second

The game itself runs at 30 frames a second in play (20 in many cutscenes), as on the N64. Lighthouse
on PC draws extra in-between frames to show 60, but the 3DS build turns that off (`LH_SLIM`, in
`GetInterpolationFPS()` in `src/port/Interpolation/FramePacing.cpp`).

* Turn frame interpolation back on for the New 3DS.
* Make room for it: every frame would need to be drawn in 16.6 ms. On hardware the renderer's CPU
  time is about 10–12 ms a frame on average and about 14 ms in the heaviest scenes; the GPU (about
  4 ms) and the game logic (about 3 ms) have plenty of room. The renderer's time grows with the
  number of draws, so the cost of each draw in libultraship's citro3d backend is the thing to cut.
* Fall back to the game's own rate in scenes that don't fit, rather than stuttering.

### Use every core the 3DS gives us

| Core | Today | Plan |
|---|---|---|
| 0 | Renderer, main loop, audio | Renderer and main loop |
| 1 | Unused | Audio, and other work that can move off core 0 (the app can borrow part of this core's time) |
| 2 (New 3DS) | Game logic | Game logic |
| 3 (New 3DS) | Unused | Spare renderer work, such as building in-between frames, when the system grants the core |

On an Old 3DS (cores 0 and 1 only), the layout should fall back sensibly.

### A clear error when `bk.o2r` is missing or broken

If `bk.o2r` isn't in `sdmc:/3ds/lighthouse/`, was made by a different Lighthouse version, or can't
be read, show a plain message on screen saying what's wrong and how to fix it, instead of exiting
or hanging.

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

Install from the HOME Menu as well as the Homebrew Launcher. A CIA can also be given more memory
and CPU time than a `.3dsx`, which matters most on an Old 3DS.

### Lighthouse features

Bring back the PC version's features where they fit on the 3DS, for example:

* The randomizer
* Mods. The 3DS can't load code at runtime, so mods would have to be built into the app.
* A settings menu on the bottom screen, for options such as draw distance and controls.

### Known issues

The [known issues](../README.md#known-issues) in the README: the particle effects that read back
the screen, the grayscale and noise effects, the intro waterfall's edge, and the pause when a level
loads.
