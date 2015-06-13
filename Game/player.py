# player.py
# Paul Krishnamurthy 2015
# Main player class

# The Third Element
# ICS3U Final Project

from pygame import *
from sys import exit as abandon

class Player(object):
	""" Main player class """
	
	def __init__(self, screen, message, fade):
		self.screen = screen
		self.message = message
		self.fade = fade
		# Use list comprehension to create lists of animated sprites in a dictionary
		self.sprites = {
			"left" : [image.load("resources/graphics/player/lMove/%s.gif"%str(i)).convert() for i in range(4)],
			"right": [image.load("resources/graphics/player/rMove/%s.png"%str(i)).convert() for i in range(4)],
			"down": [image.load("resources/graphics/player/dMove/%s.gif"%str(i)).convert() for i in range(4)],
			"up": [image.load("resources/graphics/player/uMove/%s.gif"%str(i)).convert() for i in range(4)]
		}
		self.boatSprites = {
			"left" : [image.load("resources/graphics/player/boat/lMove/%s.png"%str(i)).convert_alpha() for i in range(8)],
			"right": [image.load("resources/graphics/player/boat/rMove/%s.png"%str(i)).convert_alpha() for i in range(8)],
			"down": [image.load("resources/graphics/player/boat/dMove/%s.png"%str(i)).convert_alpha() for i in range(5)],
			"up": [image.load("resources/graphics/player/boat/uMove/%s.png"%str(i)).convert_alpha() for i in range(5)]	
		}
		# Player's starting image
		self.image = self.sprites["down"][0]
		# Player starting coordinates
		self.x = 601
		self.y = 378
		# Current frame
		self.frame = 0
		# Player direction
		self.direction = "right"
		# Flag to check player movement
		self.isMoving = False
		# Flag to check if player is in the boat
		self.inBoat = False
		# Player speed
		self.speed = 1.5
		# Map moving speed
		self.mapSpeed = 2
		# Starting coordiantes for all scrolling maps
		self.mapCoords = {
			"mainWorld": [-534, -1585],
			"waterWorld": [0, -602],
			"surpriseTemple" : [0, -602],
			"waterWorldBoss" : [0, -572],
			"church" : [0, -790],
			"finalTemple" : [0,-312]
		}
		# Current map positions
		self.mapx, self.mapy = self.mapCoords["mainWorld"]

		# Dictionary of all bounding rects for moving maps
		# Main boundary rect -> right,left,up,down boundary rects -> corner positions
		self.boundaries = {
			"mainWorld" : [
				Rect(150,150,788,300), Rect(936,0,150,600), Rect(0,0,150,600), Rect(0,0,1086,150), Rect(0,450,1086,150),
				(-926,0,0,-2436)
			],
			"waterWorld" : [
				Rect(150,150,788,300), Rect(936,0,150,600), Rect(0,0,150,600), Rect(0,0,1086,150), Rect(0,450,1086,150),
				(0,0,-70,-602)
			],
			"surpriseTemple" : [
				Rect(150,150,788,300), Rect(936,0,150,600), Rect(0,0,150,600), Rect(0,0,1086,150), Rect(0,450,1086,150),
				(0,0,-70,-602)
			],
			"waterWorldBoss" : [
				Rect(150,150,788,300), Rect(936,0,150,600), Rect(0,0,150,600), Rect(0,0,1086,150), Rect(0,450,1086,150),
				(0,0,-70,-572)
			],
			"church" : [
				Rect(150,150,788,300), Rect(936,0,150,600), Rect(0,0,150,600), Rect(0,0,1086,150), Rect(0,450,1086,150),
				(0,0,-70,-790)
			],
			"finalTemple" : [
				Rect(150,150,788,300), Rect(936,0,150,600), Rect(0,0,150,600), Rect(0,0,1086,150), Rect(0,450,1086,150),
				(0,0,-70,-312)
			]
		}
		# World view bounding rect
		self.boundary = Rect(150,150,788,300)
		# Specific direction bounding rects
		self.rBoundary = Rect(936,0,150,600)
		self.lBoundary = Rect(0,0,150,600)
		self.uBoundary = Rect(0,0,1086,150)
		self.dBoundary = Rect(0,450,1086,150)
		# Delta x,y
		self.dx = 0
		self.dy = 0
		# Frame animation speed
		self.frameSpeed = .2
		# All player speeds based on map
		self.speeds = {
			"mainWorld" : 1.5,
			"mainWorldShop" : 2,
			"waterTemple": 2,
			"waterWorldEnter" : 2,
			"waterWorld" : 1,
			"waterWorldRoom1" : 1.5,
			"waterWorldRoom2" : 1.5,
			"waterWorldRoom3" : 1.5,
			"waterWorldRoom4" : 1.5,
			"waterWorldBoss" : 1.5,
			"fireTemple" : 2,
			"fireWorldEnter" : 2,
			"fireWorld" : 1.5,
			"fireWorldRoom1" : 1.5,
			"fireWorldRoom2" : 1.5,
			"surpriseTemple" : 1.5,
			"church" : 1.5,
			"finalTemple" : 1.5,
			"ultimateShop" : 1.5
		}
		# Can the player can move
		self.canMove = False
		# Tries to go on water without boat
		self.waterAttempt = False
		# Check if player if alive
		self.isAlive = True

		# Game over screen
		self.gameOver = image.load("resources/graphics/misc/gameOver.png").convert()
		self.continueRect = Rect(139,482,180,65)
		self.abandonRect = Rect(453,488,180,65)

	def get_surrounding(self, scene):
		""" Returns collision point(s) based on direction """
		# Scrolling maps
		if scene in ["mainWorld", "waterWorld", "surpriseTemple", "waterWorldBoss", "church", "finalTemple"]:
			# Return point on player relative to the world
			if self.direction == "up":
				return [(self.x+abs(self.mapx)+16, self.y+abs(self.mapy)+30)]
			if self.direction == "down":
				return [(self.x+abs(self.mapx)+16, self.y+abs(self.mapy)+42)]
			if self.direction == "right":
				return [(self.x+abs(self.mapx)+30, self.y+abs(self.mapy)+30)]
			if self.direction == "left":
				return [(self.x+abs(self.mapx)+6, self.y+abs(self.mapy)+30)]
		# Fixed position maps
		else:
			# Return point on player
			if self.direction == "up": return [(self.x+16, self.y+30)]
			if self.direction == "down": return [(self.x+16, self.y+42)]
			if self.direction == "right": return [(self.x+30, self.y+30)]
			if self.direction == "left": return [(self.x+6, self.y+30)]

	def collision(self, mask, scene):
		""" Checks for x and y collision """
		points = self.get_surrounding(scene)

		for p in points:
			x,y = p
			# Try/except to catch pixel index out of range
			try:
				#print(mask.get_at((int(x+self.dx), int(y+self.dy)))[:3])
				if mask.get_at((int(x+self.dx), int(y+self.dy)))[:3] == (0,0,0):
					return "black"
				elif mask.get_at((int(x+self.dx), int(y+self.dy)))[:3] == (0,0,255):
					return "water"
			except:
				pass
			return "white"

	def move(self, scrollingCamera, canMove, scene, mask, collectedItems, treasure, maps):
		""" Update player position """
		# Reset delta x,y
		self.dx, self.dy = 0, 0
		# Get keyboard events
		keys = key.get_pressed()
		# Set new speeds
		self.speed = self.speeds[scene]
		screenW, screenH = 1086, 600

		# Keep track of what player sprites to use
		s = self.boatSprites if self.inBoat else self.sprites

		# Change image if frame is a whole number
		if self.frame%1==0:
			try: self.image = s[self.direction][int(self.frame)]
			except: self.image = s[self.direction][0]

		if self.isMoving:
			# Add to frames
			if s == self.boatSprites:
				self.frame += eval("."+"3"*22) # lol
			else:
				self.frame += .2
			if self.frame >= len(s[self.direction]):
				self.frame = 0
		else:
			self.frame = 0
			self.image = s[self.direction][0]
		
		# Width and height of image
		self.imageW = self.image.get_width()
		self.imageH = self.image.get_height()

		if canMove:
		# Set the delta x, delta y, speed, isMoving flag and the direction based on the keys pressed
			if keys[K_d] or keys[K_RIGHT]:
				self.dx = self.speed
				self.isMoving = True
				self.direction = "right"
			elif keys[K_a] or keys[K_LEFT]:
				self.dx = -self.speed
				self.isMoving = True
				self.direction = "left"
			elif keys[K_w] or keys[K_UP]:
				self.dy = -self.speed
				self.isMoving = True
				self.direction = "up"
			elif keys[K_s] or keys[K_DOWN]:
				self.dy = self.speed
				self.isMoving = True
				self.direction = "down"
			else:
				self.isMoving = False

			# Move map and player
			if self.collision(mask, scene) == "water" and "boat" in collectedItems:
				self.inBoat = True
			if self.collision(mask, scene) == "white":
				self.inBoat = False

			# # Allow player to go on water only with boat
			if self.collision(mask, scene) == "water" and not self.inBoat:
				self.waterAttempt = True
			else:
				self.waterAttempt = False

			# Check player's future position
			if (self.collision(mask, scene) != "black" and self.collision(mask, scene) != "water") or \
				(self.collision(mask, scene) == "water" and self.inBoat):# \
				#and self.collision(mask, scene) == "blue" and not self.inBoat:

				# For scrolling maps, only move the player if they are inside the boundary rect
				# If not, move the map based on the direction of the player
				if scrollingCamera:
					# Player moving right
					if self.direction == "right": 
						if self.boundaries[scene][1].collidepoint((self.x+self.dx, self.y+self.dy)):
							self.mapx = max(self.boundaries[scene][5][0], self.mapx-self.dx*1.5)
						else:
							self.x += self.dx
					# Player moving left
					elif self.direction == "left":
						if self.boundaries[scene][2].collidepoint((self.x+self.dx, self.y+self.dy)):
							self.mapx =  min(self.boundaries[scene][5][1], self.mapx-self.dx*1.5)
						else:
							self.x += self.dx
					# Player moving up
					if self.direction == "up":
						if self.boundaries[scene][3].collidepoint((self.x+self.dx, self.y+self.dy)):
							self.mapy = min(self.boundaries[scene][5][2], self.mapy-self.dy*1.5)
						else:
							self.y += self.dy
					# Player moving down
					elif self.direction == "down":
						if self.boundaries[scene][4].collidepoint((self.x+self.dx, self.y+self.dy)):
							self.mapy =  max(self.boundaries[scene][5][3], self.mapy-self.dy*1.5)
						else:
							self.y += self.dy

					# Move the player if map touches any of the four corners
					if not self.boundaries[scene][0].collidepoint((self.x+self.dx, self.y+self.dy)):
						# Top left corner
						if self.mapx == self.boundaries[scene][5][0]:
							self.x = min(screenW-self.imageW, min(self.x+self.dx*2, screenW-self.imageW))
						# Top right corner
						elif self.mapx == self.boundaries[scene][5][1]:
							self.x = max(0, min(self.x+self.dx*2, screenW))
						# Botton left corner
						if self.mapy == self.boundaries[scene][5][2]:
							self.y = max(0, min(self.y+self.dy*2, screenH))
						# Botton right corner
						elif self.mapy == self.boundaries[scene][5][3]:
							self.y = min(screenH-self.imageH, min(self.y+self.dy*2, screenH-self.imageH))

					else:
						# Add delta x and y to player coordinates
						self.x += self.dx
						self.y += self.dy

					# Update map coordinates in dictionary
					self.mapCoords[scene] = self.mapx, self.mapy

				# For fixed maps, just add the delta x,y to the player's position
				else:
					if self.direction == "right": self.x += self.dx
					elif self.direction == "left": self.x += self.dx
					if self.direction == "up": self.y += self.dy
					elif self.direction == "down": self.y += self.dy


	def die(self, click, treasure, maps, fight):
		""" Player dies """
		pos = mouse.get_pos()
		self.screen.blit(self.gameOver, (0,0))

		# I changed my mind about allowing the player to continue
		# if self.continueRect.collidepoint(pos) and click:
		# 	# Reset player stats
		# 	self.isAlive = True
		# 	fight.playerDied = False
		# 	treasure.health = 10
		# 	treasure.money = 0
		# 	# Send player back to starting point

		# 	# Fade back into main world
		# 	self.fade.fadeDark(maps.allScenes["mainWorld"][0], self.screen, self.mapCoords["mainWorld"])
		# 	#display.flip()
		# 	# self.fade.reset()

		if self.abandonRect.collidepoint(pos) and click:
			# Fade away and abandon Oslax
			surf = Surface((1086,600))
			surf.fill((0,0,0))
			self.fade.fadeDark(surf, self.screen, (0,0))

			# Save results to file
			f = open("save.dat", "w")
			gems = ""
			if treasure.gems["earth"]: gems += "earth "
			if treasure.gems["fire"]: gems += "fire "
			if treasure.gems["water"]: gems += "water "
			f.write(gems+"\n")
			f.write("10"+"\n")
			f.write(str(treasure.money)+"\n")
			f.close()
			abandon(0)

	
	def render(self):
		""" Render player to screen """
		# If player is alive, render screen
		if self.isAlive:
			self.screen.blit(self.image, (self.x, self.y))
			# Notification when trying to travel on water without boat
			if self.waterAttempt:
				self.message.narration(["You need to obtain the power to travel on water..."], False, "bottom")

