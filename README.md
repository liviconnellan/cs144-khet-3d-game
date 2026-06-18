# Khet 3D Project
Olivia Connellan
29004691

Welcome to the Khet 3D project for RW144 2025!

## Project Overview
My project is a 3D strategic game where players use mirrors to direct lasers across multiple board layers to eliminate opponent pieces. This is a command-line based adaptation of the classic board game Khet with exciting vertical laser propagation mechanics.

### 2. Project Structure
```
<your-repo-name>
├── .gitignore                  # Git ignore rules (explained below)
├── README.md                   # This file, replace the content with your own
├── src/
│   ├── khet.py                 # Your main program starts here
│   └── cube.py                 
|   └── error.py
|   └── gameboard.py
|   └── lazer.py
│   └── manager.py
|   └── piece.py
|
├── out/                        # Output files go here
├── tests/                      # Test files go here
└── stdlib-python/              # Textbook standard libraries
```

### 4. Implementation Starting Point
- Start coding in `./src/khet.py` - this is my main program entry point
- in the `src/` , there are more files for the project

### The project is executed with the following commands:
```bash
# Standard mode
python3 ./src/khet.py <path_to_config_file>

# With draw detection
python3 ./src/khet.py <path_to_config_file> --draw-detection

# Forced win mode
python3 ./src/khet.py <path_to_config_file> --win-detection <depth>
```

## Additional Resources
- I used w3 Schools to help me understand and use different aspects of the project

**Good luck!**\
\
\
*Author of README: Olivia Connellan
