"""
game.py — LinearEquations core logic + GTK3 UI.

THE GAME:
  Solve linear equations at two difficulty levels.
  Level 1: one-step equations  (x + 7 = 15,  3x = 24)
  Level 2: two-step equations  (4x + 3 = 19, 2x - 5 = 11)

HOW TO PLAY:
  • Read the equation displayed on screen.
  • Type your answer (the value of x) in the input box.
  • Press Enter or click CHECK to submit.
  • Correct answers increase your score and streak.
  • Wrong answers show the correct answer so you can learn.
  • Complete 10 questions per level to advance (or use toolbar).

No Sugar dependency — activity.py wraps this widget.
"""

import random

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango


CSS = b"""
window, .view { background-color: #1a1a2e; }
#game-box     { background-color: #1a1a2e; }
#card {
    background-color: #16213e;
    border-radius: 16px;
    padding: 32px;
    border: 2px solid #0f3460;
}
#equation-label { font-size: 42px; font-weight: bold; color: #ffffff; }
#level-label    { font-size: 15px; color: #4a90d9; font-weight: bold; }
#score-label    { font-size: 15px; color: #bdc3c7; }
#streak-label   { font-size: 14px; color: #f39c12; }
#feedback-label { font-size: 18px; font-weight: bold; min-height: 30px; }
#answer-entry {
    font-size: 28px;
    background-color: #0f3460;
    color: #ffffff;
    border-radius: 10px;
    border: 2px solid #4a90d9;
    padding: 8px 20px;
    min-width: 160px;
}
#check-btn {
    background-color: #4a90d9;
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 28px;
    border: none;
}
#check-btn:hover { background-color: #357abd; }
#next-btn {
    background-color: #2ecc71;
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
    border-radius: 10px;
    padding: 8px 24px;
    border: none;
}
#hint-label { font-size: 13px; color: #bdc3c7; font-style: italic; }
"""


def _make_level1():
    kind = random.choice(['add', 'sub', 'mul'])
    if kind == 'add':
        x = random.randint(1, 20)
        b = random.randint(1, 20)
        return f'x + {b} = {x + b}', x
    elif kind == 'sub':
        x = random.randint(1, 20)
        b = random.randint(1, x)
        return f'x - {b} = {x - b}', x
    else:
        x = random.randint(2, 12)
        a = random.randint(2, 10)
        return f'{a}x = {a * x}', x


def _make_level2():
    x  = random.randint(1, 15)
    a  = random.randint(2, 8)
    b  = random.randint(1, 15)
    op = random.choice(['+', '-'])
    rhs = a * x + b if op == '+' else a * x - b
    return f'{a}x {op} {b} = {rhs}', x


GENERATORS = {1: _make_level1, 2: _make_level2}


