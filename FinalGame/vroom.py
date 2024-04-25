# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 01:38:03 2024

@author: axeve

Alexis Evans
CS 120
Final Game
April 25, 2024

Car: https://openclipart.org/detail/218068/pixel-car-red-front
Race track: https://thumbs.dreamstime.com/b/cartoon-race-track-top-view-curves-finish-line-flat-design-cartoon-race-track-figure-top-view-191145234.jpg
Background music: https://opengameart.org/content/happy-arcade-tune
Coin: https://opengameart.org/content/coins-pixel-art-silver-gold-crystal-and-more
Coin sound effect: https://opengameart.org/content/picked-coin-echo
"""

import pygame, simpleGE, random

class Coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Coin.gif")
        self.setSize(85, 85)
        self.reset()

    def reset(self):
        self.y = random.randint(0, self.screenHeight)
        self.x = random.randint(0, self.screenWidth)

class redCar(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("redCar.png")
        self.setSize(40, 25)

    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.turnBy(3.5)
        if self.isKeyPressed(pygame.K_RIGHT):
            self.turnBy(-3.5)
        if self.isKeyPressed(pygame.K_UP):
            self.forward(5)
        if self.isKeyPressed(pygame.K_DOWN):
            self.forward(-3)
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 430)
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 30"
        self.center = (540, 430)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background.fill((33, 80, 38))
        self.setImage("track")
        
        self.redCar = redCar(self)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 50)

        pygame.mixer.music.load("happy.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        
        self.sndCoin = simpleGE.Sound("coinSound.wav")
        self.numCoin = 1
        self.score = 0
        self.lblScore = LblScore()
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 30
        self.lblTime = LblTime()
        
        self.Coin = []
        for i in range(self.numCoin):
            self.Coin.append(Coin(self))
        
        self.sprites = [self.redCar,
                        self.btnQuit,
                        self.lblScore,
                        self.lblTime,
                        self.Coin]

    def process(self):
        for Coin in self.Coin:
            if Coin.collidesWith(self.redCar):
                Coin.reset()
                self.sndCoin.play()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
            self.lblTime.text = f"Time left: {self.timer.getTimeLeft():.2f}"
            if self.timer.getTimeLeft() < 0:
                print(f"Score: {self.score}")
                self.stop()
                
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        
class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        self.prevScore = prevScore
        self.setImage("track")
        self.response = "Quit"
        
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are a race car!",
        "Move with left, right, up, and down",
        "arrow keys.",
        "Drive around freely and collect coins",
        "in the time provided.",
        "",
        "Have fun!"]
        
        self.directions.center = (320, 200)
        self.directions.size = (400, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (145, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (495, 400)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center = (320, 400)
        
        self.lblScore.text = f"Last score: {self.prevScore}"
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
        
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
            
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()

def main():
    keepGoing = True
    lastScore = 0
    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
        else:
            keepGoing = False
            
if __name__ == "__main__":
    main()