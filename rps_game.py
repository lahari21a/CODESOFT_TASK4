#!/usr/bin/env python3
"""
Rock Paper Scissors Arena (CLI Version)
A feature-rich command-line implementation of Rock-Paper-Scissors with extended R-P-S-L-S mode,
ANSI color highlights, ASCII art, score tracking, win streaks, and sound effects.
"""
import os
import sys
import time
import random
import platform
# Enable ANSI escape sequences on Windows Command Prompt if needed
if platform.system() == "Windows":
    os.system("")
    try:
        import winsound
        HAS_WINSOUND = True
    except ImportError:
        HAS_WINSOUND = False
else:
    HAS_WINSOUND = False
# Color Constants (ANSI)
COLOR_CYAN = "\033[96m"
COLOR_MAGENTA = "\033[95m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"
COLOR_RESET = "\033[0m"
# ASCII Art Visuals for Moves
ASCII_ART = {
    "rock": """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
    """,
    "paper": """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
    """,
    "scissors": """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
    """,
    "lizard": """
       v  v
      (o.o) 
    /  ---  \\
   (__/   \\__)
    """,
    "spock": """
     _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(____)
    """
}
# Move Rules & Definitions
CHOICES = {
    "rock": {
        "name": "Rock 🪨",
        "aliases": ["1", "r", "rock"],
        "beats": {
            "scissors": "crushes",
            "lizard": "crushes"
        }
    },
    "paper": {
        "name": "Paper 📄",
        "aliases": ["2", "p", "paper"],
        "beats": {
            "rock": "covers",
            "spock": "disproves"
        }
    },
    "scissors": {
        "name": "Scissors ✂️",
        "aliases": ["3", "s", "scissors"],
        "beats": {
            "paper": "cuts",
            "lizard": "decapitates"
        }
    },
    "lizard": {
        "name": "Lizard 🦎",
        "aliases": ["4", "l", "lizard"],
        "beats": {
            "spock": "poisons",
            "paper": "eats"
        }
    },
    "spock": {
        "name": "Spock 🖖",
        "aliases": ["5", "k", "spock"],
        "beats": {
            "scissors": "smashes",
            "rock": "vaporizes"
        }
    }
}
class SoundEffects:
    @staticmethod
    def play_tick():
        if HAS_WINSOUND:
            try:
                winsound.Beep(600, 80)
            except Exception:
                pass
    @staticmethod
    def play_win():
        if HAS_WINSOUND:
            try:
                winsound.Beep(523, 100) # C5
                winsound.Beep(659, 100) # E5
                winsound.Beep(784, 150) # G5
            except Exception:
                pass
    @staticmethod
    def play_lose():
        if HAS_WINSOUND:
            try:
                winsound.Beep(300, 120)
                winsound.Beep(200, 180)
            except Exception:
                pass
    @staticmethod
    def play_tie():
        if HAS_WINSOUND:
            try:
                winsound.Beep(440, 150)
            except Exception:
                pass
