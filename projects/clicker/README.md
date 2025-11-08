# Auto Clicker

This is a simple auto clicker program that performs 10,000 mouse clicks in approximately 10 seconds.

## Requirements

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

Run the program with:

```
python autoclicker.py
```

After running the command, you'll have 3 seconds to position your cursor where you want the clicks to occur.

## How It Works

The program uses the `pynput` library to control the mouse. It performs 10,000 left mouse clicks with a small delay (1ms) between each click to prevent system overload. The entire process should take approximately 10 seconds to complete.

## Warning

Use this program responsibly. Rapid clicking may cause issues with some applications or games. The developers are not responsible for any damage caused by using this software.
