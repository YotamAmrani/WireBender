from Consts import *

# Drawing with rounded corners
# https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame

# Rotating an object:
# https://stackoverflow.com/questions/59902716/how-to-rotate-element-around-pivot-point-in-pygame

# def rotate_multiple_points(points):
#     global angle
#     result = [points[0]]
#     for i in range(len(points)-1):
#         distance = points[i+1] - points[i]
#         magnitude, current_angle = distance.as_polar()
#         current_angle += angle
#         distance.from_polar((magnitude, current_angle))
#         distance += result[i]
#         result.append(distance)
#     return result


class Button(object):
    def __init__(self, pos, size, color, coloron, img, imghov ,imgon, function, press_once=False):
        self.pos = pos
        self.size = size
        self.color = color
        self.coloron = coloron
        self.img = img
        self.imghov = imghov
        self.imgon = imgon
        self.function = function
        self.press_once = press_once
        self.done = True

    def check(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        on_button = rect.collidepoint(mouse)
        if not on_button:
            pygame.draw.rect(screen, self.color, rect)
            screen.blit(self.img, self.img.get_rect(center=rect.center))
            self.done = True
        elif click[0] == 0:
            pygame.draw.rect(screen, self.color, rect)
            screen.blit(self.imghov, self.imghov.get_rect(center=rect.center))
            self.done = True
        elif click[0] == 1 and self.done:
            pygame.draw.rect(screen, self.coloron, rect)
            screen.blit(self.imgon, self.imgon.get_rect(center=rect.center))
            if self.press_once:
                self.done = False
            if self.function is not None:
                self.function()
        else:
            pygame.draw.rect(screen, self.coloron, rect)
            screen.blit(self.imgon, self.imgon.get_rect(center=rect.center))

# for each button, check if it was pressed
def check_buttons():
    global buttons
    for button in buttons:
        button.check()

def extract_multiple_points(screen):
    global angle
    global points
    global polar_points
    points = []
    if polar_points:
        origin = pygame.Vector2(screen.get_width() // 2, screen.get_height() - SPINNER_DISTANCE)
        # points.append(origin)
        edge_point = pygame.Vector2(0, 0)
        edge_point.from_polar((line_length - SPINNER_DISTANCE, -(90 + angle)))
        edge_point += origin

        # new_polar_points = [origin.as_polar()] + polar_points
        points = [edge_point]
        current_angle = angle
        for p in range(len(polar_points)):
            phi, r = polar_points[p]
            # convert to current presentation
            r = -(r + current_angle + 90)
            # rotate by angles of previous lines
            current_polar_point = pygame.Vector2(0, 0)
            current_polar_point.from_polar((phi, r))
            current_polar_point += points[p]
            points.append(current_polar_point)
            current_angle += polar_points[p][1]

            # print(points)


def add_segment():
    global points
    global angle
    global polar_points
    global total_length
    current_segment = (line_length - SPINNER_DISTANCE, angle)
    total_length += line_length - SPINNER_DISTANCE
    polar_points = [current_segment] + polar_points
    # print(polar_points)


def reset_state():
    global angle
    global line_length
    angle = 0
    line_length = SPINNER_DISTANCE


def revert():
    global polar_points
    global line_length
    global angle
    global total_length
    if polar_points:
        line_length, angle = polar_points[0]
        total_length -= line_length
        polar_points = polar_points[1:]
        print(total_length)


def draw_current_line(screen):
    global line_length
    start_position = pygame.math.Vector2(screen.get_width() // 2, screen.get_height())
    end_position = pygame.math.Vector2(screen.get_width() // 2, screen.get_height() - line_length)
    screen.fill(SCREEN_COLOR)  # Fill the screen with black.
    draw_metal_line(screen, start_position, end_position)

    if (line_length > SPINNER_DISTANCE):
        screen.fill(SCREEN_COLOR)

        radar_center = (screen.get_width() // 2, screen.get_height() - SPINNER_DISTANCE)
        x = radar_center[0] + math.sin(math.radians(angle)) * (SPINNER_DISTANCE - line_length)
        y = radar_center[1] + math.cos(math.radians(angle)) * (SPINNER_DISTANCE - line_length)

        # then render the line radar->(x,y)
        draw_metal_line(screen, start_position, radar_center)
        draw_metal_line(screen, radar_center, (x, y))
        # pygame.draw.line(screen, Color("black"), radar_center, (x, y), 1)


def draw_multiple_lines(screen, points):
    for i in range(len(points) - 1):
        draw_metal_line(screen, points[i + 1], points[i])
    # for i in range(len(points) - 1):
    #     draw_line_round_corners_polygon(screen, points[i + 1] + pygame.math.Vector2(5, 0),
    #                                 points[i] + pygame.math.Vector2(5, 0), DARK_GREY, 7)
    # for i in range(len(points) - 1):
    #     draw_line_round_corners_polygon(screen, points[i + 1] + pygame.math.Vector2(0, 0),
    #                                 points[i] + pygame.math.Vector2(0, 0), 'white', 5)


def draw_current_spinner(screen):
    global angle
    rotated = pygame.transform.rotate(spinner, angle)
    screen.blit(rotated, rotated.get_rect(center=(screen.get_width() // 2, screen.get_height() - SPINNER_DISTANCE )))
    # circle = pygame.draw.circle(screen, 'black', (0, 0), 30, width=2)
    # rotated = pygame.transform.rotate(circle, angle)
    # screen.blit(rotated, rotated.get_rect(center=(screen.get_width() // 2, screen.get_height() - SPINNER_DISTANCE)))


def draw_line_round_corners_polygon(surf, p1, p2, c, w):
    p1v = pygame.math.Vector2(p1)
    p2v = pygame.math.Vector2(p2)
    if p2v - p1v:
        lv = (p2v - p1v).normalize()
        lnv = pygame.math.Vector2(-lv.y, lv.x) * w // 2
        pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
        pygame.draw.polygon(surf, c, pts)
        pygame.draw.circle(surf, c, p1, round(w / 2))
        pygame.draw.circle(surf, c, p2, round(w / 2))


def draw_metal_line(screen, start_position, end_position):
    draw_line_round_corners_polygon(screen, start_position, end_position, LINE_COLOR, LINE_WIDTH)
    # draw_line_round_corners_polygon(screen, start_position + pygame.math.Vector2(5, 0),
    #                                 end_position + pygame.math.Vector2(5, 0), DARK_GREY, 7)
    # draw_line_round_corners_polygon(screen, start_position + pygame.math.Vector2(0, 0),
    #                                 end_position + pygame.math.Vector2(0, 0), 'white', 5)


def draw(screen):
    """
    Draw things to the window. Called once per frame.
    """
    global points
    draw_current_line(screen)
    extract_multiple_points(screen)

    if points:
        draw_multiple_lines(screen, points)
    draw_current_spinner(screen)



def extrude():
    global line_length
    line_length += 1
def rotate_right():
    global angle
    if angle > RIGHT_MIN_VALUE:
        angle -= 1
def rotate_left():
    global angle
    if angle < LEFT_MAX_VALUE:
        angle += 1
def add_segment_and_reset():
    add_segment()
    reset_state()
def finish():
    print("finish")
    pygame.event.post(pygame.event.Event(QUIT))

def update(dt):
    """
    Update game. Called once per frame.
    dt is the amount of time passed since last frame.
    If you want to have constant apparent movement no matter your framerate,
    what you can do is something like

    x += v * dt

    and this will scale your velocity based on time. Extend as necessary."""

    # Go through events that are passed to the script by the window.
    for event in pygame.event.get():
        # We need to handle these events. Initially the only one you'll want to care
        # about is the QUIT event, because if you don't handle it, your game will crash
        # whenever someone tries to exit.
        if event.type == QUIT:
            pygame.quit()  # Opposite of pygame.init
            sys.exit()  # Not including this line crashes the script on Windows. Possibly
            # on other operating systems too, but I don't know for sure.
            # Handle other events as you wish.
    global line_length
    global angle
    global key_0_pressed
    global key_1_pressed

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        line_length += 1
    elif keys[pygame.K_DOWN]:
        line_length -= 1
    if (keys[K_LEFT]) and angle < LEFT_MAX_VALUE:
        angle += 1
    elif (keys[K_RIGHT]) and angle > RIGHT_MIN_VALUE:
        angle -= 1
    elif keys[K_0]:
        key_0_pressed = keys[K_0]
    elif not keys[K_0] and key_0_pressed:
        add_segment()
        reset_state()
        key_0_pressed = keys[K_0]
    elif keys[K_1]:
        key_1_pressed = keys[K_1]
    elif not keys[K_1] and key_1_pressed:
        revert()
        key_1_pressed = keys[K_1]
    if keys[K_ESCAPE]:
        pygame.event.post(pygame.event.Event(QUIT))


def runPyGame():
    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.
    while True:
        update(dt)
        draw(screen)
        check_buttons()

        pygame.display.update()
        pygame.display.flip()
        dt = fpsClock.tick(fps)

# Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
fpsClock = pygame.time.Clock()
# screen = pygame.display.set_mode((width, height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill(SCREEN_COLOR)

# set the buttons and make an array of them
extrude_button = Button(EXTRUDE_BUTTON_POSITION, EXTRUDE_BUTTON_SIZE, buttonInactiveColour, buttonPressedColour, pic_extrude_button, pic_extrude_button_hover, pic_extrude_button_pressed, extrude)
rotate_right_button = Button(ROTATE_RIGHT_BUTTON_POSITION, ROTATE_RIGHT_BUTTON_SIZE, buttonInactiveColour, buttonPressedColour, pic_rotate_right_button, pic_rotate_right_button_hover, pic_rotate_right_button_pressed, rotate_right)
rotate_left_button = Button(ROTATE_LEFT_BUTTON_POSITION, ROTATE_LEFT_BUTTON_SIZE, buttonInactiveColour, buttonPressedColour, pic_rotate_left_button, pic_rotate_left_button_hover, pic_rotate_left_button_pressed, rotate_left)
add_segment_button = Button(ADD_SEGMENT_BUTTON_POSITION, ADD_SEGMENT_BUTTON_SIZE, buttonInactiveColour, buttonPressedColour, pic_add_segment_button, pic_add_segment_button_hover, pic_add_segment_button_pressed, add_segment_and_reset, True)
revert_button = Button(REVERT_BUTTON_POSITION, REVERT_BUTTON_SIZE, buttonInactiveColour, buttonPressedColour, pic_revert_button, pic_revert_button_hover, pic_revert_button_pressed, revert, True)
finish_button = Button(FINISH_BUTTON_POSITION, FINISH_BUTTON_SIZE, buttonInactiveColour, buttonPressedColour, pic_finish_button, pic_finish_button_hover, pic_finish_button_pressed, finish, True)

buttons = [extrude_button, rotate_right_button, rotate_left_button, add_segment_button, finish_button, revert_button]

runPyGame()
