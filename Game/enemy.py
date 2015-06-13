# enemy.py
# Paul Krishnamurthy 2015
# Enemy class

# The Third Element
# ICS3U Final Project

from pygame import *
from random import choice

class Enemy(object):
	""" Enemy class """
	
	def __init__(self):
		# All enemies
		self.enemies = ["an Olive Serpent", "a King Frog", "a Skeleton Dancer", "a Double Dragon"]
		self.waterEnemies = ["a Swarly", "a Tentacruel"]
		# Enemy data -> (sprites, position, attack power possibilities, location of health bar)
		self.enemyData = {
			"an Olive Serpent" : [[transform.scale2x(image.load("resources/graphics/enemies/Olive Serpant/%s.png"%str(i)).convert_alpha()) for i in range(3)],
									(191,217), [2,2,2,3], (175,183)],
			"a King Frog" : [[transform.scale2x(image.load("resources/graphics/enemies/King Frog/%s.png"%str(i)).convert_alpha()) for i in range(3)],
								(121,174), [4,3,4,4,5], (137,149)],
			"a Skeleton Dancer" : [[transform.scale2x(image.load("resources/graphics/enemies/Skeleton Dancer/%s.png"%str(i)).convert_alpha()) for i in range(3)],
								(141,244), [2,2,2,3,3,2], (151,202)],
			"a Double Dragon" : [[transform.scale2x(image.load("resources/graphics/enemies/Double Dragon/%s.png"%str(i)).convert_alpha()) for i in range(4)],
								(161,214), [4,5,5,5], (174,168)]
		}
		self.waterEnemyData = {
			"a Swarly" : [[transform.scale2x(transform.scale2x(image.load("resources/graphics/enemies/Swarly/%s.png"%str(i)).convert_alpha())) for i in range(6)],
									(191,252), [2,2,2,3,3], (188,206)],
			"a Tentacruel" : [[transform.scale2x(transform.scale2x(image.load("resources/graphics/enemies/Tentacruel/%s.png"%str(i)).convert_alpha())) for i in range(10)],
								(155,204), [4,3,3,4,4,5], (164,163)]
		}
		# Other individual enemies (name, sprites, position, location of health bar, total health)
		self.broth = ["Broth", [transform.scale2x(image.load("resources/graphics/enemies/Broth/%s.png"%str(i)).convert_alpha()) for i in range(7)],
						(125,194), (132,161), 50, 20]
		# Dictionary to reference custom enemies
		self.customEnemies = {
			"broth" : self.broth
		}

	def randomEnemy(self, area, custom=None):
		""" Returns random enemy based on location"""
		# Return list if custom enemy is requested
		if custom != None:
			info = self.customEnemies[custom]
			return [info[0], info[2], info[4], info[3]]
		# Handle main world enemies
		else:
			if area == "water":
				enemy = choice(self.waterEnemies)
				# name, pos, attack, health pos
				return [enemy, self.waterEnemyData[enemy][1], choice(self.waterEnemyData[enemy][2]), self.waterEnemyData[enemy][3]]
			else:
				enemy = choice(self.enemies)
				return [enemy, self.enemyData[enemy][1], choice(self.enemyData[enemy][2]), self.enemyData[enemy][3]]
