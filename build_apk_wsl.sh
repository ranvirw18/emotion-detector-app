#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "[1/4] Installing Linux build dependencies..."
sudo apt update
sudo apt install -y \
  python3-pip python3-venv git zip unzip openjdk-17-jdk \
  autoconf libtool pkg-config zlib1g-dev libncurses-dev \
  cmake libffi-dev libssl-dev build-essential liblzma-dev

echo "[2/4] Installing Buildozer in a local venv..."
python3 -m venv .buildozer-venv
source .buildozer-venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install buildozer cython==0.29.36

echo "[3/4] Building debug APK..."
export BUILDOZER_ALLOW_ROOT=1
printf 'y\n' | buildozer android debug

echo "[4/4] Done. Check the bin/ folder for the generated APK."
