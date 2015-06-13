# chest.py
# Paul Krishnamurthy 2015
# Handle treasure chest actions

# The Third Element
# ICS3U Final Project

from pygame import *
from random import choice, randint

class Chest:
	""" Handles treasure chest actions """
	
	def __init__(self, screen, treasure, message, maps, player, fight, sound, fade):
		self.screen = screen
		self.treasure = treasure
		self.message = message
		self.maps = maps
		self.player = player
		self.fight = fight
		self.sound = sound
		self.fade = fade
		self.chest = image.load("resources/graphics/items/chest.png")
		self.openChest = image.load("resources/graphics/items/chest-opened.png")
		# Possible random prizes (basic)
		self.prizes = ["money", "health", "enemy"]

		# Each chest has -> (position, state [opened or not], random prize, scrolling view)
		self.allChests = {
			"surpriseTemple" : [
				[[482,729], False, choice(self.prizes), True],
				[[614,729], False, choice(self.prizes), True],
				[[614,645], False, choice(self.prizes), True],
				[[482,320], False, choice(self.prizes), True],
				[[614,320], False, choice(self.prizes), True],
				[[482,400], False, choice(self.prizes), True],
				[[494,94], False, choice(self.prizes), True],
				[[609,94], False, choice(self.prizes), True],
				[[482,645], False, choice(self.prizes), True]
			],
			"waterWorldRoom1" : [[[531,288], False, choice(self.prizes[:1]), False]],
			"waterWorldRoom2" : [[[533,204], False, "enemy", False]],
			"waterWorldRoom3": [[[507,169], False, choice(self.prizes[:1]), False]],
			"waterWorldRoom4" : [[[526,278], False, "enemy", False]],
			"waterWorldBoss" : [[[526,278], False, "full health", True]],

			"fireWorldEnter" : [
				# Good prize
				[[1026,478], False, choice(self.prizes[:1]), False],
				[[23,340], False, choice(self.prizes[:1]), False],
				[[867,222], False, choice(self.prizes[:1]), False]
			],
			"fireWorld" : [
				# Flame Sword
				[[694,484], False, "flameSword", False]
			],
			"fireWorldRoom1" : [
				[[694,365], False, choice(self.prizes), False],
				# Chest that contains the fire gem
				[[523,533], False, "fire gem", False],
				[[335,533], False, choice(self.prizes), False]
			],
			"fireWorldRoom2" : [[[524,411], False, choice(self.prizes), False]],
			"finalTemple" : [
				[[347,340], False, choice(self.prizes[:1]), True],
				[[525,337], False, choice(self.prizes[:1]), True],
				[[705,337], False, choice(self.prizes[:1]), True]
			]
		}

	def render(self, pRect):
		""" Renders treasure chest """

		def pause(length):
			""" Pauses screen """
			display.flip()
			time.wait(length)

		def drawChests():
			""" To fix flashing chest bug """
			for key,val in self.allChests.items():
				# Draw chests based on current screen
				if key == self.maps.sceneName:
					for i in range(len(self.allChests[key])):
						coords = self.allChests[key][i][0]
						# Add the map coordinates only if the map is scrolling
						if self.allChests[key][i][3]:
							self.screen.blit(self.chest, (coords[0]+self.player.mapx, coords[1]+self.player.mapy))
						else:
							self.screen.blit(self.chest, coords)

		# Blit the opened or closed chest at specified positions
		for key,val in self.allChests.items():
			# Handle collision based on current screen
			if key == self.maps.sceneName:
				for i in range(len(self.allChests[key])):
					# Chest coordinattes
					coords = self.allChests[key][i][0]
					# Blit opened or closed chest

					# Draw the opened or closed treasure chest
					if self.allChests[key][i][1]:
						# Add the map coordinates if the map is scrolling
						if self.allChests[key][i][3]:
							self.screen.blit(self.openChest, (coords[0]+self.player.mapx, coords[1]+self.player.mapy))
						else:
							self.screen.blit(self.openChest, coords)
					else:
						# Add the map coordinates if the map is scrolling
						if self.allChests[key][i][3]:
							self.screen.blit(self.chest, (coords[0]+self.player.mapx, coords[1]+self.player.mapy))
						else:
							self.screen.blit(self.chest, coords)

						# Set the chest rect coordinates if the map is scrolling
						if self.allChests[key][i][3]:
							x = coords[0]+self.player.mapx
							y = coords[1]+self.player.mapy
						else:
							x = coords[0]
							y = coords[1]

						# Set chest state to opened
						if pRect.colliderect(Rect(x,y,32,32)):
							self.allChests[key][i][1] = True
							# Random prize
							prize = self.allChests[key][i][2]
							# Award prizes
							if prize == "money":
								reward = randint(10,30)
								drawChests()
								self.player.render()
								self.treasure.render(self.screen, True, False, False, self.message)
								self.message.botMessage("You have been rewarded with %s coins!"%str(reward), False)
								#self.sound.play("coinCollected")
								self.treasure.money += reward
								pause(1300)
							elif prize == "full health":
								drawChests()
								self.player.render()
								self.treasure.render(self.screen, True, False, False, self.message)
								self.message.botMessage("Your health has been restored.", False)
								#self.sound.play("coinCollected")
								self.treasure.health = 100
								pause(1300)
							elif prize == "fire gem":
								drawChests()
								self.player.render()
								self.treasure.render(self.screen, True, False, False, self.message)
								self.message.botMessage("You have obtained the fire gem!", False)
								self.treasure.gems["fire"] = True
								pause(1300)	
							elif prize == "health":
								reward = randint(10,20)
								drawChests()
								self.player.render()
								self.treasure.render(self.screen, True, False, False, self.message)
								self.message.botMessage("You have been rewarded with %s health!"%str(reward), False)
								self.treasure.health = min(100, self.treasure.health+reward)
								pause(1300)
							elif prize == "flameSword":
								drawChests()
								self.player.render()
								self.treasure.collectedItems.add("flameSword")
								self.treasure.render(self.screen, True, False, False, self.message)
								self.message.topMessage("You have been rewarded with the flame Sword!", False)
								pause(1300)
							else:
								# Call random fight
								self.fight.start()
