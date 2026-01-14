import pyxel

class SimpleJumpApp:
    def __init__(self):
        self.width = 160
        self.height = 120
        pyxel.init(self.width, self.height, title="Simple Jump Game")
        self.player_x = 72
        self.player_y = 50
        self.player_w = 16
        self.player_h = 16
        self.vy = 0
        self.gravity = 0.5
        self.jump_power = -6
        self.floor_y = 100
        self.score = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, self.width - self.player_w)
        if pyxel.btnp(pyxel.KEY_Z) and self.player_y + self.player_h >= self.floor_y:
            self.vy = self.jump_power
        self.vy += self.gravity
        self.player_y += self.vy
        if self.player_y + self.player_h >= self.floor_y:
            self.player_y = self.floor_y - self.player_h
            self.vy = 0
            self.score += 1
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(12)
        pyxel.rect(0, self.floor_y, self.width, self.height - self.floor_y, 8)
        pyxel.rect(self.player_x, self.player_y, self.player_w, self.player_h, 11)
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        pyxel.text(5, 15, "Arrow: move, Z: jump, Q: quit", 7)

SimpleJumpApp()
