pkgname=pickles-man-viewer
pkgver=1.0.0
pkgrel=2
pkgdesc="A PyQt6-based man page viewer for Pickles Linux"
arch=('any')
url="https://github.com/Stu-Pickles3047/pickles-man-viewer"
license=('GPL')
depends=('python' 'python-pyqt6' 'man-db')
source=("$pkgname-$pkgver.tar.gz")
sha256sums=('SKIP')

prepare() {
    # Create source directory
    mkdir -p "$pkgname-$pkgver"

    # Copy source files
    cp ../*.py ../*.ico ../*.desktop ../CHANGELOG.md ../version.txt "$pkgname-$pkgver/"
}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    
    # Create installation directory
    install -dm755 "$pkgdir/etc/pickles-linux/pickles-man-viewer"
    
    # Install Python files
    install -Dm644 welcome_widget.py "$pkgdir/etc/pickles-linux/pickles-man-viewer/welcome_widget.py"
    install -Dm644 man_page_list_widget.py "$pkgdir/etc/pickles-linux/pickles-man-viewer/man_page_list_widget.py"
    install -Dm644 search_widget.py "$pkgdir/etc/pickles-linux/pickles-man-viewer/search_widget.py"
    install -Dm644 man_page_viewer_widget.py "$pkgdir/etc/pickles-linux/pickles-man-viewer/man_page_viewer_widget.py"
    install -Dm644 menu_bar.py "$pkgdir/etc/pickles-linux/pickles-man-viewer/menu_bar.py"
    
    # Install main executable
    install -Dm755 main.py "$pkgdir/etc/pickles-linux/pickles-man-viewer/main.py"

    # Install version file
    install -Dm644 version.txt "$pkgdir/etc/pickles-linux/pickles-man-viewer/version.txt"

    # Install icon
    install -Dm644 pickle-logo.ico "$pkgdir/etc/pickles-linux/pickles-man-viewer/pickle-logo.ico"

    # Install changelog
    install -Dm644 CHANGELOG.md "$pkgdir/etc/pickles-linux/pickles-man-viewer/CHANGELOG.md"

    # Create /usr/bin directory
    install -dm755 "$pkgdir/usr/bin"

    # Create symlink to /usr/bin
    ln -s /etc/pickles-linux/pickles-man-viewer/main.py "$pkgdir/usr/bin/pickles-man-viewer"
    
    # Install desktop file
    install -Dm644 pickles-man-viewer.desktop "$pkgdir/usr/share/applications/pickles-man-viewer.desktop"
}
