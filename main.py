#!/usr/bin/env python3
"""
Rock Paper Scissors Arena - Main Launcher
Chooses automatically between GUI mode (Tkinter) and CLI mode (Terminal).
"""
import sys
import os
def main():
    print("=" * 50)
    print(" 🪨 📄 ✂️  ROCK PAPER SCISSORS ARENA (PYTHON)  ✂️ 📄 🪨")
    print("=" * 50)
    print("Select interface mode:")
    print("  [1] Graphical Interface (Tkinter GUI)")
    print("  [2] Command Line Interface (Terminal CLI)")
    print("  [Q] Quit")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\nStarting Tkinter GUI Application...")
        from gui_game import main as run_gui
        run_gui()
    elif choice == "2":
        from rps_game import RockPaperScissorsCLI
        cli = RockPaperScissorsCLI()
        cli.run()
    elif choice.lower() in ["q", "quit"]:
        print("Goodbye!")
    else:
        print("Defaulting to Graphical Interface (GUI)...")
        from gui_game import main as run_gui
        run_gui()
if __name__ == "__main__":
    main()
