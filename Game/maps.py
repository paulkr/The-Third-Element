# maps.py
# Paul Krishnamurthy 2015
# Maps class to update and render scenes

# The Third Element
# ICS3U Final Project

from pygame import *

class Maps:
	""" Main map class """
	
	def __init__(self, screen, player):
		self.screen = screen
		self.player = player
		# Dictionary with map image -> coordinates -> scrolling camera
		self.allScenes = {
			"mainWorld" : [transform.scale2x(image.load("resources/graphics/map/mainWorld.png").convert()), (-534,-1585), True],
			"mainWorldShop" : [image.load("resources/graphics/map/mainWorldShop.png").convert(), (0,0), False],

			"waterTemple" : [image.load("resources/graphics/map/portalRoom.png").convert(), (0,0), False],
			"waterWorldEnter" : [image.load("resources/graphics/map/waterWorldEnter.png").convert(), (0,0), False],
			"waterWorld" : [image.load("resources/graphics/map/waterWorld.png").convert(), (0,-602), True],
			"waterWorldRoom1" : [image.load("resources/graphics/map/waterWorldRoom1.png").convert(), (0,0), False],
			"waterWorldRoom2" : [image.load("resources/graphics/map/waterWorldRoom2.png").convert(), (0,0), False],
			"waterWorldRoom3" : [image.load("resources/graphics/map/waterWorldRoom3.png").convert(), (0,0), False],
			"waterWorldRoom4" : [image.load("resources/graphics/map/waterWorldRoom4.png").convert(), (0,0), False],
			"waterWorldBoss" : [image.load("resources/graphics/map/waterWorldBoss.png").convert(), (0,-582), True],

			"fireTemple" :  [image.load("resources/graphics/map/portalRoom.png").convert(), (0,0), False],
			"fireWorldEnter" : [image.load("resources/graphics/map/fireWorldEnter.png").convert(), (0,0), False],
			"fireWorld" : [image.load("resources/graphics/map/fireWorld.png").convert(), (0,0), False],
			"fireWorldRoom1" : [image.load("resources/graphics/map/fireWorldRoom1.png").convert(), (0,0), False],
			"fireWorldRoom2" : [image.load("resources/graphics/map/fireWorldRoom2.png").convert(), (0,0), False],

			"surpriseTemple" : [image.load("resources/graphics/map/surpriseTemple.png").convert(), (0,-602), True],
			"church" : [image.load("resources/graphics/map/church.png").convert(), (0,-790), True],
			"finalTemple" : [image.load("resources/graphics/map/finalTemple.png").convert(), (0,-312), True],
			"ultimateShop" : [transform.scale(image.load("resources/graphics/map/ultimateShop.jpg").convert(),(1086,600)), (0,0), False]
		}
		# Masks for each scene
		self.allScenesMasks = {
			"mainWorld" : transform.scale2x(image.load("resources/graphics/map/mainWorldMask.png").convert()),
			"mainWorldShop" : image.load("resources/graphics/map/mainWorldShopMask.png").convert(),

			"waterTemple" : image.load("resources/graphics/map/portalRoomMask.png").convert(),
			"waterWorldEnter" : image.load("resources/graphics/map/waterWorldEnterMask.png").convert(),
			"waterWorld" : image.load("resources/graphics/map/waterWorldMask.png").convert(),
			"waterWorldRoom1" : image.load("resources/graphics/map/waterWorldRoom1Mask.png").convert(),
			"waterWorldRoom2" : image.load("resources/graphics/map/waterWorldRoom2Mask.png").convert(),
			"waterWorldRoom3" : image.load("resources/graphics/map/waterWorldRoom3Mask.png").convert(),
			"waterWorldRoom4" : image.load("resources/graphics/map/waterWorldRoom4Mask.png").convert(),
			"waterWorldBoss" : image.load("resources/graphics/map/waterWorldBossMask.png").convert(),

			"fireTemple" : image.load("resources/graphics/map/portalRoomMask.png").convert(),
			"fireWorldEnter" : image.load("resources/graphics/map/fireWorldEnterMask.png").convert(),
			"fireWorld" : image.load("resources/graphics/map/fireWorldMask.png").convert(),
			"fireWorldRoom1" : image.load("resources/graphics/map/fireWorldRoom1Mask.png").convert(),
			"fireWorldRoom2" : image.load("resources/graphics/map/fireWorldRoom1Mask.png").convert(),

			"surpriseTemple" : image.load("resources/graphics/map/surpriseTempleMask.png").convert(),
			"church" : image.load("resources/graphics/map/churchMask.png").convert(),
			"finalTemple" : image.load("resources/graphics/map/finalTempleMask.png").convert(),
			"ultimateShop" : transform.scale(image.load("resources/graphics/map/ultimateShop.jpg").convert(),(1086,600)).convert()
		}

		# Initial World Setup
		self.sceneName = "mainWorld"
		# Current image
		self.image = self.allScenes[self.sceneName][0]
		# Scrolling camera boolean
		self.scrollingCamera = self.allScenes[self.sceneName][2]
		# Mask image
		self.mask = self.allScenesMasks[self.sceneName]

	def newScene(self, scene):
		""" Set new scene """
		# Set new image and scene
		self.image = self.allScenes[scene][0]
		self.sceneName = scene
		# Flag if map can move
		self.scrollingCamera = self.allScenes[self.sceneName][2]
		# Update collision map
		self.mask = self.allScenesMasks[self.sceneName]

		# Scrolling map
		if self.allScenes[scene][2]:
			self.player.mapx, self.player.mapy = self.player.mapCoords[scene]

	def render(self, screen, x=None, y=None):
		""" Update new scene """

		# If map can move blit it at specific coordinates
		if self.allScenes[self.sceneName][2]:
			screen.blit(self.image, (x,y))
		# If not blit it at the top left
		else:
			screen.blit(self.image, (0,0))
