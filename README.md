# BowsersOptometrist

Image Processing Program designed to destroy Bowsers Inside Story

The program can now play the game at normal speed, with a high score capping around 123

Looking to switch to a vertical display for personal preference. As long as it works, this might inherently work better (smaller search space), though it shouldn't come at the cost of performance

Search space was reduced (increasing search speed), and time to click was reduced. This increased score by 40.

Remaining issues:

major update, using mousedown we have a significantly faster click. However, this has ironcially made performance worse. It seems that with the extra time saved on clicking, we take another screenshot the goomba we already targeted


one screenshot can capture multiple goombas, but only click one (due to click time, they'll move by the time you try to click the second)
we click from left to right (in theory we might have time to make a save, but instead the program clicks a leftmost goomba)
