# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### [Added]
- A basic search pane renderer with back and forward button.
- A viewer pane exclusively to play videos.
- Keyboard shortcut 'T' to toggle the search pane visibility.
- Switches the position of search pane according to the size of the main window for (perceived) convenience.
### [Changed]
- Browser stores downloads and cache in `browser/` folder. Persistent storage for cookies and session follows `PySide` default.
