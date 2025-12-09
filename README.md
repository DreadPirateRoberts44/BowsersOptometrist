# BowsersOptometrist

Image Processing Program designed to destroy Bowsers Inside Story

The program can now play the game at normal speed, with a high score capping around 123

Looking to switch to a vertical display for personal preference. As long as it works, this might inherently work better (smaller search space), though it shouldn't come at the cost of performance

Search space was reduced (increasing search speed), and time to click was reduced. This increased score by 40.

Remaining issues:
the click time is a bottleneck, it takes at least .1 second to click
one screenshot can capture multiple goombas, but only click one (due to click time, they'll move by the time you try to click the second)
we click from left to right (in theory we might have time to make a save, but instead the program clicks a leftmost goomba)
