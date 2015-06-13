# treasure.py
# Paul Krishnamurthy 2015
# Class that contains treasures and menu

# The Third Element
# ICS3U Final Project

from pygame import *
from random import randint

class Treasure:
	""" Displays treasures """

	def __init__(self, screen, player):
		self.screen = screen
		self.player = player
		# Resources
		self.coin = transform.scale(image.load("resources/graphics/misc/coin.png").convert(),(16,16))

		# Heart health system
		# self.heart = transform.scale(image.load("resources/graphics/misc/heart.png"),(16,16))
		# self.hHeart = self.heart.subsurface(0,0,8,16)

		# Fonts
		self.font = font.Font("resources/fonts/TooSimple.ttf", 12)
		self.arial = font.SysFont("Arial", 25)

		# Gem animation stuff
		self.gemFrame = 0
		self.gemSprites = {
			"earth" : [image.load('resources/graphics/items/gems/eGem/eGem%s.png'%str(i)).convert_alpha() for i in range(4)],
			"fire" : [image.load('resources/graphics/items/gems/fGem/fGem%s.png'%str(i)).convert_alpha() for i in range(4)],
			"water" : [image.load('resources/graphics/items/gems/wGem/wGem%s.png'%str(i)).convert_alpha() for i in range(4)]
		}
		self.noGem = image.load("resources/graphics/items/gems/noGem.gif").convert_alpha()
		# Check if player has been told to go to the temple
		self.allGemsCollectedMsg = False
		# Player's treasures
		self.money = 10
		# Player's health
		self.health = 50
		# Collected gems
		self.gems = {
			"earth": False,
			"fire": False,
			"water": False
		}

		# Weapons to keep track of max possible attack
		self.weapons = ["sword", "flameSword"]
		# Items -> (name, image, description, coordinates, rect, attack power)
		self.items = {
			"sword" : [
				"sword", 
				transform.scale2x(image.load("resources/graphics/items/sword.png").convert_alpha()),
				["A sword with an attack", "power of 5."],
				(363,209),
				Rect(363,209,50,50),
				5],
			"flameSword" : [
				"flameSword",
				transform.scale2x(image.load("resources/graphics/items/flameSword.png").convert_alpha()),
				["A fire sword with an", "attack power of 7"],
				(497,205),
				Rect(497,205,50,50),
				7],
			"boat" : [
				"boat", 
				image.load("resources/graphics/items/boat.png").convert_alpha(),
				["Power that allows you","to travel on water."],
				(422,200),
				Rect(422,200,50,50)],
			"speedBoots" : [
				"speedBoots",
				transform.scale(image.load("resources/graphics/items/speedBoots.png").convert_alpha(), (50,50)),
				["Boots that increase your","speed."],
				(565,206),
				Rect(565,206,50,50)
			]
		}

		# All collected items
		self.collectedItems = set()
		# For speed instead of drawing text
		self.inventory = transform.scale2x(transform.scale2x(image.load("resources/graphics/misc/inventory.png").convert_alpha()))
		self.settings = transform.scale2x(transform.scale2x(image.load("resources/graphics/misc/settings.png").convert_alpha()))
		self.mapView = transform.scale2x(transform.scale2x(image.load("resources/graphics/misc/mapView.png").convert_alpha()))
		self.smallMap = image.load("resources/graphics/map/smallMap.png")

		# Item placeholders.
		self.placeholder = transform.scale2x(image.load("resources/graphics/misc/placeholder.png").convert_alpha())
		self.sPlaceholder = image.load("resources/graphics/misc/dropDown.png").convert_alpha()
		self.gemPlaceholder = transform.scale2x(image.load("resources/graphics/misc/gemPlaceholder.png").convert_alpha())
		self.healthBar = transform.scale2x(image.load("resources/graphics/misc/healthBar.png").convert())

		self.inventoryRect = Rect(1028,140,40,40)
		self.settingsRect = Rect(1028,187,40,40)
		self.mapViewRect = Rect(1028,234,40,40)

		# Slice up health bar and add to list
		self.healthPercent = []
		self.div = self.healthBar.get_width()/100
		for i in range(100):
			self.healthPercent.append(self.healthBar.subsurface(0,0,self.div*(i+1),self.healthBar.get_height()))

		self.transCol = (128,128,128)
		self.surf = Surface((150,150))
		self.surf.fill(self.transCol)
		self.surf.set_colorkey(self.transCol)
		draw.circle(self.surf, (0,0,0,100), (50,50), 50)
		self.surf.set_alpha(100)

		# Chosen setting
		self.inventoryOn = False
		self.settingsOn = False
		self.mapViewOn = False

		# Inventory/Settings surfaces
		self.back = Surface((1086,600))
		self.back.fill((0,0,0))
		self.back.set_alpha(150)

	def inventoryDisplay(self, click):
		""" Inventory (items) """
		pos = mouse.get_pos()
		close = Rect(707,56,65,80)
		self.screen.blit(self.back, (0,0))
		self.screen.blit(self.inventory, (318,30))
		# Blit collected items
		for item in self.collectedItems:
			self.screen.blit(self.items[item][1], self.items[item][3])
			# Text bitting with word wrap
			if self.items[item][4].collidepoint(pos):
				y = 441
				for i in range(len(self.items[item][2])):
					self.screen.blit(self.arial.render(self.items[item][2][i], True, (255,255,255)), (414,y))
					y += 26
		# Check for button press
		if close.collidepoint(pos) and click:
			self.inventoryOn = False

	def settingsDisplay(self, click):
		""" Settings """
		pos = mouse.get_pos()
		close = Rect(707,56,65,80)
		self.screen.blit(self.back, (0,0))
		self.screen.blit(self.settings, (318,30))
		# Check for button press
		if close.collidepoint(pos) and click:
			self.settingsOn = False

	def mapViewDisplay(self, click):
		""" Large scale map view """
		pos = mouse.get_pos()
		close = Rect(707,56,56,80)
		self.screen.blit(self.back, (0,0))
		self.screen.blit(self.mapView, (318,30))
		self.screen.blit(self.smallMap, (347,196))
		# Check for button press
		if close.collidepoint(pos) and click:
			self.mapViewOn = False

	def render(self, showing, inWorld, click, fighting, message):
		""" Render to screen """
		pos = mouse.get_pos()
		if showing:
			# Blit placeholders
			self.screen.blit(self.placeholder, (10,10))

			self.screen.blit(self.sPlaceholder, (940,10))
			self.screen.blit(self.healthPercent[self.health-1], (83,22))
			self.screen.blit(self.font.render(str(self.money), True, (255,255,255)), (111,38))
			self.screen.blit(self.gemPlaceholder, (10,80))

			# Gems
			if self.gems["earth"]:
				self.screen.blit(self.gemSprites["earth"][int(self.gemFrame)], (41,93))
			else:
				self.screen.blit(self.noGem, (41,93))
			if self.gems["fire"]:
				self.screen.blit(self.gemSprites["fire"][int(self.gemFrame)], (91,93))
			else:
				self.screen.blit(self.noGem, (91,93))
			if self.gems["water"]:
				self.screen.blit(self.gemSprites["water"][int(self.gemFrame)], (141,93))
			else:
				self.screen.blit(self.noGem, (141,93))

			# Add to gem frames
			self.gemFrame += .1
			if self.gemFrame >= 3:
				self.gemFrame = 0

			if fighting:
				if self.inventoryRect.collidepoint(pos) and click and not self.settingsOn and not self.mapViewOn:
					self.inventoryOn = True
				elif self.settingsRect.collidepoint(pos) and click and not self.inventoryOn and not self.mapViewOn:
					self.settingsOn = True
				elif self.mapViewRect.collidepoint(pos) and click and not self.settingsOn and not self.inventoryOn:
					self.mapViewOn = True

				# Check for button presses
				if self.inventoryOn and not self.settingsOn and not self.mapViewOn:
					self.player.canMove = False
					self.inventoryDisplay(click)
				if self.settingsOn and not self.inventoryOn and not self.mapViewOn:
					self.player.canMove = False
					self.settingsDisplay(click)
				if self.mapViewOn and not self.inventoryOn and not self.settingsOn:
					self.player.canMove = False
					self.mapViewDisplay(click)

			else:
				# After all the 
				if self.gems["earth"] and self.gems["fire"] and self.gems["water"]:
					if not self.allGemsCollectedMsg:
						message.botMessage("You have all the gems! Visit the temple!", False)
						display.flip()
						time.delay(1300)
						self.allGemsCollectedMsg = True
