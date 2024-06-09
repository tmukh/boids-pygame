# Boids  with PyGame

Boids is an artificial life program, developed by Craig Reynolds in 1986,  which attempts to simulate the behaviour of birds known as flocking.


## Main idea behind boids

Boids follow a set of 3 rules:
1. Avoidance: Every boids steers away from other boids in a certain radius, which is basically it's "personal space". If there are multiple boids in it's radius, it takes the weighted average of avoidance vectors and steers towards it.
2. Alignment: Every boids tries to rectify it's course to align with other boids in it's vicinity, to face the same direction, it does that by taking the average of the directions in a given radius.
3. Cohesion: Every boids will gravitate towards the center of it's current flock, via the average position of a radius.

# Usage

Install the required dependencies:

    pip install pygame

Run the simulation:

    python boids_simulation.py

# Demo

https://github.com/tmukh/boids-pygame/assets/63726184/5aafd838-57ef-4f95-aab3-e161720030c7


Experiment with the parameters! The current setup is merely a demo of fast boids.




