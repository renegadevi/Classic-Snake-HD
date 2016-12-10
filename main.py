#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#
# Classic Snake HD (main.py)
#
# Copyright (c) 2016 Philip Andersen <philip.andersen@codeofmagi.net>
# Copyright (c) 2016 Code of Magi (http://codeofmagi.net)
#
# This file is part of Snake One HD application
# (https://github.com/renegadevi/Classic-Snake-HD).
#

__author__ = "Philip Andersen <philip.andersen@codeofmagi.net>"
__license__ = "MIT"
__version__ = "1.2"
__copyright__ = "Copyright © 2016 Philip Andersen"

try:
    import sys
    import random
    import json
    import pygame
except ImportError as e:
    exit(str(e) + ". Try install pygame with 'pip3 install pygame'")


class SnakeGame:
    """ A Snake Game made with PyGame """

    def __init__(self):
        """ Load pygame and show the welcome screen

        Load pygame and resources, switch to fullscreen mode, set default
        settings and welcome the user to the welcome screen.
        """

        # Load PyGame
        pygame.init()

        # Switch to fullscreen mode and save resolusion
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_res_x = pygame.display.Info().current_w
        self.screen_res_y = pygame.display.Info().current_h

        # Path to resources
        self.image_welcome = "resources/bg.png"
        self.image_black = "resources/black_35.png"
        self.font = "resources/BowlbyOneSC-Regular.ttf"

        # Set font
        self.font_size_big = int(self.screen_res_x/40)
        self.font_size_small = int(self.screen_res_x/50)
        self.font_big = pygame.font.Font(self.font, self.font_size_big)
        self.font_small = pygame.font.Font(self.font, self.font_size_small)

        # Default (global) game settings
        self.snake_speed = (15, "Easy")
        self.highscore = 0
        self.calculate_grid(first_run=True)

        # Get skins
        try:
            with open('skins.json') as data:
                self.skins = json.load(data)
        except FileNotFoundError as e:
            self.skins = None
            print(str(e) + "\nSkins file missing, using default variables.")
        self.toggle_skin('dark')

        # Show welcome screen
        self.show_welcome_screen(background=self.image_welcome)

    def generate_menu(self, menu, actions, spacing=0.5, item_id=0,
                      item_rgb=(255, 255, 255), item_rgb_active=(255, 0, 255),
                      pos_x=None, pos_y=None):
        """Generates a menu, call it a second time for sub-menus.

        Args:
            menu (list): Menu titles
            actions (list): Menu actions
            spacing (int|float): Item spacing
            item_id (int): Active item id number
            item_rgb (tuple): Item color (RGB value)
            item_rgb_active (tuple): Active item color (RGB value)
            pos_x (int): Menu x position
            pos_y (int): Menu y position
         """

        # Default menu position
        if (pos_x and pos_y) is None:
            pos_x = (self.screen_res_x/10)
            pos_y = (self.screen_res_y/2)

        # Render menu items
        for idx, item in enumerate(menu):
            item_text = self.font_big.render(item, True, item_rgb)
            item_pos = pos_x, self.font_size_big // spacing * idx + pos_y
            self.screen.blit(item_text, item_text.get_rect().move(item_pos))
            pygame.display.update(item_text.get_rect().move(item_pos))

        # Add selected/selected status for menu items
        selected_text = self.font_big.render(item, True, item_rgb_active)
        selected_rect = item_text.get_rect().move(item_pos)
        selected_fill = pygame.Surface.copy(self.screen)

        # Menu loop, wait for user interaction
        key_pressed = True
        while True:

            if key_pressed:

                # Update selected status
                self.screen.blit(selected_fill, selected_fill.get_rect())
                pygame.display.update(selected_rect)

                # Create next selecteded/selected text
                selected_text = self.font_big.render(
                    menu[item_id], True, item_rgb_active)
                selected_rect = selected_text.get_rect().move(
                    pos_x, self.font_size_big // spacing * item_id + pos_y)

                # Draw and update screen
                self.screen.blit(selected_text, selected_rect)
                pygame.display.update(selected_rect)

                # Prevent infinite loop of flickering selected
                key_pressed = False

            for event in pygame.event.get():

                # Check if any key is pressed
                if event.type == pygame.KEYDOWN:
                    key_pressed = True

                    # Check if UP-key is pressed
                    if event.key == pygame.K_UP:
                        if item_id == 0:
                            item_id = len(menu) - 1
                        else:
                            item_id -= 1

                    # Check if DOWN-key is pressed
                    elif event.key == pygame.K_DOWN:
                        if item_id == len(menu) - 1:
                            item_id = 0
                        else:
                            item_id += 1

                    # Check if Enter-key is pressed
                    elif event.key == pygame.K_RETURN:
                        actions[item_id]()

        return item_id

    def calculate_grid(self, first_run=False):
        """ Calculate grid based on resolusion.

        Resolusions is either divided by 8 or 10. It it to update the cell
        dimensions. Use same dimensions for height and width in order to make
        is equal squares.

        Using same dimensions for both width/height for a square grid. With
        some resolusions you need to use both 8 and 10 for x/y for a perfect
        grid, however that would result in a rectangular grid instead.

        Args:
            first_run (bool): Set default value.

        """

        # Set a default value first time running
        if first_run:
            self.cell_size = (40, "Large")

        # Check if it can be divided with resolusion
        if (self.screen_res_x % self.cell_size[0] == 0 and
           self.screen_res_y % self.cell_size[0] == 0):
            self.divided = True
        else:
            self.divided = False
            if first_run:
                self.cell_size = (64, "Large")

        # Set cell dimensions
        self.cell_width = int(self.screen_res_x / self.cell_size[0])
        self.cell_height = int(self.screen_res_y / self.cell_size[0])

    def show_welcome_screen(self, background=(0, 0, 0), game_details=True,
                            game_details_fg=(210, 210, 210), menu_id=0):
        """ Show welcome screen with main menu.

        Shows a welcome screen, the root of the game. Shows a background image
        with a generated main menu. As default showing details about the game
        and is set with game_details.

        Args:
            menu_id (int): Active menu id
            background (tuple|str): Path or RGB value
            game_details (bool): Default set to True, to show game details.
            game_details_fg (tuple): RGB value
        """
        # Draw a background
        if isinstance(background, str):
            self.screen.blit(pygame.transform.scale(
                pygame.image.load(background),
                (self.screen_res_x, self.screen_res_y)
            ), (0, 0))

        else:
            self.screen.fill(background)

        # Draw game details
        if game_details:

            # Difficulty text
            difficulty_text = self.font_small.render(
                "Snake speed: " + self.snake_speed[1], True, game_details_fg)
            difficulty_text_rect = difficulty_text.get_rect().move(
                self.screen_res_x/10,
                self.screen_res_y/5 + self.screen_res_x/40)

            # Grid text
            grid_text = self.font_small.render(
                "Grid size: " + self.cell_size[1], True, game_details_fg)
            grid_text_rect = grid_text.get_rect().move(
                self.screen_res_x/10,
                self.screen_res_y/5 + self.screen_res_x/20)

            # Skin text
            skin_text = self.font_small.render(
                "Skin: " + self.skin_text, True, game_details_fg)
            skin_text_rect = skin_text.get_rect().move(
                self.screen_res_x/10,
                self.screen_res_y/5 + self.screen_res_x/13)

            # Highscore
            highscore_text = self.font_small.render(
                "Highscore:  " + str(self.highscore), True, game_details_fg)
            highscore_text_rect = highscore_text.get_rect().move(
                self.screen_res_x/10,
                self.screen_res_y/5 + self.screen_res_x/8)

            # Draw to screen
            self.screen.blit(difficulty_text, difficulty_text_rect)
            self.screen.blit(grid_text, grid_text_rect)
            self.screen.blit(skin_text, skin_text_rect)
            self.screen.blit(highscore_text, highscore_text_rect)
        pygame.display.update()

        # Main menu
        self.generate_menu(
            menu=[
                'Start Game',
                '- Toggle Speed',
                '- Toggle Grid size',
                '- Toggle Skin',
                'Quit Game'
            ],
            actions=[
                self.game_start,
                self.toggle_snake_speed,
                self.toggle_cell_size,
                self.toggle_skin,
                self.game_exit
            ],
            item_id=menu_id,
            item_rgb=self.skin_fg,
            item_rgb_active=self.skin_fg_active)

    def show_countdown(self, background=None, fg_color=(255, 255, 255)):
        """ Show a countdown (3..2..1..)

        Show a 3-2-1 countdown with a sec delay between each. If no background
        color or path is specificed it will draw ontop of the current screen.

        Args:
            background (str|tuple): Path or RGB value for background
            fg_color (tuple): RGB value for text
        """

        # Load background if any
        if background is not None:
            if isinstance(background, str):
                self.screen.blit(pygame.transform.scale(
                    pygame.image.load(background),
                    (self.screen_res_x, self.screen_res_y)
                ), (0, 0))
            else:
                self.screen.fill(background)

        # Set font
        countdown_font = pygame.font.Font(self.font, int(self.screen_res_x/15))

        # 3
        countdown_3 = countdown_font.render('3', True, fg_color)
        countdown_3_rect = countdown_3.get_rect()
        countdown_3_rect.midtop = (self.screen_res_x/2, self.screen_res_y/8)
        self.screen.blit(countdown_3, countdown_3_rect)
        pygame.display.update()
        pygame.time.wait(1000)

        # 2
        countdown_2 = countdown_font.render('2', True, fg_color)
        countdown_2_rect = countdown_2.get_rect()
        countdown_2_rect.midtop = (self.screen_res_x/2, self.screen_res_y/3)
        self.screen.blit(countdown_2, countdown_2_rect)
        pygame.display.update()
        pygame.time.wait(1000)

        # 1
        countdown_1 = countdown_font.render('1', True, fg_color)
        countdown_1_rect = countdown_1.get_rect()
        countdown_1_rect.midtop = (self.screen_res_x/2, self.screen_res_y/1.8)
        self.screen.blit(countdown_1, countdown_1_rect)
        pygame.display.update()
        pygame.time.wait(1000)

    def toggle_cell_size(self):
        """ Toggle between gird sizes by changing the cell size.

        The value is the amoune of pixel width/height of a sqaure. If the
        resolusion is divided by 10 pixels, then toggle between 10, 20 and 40
        pixels per square. If screen resolusion is dicided by 8, then toggle
        between 16, 32, 64 pixels.

        After new value is set, then recalculate the grid and return to the
        welcome screen.
        """
        if self.cell_size[0] == 10:
            self.cell_size = (20, "Medium")
        elif self.cell_size[0] == 20:
            self.cell_size = (40, "Large")
        elif self.cell_size[0] == 40:
            self.cell_size = (10, "Small")
        elif self.cell_size[0] == 16:
            self.cell_size = (32, "Medium")
        elif self.cell_size[0] == 32:
            self.cell_size = (64, "Large")
        elif self.cell_size[0] == 64:
            self.cell_size = (16, "Small")

        self.calculate_grid()
        self.show_welcome_screen(menu_id=2, background=self.image_welcome)

    def toggle_skin(self, get_skin=False, get_toggle=False):
        """ Toggle between skins or get desired skin.

        Args:
            get_skin (bool): If true get the skin instead of toggle
            get_toggle (bool): If true place menu marker on skin toggle
        """

        # Check if skins.json returned some data
        if self.skins:

            # See if it's asking for a specified skin, else toggle
            if get_skin:
                self.skin = get_skin
            else:
                get_toggle = True

                # Loop and get key-value of next skin, if it loops
                # to the end, then pick the first one from the loop
                loop, first_loop = 0, 0
                for key, value in sorted(self.skins.items()):

                    # Save data from first loop
                    if first_loop == 0:
                        first_key = key
                        first_loop += 1

                    # Check if to break
                    if loop == 1:
                        get_skin = key
                        self.skin = key
                        break

                    # If skin matches, then break next loop
                    if key == self.skin:
                        loop += 1

            # If the loop never break, use values from first loop
            if get_skin is False:
                get_skin = first_key
                self.skin = first_key

            # Set skin variables
            self.skin_text = self.skins[get_skin]['label']
            self.skin_bg = tuple(self.skins[get_skin]['bg'])
            self.skin_fg = tuple(self.skins[get_skin]['fg'])
            self.skin_fg_active = tuple(self.skins[get_skin]['fg_active'])
            self.skin_apple = tuple(self.skins[get_skin]['apple'])
            self.skin_snake = tuple(self.skins[get_skin]['snake'])
            self.skin_snake_edges = tuple(self.skins[get_skin]['snake_edges'])
            self.skin_grid = tuple(self.skins[get_skin]['grid'])

        else:
            # Use default values
            self.skin = 'default'
            self.skin_text = "Default (Missing skins file)"
            self.skin_bg = (40, 44, 52)
            self.skin_fg = (225, 228, 234)
            self.skin_fg_active = (198, 120, 214)
            self.skin_apple = (224, 106, 92)
            self.skin_snake = (198, 120, 214)
            self.skin_snake_edges = (168, 0, 205)
            self.skin_grid = (59, 64, 72)

        # Update background
        self.image_welcome = 'skins/' + self.skin + '.png'

        # Return to welcome screen
        if get_toggle:
            self.show_welcome_screen(menu_id=3, background=self.image_welcome)
        else:
            self.show_welcome_screen(background=self.image_welcome)

    def toggle_snake_speed(self):
        """ Toggle between snake speed difficulty.

        Snake speed is based on the fps clock, which is divided in 4 speeds
        which also makes up for the difficulty in the game.

        10 = Very Easy
        15 = Easy
        30 = Medium
        60 = Hard
        """
        if self.snake_speed[0] == 10:
            self.snake_speed = (15, "Easy")
        elif self.snake_speed[0] == 15:
            self.snake_speed = (30, "Medium")
        elif self.snake_speed[0] == 30:
            self.snake_speed = (60, "Hard")
        elif self.snake_speed[0] == 60:
            self.snake_speed = (10, "Very Easy")

        self.fps_clock = pygame.time.Clock()
        self.fps_clock.tick(self.snake_speed[0])
        self.show_welcome_screen(menu_id=1, background=self.image_welcome)

    def get_keypress(self):
        """ Wait for user interaction for Enter-key. """
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and
                   event.key == pygame.K_RETURN):
                    return True

    def get_random_location(self):
        """ Get a random location on grid """
        return {
            'x': random.randint(0, self.cell_width - 1),
            'y': random.randint(0, self.cell_height - 1)
        }

    def draw_grid(self):
        """ Draw a square grid """

        # Horizontal lines
        for x in range(0, self.screen_res_x, self.cell_size[0]):
            pygame.draw.line(
                self.screen,
                self.skin_grid,
                (x, 0),
                (x, self.screen_res_y))

        # Vertical lines
        for y in range(0, self.screen_res_y, self.cell_size[0]):
            pygame.draw.line(
                self.screen,
                self.skin_grid,
                (0, y),
                (self.screen_res_x, y))

    def draw_snake(self, snake_coord):
        """ Draw snake based on coordinates.

        Args:
            snake_coord (dict): List of three dicts with x/y coordinates
        """
        for coordinates in snake_coord:

            # Get coordinates
            x = coordinates['x'] * self.cell_size[0]
            y = coordinates['y'] * self.cell_size[0]

            # Draw snake inner edge
            snake_edge_rect = pygame.Rect(
                x, y,
                self.cell_size[0],
                self.cell_size[0]
            )
            pygame.draw.rect(
                self.screen,
                self.skin_snake_edges,
                snake_edge_rect
            )

            # Fill snake color
            snake_rect = pygame.Rect(
                x + 2,
                y + 2,
                self.cell_size[0] - 4,
                self.cell_size[0] - 4
            )
            pygame.draw.rect(
                self.screen,
                self.skin_snake,
                snake_rect
            )

    def draw_apple(self, coordinates):
        """ Draw a square (apple) based on coordinates.

        Args:
            coordinates (dict): Dict with x/y coordinates
        """
        x = coordinates['x'] * self.cell_size[0]
        y = coordinates['y'] * self.cell_size[0]

        apple_rect = pygame.Rect(
            x, y,
            self.cell_size[0],
            self.cell_size[0]
        )
        pygame.draw.rect(
            self.screen,
            self.skin_apple,
            apple_rect
        )

    def draw_score(self, score):
        """ Draw score during the game.

        Args:
            score (int): current score
        """
        # Create score text
        score_text = 'Score: ' + str(score * self.snake_speed[0])
        score_text = self.font_small.render(score_text, True, self.skin_fg)
        score_rect = score_text.get_rect()
        score_rect.topleft = (20, 10)

        # Update on screen
        self.screen.blit(score_text, score_rect)

    def game_start(self):
        """ Start the snake game

        Starting a new game, sets default in-game settings and the main game
        loop.
        """
        # Default in-game settings
        self.fps_clock = pygame.time.Clock()
        self.total_score = 0
        apple = self.get_random_location()
        move = 'up'
        tip = 0
        if self.divided:
            snake_coord = [
                {
                    'x': self.cell_width - 6,
                    'y': self.cell_height - 6
                },
                {
                    'x': self.cell_width - 7,
                    'y': self.cell_height - 6
                },
                {
                    'x': self.cell_width - 8,
                    'y': self.cell_height - 6
                }]
        else:
            snake_coord = [
                {
                    'x': self.cell_width - 4,
                    'y': self.cell_height - 4
                },
                {
                    'x': self.cell_width - 5,
                    'y': self.cell_height - 4
                },
                {
                    'x': self.cell_width - 6,
                    'y': self.cell_height - 4
                }]

        # Main game loop
        first_loop = True
        while True:
            # Set fps clock
            self.fps_clock.tick(self.snake_speed[0])
            # Draw background and grid
            self.screen.fill(self.skin_bg)
            self.draw_grid()

            # Show countdown
            if first_loop:
                self.show_countdown(
                    background='resources/black_35.png',
                    fg_color=self.skin_fg
                )
                first_loop = False

            # Change snake move depending on user input
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and move is not 'right':
                        move = 'left'
                    elif event.key == pygame.K_RIGHT and move is not 'left':
                        move = 'right'
                    elif event.key == pygame.K_DOWN and move is not 'up':
                        move = 'down'
                    elif event.key == pygame.K_UP and move is not 'down':
                        move = 'up'
                    elif event.key == pygame.K_ESCAPE:
                        return self.game_over(
                            background='resources/black_35.png',
                            fg_color=self.skin_fg
                        )

            # Game over if the snake hit a edge
            if (snake_coord[tip]['x'] == -1 or
                snake_coord[tip]['x'] == self.cell_width or
                snake_coord[tip]['y'] == -1 or
               snake_coord[tip]['y'] == self.cell_height):
                return self.game_over(
                    background='resources/black_35.png',
                    fg_color=self.skin_fg
                )

            # Game over if the snake hit it self
            for body in snake_coord[1:]:
                if (body['x'] == snake_coord[tip]['x'] and
                   body['y'] == snake_coord[tip]['y']):
                    return self.game_over(
                        background='resources/black_35.png',
                        fg_color=self.skin_fg
                    )

            # Check if the snake hit a apple
            if (snake_coord[tip]['x'] == apple['x'] and
               snake_coord[tip]['y'] == apple['y']):
                apple = self.get_random_location()
            else:
                del snake_coord[-1]

            # Move the snake by switching squares
            if move is 'right':
                snake_head = {
                    'x': snake_coord[tip]['x'] + 1,
                    'y': snake_coord[tip]['y']
                }
            elif move is 'left':
                snake_head = {
                    'x': snake_coord[tip]['x'] - 1,
                    'y': snake_coord[tip]['y']
                }
            elif move is 'up':
                snake_head = {
                    'x': snake_coord[tip]['x'],
                    'y': snake_coord[tip]['y'] - 1
                }
            elif move is 'down':
                snake_head = {
                    'x': snake_coord[tip]['x'],
                    'y': snake_coord[tip]['y'] + 1
                }

            # Draw and update screen and variables
            snake_coord.insert(0, snake_head)
            self.draw_snake(snake_coord)
            self.draw_apple(apple)
            self.draw_score(len(snake_coord) - 3)
            self.total_apples = len(snake_coord) - 3
            self.total_score = self.total_apples * self.snake_speed[0]
            pygame.display.update()

    def game_over(self, background=None, fg_color=(255, 255, 255)):
        """ Game over screen

        Args:
            background (str|tuple): Path or RGB value
            fg_color (tuple): RGB value for primary text
        """
        # Load background
        if background is not None:
            if isinstance(background, str):
                self.screen.blit(pygame.transform.scale(
                    pygame.image.load(background),
                    (self.screen_res_x, self.screen_res_y)
                ), (0, 0))
            else:
                self.screen.fill(background)

        # Fonts
        font_game_over = pygame.font.Font(self.font, 150)
        font_game_over_small = pygame.font.Font(self.font, 75)
        font_game_over_smallest = pygame.font.Font(self.font, 50)

        # Game over
        game_over = font_game_over.render('Game Over', True, fg_color)
        game_over_rect = game_over.get_rect()
        game_over_rect.midtop = (self.screen_res_x / 2, 10)

        # Total score
        total_score = font_game_over_small.render(
            "Total score: " + str(self.total_score), True, fg_color
        )
        total_score_rect = total_score.get_rect()
        total_score_rect.midtop = (
            self.screen_res_x / 2,
            self.screen_res_y / 3
        )

        # Highscore
        if self.total_score > self.highscore:
            self.highscore = self.total_score
            highscore_text = font_game_over_smallest.render(
                "New highscore!", True, fg_color
            )
            highscore_rect = highscore_text.get_rect()
            highscore_rect.midtop = (
                self.screen_res_x / 2,
                self.screen_res_y / 4
            )
            self.screen.blit(highscore_text, highscore_rect)

        # Total apples
        apples_text = font_game_over_smallest.render(
            "Total apples: " + str(self.total_apples), True, fg_color
        )
        apples_rect = apples_text.get_rect()
        apples_rect.midtop = (
            self.screen_res_x / 2,
            self.screen_res_y / 2
        )

        # Press enter
        press_enter = self.font_big.render(
            'Press ENTER to return', True, fg_color
        )
        press_enter_rect = press_enter.get_rect()
        press_enter_rect.midbottom = (
            self.screen_res_x / 2,
            self.screen_res_y - 100
        )

        # Draw on to screen
        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(total_score, total_score_rect)
        self.screen.blit(apples_text, apples_rect)
        self.screen.blit(press_enter, press_enter_rect)
        pygame.display.update()

        # Wait for user to press Enter before returning to show_welcome_screen
        while True:
            if self.get_keypress():
                pygame.event.get()
                self.show_welcome_screen(background=self.image_welcome)

    def game_exit(self):
        """ Quit application; Uninitialize pygame, then system exit """
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Snake = SnakeGame()
