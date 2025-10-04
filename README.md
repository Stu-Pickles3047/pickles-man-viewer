# Pickles Man Page Viewer

A PyQt6-based graphical user interface for viewing Linux man pages, designed for Pickles Linux.

## Features

- Browse man pages by section with collapsible groups
- Search functionality across all man pages
- Random man page display
- Light and dark theme support
- Print man pages
- Zoom controls for text viewing
- Command-line version display

## Requirements

- Python 3
- PyQt6
- man-db (for man page database)

## Installation

### From Pickles-Linux Repo
1. Coming Soon

### Manual Build

1. Clone the repository:
   ```bash
   git clone https://github.com/Stu-Pickles3047/pickles-man-viewer.git
   cd pickles-man-viewer
   ```

2. Run the build script:
   ```bash
   ./build.sh
   ```

3. Install the package:
   ```bash
   sudo pacman -U pickles-man-viewer-1.0.0-1-any.pkg.tar.zst
   ```

## Usage

Launch the application:
```bash
pickles-man-viewer
```

Or run directly:
```bash
python main.py
```

## Building from Source

To build the package locally:

1. Ensure you have the necessary dependencies installed
2. Run `./build.sh` to create the package

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the GPL.

## Author

Stu-Pickles3047

Website: [https://github.com/Stu-Pickles3047](https://github.com/Stu-Pickles3047)
