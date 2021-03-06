import pygame, sys

from game_componenets.game import Game

# from agents.realtime_agent import

pygame.init()
backgroundimage = pygame.image.load('assets/backgroundimage.jpg')
unitedstatesmap = pygame.image.load('assets/unitedstatesmap.png')
worldMap = pygame.image.load('assets/kk.jpg')
clock = pygame.time.Clock()


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()



class GUI:
    # chaning the cursor of the mouse and making sound on click

    class GameState:
        def __init__(self):
            self.ready = False
            self.state = 'intro'
            self.agent1 = ''
            self.agent2 = ''
            self.agent1bool = False
            self.agent2bool = False
            self.isSimulation = False
            self.gameimage = pygame.image.load("assets/unitedstatesmap.png")
            self.chosenimage = "USmap.txt"  # made for comparison only in GUI class
            self.bonusArmyCity = ''
            self.attackingCity = ''
            self.defendingCity = ''
            self.withArmy = ''
            self.bonusAttack = False  # false means bonus army turn, true means attacking turn
            self.citiesRectx = []
            self.citiesRecty = []

        def intro(self):
            image = pygame.image.load('assets/backgroundimage.jpg')
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
                        # self.state = "playingmode"
                        self.state = "choosePlayerPlaying"
                    # if simulation mode pressed
                    elif screen.get_width() / 4 - 100 + 850 > mouse[
                        0] > screen.get_width() / 4 - 100 and screen.get_height() / 2 + 100 + 100 > mouse[
                        1] > screen.get_height() / 2 + 100:
                        # screen change
                        # self.state = "simulationMode"
                        self.state = "choosePlayerSimulation"

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

        def rendermap(self, map, cityList, screen, game):
            for city in range(0, len(cityList), 1):
                text = pygame.font.Font('freesansbold.ttf', 30)
                if cityList[city].isRedArmy:
                    color = (255, 0, 0)
                else:
                    color = (0, 255, 0)
                    # print(color , " " , cityList[city])
                textsurf, textrect = text_objects(str(cityList[city].armyCount), text, color)  # get city.armyCount
                # str(id) because the key in the dictionary is string
                textrect.center = (map[str(city)][0], map[str(city)][1])  # get city location
                screen.blit(textsurf, textrect)
                # draw rectangle over text to detect clicks
                rect = pygame.draw.rect(screen, color,
                                        pygame.Rect(map[str(city)][0] - 15,
                                                    map[str(city)][1] - 15,
                                                    30,
                                                    30), 1)
                self.citiesRectx.append(map[str(city)][0] - 15)
                self.citiesRecty.append(map[str(city)][1] - 15)

                # detect if a mouse hovered over a rect
                # hanzawed code elsoldiers placing wala attack....
                if rect.collidepoint(pygame.mouse.get_pos()):
                    # currentCity = cityList[city]
                    # print(cityList[city].armyCount)
                    rect = pygame.draw.rect(screen, color,
                                            pygame.Rect(map[str(city)][0] - 20,
                                                        map[str(city)][1] - 20,
                                                        40, 40), 3)

                    # for event in pygame.event.get():
                    #     if event.type == pygame.MOUSEBUTTONDOWN: #detected the human click on city
                    #         print(cityList[city])
                    #         if self.bonusAttack is False: #turn of placing bonus army
                    #             if cityList[city].isRedArmy is True:
                    #                 army = game.bonusSoldiers(True)
                    #                 game.placeBonusSoldiers(cityList[city].id, army)
                    #                 self.bonusAttack = True
                    # else:
                    #     if cityList[city].isRedArmy:
                    #         self.attackingCity = cityList[city]
                    #         print(self.attackingCity , "attack")
                    #         print(game.map.graph[self.attackingCity.id])
                    #         print(city , " currentCity")
                    #         elif cityList[city].isRedArmy is False and self.attackingCity != '' and game.map.graph[self.attackingCity.id].__contains__(city):
                    #             self.defendingCity = cityList[city]
                    #             print(self.defendingCity  , " defending")
                    # if self.attackingCity != '' and self.defendingCity != '' and event.type == pygame.KEYDOWN:
                    #     self.withArmy+=event.unicode
                    #     self.ready = True
                    #     print(self.withArmy)
                    # if event.type == pygame.KEYDOWN:
                    #     print(event.unicode)
                else:
                    rect = pygame.draw.rect(screen, color,
                                            pygame.Rect(map[str(city)][0] - 15,
                                                        map[str(city)][1] - 15,
                                                        30, 30), 3)

            pygame.display.update()

        def returnHumanBonusArmy(self):
            return self.bonusArmyCity, 3

        def renderSimulationMode(self, game: Game):
            cityList = game.getCityList()
            screen = pygame.display.set_mode((self.gameimage.get_width(), self.gameimage.get_height()))
            screen.blit(self.gameimage, (0, 0))

            Quit = pygame.draw.rect(screen, (0, 0, 255), [0, 0, 140, 40])
            text = pygame.font.Font('freesansbold.ttf', 30)
            textsurf, textrect = text_objects("Quit", text, (0, 0, 0))  # get city.armyCount
            textrect.center = (Quit.center)
            screen.blit(textsurf, textrect)
            if self.chosenimage == "USmap.txt":
                map = game.map.USmap
            else:
                map = game.map.worldMap
            self.rendermap(map, cityList, screen, game)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.MOUSEMOTION:
                #     for city in range(0, len(map), 1):
                #         if pygame.mouse.get_pos() == map[str(city)]:
                #             text = pygame.font.Font('freesansbold.ttf', 30)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 140 > pygame.mouse.get_pos()[0] > 0 and 40 > pygame.mouse.get_pos()[1] > 0:
                        self.state = "intro"
                    # crosshair.shoot()
            # loop over the cities to check the color with city is the index (or id) of the city

            # crosshairgroup.draw(screen)
            # crosshairgroup.update()
            pygame.display.update()

        def choosePlayerModeSimulation(self):
            image = pygame.image.load('assets/backgroundimage.jpg')
            screen = pygame.display.set_mode((image.get_width(), image.get_height()))
            screen.blit(backgroundimage, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if screen.get_width() - 873 > mouse[
                        0] > screen.get_width() - 1013 and screen.get_height() - 313 > mouse[
                        1] > screen.get_height() - 354:
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "greedy"
                        else:
                            self.agent2bool = True
                            self.agent2 = "greedy"

                    elif screen.get_width() - 898 > mouse[
                        0] > screen.get_width() - 1007 and screen.get_height() - 214 > mouse[
                        1] > screen.get_height() - 254:
                        # scren change
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "RT A*"
                        else:
                            self.agent2bool = True
                            self.agent2 = "RT A*"
                    elif screen.get_width() - 960 > mouse[
                        0] > screen.get_width() - 1005 and screen.get_height() - 264 > mouse[
                        1] > screen.get_height() - 304:
                        # scren change
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "aStar"
                        else:
                            self.agent2bool = True
                            self.agent2 = "aStar"
                    elif screen.get_width() - 838 > mouse[
                        0] > screen.get_width() - 1007 and screen.get_height() - 164 > mouse[
                        1] > screen.get_height() - 204:
                        # scren change
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "minimax"
                        else:
                            self.agent2bool = True
                            self.agent2 = "minimax"
                    elif screen.get_width() - 387 > mouse[
                        0] > screen.get_width() - 538 and screen.get_height() - 314 > mouse[
                        1] > screen.get_height() - 354:
                        # scren change
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "passive"
                        else:
                            self.agent2bool = True
                            self.agent2 = "passive"
                    elif screen.get_width() - 346 > mouse[
                        0] > screen.get_width() - 539 and screen.get_height() - 263 > mouse[
                        1] > screen.get_height() - 305:
                        # scren change
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "agressive"
                        else:
                            self.agent2bool = True
                            self.agent2 = "agressive"
                    elif screen.get_width() - 252 > mouse[
                        0] > screen.get_width() - 533 and screen.get_height() - 213 > mouse[
                        1] > screen.get_height() - 254:
                        # scren change
                        if (self.agent1bool is False):
                            self.agent1bool = True
                            self.agent1 = "nearly"
                        else:
                            self.agent2bool = True
                            self.agent2 = "nearly"
                    elif 758 > mouse[0] > 609 and 696 > mouse[1] > 666:
                        self.gameimage = pygame.image.load("assets/unitedstatesmap.png")
                        self.chosenimage = "USmap.txt"
                    elif 1181 > mouse[0] > 926 and 696 > mouse[1] > 666:
                        self.gameimage = pygame.image.load("assets/kk.jpg")
                        self.chosenimage = "WorldMap.txt"
            # game title

            # coordinateList = [(),(),(),() .... ]
            # for tuple in coordinateList:
            #     width,height,dada,mama,oma7ma = tuple
            #

            self.coordinates(screen, 0, -200, "RISK")
            self.coordinates(screen, -270, -30, "AI Agents")
            self.coordinates(screen, -260, 50, "Greedy")
            self.coordinates(screen, -300, 100, "A*")
            self.coordinates(screen, -270, 150, "RT A*")
            self.coordinates(screen, -240, 200, "minimax")
            self.coordinates(screen, 220, 50, "Passive")
            self.coordinates(screen, 280, -30, "Non AI Agents")
            self.coordinates(screen, 240, 100, "Agressive")
            self.coordinates(screen, 290, 150, "Nearly pacifist")
            self.coordinates(screen, 0, 300, "USMAP")
            self.coordinates(screen, 380, 300, "WORLD MAP")

            if self.agent1bool is True and self.agent2bool is True:
                self.state = "simulationMode"
            pygame.display.update()
            # myTuple=(True,self.aiAgent,self.nonAiAgent)
            # print(myTuple)
            # return myTuple

        def coordinates(self, screen, x, y, string):
            text = pygame.font.Font('freesansbold.ttf', 40)
            textsurf, textrect = text_objects(string, text, (0, 0, 0))
            textrect.center = (screen.get_width() / 2 + x, screen.get_height() / 2 + y)
            screen.blit(textsurf, textrect)

        def Ready(self):
            if self.attackingCity != '' and self.defendingCity != '' and self.withArmy != '':
                self.bonusAttack = False
                return True
            return False

        def renderPlayingmode(self, game):
            cityList = game.getCityList()
            screen = pygame.display.set_mode((self.gameimage.get_width(), self.gameimage.get_height()))
            screen.blit(self.gameimage, (0, 0))

            Quit = pygame.draw.rect(screen, (0, 0, 255), [0, 0, 140, 40])
            text = pygame.font.Font('freesansbold.ttf', 30)
            textsurf, textrect = text_objects("Quit", text, (0, 0, 0))  # get city.armyCount
            textrect.center = (Quit.center)
            screen.blit(textsurf, textrect)
            if self.chosenimage == "USmap.txt":
                map = game.map.USmap
            else:
                map = game.map.worldMap
            self.rendermap(map, cityList, screen, game)

            text = pygame.font.Font('freesansbold.ttf', 30)
            textsurf, textrect = text_objects("", text, (0, 0, 0))
            input_box = pygame.Rect(600, 600, 140, 32)

            screen.blit(textsurf, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, (0,0,255), input_box, 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    print("Mouse pressed")
                    for city in range(0, len(map), 1):
                        if self.citiesRectx[city] + 40 > pygame.mouse.get_pos()[0] > self.citiesRectx[city]\
                                and self.citiesRecty[city] + 40 > pygame.mouse.get_pos()[1] > self.citiesRecty[city]:
                            text = pygame.font.Font('freesansbold.ttf', 30)
                            # print("lelelelellelelelee")
                            print(cityList[city])
                            if self.bonusAttack is False: #turn of placing bonus army
                                if cityList[city].isRedArmy is True:
                                    army = game.bonusSoldiers(True)
                                    game.placeBonusSoldiers(cityList[city].id, army)
                                    self.bonusAttack = True
                            else:
                                if cityList[city].isRedArmy:
                                    self.attackingCity = cityList[city]
                                    print(self.attackingCity , "attack")
                                    # print(city , " currentCity")
                                    # print(game.map.graph[self.attackingCity.id])
                                elif cityList[city].isRedArmy is False and self.attackingCity != '' and game.map.graph[self.attackingCity.id].__contains__(city):
                                    self.defendingCity = cityList[city]
                                    print(self.defendingCity  , " defending")
                if self.attackingCity != '' and self.defendingCity != '' and input_box.collidepoint(pygame.mouse.get_pos()):
                    # print(";lwenroinqweoifmnqwekp")
                    if event.type == pygame.KEYDOWN:
                        if event.key != pygame.K_RETURN:
                            self.withArmy+=event.unicode
                            if self.withArmy != '':
                                if int(self.withArmy) > self.attackingCity.armyCount-1:
                                    self.withArmy = ''
                            print(self.withArmy)
                        elif event.key == pygame.K_BACKSPACE:
                            self.withArmy = self.withArmy[0:len(self.withArmy)-1]
                            print(self.withArmy)
                        else:
                            print("ready")
                            if self.withArmy != '':
                                self.ready = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if 140 > pygame.mouse.get_pos()[0] > 0 and 40 > pygame.mouse.get_pos()[1] > 0:
                        self.state = "intro"

            pygame.display.update()

        def choosePlayerModePlaying(self):
            self.agent1 = "human"
            self.agent1bool = True
            image = pygame.image.load('assets/backgroundimage.jpg')
            screen = pygame.display.set_mode((image.get_width(), image.get_height()))
            screen.blit(backgroundimage, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()

                    if screen.get_width() - 873 > mouse[
                        0] > screen.get_width() - 1013 and screen.get_height() - 313 > mouse[
                        1] > screen.get_height() - 354:
                        if (self.agent2bool is False):
                            self.agent2bool = True
                            self.agent2 = "greedy"

                    elif screen.get_width() - 898 > mouse[
                        0] > screen.get_width() - 1007 and screen.get_height() - 214 > mouse[
                        1] > screen.get_height() - 254:
                        # scren change
                        if (self.agent2bool is False):
                            self.agent2bool = True
                            self.agent2 = "RT A*"
                    elif screen.get_width() - 960 > mouse[
                        0] > screen.get_width() - 1005 and screen.get_height() - 264 > mouse[
                        1] > screen.get_height() - 304:
                        # scren change
                        if (self.agent2bool is False):
                            self.agent2bool = True
                            self.agent2 = "aStar"
                    elif screen.get_width() - 838 > mouse[
                        0] > screen.get_width() - 1007 and screen.get_height() - 164 > mouse[
                        1] > screen.get_height() - 204:
                        # scren change
                        if (self.agent2bool is False):
                            self.agent2bool = True
                            self.agent2 = "minimax"
                    elif screen.get_width() - 387 > mouse[
                        0] > screen.get_width() - 538 and screen.get_height() - 314 > mouse[
                        1] > screen.get_height() - 354:
                        # scren change
                        if (self.agent2bool is False):
                            self.agent2bool = True
                            self.agent2 = "passive"
                    elif screen.get_width() - 346 > mouse[
                        0] > screen.get_width() - 539 and screen.get_height() - 263 > mouse[
                        1] > screen.get_height() - 305:
                        # scren change
                        if (self.agent2bool is False):
                            self.agent2bool = True
                            self.agent2 = "agressive"
                    elif screen.get_width() - 252 > mouse[
                        0] > screen.get_width() - 533 and screen.get_height() - 213 > mouse[
                        1] > screen.get_height() - 254:
                        # scren change
                        if (self.agent2bool is False):
                            self.agent2bool = True
                            self.agent2 = "nearly"
                    elif 758 > mouse[0] > 609 and 696 > mouse[1] > 666:
                        self.gameimage = pygame.image.load("assets/unitedstatesmap.png")
                        self.chosenimage = "USmap.txt"
                    elif 1181 > mouse[0] > 926 and 696 > mouse[1] > 666:
                        self.gameimage = pygame.image.load("assets/kk.jpg")
                        self.chosenimage = "WorldMap.txt"

            # game title

            # coordinateList = [(),(),(),() .... ]
            # for tuple in coordinateList:
            #     width,height,dada,mama,oma7ma = tuple

            self.coordinates(screen, 0, -200, "RISK")
            self.coordinates(screen, -270, -30, "AI Agents")
            self.coordinates(screen, -260, 50, "Greedy")
            self.coordinates(screen, -300, 100, "A*")
            self.coordinates(screen, -270, 150, "RT A*")
            self.coordinates(screen, -240, 200, "minimax")
            self.coordinates(screen, 220, 50, "Passive")
            self.coordinates(screen, 280, -30, "Non AI Agents")
            self.coordinates(screen, 240, 100, "Agressive")
            self.coordinates(screen, 290, 150, "Nearly pacifist")
            self.coordinates(screen, 0, 300, "USMAP")
            self.coordinates(screen, 380, 300, "WORLD MAP")
            if self.agent1bool is True and self.agent2bool is True:
                self.state = "playingmode"
            pygame.display.update()

        def statemanager(self):
            if self.state == 'intro':
                self.intro()
            elif self.state == 'choosePlayerPlaying':
                self.choosePlayerModePlaying()
            elif self.state == 'choosePlayerSimulation':
                self.isSimulation = True
                self.choosePlayerModeSimulation()

        def modesmanager(self, game):
            if self.state == 'playingmode':
                self.renderPlayingmode(game)
            elif self.state == 'simulationMode':
                self.renderSimulationMode(game)

        def start(self):
            while self.state == "choosePlayerPlaying" or self.state == "choosePlayerSimulation" or self.state == "intro":
                self.statemanager()
                clock.tick(60)

        def returnTuple(self):
            if self.state == 'playingmode' or self.state == 'simulationMode':
                return (self.isSimulation, self.agent1, self.agent2, self.chosenimage)

# # code for making text
# # text =  pygame.font.Font('freesansbold.ttf',110)
# # textsurf , textrect = text_objects("A bit racey", text)
# # textrect.center = (screen.get_width()/2,screen.get_height()/2)
# # screen.blit(textsurf,textrect)
#
#
# # the equation for collision between mouse and a rec is if mouse.x > rec.x+width && mouse.y > rec.y+height
#
# # the equation for collision between mouse and a rec is if mouse.x > rec.x+width && mouse.y > rec.y+height
