#!/usr/bin/env python3
"""
Vibration Simulator - Cross-platform CLI tool
Works on Windows, macOS, and Linux
"""

import time
import sys
import argparse
import os
from enum import Enum

# Fix encoding issues on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    os.system('chcp 65001 >nul 2>&1')

class VibrationIntensity(Enum):
    LIGHT = ("light", 0.1, "~", "░")
    MEDIUM = ("medium", 0.3, "≈", "▒")
    HEAVY = ("heavy", 0.5, "≋", "▓")
    
    def __init__(self, name, duration, symbol, block):
        self.intensity_name = name
        self.duration = duration
        self.symbol = symbol
        self.block = block

class VibrationSimulator:
    def __init__(self):
        self.colors = {
            'reset': '\033[0m',
            'blue': '\033[94m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'red': '\033[91m',
            'bold': '\033[1m',
            'purple': '\033[95m',
        }
    
    def color(self, text, color_name):
        """Add color to text (works in most terminals)"""
        return f"{self.colors.get(color_name, '')}{text}{self.colors['reset']}"
    
    def vibrate(self, intensity: VibrationIntensity, count: int = 1):
        """Simulate vibration with visual and timing feedback"""
        print(self.color("🔊 Vibration Simulator", 'bold'))
        print(self.color("━" * 40, 'blue'))
        
        for i in range(1, count + 1):
            # Create visual representation
            bar_length = int(intensity.duration * 60)
            bar = intensity.block * bar_length
            
            # Color based on intensity
            if intensity == VibrationIntensity.LIGHT:
                colored_bar = self.color(bar, 'green')
            elif intensity == VibrationIntensity.MEDIUM:
                colored_bar = self.color(bar, 'yellow')
            else:  # HEAVY
                colored_bar = self.color(bar, 'red')
            
            print(f"[{i}/{count}] {self.color(intensity.intensity_name.upper(), 'bold')}: {colored_bar}")
            
            # Simulate vibration duration with animated dots
            self._animate_vibration(intensity.duration)
            
            if i < count:
                time.sleep(0.2)  # Pause between vibrations
        
        print(self.color("━" * 40, 'blue'))
        print(self.color("✅ Vibration complete!", 'green'))
    
    def _animate_vibration(self, duration):
        """Show animated feedback during vibration"""
        steps = int(duration * 10)
        for _ in range(steps):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(duration / steps)
        print()  # New line after animation
    
    def play_pattern(self, pattern: list):
        """Play a sequence of vibrations"""
        print(self.color("🎵 Playing vibration pattern...", 'purple'))
        print(self.color("━" * 40, 'blue'))
        
        for index, intensity in enumerate(pattern):
            print(self.color(f"\nStep {index + 1}/{len(pattern)}: {intensity.intensity_name}", 'bold'))
            
            bar_length = int(intensity.duration * 60)
            bar = intensity.block * bar_length
            
            if intensity == VibrationIntensity.LIGHT:
                colored_bar = self.color(bar, 'green')
            elif intensity == VibrationIntensity.MEDIUM:
                colored_bar = self.color(bar, 'yellow')
            else:
                colored_bar = self.color(bar, 'red')
            
            print(colored_bar)
            self._animate_vibration(intensity.duration)
            
            if index < len(pattern) - 1:
                time.sleep(0.3)
        
        print(self.color("\n━" * 40, 'blue'))
        print(self.color("✅ Pattern complete!", 'green'))

def main():
    parser = argparse.ArgumentParser(
        description='📱 Vibration Simulator - Cross-platform CLI tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python vibrate.py --intensity heavy
  python vibrate.py --intensity light --count 3
  python vibrate.py --pattern light,medium,heavy,medium,light
        """
    )
    
    parser.add_argument(
        '--intensity',
        type=str,
        choices=['light', 'medium', 'heavy'],
        default='medium',
        help='Set vibration intensity (default: medium)'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of vibrations (default: 1)'
    )
    
    parser.add_argument(
        '--pattern',
        type=str,
        help='Play a pattern (comma-separated: light,medium,heavy)'
    )
    
    args = parser.parse_args()
    
    simulator = VibrationSimulator()
    
    # Validate count
    if args.count < 1:
        print("❌ Error: Count must be a positive number")
        sys.exit(1)
    
    # Handle pattern mode
    if args.pattern:
        pattern_names = [p.strip() for p in args.pattern.split(',')]
        pattern = []
        
        for name in pattern_names:
            if name == 'light':
                pattern.append(VibrationIntensity.LIGHT)
            elif name == 'medium':
                pattern.append(VibrationIntensity.MEDIUM)
            elif name == 'heavy':
                pattern.append(VibrationIntensity.HEAVY)
            else:
                print(f"❌ Error: Invalid intensity '{name}' in pattern")
                sys.exit(1)
        
        simulator.play_pattern(pattern)
    else:
        # Single intensity mode
        intensity_map = {
            'light': VibrationIntensity.LIGHT,
            'medium': VibrationIntensity.MEDIUM,
            'heavy': VibrationIntensity.HEAVY
        }
        
        intensity = intensity_map[args.intensity]
        simulator.vibrate(intensity, args.count)

if __name__ == "__main__":
    main()


# .github/workflows/vibration.yml content:
"""
name: Vibration Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: List files (debug)
      run: |
        echo "Current directory contents:"
        ls -la
      shell: bash
    
    - name: Test Light Vibration
      run: python vibrate.py --intensity light
      shell: bash
    
    - name: Test Medium Vibration
      run: python vibrate.py --intensity medium --count 2
      shell: bash
    
    - name: Test Heavy Vibration
      run: python vibrate.py --intensity heavy
      shell: bash
    
    - name: Test Pattern
      run: python vibrate.py --pattern light,medium,heavy,medium,light
      shell: bash
    
    - name: Show Help
      run: python vibrate.py --help
      shell: bash
"""
