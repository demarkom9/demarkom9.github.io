from random import randint
WIDTH = 800
HEIGHT = 600
ball = Actor("ball")
ball.pos = 400, 280
player1 = Actor("player1")
player1.pos = randint(800, 1600), randint(10, 200)
player2 = Actor("player2")
player2.pos = randint(800, 1600), 460
player3 = Actor("player3")
player3.pos = randint(800, 1600), 450
game_over = False
score = 0
number_of_updates = 0
scores = []

def update_high_scores():
    global score, scores
    filename = r"./high-scores.txt"
    scores = []
    with open(filename, "r") as file:
        line = file.readline()
        high_scores = line.split()
        for high_score in high_scores:
            if(score > int(high_score)):
                scores.append(str(score) + " ")
                score = int(high_score)
            else:
                scores.append(str(high_score) + " ")
    with open(filename, "w") as file:
        for high_score in scores:
            file.write(high_score)

def display_high_scores():
    screen.draw.text("HIGH SCORES", (350, 150), color="black")
    y = 175
    position = 1
    for high_score in scores:
        screen.draw.text(str(position) + ". " + high_score, (350, y), color="black")
        y += 25
        position += 1
        from math import sqrt

        def distance(a, b):
            return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

        if distance(ball, player1) < 40 or distance(ball, player2) < 40 or distance(ball, player3) < 40:
            game_over = True
            update_high_scores()


def draw():
    screen.blit("field", (0, 0))
    if not game_over:
        ball.draw()
        player1.draw()
        player2.draw()
        player3.draw()
        screen.draw.text("Score: " + str(score), (700, 5), color="black")
    else:
        display_high_scores()

def on_mouse_down():
    global up
    up = True
    ball.y -= 25

def on_mouse_up():
    global up
    up = False

music.play("footballmusic")

def update():
    global game_over, score, number_of_updates
    if not game_over:

            ball.y += 1
    if player1.x > 0:
        player1.x -= 4
        if number_of_updates == 9:

            number_of_updates = 0
        else:
            number_of_updates += 1
    else:
        player1.x = randint(800, 1600)
        player1.y = randint(10, 200)
        score += 1
        number_of_updates = 0

    if player2.right > 0:
        player2.x -= 4
    else:
        player2.x = randint(800, 1600)
        score += 1

    if player3.right > 0:
        player3.x -= 4
    else:
        player3.x = randint(800, 1600)
        score += 1

    if ball.top < 0 or ball.bottom > 560:
        game_over = True
        update_high_scores()

    if ball.collidepoint(player1.x, player1.y) or \
        ball.collidepoint(player2.x, player2.y) or \
        ball.collidepoint(player3.x, player3.y):
            game_over = True
            update_high_scores()
