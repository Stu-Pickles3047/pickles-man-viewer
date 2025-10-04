#!/bin/bash

# Script to build pickles-man-viewer package with incremented release number

set -e

# Get current pkgrel from PKGBUILD
current_rel=$(grep '^pkgrel=' PKGBUILD | cut -d'=' -f2)

# Increment pkgrel
new_rel=$((current_rel + 1))

# Update PKGBUILD with new pkgrel
sed -i "s/^pkgrel=.*/pkgrel=$new_rel/" PKGBUILD

# Update version.txt
echo "$pkgver-$new_rel" > version.txt

echo "Updated pkgrel from $current_rel to $new_rel"

# Get package name and version
pkgname=$(grep '^pkgname=' PKGBUILD | cut -d'=' -f2)
pkgver=$(grep '^pkgver=' PKGBUILD | cut -d'=' -f2)

# Create source directory
mkdir -p "$pkgname-$pkgver"

# Copy source files
cp main.py man_page_list_widget.py man_page_viewer_widget.py menu_bar.py search_widget.py welcome_widget.py pickle-logo.ico pickles-man-viewer.desktop CHANGELOG.md version.txt "$pkgname-$pkgver/"

# Create tar.gz
tar -czf "$pkgname-$pkgver.tar.gz" "$pkgname-$pkgver/"

# Generate checksums
makepkg -g

# Clean up
rm -rf "$pkgname-$pkgver"

echo "Created source tarball: $pkgname-$pkgver.tar.gz"

# Build package
makepkg -f

echo "Package built successfully: $pkgname-$pkgver-$new_rel-any.pkg.tar.zst"