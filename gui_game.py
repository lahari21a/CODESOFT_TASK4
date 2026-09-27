#!/usr/bin/env python3
"""
Rock Paper Scissors Arena (Tkinter GUI Version)
A modern dark-themed Graphical User Interface built using Python Tkinter.
Features move selection buttons, score cards, streak tracking, round history, 
sound effects, and mode toggling (Classic 3-choice vs Extended 5-choice).
"""
import random
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import platform
if platform.system() == "Windows":
    try:
        import winsound
        HAS_WINSOUND = True
    except ImportError:
        HAS_WINSOUND = False
else:
    HAS_WINSOUND = False
# Moves & Rules Definitions
CHOICES = {
    "rock": {
        "name": "Rock",
        "symbol": "🪨",
        "color": "#FF4757",
        "beats": {
            "scissors": "crushes",
            "lizard": "crushes"
        }
    },
    "paper": {
        "name": "Paper",
        "symbol": "📄",
        "color": "#2ED573",
        "beats": {
            "rock": "covers",
            "spock": "disproves"
        }
    },
    "scissors": {
        "name": "Scissors",
        "symbol": "✂️",
        "color": "#1E90FF",
        "beats": {
            "paper": "cuts",
            "lizard": "decapitates"
        }
    },
    "lizard": {
        "name": "Lizard",
        "symbol": "🦎",
        "color": "#A55EEA",
        "beats": {
            "spock": "poisons",
            "paper": "eats"
        }
    },
    "spock": {
        "name": "Spock",
        "symbol": "🖖",
        "color": "#FFA502",
        "beats": {
            "scissors": "smashes",
            "rock": "vaporizes"
        }
    }
}
class SoundManager:
    @staticmethod
    def play_tick():
        if HAS_WINSOUND:
            try:
                winsound.Beep(600, 60)
            except Exception:
                pass
    @staticmethod
    def play_win():
        if HAS_WINSOUND:
            try:
                winsound.Beep(523, 100)
                winsound.Beep(659, 100)
                winsound.Beep(784, 150)
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
class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors Arena")
        self.root.geometry("850x700")
        self.root.minsize(750, 600)
        self.root.configure(bg="#0F172A")  # Slate dark background
        # State
        self.player_score = 0
        self.computer_score = 0
        self.ties_score = 0
        self.current_streak = 0
        self.best_streak = 0
        self.mode = "classic"  # 'classic' or 'extended'
        self.is_animating = False
        self.history = []
        self.setup_styles()
        self.create_widgets()
        self.update_choices_grid()
        self.update_ui()
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        # Custom Dark Treeview styling
        self.style.configure("Treeview",
                             background="#1E293B",
                             foreground="#F8FAFC",
                             fieldbackground="#1E293B",
                             rowheight=28,
                             font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading",
                             background="#334155",
                             foreground="#38BDF8",
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#0EA5E9")])
    def create_widgets(self):
        # --- Top Header ---
        header_frame = tk.Frame(self.root, bg="#1E293B", bd=0, relief="flat", padding=15)
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        title_label = tk.Label(header_frame, text="🪨 📄 ✂️ ROCK PAPER SCISSORS ARENA",
                               font=("Segoe UI", 18, "bold"), fg="#00F0FF", bg="#1E293B")
        title_label.pack(side="left")
        # Mode Toggle & Rules Buttons
        controls_frame = tk.Frame(header_frame, bg="#1E293B")
        controls_frame.pack(side="right")
        self.mode_btn = tk.Button(controls_frame, text="Mode: Classic (3)", font=("Segoe UI", 9, "bold"),
                                  bg="#0EA5E9", fg="#000000", activebackground="#38BDF8", activeforeground="#000000",
                                  bd=0, padx=12, pady=6, cursor="hand2", command=self.toggle_mode)
        self.mode_btn.pack(side="left", padx=5)
        rules_btn = tk.Button(controls_frame, text="❓ Rules", font=("Segoe UI", 9, "bold"),
                              bg="#334155", fg="#F8FAFC", activebackground="#475569", activeforeground="#FFFFFF",
                              bd=0, padx=10, pady=6, cursor="hand2", command=self.show_rules)
        rules_btn.pack(side="left", padx=5)
        # --- Scoreboard Cards ---
        score_frame = tk.Frame(self.root, bg="#0F172A")
        score_frame.pack(fill="x", padx=20, pady=10)
        score_frame.columnconfigure((0, 1, 2, 3), weight=1)
        # Helper to build cards
        def create_card(parent, col, title, initial_val, color):
            card = tk.Frame(parent, bg="#1E293B", bd=1, relief="solid")
            card.grid(row=0, column=col, padx=6, sticky="ew")
            t_lbl = tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), fg="#94A3B8", bg="#1E293B")
            t_lbl.pack(pady=(10, 2))
            val_lbl = tk.Label(card, text=str(initial_val), font=("Segoe UI", 24, "bold"), fg=color, bg="#1E293B")
            val_lbl.pack(pady=(0, 10))
            return val_lbl
        self.lbl_player_score = create_card(score_frame, 0, "YOU", 0, "#00F0FF")
        self.lbl_streak = create_card(score_frame, 1, "STREAK 🔥", 0, "#FFC800")
        self.lbl_ties = create_card(score_frame, 2, "TIES", 0, "#94A3B8")
        self.lbl_cpu_score = create_card(score_frame, 3, "COMPUTER", 0, "#FF007F")
        # --- Arena Display ---
        arena_frame = tk.Frame(self.root, bg="#1E293B", bd=1, relief="solid")
        arena_frame.pack(fill="both", expand=True, padx=20, pady=10)
        # Result Banner
        self.lbl_result = tk.Label(arena_frame, text="CHOOSE YOUR MOVE!", font=("Segoe UI", 16, "bold"),
                                   fg="#F8FAFC", bg="#1E293B")
        self.lbl_result.pack(pady=(15, 5))
        self.lbl_subresult = tk.Label(arena_frame, text="Click a move below to play a round", font=("Segoe UI", 10),
                                      fg="#94A3B8", bg="#1E293B")
        self.lbl_subresult.pack(pady=(0, 15))
        # Battle Center (Player Spot vs CPU Spot)
        battle_center = tk.Frame(arena_frame, bg="#1E293B")
        battle_center.pack(expand=True, fill="both", pady=10)
        battle_center.columnconfigure((0, 2), weight=1)
        # Player Spot
        player_box = tk.Frame(battle_center, bg="#0F172A", bd=1, relief="ridge", width=140, height=140)
        player_box.grid(row=0, column=0, padx=20, pady=10)
        player_box.pack_propagate(False)
        tk.Label(player_box, text="YOU", font=("Segoe UI", 8, "bold"), fg="#00F0FF", bg="#0F172A").pack(pady=(4, 0))
        self.lbl_player_symbol = tk.Label(player_box, text="❓", font=("Segoe UI", 36), fg="#94A3B8", bg="#0F172A")
        self.lbl_player_symbol.pack(expand=True)
        self.lbl_player_move_name = tk.Label(player_box, text="Waiting...", font=("Segoe UI", 9, "bold"), fg="#F8FAFC", bg="#0F172A")
        self.lbl_player_move_name.pack(pady=(0, 6))
        # VS Badge
        vs_lbl = tk.Label(battle_center, text="VS", font=("Impact", 22, "italic"), fg="#FF007F", bg="#1E293B")
        vs_lbl.grid(row=0, column=1, padx=10)
        # Computer Spot
        cpu_box = tk.Frame(battle_center, bg="#0F172A", bd=1, relief="ridge", width=140, height=140)
        cpu_box.grid(row=0, column=2, padx=20, pady=10)
        cpu_box.pack_propagate(False)
        tk.Label(cpu_box, text="COMPUTER", font=("Segoe UI", 8, "bold"), fg="#FF007F", bg="#0F172A").pack(pady=(4, 0))
        self.lbl_cpu_symbol = tk.Label(cpu_box, text="❓", font=("Segoe UI", 36), fg="#94A3B8", bg="#0F172A")
        self.lbl_cpu_symbol.pack(expand=True)
        self.lbl_cpu_move_name = tk.Label(cpu_box, text="Waiting...", font=("Segoe UI", 9, "bold"), fg="#F8FAFC", bg="#0F172A")
        self.lbl_cpu_move_name.pack(pady=(0, 6))
        # --- Controls (Choice Buttons) ---
        self.choices_frame = tk.Frame(arena_frame, bg="#1E293B")
        self.choices_frame.pack(pady=15)
        # Action bar (Reset Stats)
        action_frame = tk.Frame(arena_frame, bg="#1E293B")
        action_frame.pack(pady=(0, 15))
        btn_reset = tk.Button(action_frame, text="🗑️ Reset Scores", font=("Segoe UI", 9),
                              bg="#334155", fg="#94A3B8", activebackground="#475569", activeforeground="#FFFFFF",
                              bd=0, padx=12, pady=4, cursor="hand2", command=self.reset_scores)
        btn_reset.pack()
        # --- Bottom History Table ---
        history_frame = tk.Frame(self.root, bg="#1E293B", bd=1, relief="solid")
        history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        hist_header = tk.Label(history_frame, text="📜 Battle History", font=("Segoe UI", 10, "bold"),
                               fg="#38BDF8", bg="#1E293B")
        hist_header.pack(anchor="w", padx=10, pady=5)
        # Treeview
        self.tree = ttk.Treeview(history_frame, columns=("round", "player", "computer", "result"),
                                 show="headings", height=4)
        self.tree.heading("round", text="Round")
        self.tree.heading("player", text="You")
        self.tree.heading("computer", text="Computer")
        self.tree.heading("result", text="Result")
        self.tree.column("round", width=70, anchor="center")
        self.tree.column("player", width=180, anchor="center")
        self.tree.column("computer", width=180, anchor="center")
        self.tree.column("result", width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    def update_choices_grid(self):
        for child in self.choices_frame.winfo_children():
            child.destroy()
        available_keys = ["rock", "paper", "scissors"] if self.mode == "classic" else ["rock", "paper", "scissors", "lizard", "spock"]
        for key in available_keys:
            choice = CHOICES[key]
            btn = tk.Button(self.choices_frame, text=f"{choice['symbol']}\n{choice['name']}",
                            font=("Segoe UI", 12, "bold"), bg="#0F172A", fg=choice['color'],
                            activebackground="#1E293B", activeforeground=choice['color'],
                            bd=2, relief="groove", width=8, height=3, cursor="hand2",
                            command=lambda k=key: self.play_round(k))
            btn.pack(side="left", padx=8)
    def play_round(self, player_move):
        if self.is_animating:
            return
        self.is_animating = True
        self.lbl_result.config(text="BATTLE IN PROGRESS...", fg="#FFC800")
        self.lbl_subresult.config(text="3... 2... 1... SHOW!")
        
        # Animate countdown
        self.countdown(3, player_move)
    def countdown(self, count, player_move):
        if count > 0:
            self.lbl_subresult.config(text=f"Battle starting in {count}...")
            SoundManager.play_tick()
            self.root.after(300, lambda: self.countdown(count - 1, player_move))
        else:
            self.finish_round(player_move)
    def finish_round(self, player_move):
        available_keys = ["rock", "paper", "scissors"] if self.mode == "classic" else ["rock", "paper", "scissors", "lizard", "spock"]
        computer_move = random.choice(available_keys)
        p_choice = CHOICES[player_move]
        c_choice = CHOICES[computer_move]
        # Update Arena Symbols
        self.lbl_player_symbol.config(text=p_choice["symbol"], fg=p_choice["color"])
        self.lbl_player_move_name.config(text=p_choice["name"])
        self.lbl_cpu_symbol.config(text=c_choice["symbol"], fg=c_choice["color"])
        self.lbl_cpu_move_name.config(text=c_choice["name"])
        # Game Logic
        if player_move == computer_move:
            result = "tie"
            self.ties_score += 1
            self.lbl_result.config(text="IT'S A TIE!", fg="#FFC800")
            self.lbl_subresult.config(text=f"Both selected {p_choice['name']}")
            SoundManager.play_tie()
        elif computer_move in p_choice["beats"]:
            result = "win"
            verb = p_choice["beats"][computer_move]
            self.player_score += 1
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
            self.lbl_result.config(text="YOU WIN! 🎉", fg="#00FF87")
            self.lbl_subresult.config(text=f"{p_choice['name']} {verb} {c_choice['name']}!")
            SoundManager.play_win()
        else:
            result = "lose"
            verb = c_choice["beats"][player_move]
            self.computer_score += 1
            self.current_streak = 0
            self.lbl_result.config(text="YOU LOSE! 💥", fg="#FF3366")
            self.lbl_subresult.config(text=f"{c_choice['name']} {verb} {p_choice['name']}!")
            SoundManager.play_lose()
        # Record History
        r_num = len(self.history) + 1
        res_display = "WIN 🏆" if result == "win" else ("LOSE ❌" if result == "lose" else "DRAW 🤝")
        self.history.insert(0, (r_num, f"{p_choice['symbol']} {p_choice['name']}",
                               f"{c_choice['symbol']} {c_choice['name']}", res_display))
        self.update_ui()
        self.is_animating = False
    def update_ui(self):
        self.lbl_player_score.config(text=str(self.player_score))
        self.lbl_cpu_score.config(text=str(self.computer_score))
        self.lbl_ties.config(text=str(self.ties_score))
        self.lbl_streak.config(text=f"{self.current_streak}")
        # Update Treeview History
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.history[:15]:  # show top 15
            self.tree.insert("", "end", values=item)
    def toggle_mode(self):
        if self.mode == "classic":
            self.mode = "extended"
            self.mode_btn.config(text="Mode: Extended (5)", bg="#A55EEA")
        else:
            self.mode = "classic"
            self.mode_btn.config(text="Mode: Classic (3)", bg="#0EA5E9")
        self.update_choices_grid()
        self.lbl_result.config(text="CHOOSE YOUR MOVE!", fg="#F8FAFC")
        self.lbl_subresult.config(text="Switched game mode")
    def show_rules(self):
        rules_text = (
            "CLASSIC RULES:\n"
            "• Rock crushes Scissors\n"
            "• Scissors cuts Paper\n"
            "• Paper covers Rock\n\n"
            "EXTENDED (R-P-S-L-S) RULES:\n"
            "• Scissors cuts Paper & decapitates Lizard\n"
            "• Paper covers Rock & disproves Spock\n"
            "• Rock crushes Lizard & crushes Scissors\n"
            "• Lizard poisons Spock & eats Paper\n"
            "• Spock smashes Scissors & vaporizes Rock"
        )
        messagebox.showinfo("Rock Paper Scissors Rules", rules_text)
    def reset_scores(self):
        if messagebox.askyesno("Reset Scores", "Are you sure you want to reset all scores and history?"):
            self.player_score = 0
            self.computer_score = 0
            self.ties_score = 0
            self.current_streak = 0
            self.best_streak = 0
            self.history.clear()
            self.lbl_player_symbol.config(text="❓", fg="#94A3B8")
            self.lbl_player_move_name.config(text="Waiting...")
            self.lbl_cpu_symbol.config(text="❓", fg="#94A3B8")
            self.lbl_cpu_move_name.config(text="Waiting...")
            self.lbl_result.config(text="CHOOSE YOUR MOVE!", fg="#F8FAFC")
            self.lbl_subresult.config(text="Scores reset")
            self.update_ui()
def main():
    root = tk.Tk()
    app = RockPaperScissorsGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()
