# story.py
# Paul Krishnamurthy 2015
# Story line class

# The Last Element
# ICS3U Final Project

from pygame import *
from Game.const import *

class Story:
	""" Story line class """

	def __init__(self, message, treasure, player, screen, fade, maps, sound):
		self.screen = screen
		self.message = message
		self.treasure = treasure
		self.player = player
		self.fade = fade
		self.maps = maps
		self.sound = sound

		self.mainWorldMsgFinished = False

		# Main World Shop
		self.mainWorldShopDialogue = False
		self.mainWorldShopVisits = 0
		self.mainWorldShopSpoken = False	

		# Scene intro messages
		self.waterWorldMsgFinished = False
		self.fireWorldMsgFinished = False
		self.surpriseTempleMsgFinished = False
		self.waterWorldBossMsgFinished = False
		self.churchMsgFinished = False
		self.finalTempleMsgFinished = False

		# Flag to see if game is over (player won)
		self.gameWon = False

		# Ultimate shop
		# -----------------------------------

		# Speed boots
		self.speedBoots = transform.scale(image.load("resources/graphics/items/speedBoots.png"), (70,70))

		# Earth gem animation
		self.earthGemSprites = [transform.scale2x(image.load('resources/graphics/items/gems/eGem/eGem%s.png'%str(i))).convert_alpha() for i in range(4)]
		self.earthGemImage = self.earthGemSprites[0]
		self.earthGemFrame = 0

		# Health Potion
		self.healthPotion = transform.scale(image.load("resources/graphics/items/healthPotion.png"), (70,70))
		# Buy prayer
		self.newPrayer = transform.scale(image.load("resources/graphics/items/newPrayer.png"), (100,100))
		# Amount of prayers
		self.prayers = 7

		# List of all available items (name -> description -> position -> cost -> rect)
		self.availableItems = {
			"speedBoots" : [["These are the boots of Hermes.", "Legend says they increase your speed."], (156,135), 30, Rect(153,133,70,70)],
			"earthGem" : [["Some sort of shining gem.", "It seems useless..."], (876,270), 200, Rect(864,262,self.earthGemImage.get_width()*2,self.earthGemImage.get_height()*2)],
			"healthPotion" : [["Potion to increase your health by 20."], (509,419), 50, Rect(509,419,70,70)],
			"newPrayer" : [["New prayer to use at the church.", "You have %s prayers."%str(self.prayers)], (132,336), 100, Rect(132,336,100,100)],
		}
		# Reuturn rect
		self.shopReturn = Rect(833,508,300,300)

		# -----------------------------------

		# Keyboard actions
		self.spaceReady = False
		self.returnReady = False
		self.pReady = False

		self.portals = {
			"water" : transform.scale(image.load("resources/graphics/misc/waterPortal.png").convert_alpha(), (70,72)),
			"fire" : transform.scale(image.load("resources/graphics/misc/firePortal.png").convert_alpha(), (70,72)),
			"earth" : transform.scale(image.load("resources/graphics/misc/earthPortal.png").convert_alpha(), (70,72))
		}
		# Degrees for portal rotation
		self.degrees = 0

		# Water fountain
		self.fountainSprites = [image.load("resources/graphics/misc/fountain/%s.png"%str(i)).convert_alpha() for i in range(4)]
		self.fountainFrame = 0
		self.fountainImage = self.fountainSprites[0]

		# Waterfall
		self.waterWorldSprites = [image.load("resources/graphics/map/waterWorldAnimation/%s.png"%str(i)).convert() for i in range(5)]
		self.waterWorldFrame = 0
		self.waterWorldImage = self.waterWorldSprites[0]

		# Temple Fire
		self.templeFireSprites = [image.load("resources/graphics/map/templeFire/%s.png"%str(i)).convert_alpha() for i in range(5)]
		self.templeFireFrame = 0
		self.templeFireImage = self.templeFireSprites[0]

		self.onlyOnce = True


	def intro(self, next):
		""" Introduction """

		# Only do the narration scene once
		if not self.mainWorldMsgFinished:
			self.message.narration(["Welcome Sylon!",
									"The people of Oslax need your help...",
									"Restore the land by collecting the 3 elemental gems...",
									"Explore the land and prepare to face what lies ahead...",
									"Go and find the the enterances to new worlds!",
									"But first, explore this building..."], next, "top")
			if self.message.done:
				self.mainWorldMsgFinished = True
				if not mac:
					mixer.music.fadeout(500)
					mixer.music.load(self.sound.getMusic("mainWorldTheme"))
					mixer.music.play(loops=-1)
				self.message.reset()


	def mainWorldShop(self, next):
		""" Main World Shop """

		def addItem(item):
			""" Adds item from shop keeper to inventory """
			self.treasure.collectedItems.add(self.treasure.items[item][0])

		keys = key.get_pressed()
		start, done = False, False

		# Proper way to get keypresses
		# Enter pressed
		if keys[K_RETURN] and self.returnReady:
			done = True
			self.returnReady = False
		if not keys[K_RETURN]:
			self.returnReady = True
		# Space pressed
		if keys[K_SPACE] and self.spaceReady:
			start = True
			self.spaceReady = False
		if not keys[K_SPACE]:
			self.spaceReady = True

		# Area to talk to show owner
		shopDude = Rect(471,82,100,150)

		# Check if player visited new time
		tmp = self.mainWorldShopVisits
		if shopDude.collidepoint((self.player.x, self.player.y)) and start:
			self.mainWorldShopDialogue = True
			self.mainWorldShopVisits += 1

		# Only do the main narration scene once
		if self.mainWorldShopDialogue and not self.mainWorldShopSpoken:
			self.message.narration(["Welcome stranger!",
									"Its been a while since someone has visited my shop!",
									"Sadly, I have some bad news...",
									"I will be closing the shop soon...",
									"So in return for all of your gold coins,",
									"I have placed some useful items in your inventory."
									], next, "bottom")
			if self.message.done:
				self.mainWorldShopDialogue = False
				self.mainWorldShopSpoken = True
				self.treasure.money = 0
				self.message.reset()
				addItem("sword")
				addItem("boat")

		# If the main narration scene is over
		# if self.mainWorldShopSpoken and self.mainWorldShopDialogue:
		# 	self.message.narration(["We already spoke...", 
		# 							"What do you want now??"], next, "bottom")
		# 	# Reset message
		# 	if self.message.done and tmp != self.mainWorldShopVisits:
		# 		self.message.reset()


	def temple(self, templeName):
		""" Water Temple Portal Room """

		# Add to degrees (max 360)
		self.degrees += 1
		if self.degrees > 360:
			self.degrees = 0

		def centerRotate(image, rect, angle):
			""" Image roatation based on center point (from pygame docs)"""
			rot_image = transform.rotate(image, angle)
			rot_rect = rot_image.get_rect(center=rect.center)
			rot_rect[0] += 524
			rot_rect[1] += 85
			return rot_image, rot_rect

		# Render rotated image
		image, pos = centerRotate(self.portals[templeName], self.portals[templeName].get_rect(), self.degrees)
		self.screen.blit(image, pos)


	def waterWorldEnter(self):
		""" Entrance to the water world """
		# Water fountain animation
		self.screen.blit(self.fountainImage, (120,300))
		self.screen.blit(self.fountainImage, (874,300))
		self.fountainFrame += .2
		if self.fountainFrame > 4:
			self.fountainFrame = 0
		self.fountainImage = self.fountainSprites[int(self.fountainFrame)]


	def waterWorld(self, next):
		"Main water world"
		# Animate water falls
		self.screen.blit(self.waterWorldImage, self.player.mapCoords["waterWorld"])
		self.waterWorldFrame += .1
		if self.waterWorldFrame > 5:
			self.waterWorldFrame = 0
		self.waterWorldImage = self.waterWorldSprites[int(self.waterWorldFrame)]

		# Only do the narration scene once
		if not self.waterWorldMsgFinished:
			self.message.narration(["It looks like you found the hidden world of Auquarelle", 
									"It is said that the rare aqua gem can be found here...",
									"Beware of what lies behind each door..."
									], next, "top")
			if self.message.done:
				self.waterWorldMsgFinished = True
				self.message.reset()


	def waterWorldBoss(self, next, fight) :
		""" Water world boss scene """

		# Once the player enter this room, they cannot run away from the boss until they die or kill Broth

		# Narration scene once
		if not self.waterWorldBossMsgFinished:
			self.message.narration(["Well done!", "You defeated Broth, beast of Auquarelle!"], next, "top")
			if self.message.done:
				self.waterWorldBossMsgFinished = True
				self.message.reset()

		# Start enemy battle if the player does not have the water gem
		if not self.treasure.gems["water"]:
			fight.start("broth")

	def fireWorld(self, next):
		""" Main fire world """
		# Animated fire
		self.screen.blit(self.templeFireImage, (456,252))
		self.screen.blit(self.templeFireImage, (584,252))
		self.templeFireFrame += .2
		if self.templeFireFrame > 5:
			self.templeFireFrame = 0
		self.templeFireImage = self.templeFireSprites[int(self.templeFireFrame)]

		# Only do the narration scene once
		if not self.fireWorldMsgFinished:
			self.message.narration(["Welcome to the Inferno Castle...",
									"It is said that in this small castle lies a rare gem...",
									"Explore its rooms to find it!"
									], next, "top")
			if self.message.done:
				self.fireWorldMsgFinished = True
				self.message.reset()


	def surpriseTemple(self, next):
		""" Main surprise temple """

		# Only do the narration scene once
		if not self.surpriseTempleMsgFinished:
			self.message.narration(["Welcome to the Blackbeard's castle...",
									"It is said that he hid all his treasures in this castle...",
									"But amongst his treasures lie traps as well...",
									"Beware what chests you open.."
									], next, "top")
			if self.message.done:
				self.surpriseTempleMsgFinished = True
				self.message.reset()


	def church(self, next):
		""" Church """

		keys = key.get_pressed()

		if Rect(self.player.x,self.player.y,32,42).colliderect(Rect(self.player.mapCoords["church"][0]+471,self.player.mapCoords["church"][1]+303,130,80)):
			self.message.botMessage("Press [p] to pray and restore your health.", False)
			# Check if [p] is pressed
			if keys[K_p] and self.pReady:
				# Check the number of prayers left
				if self.prayers > 0:
					# Restore health to 100% if health is less than 95
					if self.treasure.health == 100:
						self.message.botMessage("You have full health already.", False)
						self.treasure.render(self.screen, True, False, False, self.message)
						self.player.render()
						display.flip()
						time.delay(1300)
						# Lower prayer count
						self.prayers -= 1
					else:
						# Prayer
						self.treasure.health = 100
						self.message.botMessage("You have %s prayers left."%str(self.prayers-1), False)
						self.treasure.render(self.screen, True, False, False, self.message)
						self.player.render()
						display.flip()
						time.delay(1300)
				else:
					# No prayers left
					self.message.botMessage("You have used all 7 prayers.", False)
					self.treasure.render(self.screen, True, False, False, self.message)
					self.player.render()
					display.flip()
					time.delay(1300)

			# Keypress actions
				self.pReady = False
			if not keys[K_p]:
				self.pReady = True

		if not self.churchMsgFinished:
			self.message.narration(["Welcome to the Grand Church of Oslax!",
									"Approach the end of the church to pray for health",
									"You may pray %s times in total."%str(self.prayers)
									], next, "top")
			if self.message.done:
				self.churchMsgFinished = True
				self.message.reset()


	def finalTemple(self, next):
		""" Final temple to place all gems """

		# Only do the narration scene once
		if not self.finalTempleMsgFinished:
			# If the player has collected all the gems
			if self.treasure.gems["earth"] and self.treasure.gems["water"] and self.treasure.gems["fire"]:
				self.message.narration(["Well done Sylon!",
										"You have collected all the gems and restored our land!",
										"The people of Oslax thank you for your bravery!"
										], next, "top")
				if self.message.done:
					self.gameWon = True
					self.finalTempleMsgFinished = True
					self.message.reset()
			else:
				self.message.topMessage("Come back when you have collected all 3 gems!", False)


	def ultimateShop(self, click):
		""" Ultimate shop to buy items """
		pos = mouse.get_pos()

		# Update number of prayers
		self.availableItems["newPrayer"][0][1] = "You have %s prayers."%str(self.prayers)

		# def locate2d(element):
		# 	""" Returns position of element in list """
		# 	pos = 0
		# 	for lst in range(len(self.availableItems)):
		# 		if self.availableItems[lst][0] == element:
		# 			pos = lst
		# 	return pos

		def msg(text):
			""" Render message """
			self.screen.blit(transform.scale(self.message.background, (600,150)), (259,30))
			self.screen.blit(self.message.font.render(text, True, (0,0,0)), (275,59))
			self.treasure.render(True, False, False, False, self.message)
			# Render and pause
			display.flip()
			time.wait(1300)

		# Blit background
		self.screen.blit(transform.scale(self.message.background, (600,150)), (259,30))

		# Loop through the dictionary and draw the items
		for key,val in self.availableItems.items():
			if key == "speedBoots":
				self.screen.blit(self.speedBoots, val[1])

			if key == "earthGem":
				# Animate gem shine
				self.screen.blit(self.earthGemImage, val[1])
				self.earthGemFrame += .2
				if self.earthGemFrame >= 3:
					self.earthGemFrame = 0
				self.earthGemImage = self.earthGemSprites[int(self.earthGemFrame)]

			if key == "healthPotion":
				self.screen.blit(self.healthPotion, (val[1]))

			if key == "newPrayer":
				self.screen.blit(self.newPrayer, (val[1]))

		# General description
		# Loop through items
		for item in [
			["speedBoots", Rect(153,133,70,70)], 
			["earthGem", Rect(864,262,self.earthGemImage.get_width()*2,self.earthGemImage.get_height()*2)],
			["healthPotion", Rect(509,419,70,70)],
			["newPrayer", Rect(132,336,100,100)]
		]:
			if not item[1].collidepoint(pos):
				self.screen.blit(transform.scale(self.message.background, (600,150)), (259,30))
				self.screen.blit(self.message.font.render("Hover over item for its description.", True, (0,0,0)), (275,59))
				self.screen.blit(self.message.font.render("Click on it to buy it.", True, (0,0,0)), (275,109))

			else:
				if not item[0] in self.availableItems:
					self.screen.blit(transform.scale(self.message.background, (600,150)), (259,30))
					self.screen.blit(self.message.font.render("Hover over item for its description.", True, (0,0,0)), (275,59))
					self.screen.blit(self.message.font.render("Click on it to buy it.", True, (0,0,0)), (275,109))

		# Speed boots
		if "speedBoots" in self.availableItems:
			if self.availableItems["speedBoots"][3].collidepoint(pos):
				# Word wrap text
				self.screen.blit(transform.scale(self.message.background, (600,150)), (259,30))
				self.screen.blit(self.message.font.render(self.availableItems["speedBoots"][0][0], True, (0,0,0)), (275,59))
				self.screen.blit(self.message.font.render(self.availableItems["speedBoots"][0][1], True, (0,0,0)), (275,109))
				self.screen.blit(self.message.font.render("$ %s"%str(self.availableItems["speedBoots"][2]), True, (255,255,255)), (515,532))

				if click:
					if self.treasure.money >= self.availableItems["speedBoots"][2]:
						# Add item to inventory
						self.treasure.collectedItems.add("speedBoots")
						# Increase the player speed in all maps
						for key,val in self.player.speeds.items():
							self.player.speeds[key] += .5
						# Subtract the money
						self.treasure.money -= self.availableItems["speedBoots"][2]
						# Remove item from dictionary
						self.availableItems.pop("speedBoots", None)
						# Notification
						msg("You obtained the boots of Hermes!")
					else:
						msg("You do not have enough coins to buy this!")

		# Earth gem
		if "earthGem" in self.availableItems:
			if self.availableItems["earthGem"][3].collidepoint(pos):
				self.screen.blit(transform.scale(self.message.background, (600,150)), (259,30))
				self.screen.blit(self.message.font.render(self.availableItems["earthGem"][0][0], True, (0,0,0)), (275,59))
				self.screen.blit(self.message.font.render(self.availableItems["earthGem"][0][1], True, (0,0,0)), (275,109))
				self.screen.blit(self.message.font.render("$ %s"%str(self.availableItems["earthGem"][2]), True, (255,255,255)), (515,532))

				if click:
					if self.treasure.money >= self.availableItems["earthGem"][2]:
						# Add gem to collected gems
						self.treasure.gems["earth"] = True
						# Subtract money
						self.treasure.money -= self.availableItems["earthGem"][2]
						# Remove item from dictionary
						self.availableItems.pop("earthGem", None)
						# Notification
						msg("You obtained the Earth Gem!")
					else:
						msg("You do not have enough coins to buy this!")

		if self.availableItems["healthPotion"][3].collidepoint(pos):
			self.screen.blit(transform.scale(self.message.background, (600,150)), (259,30))
			self.screen.blit(self.message.font.render(self.availableItems["healthPotion"][0][0], True, (0,0,0)), (275,59))
			self.screen.blit(self.message.font.render("$ %s"%str(self.availableItems["healthPotion"][2]), True, (255,255,255)), (515,532))

			if click:
				if self.treasure.money >= self.availableItems["healthPotion"][2]:
					# Add 20 to player's health if they are not at full health
					if self.treasure.health < 100:
						self.treasure.health = min(self.treasure.health+20, 100)
						# Subtract money
						self.treasure.money -= self.availableItems["healthPotion"][2]
						# Notification
						msg("Health increased by 20!")
					else:
						msg("You are already at max health!")
				else:
					msg("You do not have enough coins to buy this!")

		if self.availableItems["newPrayer"][3].collidepoint(pos):
			self.screen.blit(transform.scale(self.message.background, (600,150)), (259,30))
			self.screen.blit(self.message.font.render(self.availableItems["newPrayer"][0][0], True, (0,0,0)), (275,59))
			self.screen.blit(self.message.font.render(self.availableItems["newPrayer"][0][1], True, (0,0,0)), (275,109))
			self.screen.blit(self.message.font.render("$ %s"%str(self.availableItems["newPrayer"][2]), True, (255,255,255)), (515,532))

			if click:
				if self.treasure.money >= self.availableItems["newPrayer"][2]:
					# Add gem to collected gems
					self.prayers += 1
					# Subtract money
					self.treasure.money -= self.availableItems["newPrayer"][2]
					# Notification
					msg("Prayer added. Use it at the church!")
				else:
					msg("You do not have enough coins to buy this!")


		if self.shopReturn.collidepoint(pos) and click:
			# Fade into main world
			self.fade.fadeDark(self.maps.allScenes["mainWorld"][0], self.screen, self.player.mapCoords["mainWorld"])
			# Create new scene
			self.maps.newScene("mainWorld")
			# Set player coordinates
			self.player.x = self.player.mapx+1293
			self.player.y = self.player.mapy+1044
			# Reset fade
			self.fade.reset()
			# Change music

			if not mac:
				mixer.music.fadeout(500)
				mixer.music.load(self.sound.getMusic("mainWorldTheme"))
				mixer.music.play(loops=-1)
