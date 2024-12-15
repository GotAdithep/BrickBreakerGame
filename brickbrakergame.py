import turtle
from paddle import Paddle

# screen and border
class Game:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.screensize(1000, 1000)
        self.screen.title("Brick Breaker Game")
        self.screen.bgcolor("black")
        self.screen.tracer(0)
        # make border
        self.border = turtle.Turtle()
        self.border.color('red')
        self.border.hideturtle()
        self.border.speed(0)
        self.border.penup()
        self.border.setposition(-300, -300)
        self.border.pendown()
        self.border.pensize(3)
        for side in range(4):
            self.border.forward(600)
            self.border.left(90)

    def update(self):
        self.screen.update()

    def get_screen(self):
        return self.screen


game = Game()
screen = game.get_screen()

# Create Paddle from paddle.py
locationx = 0
locationy = -250
paddle_turtle = turtle.Turtle()
Paddlegame = Paddle(100, 20, "red", paddle_turtle)
Paddlegame.set_location([locationx, locationy])
Paddlegame.draw()

# Paddle move
def moveleft():
    global locationx, locationy
    if locationx - Paddlegame.width / 2 > -300:
        locationx -= 60
        Paddlegame.clear()
        Paddlegame.set_location([locationx, locationy])
        Paddlegame.draw()

def moveright():
    global locationx, locationy
    if locationx + Paddlegame.width / 2 < 300:
        locationx += 60
        Paddlegame.clear()
        Paddlegame.set_location([locationx, locationy])
        Paddlegame.draw()

# Create bricks
class Brick:
    def __init__(self, width, height, color, x, y):
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.turtle = turtle.Turtle()
        self.turtle.penup()
        self.turtle.hideturtle()
        self.turtle.color(self.color)
        self.active = True
        self.draw()

    def draw(self):
        if self.active:
            self.turtle.goto(self.x - self.width / 2, self.y - self.height / 2)
            self.turtle.pendown()
            self.turtle.begin_fill()
            for _ in range(2):
                self.turtle.forward(self.width)
                self.turtle.left(90)
                self.turtle.forward(self.height)
                self.turtle.left(90)
            self.turtle.end_fill()
            self.turtle.penup()

    def clear(self):
        self.turtle.clear()
        self.active = False

brick_width = 60
brick_height = 25
brick_colors = ["blue", "green", "yellow", "orange", "purple"]
bricks = []

rows = 5
cols = 8
start_x = -240
start_y = 250
gap = 5

for row in range(rows):
    for col in range(cols):
        x = start_x + col * (brick_width + gap)
        y = start_y - row * (brick_height + gap)
        color = brick_colors[row % len(brick_colors)]
        brick = Brick(brick_width, brick_height, color, x, y)
        bricks.append(brick)

# make ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.speed(0)
ball.goto(30, 30)
ball.dx = 4
ball.dy = -4

# show score
score = 0
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-290, 270)
score_display.write(f"Score: {score}", align="left", font=("Arial", 16, "normal"))

def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}", align="left", font=("Arial", 16, "normal"))

# show Game Over
class GameOver:
    def __init__(self):
        self.display = turtle.Turtle()
        self.display.color("red")
        self.display.penup()
        self.display.hideturtle()

    def show(self):
        self.display.goto(0, 0)
        self.display.write("GAME OVER", align="center", font=("Helvetica", 36, "bold"))

# Win Game
class GameWon:
    def __init__(self):
        self.display = turtle.Turtle()
        self.display.color("green")
        self.display.penup()
        self.display.hideturtle()

    def show(self):
        self.display.goto(0, 0)
        self.display.write("YOU WON", align="center", font=("Arial", 36, "bold"))

# Pause text
is_paused = False
pause_text = turtle.Turtle()
pause_text.color("white")
pause_text.penup()
pause_text.hideturtle()
pause_text.goto(250, 270)
pause_text.write("Pause", align="center", font=("Arial", 16, "normal"))

def toggle_pause(x, y):
    global is_paused
    if 230 < x < 270 and 260 < y < 280:
        is_paused = not is_paused
        if is_paused:
            pause_text.clear()
            pause_text.color("green")
            pause_text.write("Resume", align="center", font=("Arial", 16, "normal"))
        else:
            pause_text.clear()
            pause_text.color("red")
            pause_text.write("Pause", align="center", font=("Arial", 16, "normal"))

screen.onclick(toggle_pause)

game_over_display = GameOver()
game_won_display = GameWon()

# Game loop
def game_loop():
    global score, is_paused

    if not is_paused:
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        if ball.xcor() > 290 or ball.xcor() < -290:
            ball.dx *= -1

        if ball.ycor() > 290:
            ball.dy *= -1

        if (locationy - 10 < ball.ycor() < locationy + 10) and \
           (locationx - Paddlegame.width / 2 < ball.xcor() < locationx + Paddlegame.width / 2):
            ball.dy *= -1

        for brick in bricks:
            if brick.active:
                within_x = brick.x - brick.width / 2 <= ball.xcor() <= brick.x + brick.width / 2
                within_y = brick.y - brick.height / 2 <= ball.ycor() <= brick.y + brick.height / 2
                if within_x and within_y:
                    ball.dy *= -1
                    brick.clear()
                    score += 10
                    update_score()
                    break

        if all(not brick.active for brick in bricks):
            game_won_display.show()
            return

        if ball.ycor() < -290:
            game_over_display.show()
            return

    game.update()
    screen.ontimer(game_loop, 10)

screen.listen()
screen.onkey(moveleft, "Left")
screen.onkey(moveright, "Right")
game_loop()
screen.mainloop()
