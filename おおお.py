import pyxel
import random

WIDTH = 256
HEIGHT = 256

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2


# =====================
# 🐿️ プレイヤー（リス）
# =====================
class Squirrel:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 30
        self.speed = 2
        self.max_speed = 6      # ← 最大スピード
        self.score = 0
        self.boost_timer = 0    # ← スピードアップ演出用

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed

        self.x = max(95, min(self.x, 165))
        self.score += 1

        if self.boost_timer > 0:
            self.boost_timer -= 1

    def speed_up(self):
        self.speed = min(self.speed + 1.5, self.max_speed)  # ← ガッツリ加速
        self.boost_timer = 20

    def draw(self):
        # 🐿️ リス（加速中は色変化）
        color = 8 if self.boost_timer > 0 else 4
        pyxel.circ(self.x, self.y, 8, color)
        pyxel.circ(self.x - 6, self.y - 6, 3, color)
        pyxel.circ(self.x + 6, self.y - 6, 3, color)
        pyxel.circ(self.x + 11, self.y + 3, 4, color)


# =====================
# 🍃🍂🌰 アイテム
# =====================
class Item:
    SAFE = 0
    DANGER = 1
    ACORN = 2

    def __init__(self):
        self.x = random.randint(100, 160)
        self.y = -20
        self.kind = random.choice([0, 0, 1, 2])
        self.speed = 1.5

    def update(self):
        self.y += self.speed

    def draw(self):
        if self.kind == Item.SAFE:
            pyxel.elli(self.x, self.y, 16, 10, 11)
            pyxel.line(self.x - 16, self.y, self.x + 16, self.y, 3)

        elif self.kind == Item.DANGER:
            pyxel.elli(self.x, self.y, 16, 10, 4)
            pyxel.line(self.x - 16, self.y, self.x + 16, self.y, 1)

        else:
            # 🌰 どんぐり（目立つ）
            pyxel.circ(self.x, self.y + 6, 8, 9)
            pyxel.rect(self.x - 8, self.y - 4, 16, 4, 4)


# =====================
# 🎮 メイン
# =====================
class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Tree Climbing Game")
        self.scene = SCENE_TITLE
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.player = Squirrel()
        self.items = []
        self.timer = 0

    def update(self):
        if self.scene == SCENE_TITLE:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.scene = SCENE_PLAY

        elif self.scene == SCENE_PLAY:
            self.timer += 1
            self.player.update()

            if self.timer % 30 == 0:
                self.items.append(Item())

            for item in self.items[:]:
                item.update()
                dx = item.x - self.player.x
                dy = item.y - self.player.y

                if dx * dx + dy * dy < 250:
                    if item.kind == Item.DANGER:
                        self.scene = SCENE_GAMEOVER

                    elif item.kind == Item.ACORN:
                        self.player.speed_up()  # ← ここ重要！

                    self.items.remove(item)

                elif item.y > HEIGHT:
                    self.items.remove(item)

        elif self.scene == SCENE_GAMEOVER:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset()
                self.scene = SCENE_TITLE

    def draw(self):
        pyxel.cls(12)

        # 🌳 木
        pyxel.rect(110, 0, 36, HEIGHT, 3)

        if self.scene == SCENE_TITLE:
            pyxel.text(80, 100, "TREE CLIMBING GAME", 0)
            pyxel.text(70, 120, "PRESS SPACE TO START", 0)

        elif self.scene == SCENE_PLAY:
            for item in self.items:
                item.draw()
            self.player.draw()
            pyxel.text(5, 5, f"SCORE:{self.player.score}", 0)
            pyxel.text(5, 15, f"SPEED:{self.player.speed:.1f}", 0)

        elif self.scene == SCENE_GAMEOVER:
            pyxel.text(95, 110, "GAME OVER", 8)
            pyxel.text(85, 125, f"SCORE:{self.player.score}", 7)
            pyxel.text(60, 145, "PRESS SPACE TO RESTART", 7)


App()
