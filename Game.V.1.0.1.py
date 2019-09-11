import pygame

pygame.init()


class Root:  # 기초

    size = (800, 800)
    color = (200, 200, 200)
    run = True
    time = 50
    win = pygame.display.set_mode(size)
    font = pygame.font.Font("./res/malgun.ttf", 20)  # 기본 폰트
    pygame.display.set_caption("안녕칭구들 ~~")
    player_color = (0, 0, 200)
    wall_color = (10, 10, 10)
    teleport_color = (0, 255, 0)
    enemy_color = (200, 0, 0)


class Entity:

    def __init__(self, x, y, wid, hei):
        self.x, self.y = x, y
        self.wid, self.hei = wid, hei

    def draw(self):
        pass

    def tick(self):
        pass


class Player(Entity):

    def __init__(self, x, y, wid, hei, vel):
        super().__init__(x, y, wid, hei)
        self.vel = vel
        self.go_left = True
        self.go_right = True
        self.go_up = True
        self.go_down = True

    def draw(self):
        pygame.draw.rect(Root.win, Root.player_color, (self.x, self.y, self.wid, self.hei))

    def tick(self):
        self.draw()
        self.control()
        self.init()

    def control(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Root.run = False

        if keys[pygame.K_LEFT] and self.go_left:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.go_right:
            self.x += self.vel
        if keys[pygame.K_UP] and self.go_up:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.go_down:
            self.y += self.vel

    def init(self):
        self.go_left = True
        self.go_right = True
        self.go_up = True
        self.go_down = True

    def go_start(self):
        global Sys
        self.x, self.y = Sys.player_startpoint[0], Sys.player_startpoint[1]
        self.wid, self.hei = Sys.player_startpoint[2], Sys.player_startpoint[3]


class State:
    class Object(Entity):

        def __init__(self, x, y, wid, hei):
            super().__init__(x, y, wid, hei)
            self.color = ()

        def draw(self):
            pygame.draw.rect(Root.win, (self.color), (self.x, self.y, self.wid, self.hei))

        def tick(self):
            self.draw()
            self.collision()

        def event(self):
            pass

        def collision(self):
            global Bob

            if self.x <= Bob.x <= self.x + self.wid and self.y <= Bob.y <= self.y + self.hei - Bob.hei:
                self.event()
            if self.x + self.wid >= Bob.x + Bob.wid >= self.x and self.y <= Bob.y <= self.y + self.hei - Bob.hei:
                self.event()
            if self.y <= Bob.y <= self.y + self.hei and self.x <= Bob.x <= self.x + self.wid - Bob.wid:
                self.event()
            if self.y + self.hei >= Bob.y + Bob.hei >= self.y and self.x <= Bob.x <= self.x + self.wid - Bob.wid:
                self.event()

    class Wall(Object):

        def __init__(self, x, y, wid, hei):
            super().__init__(x, y, wid, hei)
            self.color = Root.wall_color

        def collision(self):
            global Bob

            if self.x <= Bob.x <= self.x + self.wid and self.y <= Bob.y <= self.y + self.hei - Bob.hei:
                Bob.go_left = False
            if self.x + self.wid >= Bob.x + Bob.wid >= self.x and self.y <= Bob.y <= self.y + self.hei - Bob.hei:
                Bob.go_right = False
            if self.y <= Bob.y <= self.y + self.hei and self.x <= Bob.x <= self.x + self.wid - Bob.wid:
                Bob.go_up = False
            if self.y + self.hei >= Bob.y + Bob.hei >= self.y and self.x <= Bob.x <= self.x + self.wid - Bob.wid:
                Bob.go_down = False

    class Teleport(Object):

        def draw(self):
            pygame.draw.rect(Root.win, Root.teleport_color, (self.x, self.y, self.wid, self.hei))

        @staticmethod
        def event():
            global Sys
            Sys.teleport()

        def tick(self):
            self.draw()

    class Enemy(Object):

        def __init__(self, x, y, wid, hei, x_range, y_range, vel):
            super().__init__(x, y, wid, hei)
            self.start_x = x
            self.start_y = y
            self.x_range = x_range
            self.y_range = y_range
            self.color = Root.enemy_color
            self.vel = vel
            self.x_finish = False
            self.y_finish = False

        def draw(self):
            pygame.draw.rect(Root.win, self.color, (self.x, self.y, self.wid, self.hei))

        def move(self):
            if not self.x_finish and self.x_range != 0:
                self.x += self.vel
            elif self.x_finish and self.x_range != 0:
                self.x -= self.vel
            else:
                pass

            if not self.y_finish and self.y_range != 0:
                self.y += self.vel
            elif self.y_finish and self.y_range != 0:
                self.y -= self.vel
            else:
                pass

        def change(self):
            if self.x >= self.x_range:
                self.x_finish = True
            elif self.x <= self.start_x:
                self.x_finish = False
            else:
                pass

            if self.y >= self.y_range:
                self.y_finish = True
            elif self.y <= self.start_y:
                self.y_finish = False
            else:
                pass

        def event(self):
            global Sys
            Sys = DeathScreen()

        def tick(self):
            self.move()
            self.change()
            self.draw()

    def __init__(self):
        self.walls = []
        self.player_startpoint = ()

    def tick(self):
        for i in self.walls:
            i.tick()
            i.collision()

class Start_screen(State):

    text1 = Root.font.render('탈출게임', False, Root.wall_color)
    text2 = Root.font.render('스페이스를 눌러 시작', False, Root.wall_color)

    @staticmethod
    def tick():
        global Sys
        global Bob
        Root.win.blit(Start_screen.text1, (Root.size[0] / 2 - 60, Root.size[1] / 2 - 20))
        Root.win.blit(Start_screen.text2, (Root.size[0] / 2 -120, Root.size[1] / 2 ))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Root.run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                  Sys = Room_1()
                  Bob = Player(Sys.player_startpoint[0], Sys.player_startpoint[1], Sys.player_startpoint[2], Sys.player_startpoint[3], 10)




class Room_1(State):
    Wall1 = State.Wall(100, 100, 210, 10)
    Wall2 = State.Wall(100, 100, 10, 210)
    Wall3 = State.Wall(310, 100, 10, 220)
    Wall4 = State.Wall(100, 310, 220, 10)
    Wall5 = State.Wall(210, 200, 10, 110)
    Enemy1 = State.Enemy(150, 160, 10, 10, 250, 0, 5)
    tele = State.Teleport(250, 290, 10, 10)

    def __init__(self):
        self.walls = [Room_1.Wall1, Room_1.Wall2, Room_1.Wall3, Room_1.Wall4, Room_1.Wall5, Room_1.Enemy1, Room_1.tele]
        self.player_startpoint = (150, 260, 10, 10)

    @staticmethod
    def teleport():
        global Sys
        global Bob
        Sys = Room_2()
        DeathScreen.last_room = Room_2()
        Bob.go_start()


class Room_2(State):
    Wall1 = State.Wall(50, 50, 310, 10)
    Wall2 = State.Wall(50, 50, 10, 310)
    Wall3 = State.Wall(50, 350, 310, 10)
    Wall4 = State.Wall(350, 50, 10, 310)
    Enemy1 = State.Enemy(170, 55, 10, 10, 0, 340, 5)
    Enemy2 = State.Enemy(190, 55, 10, 10, 0, 340, 10)
    Enemy3 = State.Enemy(230, 55, 10, 10, 0, 340, 12)

    tele = State.Teleport(250, 250, 10, 10)

    def __init__(self):
        self.walls = [Room_2.Wall1, Room_2.Wall2, Room_2.Wall3, Room_2.Wall4, Room_2.Enemy1, Room_2.Enemy2,
                      Room_2.Enemy3, Room_2.tele]
        self.player_startpoint = (100, 150, 10, 10)

    @staticmethod
    def teleport():
        global Sys
        global Bob
        Sys = Room_1()
        DeathScreen.last_room = Room_1()
        Bob.go_start()


class DeathScreen(State):
    text = Root.font.render('죽었지롱', False, (Root.wall_color))
    last_room = Room_1()

    def tick(self):
        global Bob
        global Sys
        Root.win.blit(DeathScreen.text, (Root.size[0] / 2 - 50, Root.size[1] / 2 - 50))
        pygame.display.update()
        Sys = DeathScreen.last_room
        Bob.go_start()
        i = 0
        while i < 50:
            pygame.time.delay(50)
            i += 1


Sys = Start_screen()
Bob = Player(0,0,0,0,0)


while Root.run:
    pygame.time.delay(Root.time)


    Root.win.fill(Root.color)
    Sys.tick()
    Bob.tick()
    pygame.display.update()

pygame.quit()
