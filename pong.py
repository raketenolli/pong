import pyxel
import random

_COL = 7

class Bar:
    def __init__(self, x, up, down):
        self.height = 12
        self.x = x
        self.up = up
        self.down = down
        self.reset()
    
    def reset(self):
        self.y1 = (pyxel.height - self.height) // 2
        self.y2 = (pyxel.height + self.height) // 2
        self.vy = 0
    
    def update(self):
        if(pyxel.btn(self.up) and self.y1 >= 3):
            self.y1 -= 3
            self.y2 -= 3
            self.vy = -1
        elif(pyxel.btn(self.down) and self.y2 < pyxel.height-3):
            self.y1 += 3
            self.y2 += 3
            self.vy = 1
        else:
            self.vy = 0
    
    def draw(self):
        pyxel.rect(self.x, self.y1, self.x, self.y2, _COL)

class Ball:
    def __init__(self, r):
        self.r = r
        self.reset(1)
    
    def reset(self, vx):
        self.x = pyxel.width // 2
        self.y = pyxel.height // 2
        self.vx = vx
        # self.vy = random.randint(-3, 3) / 3.0
        self.vy = 0
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if(self.x <= self.r):
            self.x = 2 * self.r - self.x
            self.vx = -1 * self.vx
        elif(self.x >= (pyxel.width - self.r)):
            self.x = 2 * (pyxel.width - self.r) - self.x
            self.vx = -1 * self.vx
        if(self.y <= self.r):
            self.y = 2 * self.r - self.y
            self.vy = -1 * self.vy
        elif(self.y >= (pyxel.height - self.r)):
            self.y = 2 * (pyxel.height - self.r) - self.y
            self.vy = -1 * self.vy
    
    def draw(self):
        pyxel.circ(self.x, self.y, self.r, _COL)

def checkBboxCollision(o1T, o1B, o1L, o1R, o2T, o2B, o2L, o2R):
    if(o1B < o2T): return False
    if(o2B < o1T): return False
    if(o1L > o2R): return False
    if(o2L > o1R): return False
    return True

class App:
    def __init__(self):
        self.leftScore = 0
        self.rightScore = 0
        self.game_on = False
        pyxel.init(160, 120)
        self.ball = Ball(3)
        self.leftBar = Bar(1, pyxel.KEY_W, pyxel.KEY_S)
        self.rightBar = Bar(pyxel.width-2, pyxel.KEY_UP, pyxel.KEY_DOWN)
        pyxel.run(self.update, self.draw)
        
    def checkBallHitsCeilingOrFloor(self, ball):
        if(ball.y <= ball.r):
            ball.y = 2 * ball.r - ball.y
            ball.vy = -1 * ball.vy
        elif(ball.y >= (pyxel.height - ball.r)):
            ball.y = 2 * (pyxel.height - ball.r) - ball.y
            ball.vy = -1 * ball.vy

    def checkBallInGoal(self, ball):
        if(ball.x <= 0):
            self.rightScore += 1
            ball.reset(-1)
            self.leftBar.reset()
            self.rightBar.reset()
            self.game_on = False
        if(ball.x >= pyxel.width):
            self.leftScore += 1
            ball.reset(1)
            self.leftBar.reset()
            self.rightBar.reset()
            self.game_on = False
    
    def checkCollision(self, ball, bar):
        ball_top = ball.y - ball.r
        ball_bot = ball.y + ball.r
        ball_left = ball.x - ball.r
        ball_right = ball.x + ball.r
        
        # check whether bounding boxes of ball and bar overlap
        if(checkBboxCollision(ball_top, ball_bot, ball_left, ball_right, bar.y1, bar.y2, bar.x, bar.x)):
            # collision on top of bar, ball coming down
            if(ball.y < bar.y1 and ball.vy > 0):
                ball.vy = -1 * ball.vy + 0.5 * bar.vy

            # collision at bottom of bar, ball going up
            elif(ball.y > bar.y2 and ball.vy < 0):
                ball.vy = -1 * ball.vy + 0.5 * bar.vy

            # otherwise "normal" collision
            else:
                ball.vy = ball.vy + 0.5 * bar.vy
            
            ball.vx = -1 * ball.vx

        ball.x += ball.vx
        ball.y += ball.vy
    
    def update(self):
        # self.ball.update()
        if(self.game_on is False):
            if(pyxel.btn(pyxel.KEY_SPACE)):
                self.game_on = True
        else:
            self.leftBar.update()
            self.rightBar.update()
            self.checkBallHitsCeilingOrFloor(self.ball)
            self.checkBallInGoal(self.ball)
            self.checkCollision(self.ball, self.leftBar)
            self.checkCollision(self.ball, self.rightBar)
    
    def draw(self):
        pyxel.cls(0)
        pyxel.text(pyxel.width // 4, 1, str(self.leftScore), _COL)
        pyxel.text(3 * pyxel.width // 4, 1, str(self.rightScore), _COL)
        self.ball.draw()
        self.leftBar.draw()
        self.rightBar.draw()

App()

"""
checkcollision
von rechts:
    (x - r + vx) <= bar.x
von links:
    (x - r + vx) >= bar.x
von oben oder unten
    max(y+r, y+r+vy) >= bar.y1
    min(y-r, y-r+vy) <= bar.y2
"""