# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Current

### Added
- Command line version print when running the application
- Clickable GitHub link in the About dialog
- Random man page now shows name and description summary instead of full content
- Name in random man page is clickable to open the full man page
- Random man page refreshes to a new selection when returning to the welcome screen
- Version file for consistent version display across application, About dialog, and command line output
- Menu bar with File, Edit, View, and Help menus
- Print functionality for man pages (File > Print)
- Select All and Copy actions for text selection (Edit menu)
- Light and Dark theme toggles (View menu)
- Zoom In, Zoom Out, and Zoom Reset for the man page viewer (View menu, with Ctrl+ shortcuts)
- Custom About dialog with detailed application information (Help > About)
- Grouping of man pages by section in the list view with collapsible groups
- Human-friendly section names (e.g., "User Commands" for Section 1)
- Improved user interface with better organization

### Changed
- List page now displays section groups with descriptive names instead of generic "Section X"
- List groups now start collapsed by default for better navigation
- List page now uses a tree widget for section-based grouping instead of a flat list

### Fixed
- Improved random man page display logic
- Typos in TODO.md (select instead of seleact, Changelog instead of Chnagelog)
- Syntax error in About dialog due to unterminated string literal in main.py

### Notes
- Program does not create cache files; man pages are loaded on demand