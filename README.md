# ➕ LinearEquations — Sugar Activity

Solve linear equations at two difficulty levels. Built for the [Sugar Learning Platform](https://sugarlabs.org).

---

## 🎮 How to Play

- An equation with **x** is shown on screen
- Type the value of **x** in the input box
- Press **Enter** or click **CHECK** to submit
- Correct answers earn points + streak bonus
- Wrong answers reveal the correct answer so you learn
- Complete 10 questions to advance to Level 2

### Levels

| Level | Example equations |
|---|---|
| 1 — One-step | `x + 7 = 15`, `3x = 24`, `x - 4 = 9` |
| 2 — Two-step | `4x + 3 = 19`, `2x - 5 = 11` |

### Scoring

- **+10** per correct answer
- **+2 bonus** per active streak point (🔥 keep it going!)

---

## 📁 File Structure

```
linear-equations-activity/
├── activity/
│   ├── activity.info
│   └── activity-linearequations.svg
├── activity.py       ← Sugar wrapper (toolbar, Journal)
├── game.py           ← GTK3 game logic (no Sugar dependency)
├── setup.py
├── po/
│   └── POTFILES
└── README.md
```

---

## 🚀 Running

```bash
# On Sugar OS
cd ~/Activities
git clone https://github.com/Bindkushal/linear-equations-activity.git LinearEquations.activity

# Dev testing on Ubuntu
GDK_BACKEND=x11 sugar-activity3
```

---

## 📄 Licence

GPLv3+ — **Kushal** [@Bindkushal](https://github.com/Bindkushal)
