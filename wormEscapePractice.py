import pygame, sys, time , random, math, copy

# Initializes pygame
pygame.init()

# Creates surface/window with your monitors dimensions
display_info = pygame.display.Info()

window_width = display_info.current_w - 40
window_height = display_info.current_h - 70

surface = pygame.display.set_mode((window_width, window_height))

#Create sounds:
correct_sound = pygame.mixer.Sound(r"wormEscapeSounds\correct_sound.mp3")
wrong_sound = pygame.mixer.Sound(r"wormEscapeSounds\wrong_sound.mp3")

#Creates color's:
background_color = (65,65,65)
item_color = (255,255,255)
score_color = (100, 255, 100)

#testing variables:
scale_factor = math.sqrt(3 / 4 * 500)
current_input = -scale_factor

#Score variable: the length of the green rectangle
score = 0

#Defining all item/directions
#They are each a dictionary containing two values:
#Image Source and Value (eg. left, right , up, ...)

image_choices = [pygame.image.load(r"wormEscapeImages\arrow_left.png"),
                 pygame.image.load(r"wormEscapeImages\arrow_right.png"),
                 pygame.image.load(r"wormEscapeImages\arrow_up.png"),
                 pygame.image.load(r"wormEscapeImages\arrow_down.png"),
                 pygame.image.load(r"wormEscapeImages\jump.png")]

value_choices = ["left", "right", "up", "down", "jump"]

#///////////////////////////////////////////////////////////////////////////
#The directions which players must react to
class Direction:
    
    #initalized values
    def __init__(self, position = 2000):
        #creates a random index to decide the specific direction
        self.random_choice = random.randint(0,4)
        self.image_source = image_choices[self.random_choice]
        self.value = value_choices[self.random_choice]
        self.position_x = position
        self.position_y = window_height/2 - 250
        self.current_add = 0
        self.copy = self.image_source.copy()
        self.test_value = random.randint(-2,2)

    def draw_transition(self, input):
        if self == direction_list[0]:
            scale = math.sqrt( 3 / 4 * (self.position_x - (window_width/4 - 1500)))
        elif self == direction_list[1]:
            scale = math.sqrt( 3 / 4 * (self.position_x - (window_width/2 - 1000)))
        else:
            return

        
        #Current add equals to y where y = (-x^2)/c + c
        self.current_add = (-(input**2)/scale + scale)

        self.position_x -= self.current_add

        surface.blit(self.image_source, (self.position_x, self.position_y))

    def draw_static(self):

        surface.blit(self.image_source, (self.position_x, self.position_y))
    
    #Makes the image fall away when correctly inputed
    def fall_away(self):

        image = self.copy

        alpha = image.get_alpha() - 3

        if alpha <= 0 or self.position_y > window_height:

            return True

        image.set_alpha( alpha )

        self.position_y += self.position_y ** 1.5 / 1000

        self.position_x += self.position_x ** 1.2 / 1000 * self.test_value

        surface.blit(image, (self.position_x, self.position_y))

#/////////////////////////////////////////////////////////////////////

direction1 = Direction(window_width/4)
direction2 = Direction(window_width/2 + 250)
direction3 = Direction(window_width/4 * 3 + 500)

direction_list = [direction1, direction2, direction3]

falling_list = []

#Transition is true if items are moving and false if not
transition = False

running = True

current_pos = 0

run_through_count = 3

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #mechanics:
        current_value = direction_list[0].value

        keypressed = ""
            
        if event.type == pygame.KEYDOWN:
            key= pygame.key.name(event.key)
            if key == "a":
                keypressed = "left"
            elif key == "s":
                keypressed = "down"
            elif key == "d":
                keypressed = "right"
            elif key == "w":
                keypressed = "up"
            elif key == "space":
                keypressed = "jump"

        if keypressed == current_value or run_through_count > 0:

            pygame.mixer.Sound.play(correct_sound)

            #Removes correctly followed direction and adds it to the list of falling items
            falling_list.append(direction_list.pop(0))

            score += window_width/10
            
            direction_list.append(Direction(window_width/4 * 3 - 250))

            current_input = 0

            transition = True

            run_through_count = max(0, run_through_count - 1)

            

        elif keypressed != "":
            pygame.mixer.Sound.play(wrong_sound)
            score = 0

    #cleans the screen
    surface.fill(background_color)
    


    #Draws the score rectangle and decreases score
    pygame.draw.rect(surface, score_color, pygame.Rect(0, 0, score, 50))
    score -= max(0, (score ** 1.1 ) / 300)

    #Draws all falling directions:
    for falling_item in falling_list:
        #Deletes the object if its fully dissapeared
        if falling_item.fall_away():
            del falling_item

    if score <= 0:
        score = 0
    

    if transition and current_input <= scale_factor:
        #iterate through all directions (3 max)

        #Draws the circle for items
        pygame.draw.circle(surface, item_color, (current_pos + 250,window_height/2), 300)
        pygame.draw.circle(surface, background_color, (current_pos + 250 ,window_height/2), 280)

        for direction in direction_list:
            if direction != direction_list[2]:
                direction.draw_transition(current_input)
            

        current_input += 1

    else: 
        current_pos = direction_list[0].position_x

        #Draws the circle for items
        pygame.draw.circle(surface, item_color, (current_pos + 250,window_height/2), 300)
        pygame.draw.circle(surface, background_color, (current_pos + 250 ,window_height/2), 280)

        for direction in direction_list:
            direction.draw_static()


        scale_factor = math.sqrt(3 / 4 * 500 ) 
        transition = False
        current_input = -scale_factor

    pygame.display.flip()

    time.sleep(0.0005)

    #updates the display
    #pygame.display.flip()

    #Parabolic pixels per frame can be used to simulate movement of items
    #There are 3 items ( X ) X  X
    #The moment the one within the circle is completed, the circled item
    #drops and the two right ones shift left using the motion described
    #The right most X is replaced with a new command