import random
import pygame
import math


class Boid:
    def __init__(self) -> None:
        Vector2 = pygame.Vector2
        self.position = Vector2(random.randint(
            0, 1280), random.randint(0, 720))

        self.velocity = Vector2(random.random(), random.random())
        self.icon = pygame.image.load("boids.png")

        self.icon = pygame.transform.scale(self.icon, (10, 10))
        self.ray_end = self.position

        print(self.position, self.velocity)

    def update(self, boids):
        self.position += self.velocity

        self.angle = math.degrees(
            math.atan2(-self.velocity.y, self.velocity.x))

        self.avoid(boids)
        self.align(boids)
        self.cohere(boids)

        self.velocity.scale_to_length(10)

        self.position += self.velocity
        print(self.velocity, self.position)

    def cohere(self, boids):
        cohesion_radius = 200
        cohesion_vector = pygame.Vector2()
        total_weight = 0

        for boid in boids:
            if boid != self:
                vector_to_other = boid.position - self.position
                distance_to_other = vector_to_other.length()

                if distance_to_other < cohesion_radius:
                    cohesion_vector += boid.position
                    total_weight += 1

        if total_weight > 0:

            cohesion_vector /= total_weight

            cohesion_vector = cohesion_vector - self.position

            self.velocity += cohesion_vector.normalize()

            pygame.draw.line(screen, (0, 255, 0), self.position,
                             self.position + cohesion_vector, 2)

    def avoid(self, boids):
        edge_threshold = 100
        avoidance_radius = 50
        fov_angle = 260

        boid_avoidance_vector = pygame.Vector2()
        total_weight = 0
        forward_vector = self.velocity.normalize()

        edge_avoidance_vector = pygame.Vector2()
        if self.position.x < edge_threshold:
            edge_avoidance_vector += pygame.Vector2(
                1, 0) * (1 / max(self.position.x, 1))
        if self.position.x > screen.get_width() - edge_threshold:
            edge_avoidance_vector += pygame.Vector2(-1, 0) * (
                1 / max(screen.get_width() - self.position.x, 1))
        if self.position.y < edge_threshold:
            edge_avoidance_vector += pygame.Vector2(
                0, 1) * (1 / max(self.position.y, 1))
        if self.position.y > screen.get_height() - edge_threshold:
            edge_avoidance_vector += pygame.Vector2(0, -1) * (
                1 / max(screen.get_height() - self.position.y, 1))

        if edge_avoidance_vector.length() > 0:
            self.velocity += edge_avoidance_vector.normalize() * 5
        else:
            for boid in boids:
                if boid != self:
                    vector_to_other = boid.position - self.position
                    distance_to_other = vector_to_other.length()

                    if distance_to_other < avoidance_radius:
                        angle_to_other = forward_vector.angle_to(
                            vector_to_other)

                        if abs(angle_to_other) <= fov_angle / 2:
                            weight = 1 / distance_to_other if distance_to_other > 0 else 0
                            boid_avoidance_vector -= vector_to_other.normalize() * weight
                            total_weight += weight

            if total_weight > 0:
                boid_avoidance_vector /= total_weight

            if boid_avoidance_vector.length() > 0:
                self.velocity += boid_avoidance_vector.normalize()

        if self.position.x < 0:
            self.position.x = 0
        if self.position.x > screen.get_width():
            self.position.x = screen.get_width()
        if self.position.y < 0:
            self.position.y = 0
        if self.position.y > screen.get_height():
            self.position.y = screen.get_height()

    def align(self, boids):
        alignment_radius = 50
        alignment_vector = pygame.Vector2()
        total_weight = 0

        for boid in boids:
            if boid != self:
                vector_to_other = boid.position - self.position
                distance_to_other = vector_to_other.length()

                if distance_to_other < alignment_radius:
                    alignment_vector += boid.velocity
                    total_weight += 1

        if total_weight > 0:

            alignment_vector /= total_weight

            self.velocity += alignment_vector.normalize()

    def draw(self, screen):

        rotated_icon = pygame.transform.rotate(self.icon, self.angle)

        rect = rotated_icon.get_rect(center=self.position)
        screen.blit(rotated_icon, rect.topleft)


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


boids = [Boid() for _ in range(3)]

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    for boid in boids:
        if boid.position.x < 0 or boid.position.x > 1280:
            boid.velocity.x *= -1
        if boid.position.y < 0 or boid.position.y > 720:
            boid.velocity.y *= -1

    for boid in boids:
        boid.update(boids)
        boid.draw(screen)

    if pygame.mouse.get_pressed()[0]:
        boids.append(Boid())

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
