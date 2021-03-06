from queue import PriorityQueue
from game_componenets.game import Game
from agents.agent import Agent
from copy import deepcopy

from game_componenets.heuristics import HeuristicsManager


class AStarAgent(Agent):
    def __init__(self, isRedPlayer: bool):
        super().__init__(isRedPlayer)
        self.searchExpansion = 0
        self.stepstoWin = 0

    # How many enemy cities can attack me in my new city if I decided to attack this new city.
    def dangerOnDefeatedCityHeuristic(self, enemyCity, newArmyInEnemyCity, danger, game: Game):
        for neighbourId in game.map.graph[enemyCity.id]:
            neighbour = game.cityList[neighbourId]
            if neighbour.isRedArmy == enemyCity.isRedArmy and neighbour.armyCount > newArmyInEnemyCity + 1:
                danger += 2
        return danger

    # How many enemies can attack me in my original city if I left it with only 1 army.
    def dangerOnOriginalCityHeuristic(self, myCity, newArmyInEnemyCity, danger, game: Game):
        for neighbourId in game.map.graph[myCity.id]:
            neighbour = game.cityList[neighbourId]
            if neighbour.isRedArmy != myCity.isRedArmy and neighbour.armyCount > newArmyInEnemyCity + 1:
                danger += 1
        return danger

    def calculateHeuristic(self, game: Game):
        # hnCost = 0
        # cityListId = game.citiesOf(self.isRedPlayer)
        # for cityId in cityListId:
        #     for neighbourId in game.map.graph[cityId]:
        #         city = game.cityList[cityId]
        #         neighbour = game.cityList[neighbourId]
        #         if neighbour.armyCount > city.armyCount + 1 and neighbour.isRedArmy != city.isRedArmy:
        #             hnCost += 1
        self.searchExpansion+=1
        heuristicManager = HeuristicsManager()
        return game.cityCount[not self.isRedPlayer] + game.soldiersCount[not
        self.isRedPlayer] + heuristicManager.mySecuredCities(self.isRedPlayer, game)

        # put first node in pq

        # while !pq.empty
        # pop minimum
        # investigate adjacent nodes of minimum
        # continue

    def applyHeuristic(self, initialGame: Game):
        if (initialGame.isFinished()):
            return initialGame
        pq = PriorityQueue()
        # value,curGameState , game after first move in path

        pq.put((0, 0, initialGame, initialGame))
        isFirstMove = True
        ansGame = None
        while not pq.empty():

            value, g, curGame, firstMoveInPath = minTuple = pq.get()
            if (self.isGoalState(curGame, initialGame) or pq._qsize()>10000):
                ansGame = firstMoveInPath
                break

            print(g, curGame.cityCount[self.isRedPlayer], value, pq._qsize())
            adjacentStates = self.adjacentStates(curGame)

            for nextGameState in adjacentStates:
                if (isFirstMove):
                    pq.put((g + self.calculateHeuristic(nextGameState), g + 1, nextGameState, nextGameState))
                else:
                    pq.put((g + self.calculateHeuristic(nextGameState), g + 1, nextGameState, firstMoveInPath))

            isFirstMove = False
        print(ansGame)
        self.stepstoWin+=1
        self.evaluate()
        if(ansGame==None):
            return firstMoveInPath
        return ansGame

    def isGoalState(self, gameState: Game, initialState: Game):
        return (gameState.cityCount[self.isRedPlayer] - initialState.cityCount[self.isRedPlayer] >= 2 or
                gameState.cityCount[self.isRedPlayer] == len(gameState.cityList))

    def adjacentStates(self, game: Game):
        bonusArmyPossibilities = list()
        cityListId = game.citiesOf(self.isRedPlayer)
        bonusArmy = game.bonusSoldiers(self.isRedPlayer)

        for cityId in cityListId:
            city = game.cityList[cityId]
            for neighbourId in game.map.graph[cityId]:
                neighbour = game.cityList[neighbourId]
                if(neighbour.isRedArmy != city.isRedArmy):
                    gameCopy = deepcopy(game)
                    gameCopy.addSoldiersToCity(cityId, bonusArmy)
                    bonusArmyPossibilities.append(gameCopy)
                    break

        attackingPossibilities = list()
        for gameStatee in bonusArmyPossibilities:
            cityListId = gameStatee.citiesOf(self.isRedPlayer)
            for cityId in cityListId:
                city = gameStatee.cityList[cityId]
                for neighbourId in gameStatee.map.graph[cityId]:
                    neighbour = gameStatee.cityList[neighbourId]
                    if city.armyCount > neighbour.armyCount + 1 and city.isRedArmy != neighbour.isRedArmy:
                        gameCopy = deepcopy(gameStatee)
                        gameCopy.move(cityId, neighbourId, neighbour.armyCount + 1)
                        attackingPossibilities.append(gameCopy)

        return attackingPossibilities

    def attack(self, fromCityId, toCityId, fromCityArmyCount, game):
        game.move(fromCityId, toCityId, fromCityArmyCount)

    def evaluate(self):
        print("Steps to win ", self.stepstoWin)
        print("Search Expansion " , self.searchExpansion)
        print("for f = 1 " , 1*self.stepstoWin + self.searchExpansion)
        print("for f = 100 " , 100*self.stepstoWin + self.searchExpansion)
        print("for f = 100000 " , 10000*self.stepstoWin + self.searchExpansion)