# LinearEquations

LinearEquations is an algebra practice activity for the Sugar desktop.

LinearEquations presents linear equations and challenges you to find the value of x. Two difficulty levels take you from one-step equations up to two-step equations, with scoring and streaks to keep you motivated.

LinearEquations is not part of the Sugar desktop, but can be added.

Please refer to;
- [How to Get Sugar](https://www.sugarlabs.org),
- [How to use Sugar](https://help.sugarlabs.org),
- [How to use LinearEquations](#how-to-use).

## How to use

- Read the equation shown on screen and find the value of x
- Type your answer in the input box and press Enter or click CHECK
- Correct answers earn +10 points plus a streak bonus
- Wrong answers reveal the correct answer so you can learn
- Complete 10 questions to advance from Level 1 to Level 2
- Use the Level 1 and Level 2 buttons in the toolbar to switch at any time
- Press New Game (↺) in the toolbar to reset your score and start over
- Press the ℹ button in the toolbar to reopen the how-to-play screen

## How to upgrade

On Sugar desktop systems;
- use My Settings, Software Update, or;
- use Browse to open [activities.sugarlabs.org](https://activities.sugarlabs.org), search for LinearEquations, then download.

## How to develop

Setup a [development environment for Sugar desktop](https://github.com/sugarlabs/sugar/blob/master/docs/development-environment.md),
```bash
cd ~/Activities
git clone https://github.com/Bindkushal/linear-equations.activity.git LinearEquations.activity
```

Log out and back in to Sugar — LinearEquations will appear on the home screen.

Test in Terminal by typing;
```
sugar-activity3 activity.LinearEquationsActivity
```

## Dependencies

LinearEquations depends on Python, Sugar Toolkit for GTK+ 3, and GTK+ 3.

## Licence

GPLv3+. See [COPYING](COPYING).
