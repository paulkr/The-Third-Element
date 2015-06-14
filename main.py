#!/usr/bin/env python

"""
The Third Element
ICS3U Final Project
Paul Krishnamurthy 2015
"""

from pygame import *
from os import environ
from json import load
from random import randint
from Game.const import *

# Imports
classes = ["player", "maps", "message", "fade", "treasure", 
			"sound", "fight", "story", "chest"]
for i in classes:
	exec("from Game.%s import %s"%(i, i.title()))

init()

# Get screen resolution
screen_res = display.Info()
window_posX = screen_res.current_w//2 - 543
window_posY = screen_res.current_h//2 - 300
# Set window position relative to the screen resolution
environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d"%(window_posX,window_posY)


class Main:
	""" Main game class """

	def __init__(self):
		self.screen = display.set_mode((1086,600))
		self.screenW, self.screenH = 1086, 600
		display.set_caption("The Third Element")
		display.set_icon(image.load("resources/graphics/misc/icon.png").convert_alpha())

		# Play intro music
		if not mac:
			mixer.music.load(Sound().getMusic("introTheme"))
			mixer.music.play(loops=-1)

		# Fade into loading screen
		Fade().fadeDark(image.load("resources/graphics/misc/loading.png").convert(), self.screen, (0,0))
		display.flip()

		# Startup / ending screens
		self.startup = image.load("resources/graphics/misc/startup.png").convert()
		self.ending = image.load("resources/graphics/misc/ending.png").convert()
		# Scrolling intro text
		self.introTextBack = image.load("resources/graphics/misc/introTextBack.png").convert()
		self.introText = image.load("resources/graphics/misc/introText.png").convert_alpha()
		self.introTextOver = False
		# Text y-coordinate
		self.introY = 600

		self.cursor = transform.scale2x(image.load("resources/graphics/misc/cursor.png").convert_alpha())
		self.newGame = Rect(203,268,240,63)
		self.loadGame = Rect(626,268,254,63)
		self.startOver = True

		# Game state
		self.newGameMode = False
		self.loadGameMode = False
		self.gameWon = False
		self.gameOverMusic = False

		# Create new instances
		self.message = Message(self.screen)
		self.fade = Fade()
		self.player = Player(self.screen, self.message, self.fade)
		self.maps = Maps(self.screen, self.player)
		self.sound = Sound()
		self.treasure = Treasure(self.screen, self.player)
		self.fight = Fight(self.screen, self.player, self.sound, self.message, self.treasure)
		self.story = Story(self.message, self.treasure, self.player, self.screen, self.fade, self.maps, self.sound)
		self.chest = Chest(self.screen, self.treasure, self.message, self.maps, self.player, self.fight, self.sound, self.fade)

		# Fade from loading screen to main world
		self.fade.fadeDark(self.startup, self.screen, (0,0))
		self.fade.reset()

		# Game states
		self.isFighting = False
		self.treasureShow = True
		self.inWater = False

		# Keep track of player rect
		self.playerRect = Rect(1,1,1,1)
		# Flag to play music
		self.musicPlay = True
		# Flag to only perform action once
		self.performOnce = True

		# Dictionary of ordered methods to call for each scene
		# Each scene contains a list containing the ordered methods to call
		# pm  -> playermove
		# m   -> maps [optional speicified parameter for scrolling map]
		# p   -> player
		# t   -> treasure [optional specified showing parameter]
		# s   -> story [story name]
		# i   -> if intro message is finished [flag name]
		# c   -> treasure chest
		self.sceneSequences = {
			# Main world
			"mainWorldShop" :   ["pm", "m", "p", "t", "s[self.story.mainWorldShop(next)]"],

			"waterTemple" :		["pm", "m", "s[self.story.temple('water')]", "p", "t"],
			"waterWorldEnter" : ["pm", "m", "s[self.story.waterWorldEnter()]", "p", "t"],
			# Water world
			"waterWorld" :		["i[self.story.waterWorldMsgFinished]", "m[True]", "s[self.story.waterWorld(next)]",
								"p", "t[not self.isFighting and self.story.waterWorldMsgFinished]"],
			"waterWorldRoom1" : ["pm", "m", "c", "p", "t"],
			"waterWorldRoom2" : ["pm", "m", "c", "p", "t"],
			"waterWorldRoom3" : ["pm", "m", "c", "p", "t"],
			"waterWorldRoom4" : ["pm", "m", "c", "p", "t"],
			"waterWorldBoss" : ["i[self.story.waterWorldBossMsgFinished]", "m[True]", "c", 
								 "p", "t[not self.isFighting and self.story.waterWorldBossMsgFinished]", 
								 "s[self.story.waterWorldBoss(next, self.fight)]"],

			# Fire world
			"fireTemple" : 		["pm", "m", "s[self.story.temple('fire')]", "p", "t"],
			"fireWorldEnter" :  ["pm", "m", "c", "p", "t"],
			"fireWorld" : 		["i[self.story.fireWorldMsgFinished]", "m", "s[self.story.fireWorld(next)]",
								"c", "p", "t[not self.isFighting and self.story.fireWorldMsgFinished]"],
			"fireWorldRoom1" :  ["pm", "m", "c", "p", "t"],
			"fireWorldRoom2" :  ["pm", "m", "c", "p", "t"],

			# Surprise temple
			"surpriseTemple" :  ["i[self.story.surpriseTempleMsgFinished]", "m[True]", "c", 
								"s[self.story.surpriseTemple(next)]", "p", 
								"t[not self.isFighting and self.story.surpriseTempleMsgFinished]"],

			# Church
			"church" : ["i[self.story.churchMsgFinished]", "m[True]", "c", 
						"s[self.story.church(next)]", "p",
						"t[not self.isFighting and self.story.churchMsgFinished]"],

			# Final Temple
			"finalTemple" : ["pm", "m[True]", "c", "p","t[not self.isFighting]", 
							"s[self.story.finalTemple(next)]"],

			"ultimateShop" : ["m", "s[self.story.ultimateShop(click)]", "t"]
		}

	def loadStats(self):
		""" Load saved information """
		# Statistics imported from JSON file
		try:
			f = open("save.dat", "r")
			#print(repr(f.read()))
			data = f.read().strip().split("\n")
			f.close()
			# Load saved gems
			if data[0] != "":
				for info in data[0].split():
					self.treasure.gems[info] = True
			self.treasure.health = int(data[1])
			self.treasure.money = int(data[2])
		except:
			self.treasure.health = 50
			self.treasure.money = 10

		self.startOver = True

	def start(self, pos, click):
		""" Options on startup """

		# Draw background
		self.screen.blit(self.startup, (0,0))

		# Underline on hover
		if self.newGame.collidepoint(pos):
			draw.line(self.screen, (255,0,0), (200,328), (442,328))
		elif self.loadGame.collidepoint(pos):
			draw.line(self.screen, (255,0,0), (631,328), (878,328))
		# Button collision
		if self.newGame.collidepoint(pos) and click:
			self.startOver = True
			self.newGameMode = True
		elif self.loadGame.collidepoint(pos) and click:
			self.startOver = True
			self.loadGameMode = True

	def introStory(self):
		""" Intro to introduce story-line """
		# Add scrolling effect
		self.introY = max(self.introY-.2, 0)
		self.screen.blit(self.introTextBack, (0,0))
		self.screen.blit(self.introText, (0,self.introY))
		# Pause when text reaches top then fade to game
		if self.introY == 0:
			time.delay(1000)
			self.introTextOver = True
			self.startOver = True
			self.fade.fadeDark(self.maps.allScenes["mainWorld"][0], self.screen, self.player.mapCoords["mainWorld"])
			self.fade.reset()

	def objectUpdate(self):
		""" Update objects relative to large world """
		global enemyLocs, moneyLocs

		# Dictionary of lists with scene information
		# Scrolling maps need constant rect updates
		self.sceneInfo = {
			# Contents: Scene name --> rect door --> nect scene name --> player new coordinates
			"mainWorld" : [
				[Rect(self.player.mapCoords["mainWorld"][0]+1140,self.player.mapCoords["mainWorld"][1]+1930,20,20), "mainWorldShop", (534,546)],
				[Rect(self.player.mapCoords["mainWorld"][0]+1651,self.player.mapCoords["mainWorld"][1]+182,20,20), "waterTemple", (543,546)],
				[Rect(self.player.mapCoords["mainWorld"][0]+208,self.player.mapCoords["mainWorld"][1]+1427,20,10), "fireTemple", (543,546)],
				[Rect(self.player.mapCoords["mainWorld"][0]+1911,self.player.mapCoords["mainWorld"][1]+2389,20,20), "surpriseTemple", (550,540)],
				[Rect(self.player.mapCoords["mainWorld"][0]+1036,self.player.mapCoords["mainWorld"][1]+2814,20,20), "church", (525,413)],
				[Rect(self.player.mapCoords["mainWorld"][0]+132,self.player.mapCoords["mainWorld"][1]+2486,30,20), "finalTemple", (519,536)],
				[Rect(self.player.mapCoords["mainWorld"][0]+1284,self.player.mapCoords["mainWorld"][1]+998,30,20), "ultimateShop", (519,536)],
			],
			"mainWorldShop" : [[Rect(474,595,133,20), "mainWorld", (self.player.mapCoords["mainWorld"][0]+1140,self.player.mapCoords["mainWorld"][1]+1970)]],

			"waterTemple" : [
				[Rect(474,595,133,20), "mainWorld", (self.player.mapCoords["mainWorld"][0]+1645,self.player.mapCoords["mainWorld"][1]+219)],
				[Rect(546,113,25,15), "waterWorldEnter", (517,456)]
			],
			"waterWorldEnter" : [
				[Rect(484,591,100,20), "waterTemple", (543,180)],
				[Rect(503,292,70,60), "waterWorld", (533,526)]
			],
			"waterWorld" : [
				[Rect(491,582,100,10), "waterWorldEnter", (520,406)],
				[Rect(self.player.mapCoords["waterWorld"][0]+242,self.player.mapCoords["waterWorld"][1]+732,30,10), "waterWorldRoom1", (534,529)],
				[Rect(self.player.mapCoords["waterWorld"][0]+818,self.player.mapCoords["waterWorld"][1]+732,30,10), "waterWorldRoom2", (534,528)],
				[Rect(self.player.mapCoords["waterWorld"][0]+242,self.player.mapCoords["waterWorld"][1]+284,30,10), "waterWorldRoom3", (505,513)],
				[Rect(self.player.mapCoords["waterWorld"][0]+821,self.player.mapCoords["waterWorld"][1]+284,30,10), "waterWorldRoom4", (526,542)],
				[Rect(self.player.mapCoords["waterWorld"][0]+507, self.player.mapCoords["waterWorld"][1]+143, 100,20), "waterWorldBoss", 
				(self.player.mapCoords["waterWorldBoss"][0]+530,self.player.mapCoords["waterWorldBoss"][0]+520)]
			],
			"waterWorldRoom1" : [[Rect(525,569,100,10), "waterWorld", (self.player.mapCoords["waterWorld"][0]+242,self.player.mapCoords["waterWorld"][1]+790)]],
			"waterWorldRoom2" : [[Rect(525,576,100,10), "waterWorld", (self.player.mapCoords["waterWorld"][0]+818,self.player.mapCoords["waterWorld"][1]+790)]],
			"waterWorldRoom3" : [[Rect(484,569,100,10), "waterWorld", (self.player.mapCoords["waterWorld"][0]+242,self.player.mapCoords["waterWorld"][1]+340)]],
			"waterWorldRoom4" : [[Rect(512,583,100,10), "waterWorld", (self.player.mapCoords["waterWorld"][0]+821,self.player.mapCoords["waterWorld"][1]+340)]],
			"waterWorldBoss" : [[Rect(self.player.mapCoords["waterWorld"][0]+490,self.player.mapCoords["waterWorld"][1]+650,100,20), "waterWorld", 
								(self.player.mapCoords["waterWorld"][0]+533,self.player.mapCoords["waterWorld"][1]+221)]],

			"fireTemple" : [
				[Rect(474,595,133,20), "mainWorld", (self.player.mapCoords["mainWorld"][0]+208,self.player.mapCoords["mainWorld"][1]+1487)],
				[Rect(546,113,25,15), "fireWorldEnter", (475,544)]
			],
			"fireWorldEnter" : [
				[Rect(470,591,100,20), "fireTemple", (543,180)],
				[Rect(544,88,30,25), "fireWorld", (519,337)]
			],
			"fireWorld" : [
				[Rect(521,284,30,20), "fireWorldEnter", (545,161)],
				[Rect(681,219,30,20), "fireWorldRoom1", (525,219)],
				[Rect(361,316,30,20), "fireWorldRoom2", (522,258)]
			],
			"fireWorldRoom1" : [
				[Rect(529,178,30,20), "fireWorld", (676,277)]
			],
			"fireWorldRoom2" : [
				[Rect(522,204,30,20), "fireWorld", (356,369)]
			],

			"surpriseTemple" : [[Rect(500,590,100,10), "mainWorld", (self.player.mapCoords["mainWorld"][0]+1901,self.player.mapCoords["mainWorld"][1]+2450)]],
			"church" : [[Rect(400,590,300,10), "mainWorld", (self.player.mapCoords["mainWorld"][0]+1036,self.player.mapCoords["mainWorld"][1]+2854)]],
			"finalTemple" : [[Rect(400,590,300,10), "mainWorld", (self.player.mapCoords["mainWorld"][0]+132,self.player.mapCoords["mainWorld"][1]+2520)]],
			"ultimateShop" : [[Rect(400,590,300,10), "mainWorld", (self.player.mapCoords["mainWorld"][0]+1284,self.player.mapCoords["mainWorld"][1]+1050)]],
		}

		# Update map coordinates if map has a scrolling cameras
		if self.maps.allScenes[self.maps.sceneName][2]:
			mapx, mapy = self.player.mapCoords[self.maps.sceneName]

		# Create random enemy locations
		self.enemyLocsUpdate = []

		for pt in enemyLocs:
			point = (pt[0]+self.player.mapx, pt[1]+self.player.mapy)
			check = True

			# Rects where there can be no enemies
			areas = [
				Rect(self.player.mapx+1064,self.player.mapy+1863,250,200),
				Rect(self.player.mapx+979,self.player.mapy+2738,150,150),
				Rect(self.player.mapx+1846,self.player.mapy+2329,150,130),
				Rect(self.player.mapx+1595,self.player.mapy+99,135,143),
				Rect(self.player.mapx+1224,self.player.mapy+943,150,118),
				Rect(self.player.mapx+148,self.player.mapy+1357,140,128),
				Rect(self.player.mapx+80,self.player.mapy+2428,143,125)
			]

			# Only add points if they are not around the buildings
			for area in areas:
				if area.collidepoint(point):
					check = False
			if check:
				self.enemyLocsUpdate.append((pt[0]+self.player.mapx, pt[1]+self.player.mapy))

		# Create random money locations
		self.moneyLocsUpdate = []
		for i in moneyLocs:
			self.moneyLocsUpdate.append((i[0]+self.player.mapx, i[1]+self.player.mapy))

		# Update player rect
		self.playerRect = Rect(self.player.x,self.player.y,32,42)

 
	def play(self):
		global moneyLocs, enemyLocs
		# Update variables that change in other classes
		self.inWater = self.player.inBoat
		pos = mouse.get_pos()
		keys = key.get_pressed()

		# Update objects
		self.objectUpdate()
		# Create list of data from current scene
		sceneRects = self.sceneInfo[self.maps.sceneName]

		# Loop through all the sceneRects
		for rectObj in sceneRects:
			# Check for collision
			if rectObj[0].colliderect(self.playerRect):
				# Fade to scene
				self.fade.reset()
				# Pass map coordinates if needed
				if not self.maps.allScenes[rectObj[1]][2]:
					self.fade.fadeDark(self.maps.allScenes[rectObj[1]][0], self.screen, self.maps.allScenes[rectObj[1]][1])
				else:
					self.fade.fadeDark(self.maps.allScenes[rectObj[1]][0], self.screen, (self.player.mapCoords[rectObj[1]][0], self.player.mapCoords[rectObj[1]][1]))
				# Create new scene
				self.maps.newScene(rectObj[1])
				# Set new player coordinates
				self.player.x = rectObj[2][0]
				self.player.y = rectObj[2][1]
				# Reset fade values
				self.fade.reset()
				# Stop old music and play new music

				# Music for each scene/world
				# This hard-coded method allows for music to not be repeated in different rooms
				if not mac:
					# Fadeout music when in temple
					if self.maps.sceneName == "waterTemple" or self.maps.sceneName == "fireTemple":
						mixer.music.fadeout(500)

					if self.maps.sceneName == "waterWorldEnter":
						mixer.music.fadeout(500)
						mixer.music.load(self.sound.getMusic("waterWorldTheme"))
						mixer.music.play(loops=-1)

					elif self.maps.sceneName == "fireWorldEnter":
						mixer.music.fadeout(500)
						mixer.music.load(self.sound.getMusic("fireWorldTheme"))
						mixer.music.play(loops=-1)

					elif self.maps.sceneName == "mainWorldShop" or self.maps.sceneName == "ultimateShop":
						mixer.music.fadeout(500)
						mixer.music.load(self.sound.getMusic("shopTheme"))
						mixer.music.play(loops=-1)

					elif self.maps.sceneName == "church":
						mixer.music.fadeout(500)
						mixer.music.load(self.sound.getMusic("churchTheme"))
						mixer.music.play(loops=-1)		

					elif self.maps.sceneName == "surpriseTemple":
						mixer.music.fadeout(500)
						mixer.music.load(self.sound.getMusic("castleTheme"))
						mixer.music.play(loops=-1)

					elif self.maps.sceneName == "finalTemple":
						mixer.music.fadeout(500)
						mixer.music.load(self.sound.getMusic("finalTempleTheme"))
						mixer.music.play(loops=-1)

					elif self.maps.sceneName == "mainWorld":
						mixer.music.fadeout(500)
						mixer.music.load(self.sound.getMusic("mainWorldTheme"))
						mixer.music.play(loops=-1)

					# Using dictionaries was too slow...
					# self.sound.stopMusic()
					# if self.maps.sceneName in self.sound.sceneData:
					# 	self.sound.playMusic(self.sound.sceneData[self.maps.sceneName], True)


		# Set the fighting state
		self.isFighting = self.fight.fighting
		# Set game won states
		self.gameWon = self.story.gameWon

		# If the player is alive
		if self.player.isAlive:

			if self.maps.sceneName == "mainWorld":
				# Activities when player is not in a fight
				if not self.isFighting:

					# Call scene functions
					if not self.isFighting and self.story.mainWorldMsgFinished:
						self.player.move(self.maps.scrollingCamera, not self.isFighting, 
							self.maps.sceneName, self.maps.mask, self.treasure.collectedItems, self.treasure, self.maps)
					self.maps.render(self.screen, self.player.mapx, self.player.mapy)
					self.player.render()
					self.treasure.render(not self.isFighting and self.story.mainWorldMsgFinished, True, click, not self.fight.fighting, self.message)
					self.story.intro(next)

					# Money collected
					for i in self.moneyLocsUpdate: 
						if Rect(self.player.x,self.player.y,32,42).colliderect(Rect(i[0],i[1],2,2)):
							# Play sound
							if not mac:
								self.sound.coinCollected.play()
							# Add money to player's treasures
							self.treasure.money += 1
							moneyLocs = moneyPoints()
	 
					# Enemy fights
					for i in self.enemyLocsUpdate:
						if Rect(self.player.x,self.player.y,32,42).colliderect(Rect(i[0],i[1],2,2)):
							# Change music
							if not mac:
								mixer.music.fadeout(500)
								mixer.music.load(self.sound.getMusic("mainWorldFight"))
								mixer.music.play(loops=-1)
							# Generate points and start enemy fight
							enemyLocs = enemyPoints()
							self.fight.start()
							self.isFighting = self.fight.fighting
							self.player.isMoving = False

			else:

				# Use the scene sequences dictionary to call methods in order
				for action in self.sceneSequences[self.maps.sceneName]:
					# Move player
					if action == "pm":
						self.player.move(self.maps.scrollingCamera, not self.isFighting, 
							self.maps.sceneName, self.maps.mask, self.treasure.collectedItems, self.treasure, self.maps)
					# Render map
					elif action[0] == "m":
						# Scrolling map
						if len(action) > 1:
							self.maps.render(self.screen, self.player.mapx, self.player.mapy)
						# Still map
						else:
							self.maps.render(self.screen)
					# Render player
					elif action == "p":
						self.player.render()
					# Render treasure
					elif action[0] == "t":
						# Scrolling map
						if len(action) > 1:
							self.treasure.render(eval(action[2:action.find("]")]), False, click, not self.fight.fighting, self.message)
						# Still map
						else:
							self.treasure.render(not self.isFighting, False, click, not self.fight.fighting, self.message)
					# Render story line 
					elif action[0] == "s":
						# Execute currect story
						exec(action[2:action.find("]")])
					# Restrict player movement till after intro message has been viewed
					elif action[0] == "i":
						if eval(action[2:action.find("]")]):
							self.player.move(self.maps.scrollingCamera, not self.isFighting, 
								self.maps.sceneName, self.maps.mask, self.treasure.collectedItems, self.treasure, self.maps)
					# Render treasure chest
					elif action == "c":
						self.chest.render(self.playerRect)


			# Render fight scenes
			if self.isFighting:
				
				# Call water fight scene
				if self.inWater:
					self.fight.render("mainWorldSea", self.fade,
							next, self.maps, click)
				# Normal fight scene
				else:
					# Water world boss fight
					if self.maps.sceneName == "waterWorldBoss":
						self.fight.render(self.maps.sceneName, self.fade,
								next, self.maps, click, "broth")
					else:
						self.fight.render(self.maps.sceneName, self.fade,
								next, self.maps, click)
		else:
			self.player.die(click, self.treasure, self.maps, self.fight)


	def gameOverWin(self):
		""" Game over (won) """
		self.fade.fadeDark(self.ending, self.screen, (0,0))
		self.screen.blit(self.ending, (0,0))
		# Set final music flag to true
		if self.performOnce:
			self.gameOverMusic = True
			self.performOnce = False

 
