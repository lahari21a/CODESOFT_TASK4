# CODESOFT_TASK4
A fun Rock-Paper-Scissors game where the user plays against the computer. The computer randomly selects rock, paper, or scissors, and the winner is determined using the standard game rules. The game displays results, tracks scores, and allows users to play multiple rounds.
# ✊ Rock-Paper-Scissors Game

A simple and interactive **Rock-Paper-Scissors** game where the user plays against the computer. The computer randomly selects one of the three choices, and the winner is determined according to the traditional game rules.

This project was created as **Task 4** to practice programming fundamentals, user input, randomization, conditional logic, and score tracking.

---

## 📌 Project Overview

Rock-Paper-Scissors is a classic game played between a user and a computer.

The user selects one of:

* ✊ Rock
* ✋ Paper
* ✌️ Scissors

The computer then randomly generates its own choice.

The choices are compared using the following rules:

```text
Rock     beats Scissors
Scissors beats Paper
Paper    beats Rock
```

If both the user and computer choose the same option, the round ends in a **tie**.

---

## ✨ Features

* 🎮 User-friendly game interface
* ✊ Rock selection
* ✋ Paper selection
* ✌️ Scissors selection
* 🤖 Random computer selection
* 🏆 Automatic winner determination
* 📊 Score tracking
* 🔄 Play multiple rounds
* 📢 Displays both user and computer choices
* 💬 Provides clear game feedback
* 🔁 Option to play again

---

## 🎯 Game Rules

The winner is determined according to these rules:

| User Choice | Computer Choice | Result        |
| ----------- | --------------- | ------------- |
| Rock        | Scissors        | User Wins     |
| Scissors    | Paper           | User Wins     |
| Paper       | Rock            | User Wins     |
| Rock        | Paper           | Computer Wins |
| Paper       | Scissors        | Computer Wins |
| Scissors    | Rock            | Computer Wins |
| Same Choice | Same Choice     | Tie           |

### Example

```text
User: Rock
Computer: Scissors

Result: You Win! 🎉
```

---

## 🛠️ Technologies Used

Depending on the implementation, this project can be built using:

* **HTML5** – Structure of the game
* **CSS3** – Styling and user interface
* **JavaScript** – Game logic and interactions
* **Random Number Generation** – Computer's random choice

---

## ⚙️ How the Game Works

The game follows a simple sequence:

```text
        START
          ↓
   User selects choice
          ↓
 Computer generates choice
          ↓
    Compare choices
          ↓
  Determine the winner
          ↓
 Display choices & result
          ↓
    Update the score
          ↓
     Play Again?
       ↙     ↘
     YES      NO
      ↓        ↓
  New Round   END
```

---

## 🎮 How to Play

### Step 1

Start the game.

### Step 2

Choose one of the available options:

```text
Rock
Paper
Scissors
```

### Step 3

The computer randomly selects its choice.

### Step 4

The game compares both choices.

### Step 5

The result is displayed:

* **You Win**
* **You Lose**
* **It's a Tie**

### Step 6

The score is updated.

### Step 7

Choose whether to play another round.

---

## 📊 Score Tracking

The game keeps track of the scores during multiple rounds.

Example:

```text
-------------------------
       SCORE
-------------------------
You      : 3
Computer : 2
Ties     : 1
-------------------------
```

The score is updated after every completed round.

---

## 🖥️ Example Gameplay

```text
================================
     ROCK PAPER SCISSORS
================================

Choose your option:

1. ✊ Rock
2. ✋ Paper
3. ✌️ Scissors

Your choice: Rock

Computer chose: Scissors

🎉 You Win!

Your Score: 1
Computer Score: 0

Do you want to play again? (Y/N)
```

---

## 📁 Project Structure

```text
Rock-Paper-Scissors/
│
├── gui_game.py        # Main game page
├── rps_game.py       # Game styling
├── main.py           # Game logic
└── README.md         # Project documentation
```

If your project is a Python/console version, the structure can instead be:
```

## 🚀 How to Run

### For a Web Version

1. Clone the repository:

```bash
git clone https://github.com/your-username/rock-paper-scissors.git
```

2. Open the project folder:

```bash
cd rock-paper-scissors
```

3. Open `index.html` in your browser.

You can also use **VS Code Live Server** to run the project.

### For a Python Version

Make sure Python is installed, then run:

```bash
python rock_paper_scissors.py
```

---

## 🧠 Concepts Practiced

This project helps beginners understand:

* User input
* Variables
* Conditional statements
* Functions
* Loops
* Random number generation
* Comparison operators
* Boolean logic
* Score tracking
* Event handling
* Basic game development

---

## 🔮 Future Improvements

The game can be improved by adding:

* 🏆 Best-of-3 / Best-of-5 mode
* 🎨 More advanced animations
* 🔊 Sound effects
* 🥇 High-score tracking
* 🌐 Multiplayer mode
* 📱 Improved mobile responsiveness
* 🧠 Difficulty levels
* 📈 Game statistics
* 🌈 Custom themes

---

## 🎯 Objective

The main objective of this project is to create a simple and interactive game while gaining practical experience with programming logic, randomization, user interaction, and score management.

---

## 👩‍💻 Author

**Lahari**

Created as **Task 4 – Rock-Paper-Scissors Game** for practicing programming and application development fundamentals.

---

## 📄 License

This project is created for **educational and learning purposes**.
