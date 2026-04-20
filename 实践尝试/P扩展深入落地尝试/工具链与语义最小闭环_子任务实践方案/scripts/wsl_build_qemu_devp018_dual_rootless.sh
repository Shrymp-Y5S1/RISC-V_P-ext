#!/usr/bin/env bash
set -euo pipefail

WORK_ROOT="${WORK_ROOT:-$HOME/qemu-devp018-work}"
QEMU_REPO_URL="${QEMU_REPO_URL:-https://github.com/mollybuild/qemu.git}"
QEMU_BRANCH="${QEMU_BRANCH:-dev-p-018}"
TARGET_LIST="${TARGET_LIST:-riscv64-linux-user,riscv64-softmmu}"

SRC_DIR="$WORK_ROOT/qemu-src"
DEB_CACHE="$WORK_ROOT/deb-cache"
DEPS_DIR="$WORK_ROOT/rootless-deps"

mkdir -p "$WORK_ROOT" "$DEB_CACHE" "$DEPS_DIR"

echo "[1/6] prepare qemu source"
if [[ ! -d "$SRC_DIR/.git" ]]; then
  git clone --depth 1 --branch "$QEMU_BRANCH" "$QEMU_REPO_URL" "$SRC_DIR"
else
  git -C "$SRC_DIR" fetch origin "$QEMU_BRANCH" --depth 1
  git -C "$SRC_DIR" checkout "$QEMU_BRANCH"
  git -C "$SRC_DIR" reset --hard "origin/$QEMU_BRANCH"
fi

echo "[2/6] prepare python tools"
if ! python3 -m pip --version >/dev/null 2>&1; then
  curl -fsSL https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
  python3 /tmp/get-pip.py --user --break-system-packages
fi
python3 -m pip install --user --break-system-packages meson ninja
export PATH="$HOME/.local/bin:$PATH"

echo "[3/6] download rootless deps"
cd "$DEB_CACHE"
rm -f ./*.deb
apt download \
  pkgconf pkgconf-bin libpkgconf3 \
  libglib2.0-dev libglib2.0-dev-bin \
  libpcre2-dev zlib1g-dev libpixman-1-dev \
  libfdt-dev libfdt1 >/dev/null

rm -rf "$DEPS_DIR"
mkdir -p "$DEPS_DIR"
for deb in ./*.deb; do
  dpkg-deb -x "$deb" "$DEPS_DIR"
done

echo "[4/6] configure"
cd "$SRC_DIR"
rm -rf build

export LD_LIBRARY_PATH="$DEPS_DIR/usr/lib/x86_64-linux-gnu"
export PKG_CONFIG="$DEPS_DIR/usr/bin/pkg-config"
export PKG_CONFIG_SYSROOT_DIR="$DEPS_DIR"
export PKG_CONFIG_LIBDIR="$DEPS_DIR/usr/lib/x86_64-linux-gnu/pkgconfig:$DEPS_DIR/usr/lib/pkgconfig:$DEPS_DIR/usr/share/pkgconfig"

./configure \
  --target-list="$TARGET_LIST" \
  --disable-tools \
  --disable-docs \
  --disable-slirp \
  --disable-capstone \
  --disable-bpf \
  --disable-xen \
  --disable-libssh \
  --disable-gnutls \
  --disable-nettle \
  --disable-gcrypt \
  --disable-vnc \
  --disable-sdl \
  --disable-gtk \
  --disable-opengl \
  --disable-curses \
  --disable-virglrenderer \
  --disable-curl \
  --disable-numa \
  --disable-vhost-user \
  --disable-linux-aio \
  --disable-rdma \
  --disable-smartcard \
  --disable-spice \
  --disable-usb-redir \
  --disable-lzo \
  --disable-snappy \
  --disable-zstd \
  --disable-vde \
  --disable-brlapi \
  --disable-pipewire \
  --disable-kvm \
  --disable-hvf \
  --disable-whpx \
  --disable-strip \
  --disable-vhost-vdpa

echo "[5/6] build qemu-riscv64 and qemu-system-riscv64"
make -C build -j"$(nproc)" qemu-riscv64 qemu-system-riscv64

echo "[6/6] build summary"
echo "QEMU source commit: $(git rev-parse --short HEAD)"
echo "QEMU user binary: $SRC_DIR/build/qemu-riscv64"
"$SRC_DIR/build/qemu-riscv64" --version | head -n 1
echo "QEMU system binary: $SRC_DIR/build/qemu-system-riscv64"
"$SRC_DIR/build/qemu-system-riscv64" --version | head -n 1