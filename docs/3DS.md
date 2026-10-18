# Nintendo 3DS

Lighthouse runs on the New Nintendo 3DS, New 3DS XL and New 2DS XL as a homebrew app. The original
3DS, 3DS XL and 2DS start and play in an emulator set to that model, but have not been tried on
real hardware, where they will be much slower.

There is no download: the game's assets come from your own ROM, so you build the app and its asset
archives yourself. This takes three steps:

1. Build the PC version from this branch and use it to turn your ROM into `bk.o2r`.
2. Build the 3DS app in Docker.
3. Copy the app and the two `.o2r` files to the SD card.

## What you need

* A New 3DS with custom firmware ([Luma3DS](https://3ds.hacks.guide/)) and the Homebrew Launcher
* A supported Banjo-Kazooie ROM in `.z64` format (see [Quick Start](../README.md#quick-start)). All four
  versions work on the 3DS: US v1.0, US v1.1, PAL and Japanese. The game plays in the language of the
  ROM you extract (the 3DS build has no menu for choosing a language pack).
* A Linux, macOS or Windows (WSL2) computer with Docker, CMake, Ninja, Python 3 and a C++ compiler

## 1. Generate the asset archives on the PC

The 3DS app reads two archives:

* `lighthouse.o2r`, the port's own assets, built from this repository
* `bk.o2r`, the game's assets, extracted from your ROM

The 3DS app cannot read a ROM itself, so a PC build of the same branch makes `bk.o2r`. Use the PC
build from this branch, not an official Lighthouse release: the asset formats change between
versions, and the 3DS app only accepts archives from its own version.

```bash
git clone --recursive -b 3ds https://github.com/aidenator/Lighthouse.git
cd Lighthouse

cmake -H. -Bbuild-cmake -GNinja -DCMAKE_BUILD_TYPE=Release
cmake --build build-cmake --target GeneratePortO2R
cmake --build build-cmake
```

See [BUILDING.md](BUILDING.md) for the packages each platform needs.

Then run `build-cmake/Lighthouse` and choose your ROM when it asks. It writes `bk.o2r` to its data
folder: `~/.local/share/lighthouse/` on Linux, or the folder with the executable on Windows and
macOS. Once the game reaches its title screen you can quit.

Use the `bk.o2r` the game generates. The one made by the `ExtractAssets` build target has no
version stamp, and the 3DS app rejects it.

Copy `bk.o2r` into the repository folder. The 3DS build takes its app icon (a Mumbo token) from
it; without it the app gets the Lighthouse logo instead. To use a `bk.o2r` somewhere else, add
`-DLH_3DS_ICON_O2R=<path>` to the configure command below.

## 2. Build the 3DS app

The 3DS toolchain (devkitARM, libctru, citro3d) and the libraries Lighthouse needs are set up in a
Docker image. Build the image once:

```bash
docker build -t lighthouse-3ds -f tools/docker/3ds.Dockerfile tools/docker
```

Then configure and build from the repository folder:

```bash
docker run --rm -v "$PWD":/src -w /src lighthouse-3ds \
    cmake -S . -B build-3ds -G Ninja -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_TOOLCHAIN_FILE=/opt/devkitpro/cmake/3DS.cmake
docker run --rm -v "$PWD":/src -w /src lighthouse-3ds cmake --build build-3ds
```

The app is `build-3ds/Lighthouse.3dsx`.

## 3. Copy to the SD card

```
sdmc:/
└── 3ds/
    ├── Lighthouse.3dsx
    └── lighthouse/
        ├── bk.o2r
        └── lighthouse.o2r
```

Both `.o2r` files are in the repository folder after step 1.

To copy without removing the SD card, run [ftpd](https://github.com/mtheall/ftpd) on the 3DS and
use any FTP client.

Start **Banjo-Kazooie** from the Homebrew Launcher. Startup takes a few seconds; the bottom screen
shows the startup log, then the version and frame rate.

## Controls

| 3DS | N64 |
| --- | --- |
| Circle Pad | Control stick |
| A / B | A / B |
| L or ZL | Z |
| R or ZR | R |
| C-stick (New 3DS) or D-pad | C buttons |
| X | C-up (first-person view) |
| Y | C-down |
| START | START |
| START + SELECT | Quit to the Homebrew Launcher |

## Files on the SD card

`sdmc:/3ds/lighthouse/` also holds the saves (`saves/`), settings (`lighthouse.cfg.json`) and a log
(`logs/Lighthouse.log`). The log is the first place to look if the game does not start.

## Known issues

* A few particle effects that read back the screen are missing.
* The grayscale and noise screen effects are not drawn, and the bottom of the intro waterfall has a
  hard edge.
* Entering a level or restarting one can pause for about a second while assets load.

## Development

Builds can be sent straight to the 3DS without the SD card: in the Homebrew Launcher press Y to
start NetLoader, then run

```bash
docker run --rm --network host -v "$PWD":/src -w /src lighthouse-3ds \
    3dslink -a <3ds-ip> build-3ds/Lighthouse.3dsx -s
```

With `-s` the game's output and log stream back to the terminal (they arrive when the game exits).
The [Azahar](https://azahar-emu.org/) emulator also runs the app, with the `.o2r` files in its
`sdmc/3ds/lighthouse/` folder.
