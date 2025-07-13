#!/usr/bin/env python3
"""
GetMeThatDawg CLI - Python orchestrator for getmethatdawg commands
This is a thin wrapper for future extensibility
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: getmethatdawg-cli.py <command> [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    # For now, just delegate to the bash script
    script_dir = Path(__file__).parent.parent
    getmethatdawg_script = script_dir / "bin" / "getmethatdawg"
    
    try:
        subprocess.run([str(getmethatdawg_script), command] + args, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Error: Could not find getmethatdawg script at {getmethatdawg_script}")
        sys.exit(1)

if __name__ == "__main__":
    main() 