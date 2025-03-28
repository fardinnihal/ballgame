import turtle
import random
import time

# Set up screen
def setup_screen():
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.tracer(0)
    screen.title("Ball Collision Game")
    screen.setup(500, 500)
    return screen

# Ball lists
big_balls = []
power_ups = []

# Create one big ball (moves automatically, very slow)
def create_big_ball():
    ball = turtle.Turtle()
    ball.shape("circle")
    ball.color("blue")
    ball.penup()
    ball.speed(0)
    ball.shapesize(2, 2)
    ball.goto(random.randint(-150, 150), random.randint(-150, 150))
    ball.dx = random.choice([-0.5, 0.5])
    ball.dy = random.choice([-0.5, 0.5])
    big_balls.append(ball)

# Create small ball (player-controlled)
def create_player_ball():
    player = turtle.Turtle()
    player.shape("circle")
    player.color("red")
    player.penup()
    player.speed(0)
    player.shapesize(1, 1)
    player.goto(0, 0)
    player.dx = 0
    player.dy = 0
    player.base_speed = 60  # Base speed (3x original)
    return player

# Create score display
def create_score_display():
    score_turtle = turtle.Turtle()
    score_turtle.hideturtle()
    score_turtle.penup()
    score_turtle.goto(-230, 230)
    score_turtle.color("black")
    return score_turtle

# Create power-up
def create_power_up():
    if random.random() < 0.01:  # 1% chance per frame to spawn
        power_up = turtle.Turtle()
        power_up.shape("circle")
        power_up.color("green")
        power_up.penup()
        power_up.speed(0)
        power_up.shapesize(0.8, 0.8)  # Smaller than player ball
        power_up.goto(random.randint(-150, 150), random.randint(-150, 150))
        power_up.type = random.choice(["speed", "clear"])  # Random power-up type
        power_ups.append(power_up)

# Game variables
last_collision_time = 0
collision_cooldown = 0.5
score = 0
speed_boost_duration = 0  # Tracks remaining time for speed boost

# Change direction functions
def move_up(player):
    player.dx = 0
    player.dy = player.base_speed

def move_down(player):
    player.dx = 0
    player.dy = -player.base_speed

def move_left(player):
    player.dx = -player.base_speed
    player.dy = 0

def move_right(player):
    player.dx = player.base_speed
    player.dy = 0

# Move player ball continuously
def move_player(player):
    speed_multiplier = 2 if speed_boost_duration > 0 else 1  # Double speed when boosted
    new_x = player.xcor() + player.dx * 0.05 * speed_multiplier
    new_y = player.ycor() + player.dy * 0.05 * speed_multiplier
    player.goto(new_x, new_y)
    
    # Bounce off walls
    if new_x > 200 or new_x < -200:
        player.dx *= -1
    if new_y > 200 or new_y < -200:
        player.dy *= -1

# Move big balls automatically
def move_big_balls(screen, player, score_turtle):
    global speed_boost_duration
    try:
        for ball in big_balls:
            x, y = ball.xcor(), ball.ycor()
            new_x = x + ball.dx
            new_y = y + ball.dy
            ball.setx(new_x)
            ball.sety(new_y)

            # Bounce off walls
            if new_x > 200 or new_x < -200:
                ball.dx *= -1
            if new_y > 200 or new_y < -200:
                ball.dy *= -1

        move_player(player)
        create_power_up()  # Chance to spawn power-up
        check_collision(player, screen, score_turtle)
        check_power_up_collision(player, screen)
        
        # Update speed boost timer
        if speed_boost_duration > 0:
            speed_boost_duration -= 50  # Decrease by frame time (50ms)
            if speed_boost_duration <= 0:
                player.color("red")  # Return to normal color

        screen.update()
        screen.ontimer(lambda: move_big_balls(screen, player, score_turtle), 50)

    except Exception as e:
        print("Error in move_big_balls:", e)

# Check collision with big balls and update score
def check_collision(player, screen, score_turtle):
    global last_collision_time, score
    current_time = time.time()
    
    if current_time - last_collision_time < collision_cooldown:
        return
    
    for ball in big_balls:
        distance = player.distance(ball)
        if distance < 30:
            last_collision_time = current_time
            score += 1
            update_score(score_turtle)
            create_big_ball()
            player.goto(0, 0)
            player.dx = 0
            player.dy = 0

# Check collision with power-ups
def check_power_up_collision(player, screen):
    global speed_boost_duration
    for power_up in power_ups[:]:  # Copy list to avoid modification issues
        if player.distance(power_up) < 20:  # Smaller collision radius
            if power_up.type == "speed":
                speed_boost_duration = 5000  # 5 seconds in milliseconds
                player.color("yellow")  # Visual indicator of speed boost
            elif power_up.type == "clear":
                while len(big_balls) > 1:  # Keep one ball
                    ball = big_balls.pop()
                    ball.hideturtle()
                    del ball
            power_up.hideturtle()
            power_ups.remove(power_up)

# Update score display
def update_score(score_turtle):
    score_turtle.clear()
    score_turtle.write(f"Score: {score}", font=("Arial", 16, "normal"))

# Main game function
def start_game():
    screen = setup_screen()
    player = create_player_ball()
    score_turtle = create_score_display()

    # Keyboard bindings - Arrow keys and WASD
    screen.listen()
    screen.onkey(lambda: move_up(player), "Up")
    screen.onkey(lambda: move_down(player), "Down")
    screen.onkey(lambda: move_left(player), "Left")
    screen.onkey(lambda: move_right(player), "Right")
    screen.onkey(lambda: move_up(player), "w")
    screen.onkey(lambda: move_down(player), "s")
    screen.onkey(lambda: move_left(player), "a")
    screen.onkey(lambda: move_right(player), "d")

    # Create initial single big ball
    create_big_ball()

    # Initial score display
    update_score(score_turtle)

    # Start game loop
    move_big_balls(screen, player, score_turtle)
    
    screen.mainloop()

# Run the game
if __name__ == "__main__":
    try:
        start_game()
    except Exception as e:
        print("Game crashed with error:", e)