class RockPaperScissorsCLI:
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.ties_score = 0
        self.current_streak = 0
        self.best_streak = 0
        self.rounds_played = 0
        self.mode = "classic"  # "classic" (3 choices) or "extended" (5 choices)
        self.history = []
    def clear_screen(self):
        os.system("cls" if platform.system() == "Windows" else "clear")
    def print_banner(self):
        print(f"{COLOR_CYAN}{COLOR_BOLD}" + "=" * 60)
        print("    🪨 📄 ✂️  ROCK PAPER SCISSORS ARENA (CLI)  ✂️ 📄 🪨")
        print("=" * 60 + f"{COLOR_RESET}")
        mode_label = "Classic Mode (Rock, Paper, Scissors)" if self.mode == "classic" else "Extended Mode (Rock, Paper, Scissors, Lizard, Spock)"
        print(f" Mode: {COLOR_YELLOW}{mode_label}{COLOR_RESET}")
    def print_scoreboard(self):
        total = self.player_score + self.computer_score + self.ties_score
        win_rate = round((self.player_score / total) * 100, 1) if total > 0 else 0.0
        print(f"\n{COLOR_BOLD}--- SCOREBOARD ---{COLOR_RESET}")
        print(f" {COLOR_CYAN}YOU: {self.player_score}{COLOR_RESET}  |  "
              f"{COLOR_MAGENTA}CPU: {self.computer_score}{COLOR_RESET}  |  "
              f"{COLOR_YELLOW}TIES: {self.ties_score}{COLOR_RESET}  |  "
              f"STREAK: 🔥 {COLOR_BOLD}{self.current_streak}{COLOR_RESET} (Best: {self.best_streak})  |  "
              f"Win Rate: {win_rate}%")
        print("-" * 60)
    def get_available_keys(self):
        return ["rock", "paper", "scissors"] if self.mode == "classic" else ["rock", "paper", "scissors", "lizard", "spock"]
    def prompt_user_choice(self):
        available = self.get_available_keys()
        print("\nSelect your move:")
        for idx, key in enumerate(available, 1):
            name = CHOICES[key]["name"]
            alias_hint = CHOICES[key]["aliases"][1].upper()
            print(f"  [{idx}] or [{alias_hint}] : {name}")
        
        print(f"  [M] Change Game Mode  |  [H] View History  |  [Q] Quit Game")
        while True:
            raw = input(f"\n{COLOR_BOLD}Your choice > {COLOR_RESET}").strip().lower()
            if not raw:
                continue
            if raw in ["q", "quit", "exit"]:
                return "quit"
            if raw in ["m", "mode"]:
                return "mode"
            if raw in ["h", "history"]:
                return "history"
            for key in available:
                if raw in CHOICES[key]["aliases"]:
                    return key
            print(f"{COLOR_RED}Invalid choice! Please enter a valid number or option.{COLOR_RESET}")
    def play_round(self, player_move):
        available = self.get_available_keys()
        computer_move = random.choice(available)
        # Suspense Countdown Animation
        print(f"\n{COLOR_YELLOW}Battle starting...{COLOR_RESET}")
        for i in range(3, 0, -1):
            print(f"  {i}...", end="\r", flush=True)
            SoundEffects.play_tick()
            time.sleep(0.35)
        print("  SHOW!    ")
        # Display Moves
        p_name = CHOICES[player_move]["name"]
        c_name = CHOICES[computer_move]["name"]
        print(f"\n{COLOR_CYAN}{COLOR_BOLD}You played: {p_name}{COLOR_RESET}")
        print(ASCII_ART[player_move])
        
        print(f"{COLOR_MAGENTA}{COLOR_BOLD}Computer played: {c_name}{COLOR_RESET}")
        print(ASCII_ART[computer_move])
        self.rounds_played += 1
        # Determine Winner
        if player_move == computer_move:
            result = "tie"
            self.ties_score += 1
            SoundEffects.play_tie()
            print(f"{COLOR_YELLOW}{COLOR_BOLD}>>> IT'S A TIE! Both selected {p_name} <<<{COLOR_RESET}")
        elif computer_move in CHOICES[player_move]["beats"]:
            result = "win"
            verb = CHOICES[player_move]["beats"][computer_move]
            self.player_score += 1
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
            SoundEffects.play_win()
            print(f"{COLOR_GREEN}{COLOR_BOLD}>>> VICTORY! {p_name} {verb} {c_name}! <<<{COLOR_RESET}")
        else:
            result = "lose"
            verb = CHOICES[computer_move]["beats"][player_move]
            self.computer_score += 1
            self.current_streak = 0
            SoundEffects.play_lose()
            print(f"{COLOR_RED}{COLOR_BOLD}>>> DEFEAT! {c_name} {verb} {p_name}! <<<{COLOR_RESET}")
        self.history.append({
            "round": self.rounds_played,
            "player": player_move,
            "computer": computer_move,
            "result": result
        })
    def show_history(self):
        print(f"\n{COLOR_BOLD}--- BATTLE HISTORY ({len(self.history)} Rounds) ---{COLOR_RESET}")
        if not self.history:
            print(" No rounds played yet.")
            return
        for item in self.history[-10:]:  # Last 10 rounds
            r_num = item["round"]
            p_move = CHOICES[item["player"]]["name"]
            c_move = CHOICES[item["computer"]]["name"]
            res = item["result"]
            
            if res == "win":
                res_str = f"{COLOR_GREEN}WIN{COLOR_RESET}"
            elif res == "lose":
                res_str = f"{COLOR_RED}LOSE{COLOR_RESET}"
            else:
                res_str = f"{COLOR_YELLOW}TIE{COLOR_RESET}"
            print(f" Round #{r_num:02d}: You ({p_move}) vs CPU ({c_move}) => {res_str}")
        
        input(f"\nPress Enter to return to game...")
    def toggle_mode(self):
        if self.mode == "classic":
            self.mode = "extended"
            print(f"\n{COLOR_GREEN}Switched to Extended Mode (5 choices: Rock, Paper, Scissors, Lizard, Spock)!{COLOR_RESET}")
        else:
            self.mode = "classic"
            print(f"\n{COLOR_GREEN}Switched to Classic Mode (3 choices: Rock, Paper, Scissors)!{COLOR_RESET}")
        time.sleep(1)
    def run(self):
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_scoreboard()
            action = self.prompt_user_choice()
            if action == "quit":
                print(f"\n{COLOR_CYAN}Thank you for playing Rock Paper Scissors Arena! Final Score - You: {self.player_score}, CPU: {self.computer_score}{COLOR_RESET}")
                break
            elif action == "mode":
                self.toggle_mode()
            elif action == "history":
                self.show_history()
            else:
                self.play_round(action)
                # Play Again Prompt
                print("\n" + "-" * 40)
                again = input(f"{COLOR_BOLD}Play another round? (Y/n): {COLOR_RESET}").strip().lower()
                if again in ["n", "no"]:
                    print(f"\n{COLOR_CYAN}Thanks for playing! Final Score - You: {self.player_score}, CPU: {self.computer_score}{COLOR_RESET}")
                    break
if __name__ == "__main__":
    game = RockPaperScissorsCLI()
    game.run()
