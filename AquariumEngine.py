# import all of the necessary libraries
import sys, pygame
import os
from pygame.locals import *
import random
import AquariumGraphics

class Food():
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.radius = 15
        self.speed = random.randint(4,10)

    def move_down(self):
        self.y += self.speed
        ######################################################
        # Q7: Fill in this method
        ######################################################


class Pipe():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.radius = 70
        # list of Food objects which have been added to this pipe
        self.food_pieces = []

    def add_food(self):
        add_food_int = random.randint(1, 100)
        if add_food_int == 1 or 2:
            self.food_pieces.append(Food(self.x, 70))

    def move_food(self, boundary_y, player):
        count = 0
        ######################################################
        # Q9: Remove food from self.food_pieces if it falls outside the game
        ######################################################

        for food in self.food_pieces:
            food.move_down()
            if food.y - food.radius > boundary_y:
                self.food_pieces.remove(food)

            if food.x == player.x:
                if food.y >= player.y and food.y <= player.y+player.height:
                    self.food_pieces.remove(food)
                    count += 1
        return count


class Fish(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, aquarium_width):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_pos
        self.y = y_pos



        self.aquarium_width = aquarium_width
        self.speed = 10

        ######################################################
        # Q1: Set the height and width of the player to suitable values
        ######################################################
        self.height = 80
        self.width = 100

        # Load image for player
        # (you can open the image in the assets folder to see what it looks like)
        image_unscaled_left = pygame.image.load(os.path.join("assets", "goldfish_left.png"))
        image_unscaled_right = pygame.image.load(os.path.join("assets", "goldfish_right.png"))



        # Scale the player's character have the specified height and width
        self.image_left = pygame.transform.rotate(pygame.transform.scale(
            image_unscaled_left, (self.width, self.height)), 0)

        self.rect = self.image_left.get_rect()
        self.image = self.image_left

        self.image_right = pygame.transform.rotate(pygame.transform.scale(
            image_unscaled_right, (self.width, self.height)), 0)

        self.rect = self.image_right.get_rect()




    def handle_movement(self, keys_pressed):
        """
        Update player's position according to the key pressed
        """
        if keys_pressed[pygame.K_LEFT] and self.x >= 30:
            self.x -= self.speed
            self.image = self.image_left
        elif keys_pressed[pygame.K_RIGHT] and self.x <=500:
            self.x += self.speed
            self.image = self.image_right
        else:
            return
        self.rect.x = self.x


class Aquarium():
    def __init__(self, width, height):
        ## initialise pygame
        pygame.init()
        pygame.font.init()

        self.score = 0
        self.game_running = True

        ## game constants
        self.width = width
        self.height = height

        ## player (the fish)
        self.player = Fish(x_pos=width/2,
                           y_pos=height-70,
                           aquarium_width=self.width)

        ## pipe
        self.pipe = Pipe()

        ## interface
        self.DISPLAY = AquariumGraphics.setup_display(self.width, self.height)

        ## draw initial board
        self.draw()

    def draw(self):
        # A wrapper around the `AquariumGraphics.draw_board` function that picks all
        # the right components of `self`.
        AquariumGraphics.draw_board(self.DISPLAY, self.width, self.height, self.score,
                                    self.game_running, self.player, self.pipe)

    def game_loop(self):
        while self.game_running:
            ######################################################
            # Q6: Uncomment self.pipe.add_food()
            ######################################################
            # Add food to the pipe
            add_food_int = random.randint(1, 100)
            if add_food_int == 1 or add_food_int == 2:
                self.pipe.add_food()

            # Process all events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

            # Check which key has been pressed (if any) and move player accordingly
            keys_pressed = pygame.key.get_pressed()
            self.player.handle_movement(keys_pressed)

            # Move food down pipe
            count = self.pipe.move_food(boundary_y=self.height, player=self.player)
            self.score += count

            # Refresh the display and loop back
            self.draw()
            pygame.display.update()

            pygame.time.wait(40)

        # Once the game is finished, print the user's score and wait for the `QUIT` event.
        # Note: in its current form, this game doesn't end without the user closing the application
        # since the player can't lose. However, if you extend the game to enable the player to lose,
        # the following code will be useful.
        print('SCORE:  ', self.score)
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            pygame.time.wait(40)
