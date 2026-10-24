### Upgrading from v1.0

Replace `3ds/Lighthouse.3dsx` and `3ds/lighthouse/lighthouse.o2r` with the ones in this zip. **Keep
your `bk.o2r`:** it doesn't need to be made again for this release. Your saves and settings carry
over.

### New

- **60 frames per second on a New 3DS.** The game still updates 30 times a second, but the 3DS
  now draws an in-between frame for every update, so motion is twice as smooth. Freezeezy Peak,
  the heaviest level, holds about 60.
- **Stereoscopic 3D.** Push up the 3D slider. Banjo sits at about the screen's depth and the world
  goes back into it; the HUD and pause menu sit slightly in front, and the jigsaw transition's
  pieces fly out of the screen. It holds 60 fps with 3D on, and with the slider down the game
  draws one image at no extra cost.
- **A loading screen and a stats screen** on the bottom screen: a progress bar while the game
  starts, then the current level's notes, Jiggies, honeycombs and time, your game totals and the
  frame rate.
- **Faster startup**, about 2.5 seconds.
- **Clear errors for setup problems.** If `bk.o2r` or `lighthouse.o2r` is missing, damaged or from
  another version, the bottom screen says so and how to fix it, instead of exiting or hanging.

### Under the hood

- All of the New 3DS's cores in use: the renderer, the game's audio, the game logic and the
  in-between frames each get their own.
- Textures in the GPU's own memory (VRAM), and the CPU and GPU working on frames at the same time.
- How each change sped things up is in
  [docs/3DS-PERFORMANCE.md](https://github.com/aidenator/Lighthouse-3DS/blob/3ds-v1.1/docs/3DS-PERFORMANCE.md).

### Known issues

- The Old 3DS, 3DS XL and 2DS (two cores) run the game but far too slowly to play, about 10 fps.
- Unchanged from v1.0: a few particle effects that read back the screen are missing, the grayscale
  and noise screen effects are not drawn, and entering a level can pause for about a second.