class EquationsWidget(Gtk.Box):

    QUESTIONS_PER_LEVEL = 10

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_name('game-box')

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.level     = 1
        self.score     = 0
        self.streak    = 0
        self.q_count   = 0
        self._answer   = 0
        self._answered = False

        self.on_score_change = None
        self._build_ui()
        self._new_question()

    def _build_ui(self):
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        outer.set_valign(Gtk.Align.CENTER)
        outer.set_halign(Gtk.Align.CENTER)
        self.pack_start(outer, True, True, 0)

        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        card.set_name('card')
        card.set_margin_top(20)
        card.set_margin_bottom(20)
        card.set_margin_start(40)
        card.set_margin_end(40)
        outer.pack_start(card, False, False, 0)

        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        top_row.set_halign(Gtk.Align.CENTER)

        self._level_lbl = Gtk.Label()
        self._level_lbl.set_name('level-label')
        top_row.pack_start(self._level_lbl, False, False, 0)

        self._score_lbl = Gtk.Label()
        self._score_lbl.set_name('score-label')
        top_row.pack_start(self._score_lbl, False, False, 0)

        self._streak_lbl = Gtk.Label()
        self._streak_lbl.set_name('streak-label')
        top_row.pack_start(self._streak_lbl, False, False, 0)

        card.pack_start(top_row, False, False, 0)

        self._eq_lbl = Gtk.Label()
        self._eq_lbl.set_name('equation-label')
        self._eq_lbl.set_halign(Gtk.Align.CENTER)
        card.pack_start(self._eq_lbl, False, False, 0)

        self._hint_lbl = Gtk.Label(label='What is the value of x?')
        self._hint_lbl.set_name('hint-label')
        self._hint_lbl.set_halign(Gtk.Align.CENTER)
        card.pack_start(self._hint_lbl, False, False, 0)

        input_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        input_row.set_halign(Gtk.Align.CENTER)

        self._entry = Gtk.Entry()
        self._entry.set_name('answer-entry')
        self._entry.set_placeholder_text('x = ?')
        self._entry.set_max_length(6)
        self._entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self._entry.connect('activate', self._on_check)
        input_row.pack_start(self._entry, False, False, 0)

        self._check_btn = Gtk.Button(label='CHECK')
        self._check_btn.set_name('check-btn')
        self._check_btn.connect('clicked', self._on_check)
        input_row.pack_start(self._check_btn, False, False, 0)

        card.pack_start(input_row, False, False, 0)

        self._feedback_lbl = Gtk.Label(label='')
        self._feedback_lbl.set_name('feedback-label')
        self._feedback_lbl.set_halign(Gtk.Align.CENTER)
        card.pack_start(self._feedback_lbl, False, False, 0)

        self._next_btn = Gtk.Button(label='Next →')
        self._next_btn.set_name('next-btn')
        self._next_btn.set_halign(Gtk.Align.CENTER)
        self._next_btn.connect('clicked', self._on_next)
        self._next_btn.set_no_show_all(True)
        card.pack_start(self._next_btn, False, False, 0)

        self.show_all()

    def _new_question(self):
        gen = GENERATORS.get(self.level, _make_level2)
        eq, self._answer = gen()
        self._answered = False
        self._eq_lbl.set_text(eq)
        self._feedback_lbl.set_text('')
        self._feedback_lbl.set_markup('')
        self._entry.set_text('')
        self._entry.set_sensitive(True)
        self._check_btn.set_sensitive(True)
        self._next_btn.hide()
        self._update_stats()
        self._entry.grab_focus()

    def _update_stats(self):
        self._level_lbl.set_text(
            f'Level {self.level}  •  Q {self.q_count + 1}/{self.QUESTIONS_PER_LEVEL}'
        )
        self._score_lbl.set_text(f'Score: {self.score}')
        self._streak_lbl.set_text(
            f'🔥 Streak: {self.streak}' if self.streak >= 2 else ''
        )
        if self.on_score_change:
            self.on_score_change(self.score, self.streak, self.level)

    def _on_check(self, *_):
        if self._answered:
            return
        raw = self._entry.get_text().strip()
        try:
            user_ans = int(raw)
        except ValueError:
            self._feedback_lbl.set_markup(
                '<span foreground="#e74c3c">Enter a whole number!</span>'
            )
            return

        self._answered = True
        self.q_count  += 1
        self._entry.set_sensitive(False)
        self._check_btn.set_sensitive(False)

        if user_ans == self._answer:
            self.score  += 10 + self.streak * 2
            self.streak += 1
            self._feedback_lbl.set_markup(
                f'<span foreground="#2ecc71" size="x-large">'
                f'✓ Correct!  +{10 + (self.streak - 1) * 2}</span>'
            )
        else:
            self.streak = 0
            self._feedback_lbl.set_markup(
                f'<span foreground="#e74c3c" size="large">'
                f'✗ Answer was <b>{self._answer}</b></span>'
            )

        self._update_stats()

        if self.q_count >= self.QUESTIONS_PER_LEVEL and self.level < 2:
            self.level   += 1
            self.q_count  = 0
            self._feedback_lbl.set_markup(
                self._feedback_lbl.get_label() +
                '\n<span foreground="#f39c12">⬆  Level 2 unlocked!</span>'
            )

        self._next_btn.show()

    def _on_next(self, *_):
        self._new_question()

    def new_game(self):
        self.level   = 1
        self.score   = 0
        self.streak  = 0
        self.q_count = 0
        self._new_question()

    def set_level(self, level):
        self.level   = level
        self.q_count = 0
        self._new_question()

    def get_state(self):
        return {'level': self.level, 'score': self.score, 'streak': self.streak}

    def set_state(self, state):
        self.level  = state.get('level',  1)
        self.score  = state.get('score',  0)
        self.streak = state.get('streak', 0)
        self.q_count = 0
        self._new_question()