def enemyPoints():
	""" Generates enemy points """
	return [[randint(1,2016), randint(1,3036)] for i in range(80)]

def moneyPoints():
	""" Generates money points """
	return [[randint(1,2016), randint(1,3036)] for i in range(150)]

Game = Main()
clock = time.Clock()

# Create initial points list
enemyLocs = enemyPoints()
moneyLocs = moneyPoints()

# Set mouse to invisible for custom cursor image
mouse.set_visible(False)

# Game loop
running = True
playing = False
while running:
	pos = mouse.get_pos()
	next = click = False

	for e in event.get():
		if e.type == QUIT:
			running = False
		# Update button presses
		if e.type == KEYDOWN:
			if e.key == K_RETURN: 
				next = True
		if e.type == MOUSEBUTTONDOWN: 
			click = True

	# Game screens
	# ----------------------------------
	# If the game has not been won
	if not Game.gameWon:
		# If the user has not selected the startup option
		if not playing:

			# Load / Save select
			if Game.startOver and not Game.loadGameMode and not Game.newGameMode:
				Game.start(pos, click)

			# New game
			if Game.newGameMode:
				if Game.introTextOver:
					Game.fade.fadeDark(Game.maps.allScenes["mainWorld"][0], Game.screen, Game.player.mapCoords["mainWorld"])
					Game.fade.reset()
					playing = True

				else:
					Game.fade.fadeDark(Game.introTextBack, Game.screen, (0,0))
					Game.introStory()

			# Load game
			if Game.loadGameMode:
				Game.loadStats()
				Game.loadGameMode = False
				Game.fade.fadeDark(Game.maps.allScenes["mainWorld"][0], Game.screen, Game.player.mapCoords["mainWorld"])
				Game.fade.reset()
				playing = True

		# Start the game
		if playing:
			Game.play()

	# Game won screen
	else:
		# Use flag to play conclusion music once
		if Game.gameOverMusic:
			# Play music
			if not mac:
				mixer.music.fadeout(500)
				mixer.music.load(Game.sound.getMusic("conclusion"))
				mixer.music.play(loops=-1)
			Game.gameOverMusic = False
		# Game over win screen
		Game.gameOverWin()


	# Blit custom cursor
	display.update(Game.screen.blit(Game.cursor, (pos[0],pos[1])))

	# Steady FPS
	clock.tick(70)
	display.flip()

quit()
