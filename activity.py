"""
activity.py — LinearEquations Sugar Activity
"""
import json
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sugar3.activity import activity
from sugar3.activity.widgets import ActivityToolbarButton, StopButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton

from game import EquationsWidget


class LinearEquationsActivity(activity.Activity):

    def __init__(self, handle):
        super().__init__(handle)

        tb = ToolbarBox()

        ab = ActivityToolbarButton(self)
        tb.toolbar.insert(ab, -1)
        ab.show()

        tb.toolbar.insert(Gtk.SeparatorToolItem(), -1)

        new_btn = ToolButton('view-refresh')
        new_btn.set_tooltip(_('New Game'))
        new_btn.connect('clicked', lambda *_: self._game.new_game())
        tb.toolbar.insert(new_btn, -1)
        new_btn.show()

        tb.toolbar.insert(Gtk.SeparatorToolItem(), -1)

        l1_btn = ToolButton('go-previous')
        l1_btn.set_tooltip(_('Level 1'))
        l1_btn.connect('clicked', lambda *_: self._game.set_level(1))
        tb.toolbar.insert(l1_btn, -1)
        l1_btn.show()

        l2_btn = ToolButton('go-next')
        l2_btn.set_tooltip(_('Level 2'))
        l2_btn.connect('clicked', lambda *_: self._game.set_level(2))
        tb.toolbar.insert(l2_btn, -1)
        l2_btn.show()

        tb.toolbar.insert(Gtk.SeparatorToolItem(), -1)

        self._score_lbl = Gtk.Label(label=_('Score: 0'))
        si = Gtk.ToolItem()
        si.add(self._score_lbl)
        self._score_lbl.show()
        si.show()
        tb.toolbar.insert(si, -1)

        sep = Gtk.SeparatorToolItem()
        sep.props.draw = False
        sep.set_expand(True)
        tb.toolbar.insert(sep, -1)
        sep.show()

        stop_btn = StopButton(self)
        tb.toolbar.insert(stop_btn, -1)
        stop_btn.show()

        tb.show()
        self.set_toolbar_box(tb)

        self._game = EquationsWidget()
        self._game.on_score_change = self._on_score_change
        self._game.show()
        self.set_canvas(self._game)
        self.fullscreen()

    def _on_score_change(self, score, streak, level):
        self._score_lbl.set_text(_('Score: {}').format(score))

    def write_file(self, path):
        json.dump(self._game.get_state(), open(path, 'w'))

    def read_file(self, path):
        try:
            self._game.set_state(json.load(open(path)))
        except Exception:
            self._game.new_game()
