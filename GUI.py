import pygame, sys, ctypes


# chaning the cursor of the mouse and making sound on click


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picturepath):
        super().__init__()
        self.image = pygame.image.load(picturepath)
        self.rect = self.image.get_rect()
        self.attack = pygame.mixer.Sound('attack.wav')

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self):
        self.attack.play()


# the rectangles for every city
class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, armyCount):
        super().__init__()
        self.image = pygame.image.load('circle.png')
        self.rect = self.image.get_rect()
        self.armyCount = armyCount
        self.width = width
        self.height = height
        self.rect.center = [x, y]


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


pygame.init()
clock = pygame.time.Clock()
# pygame.mouse.set_visible(False)

backgroundimage = pygame.image.load('backgroundimage.jpg')
unitedstatesmap = pygame.image.load('unitedstatesmap.png')

crosshair = Crosshair('sword.png')

crosshairgroup = pygame.sprite.Group()
crosshairgroup.add(crosshair)

texas = Circle(unitedstatesmap.get_rect()[0]/2, unitedstatesmap.get_rect()[1]/2, 40, 50, (255, 0, 0))
circlegroup = pygame.sprite.Group()
circlegroup.add(texas)


class GameState():
    def __init__(self,):
        self.state = 'intro'

    def intro(self):
        image = pygame.image.load('backgroundimage.jpg')
        screen = pygame.display.set_mode((image.get_width(), image.get_height()))
        screen.blit(backgroundimage, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # if playing mode pressed
                if screen.get_width() / 4 - 40 + 700 > mouse[
                    0] > screen.get_width() / 4 - 40 and screen.get_height() / 2 - 50 + 100 > mouse[
                    1] > screen.get_height() / 2 - 50:
                    self.state = "playingmode"
                # if simulation mode pressed
                elif screen.get_width() / 4 - 100 + 850 > mouse[
                    0] > screen.get_width() / 4 - 100 and screen.get_height() / 2 + 100 + 100 > mouse[
                    1] > screen.get_height() / 2 + 100:
                    # scren change
                    print('lel')
        # game title
        text = pygame.font.Font('freesansbold.ttf', 300)
        textsurf, textrect = text_objects("RISK", text, (0, 0, 0))
        textrect.center = (screen.get_width() / 2, screen.get_height() / 2 - 200)
        screen.blit(textsurf, textrect)

        # play button that goes to the playing mode
        text = pygame.font.Font('freesansbold.ttf', 100)
        textsurf, textrect = text_objects("Playing Mode", text, (255, 255, 255))
        textrect.center = (screen.get_width() / 2 - 25, screen.get_height() / 2)
        screen.blit(textsurf, textrect)
        s = pygame.Surface((700, 100), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((255, 255, 255, 0))  # notice the alpha value in the color
        screen.blit(s, (screen.get_width() / 4 - 40, screen.get_height() / 2 - 50))

        # play button that goes to the simulation mode
        text = pygame.font.Font('freesansbold.ttf', 100)
        textsurf, textrect = text_objects("Simulation Mode", text, (255, 255, 255))
        textrect.center = (screen.get_width() / 2 - 25, screen.get_height() / 2 + 150)
        screen.blit(textsurf, textrect)
        s = pygame.Surface((850, 100), pygame.SRCALPHA)  # per-pixel alpha
        s.fill((255, 255, 255, 0))  # notice the alpha value in the color
        screen.blit(s, (screen.get_width() / 4 - 100, screen.get_height() / 2 + 100))
        pygame.display.update()


    def playingmode(self):
        image = pygame.image.load('unitedstatesmap.png')
        screen = pygame.display.set_mode((image.get_width(), image.get_height()))
        screen.blit(image, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                crosshair.shoot()
        crosshairgroup.draw(screen)
        crosshairgroup.update()
        circlegroup.draw(screen)
        circlegroup.update()
        pygame.display.update()

    def statemanager(self):
        if self.state == 'intro':
            self.intro()
        elif self.state == 'playingmode':
            self.playingmode()

#initializing gamestate
gamestate = GameState()
while True:
    gamestate.statemanager()
    clock.tick(60)

# code for making text
# text =  pygame.font.Font('freesansbold.ttf',110)
# textsurf , textrect = text_objects("A bit racey", text)
# textrect.center = (screen.get_width()/2,screen.get_height()/2)
# screen.blit(textsurf,textrect)

# the equation for collision between mouse and a rec is if mouse.x > rec.x+width && mouse.y > rec.y+height
