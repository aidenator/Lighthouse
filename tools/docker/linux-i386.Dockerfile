# 32-bit x86 Linux build environment, for catching pointer-size bugs before they reach 32-bit
# consoles such as the 3DS. Build an LH_SLIM binary with:
#
#   docker build -t lighthouse-i386 -f tools/docker/linux-i386.Dockerfile tools/docker
#   docker run --rm -u $(id -u):$(id -g) -v "$PWD":/src -w /src lighthouse-i386 \
#       sh -c 'cmake -H. -Bbuild-i386 -GNinja -DCMAKE_BUILD_TYPE=Release -DLH_SLIM=ON && cmake --build build-i386'
#
# Xvfb is included so the binary can also run headless inside the container.
FROM i386/debian:bookworm

# Lighthouse needs CMake 3.26+; bookworm ships 3.25, backports has newer
RUN echo "deb http://deb.debian.org/debian bookworm-backports main" > /etc/apt/sources.list.d/backports.list \
    && apt-get update && apt-get install -y --no-install-recommends -t bookworm-backports cmake \
    && apt-get install -y --no-install-recommends \
        build-essential ninja-build git python3 pkg-config ca-certificates \
        libsdl2-dev libzip-dev zipcmp zipmerge ziptool nlohmann-json3-dev libtinyxml2-dev \
        libspdlog-dev libboost-dev libgl-dev libopengl-dev libogg-dev libvorbis-dev libpng-dev \
        xvfb libgl1-mesa-dri gdb \
    && rm -rf /var/lib/apt/lists/*
