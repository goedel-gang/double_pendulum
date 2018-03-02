# double\_pendulum
An animation of the classic "double pendulum" model that demonstrates chaos.
This was made using matplotlib, and all of the maths and the basis of the
animation was drawn from
[matplotlib example](https://matplotlib.org/examples/animation/double_pendulum_animated.html).
However I then refactored this code so I had a double pendulum class to work
with, and created separate subplots with different starting parameters. I also
made it plot the trail of each bob as the animation progressed. I also added a
tiny tiny command line interface.

Here is an image of the chaotic behaviour it might exhibit - the only
difference in starting conditions was that one pendulum was 10 degrees higher:

![figure of pendulums](https://github.com/elterminad0r/double_pendulum/blob/master/mat_chaotic.png)

See also [this](https://youtu.be/eM7zUfZCPS0) video of it in action.

It now also includes a Processing sketch that uses an iterative model of the
double pendulum. This sketch drew the maths from the
[video](https://www.youtube.com/watch?v=uWzPe_S-RVE)
and [code](https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_93_DoublePendulum/CC_93_DoublePendulum.pde)
by Daniel Shiffman, although mostly for formulae - the sketch is now in an
entirely different language, for example.
