# fight.py
# Paul Krishnamurthy 2015
# Main fighting class

# The Third Element
# ICS3U Final Project

from pygame import *
from random import randint, choice

from Game.enemy import Enemy
from Game.const import *

class Fight:
	""" Main fight class """
	
	def __init__(self, screen, player, sound, message, treasure):
		self.screen = screen
		self.player = player
		self.sound = sound
		self.message = message
		self.treasure = treasure
		self.enterReady = False
		self.enemyStatsShowing = False
		self.font = font.SysFont("Arial", 25)
		self.font.set_bold(True)
		# Backgrounds
		self.backgrounds = {
			"mainWorld" : transform.scale(image.load("resources/graphics/map/backgrounds/mainWorldFight.png").convert(),(1086,600)),
			"mainWorldSea" : transform.scale(image.load("resources/graphics/map/backgrounds/mainWorldWaterFight.png").convert(),(1086,600)),
			"waterWorldRoom1" : transform.scale(image.load("resources/graphics/map/backgrounds/waterWorldFight.png").convert(),(1086,600)),
			"waterWorldRoom2" : transform.scale(image.load("resources/graphics/map/backgrounds/waterWorldFight.png").convert(),(1086,600)),
			"waterWorldRoom3" : transform.scale(image.load("resources/graphics/map/backgrounds/waterWorldFight.png").convert(),(1086,600)),
			"waterWorldRoom4" : transform.scale(image.load("resources/graphics/map/backgrounds/waterWorldFight.png").convert(),(1086,600)),
			"waterWorldBoss" : transform.scale(image.load("resources/graphics/map/backgrounds/waterWorldFight.png").convert(),(1086,600)),
			"fireWorldRoom1" : transform.scale(image.load("resources/graphics/map/backgrounds/fireWorldFight.png").convert(),(1086,600)),
			"fireWorldRoom2" : transform.scale(image.load("resources/graphics/map/backgrounds/fireWorldFight.png").convert(),(1086,600)),
			"surpriseTemple" : transform.scale(image.load("resources/graphics/map/backgrounds/surpriseTempleFight.png").convert(),(1086,600))
		}
		# Player sprites
		self.pSprites  = [transform.scale2x(image.load("resources/graphics/player/dMove/%s.gif"%str(i)).convert_alpha()) for i in range(4)]
		self.pAttackSprites = [transform.scale2x(image.load("resources/graphics/player/attack/%s.png"%str(i)).convert_alpha()) for i in range(3)]
		self.pAttackWeapon = transform.scale2x(image.load("resources/graphics/player/attack/weapon.png").convert_alpha())
		self.fighting = False

		self.enemy = Enemy()
		self.eHealthBar = transform.scale2x(image.load("resources/graphics/misc/healthBarPlaceholder.png").convert())
		self.healthPercent = []
		self.healthBar = self.treasure.healthBar

		# Create enemy based on player's location
		if self.player.inBoat:
			self.curEnemy = self.newEnemy("water")
		else:
			self.curEnemy = self.newEnemy("earth")

		# Player and enemy animation frames
		self.eFrame = 0
		self.pFrame = 0
		# Possible rewards for victory
		self.possibleRewards = ["heart", "money", "joy"]
		# Enemy health
		self.enemyHealth = 0
		# If player runs
		self.fled = False
		# Attack powers
		self.power = 1
		# End fight when death occurs
		self.killFight = False
		# Keep track of number of attacks
		self.attacked = False
		# Keep track of player's life
		self.playerDied = False

	def finish(self, fade):
		self.fighting = False
		self.killFight = False
		self.attacked = False
		self.fled = False
		self.eFrame = 0
		self.turn = 0
		fade.reset()
		self.message.reset()

	def start(self, custom=None):
		# Custom enemy
		if custom != None:
			self.enemyHealth = self.enemy.customEnemies[custom][4]
			self.maxEnemyHealth = 50
			# Create subsurfaces of health bar
			try:
				div = self.healthBar.get_width()/self.enemyHealth
				self.healthPercent = []
				for i in range(self.enemyHealth):
					self.healthPercent.append(self.healthBar.subsurface(0,0,div*(i+1),self.healthBar.get_height()))
				# Create new enemy
			except: pass
			self.curEnemy = self.enemy.randomEnemy(custom)
			self.fighting = True

		else:
			# Assign random health to enemy
			self.enemyHealth = randint(15,20)
			# Create subsurfaces of health bar
			div = self.healthBar.get_width()/self.enemyHealth
			self.healthPercent = []
			for i in range(self.enemyHealth):
				self.healthPercent.append(self.healthBar.subsurface(0,0,div*(i+1),self.healthBar.get_height()))
			# Remember maximum enemy health
			self.maxEnemyHealth = self.enemyHealth
			self.fighting = True
			self.enemyStatsShowing = True
			#self.sound.play("mainWorldFight", True)
			if self.player.inBoat:
				self.curEnemy = self.newEnemy("water")
			else:
				self.curEnemy = self.newEnemy("earth")

	def newEnemy(self, area, custom=None):
		""" Creates new enemy """
		# Return chosen or random enemy
		if custom != None:
			return self.enemy.randomEnemy(area, custom)
		else:
			return self.enemy.randomEnemy(area)

	def enemyAttack(self, attack):
		""" Enemy attacking player """
		self.treasure.health -= attack

	def playerAttack(self, attack, scene, custom=None):
		""" Player attacking enemy """
		if custom != None:
			self.enemy.customEnemies[custom][4] -= attack
		else:
			self.enemyHealth -= attack

	def checkDeath(self):
		""" Check player and enemy health """
		if self.treasure.health <= 0:
			return "player"
		if self.enemyHealth <= 0:
			return "enemy"
		return "alive"

	# PROPER IMPORTS TO CLASS
	def render(self, scene, fade, next, maps, click, custom=None):
		""" Render visuals """
		keys = key.get_pressed()
		enter = False

		# Set player death flag
		self.player.isAlive = not self.playerDied

		if self.fighting:
			# Fade into fighting background based on location
			if scene == "mainWorldSea":
				fade.fadeDark(self.backgrounds["mainWorldSea"], self.screen, (0,0))
				self.screen.blit(self.backgrounds["mainWorldSea"], (0,0))
			else:
				fade.fadeDark(self.backgrounds[scene], self.screen, (0,0))
				self.screen.blit(self.backgrounds[scene], (0,0))

			# Proper way to check key press once
			if keys[K_RETURN] and self.enterReady:
				enter = True
				self.enterReady = False
			if not keys[K_RETURN]:
				self.enterReady = True

			# Enemy info
			if self.player.inBoat:
				eSprites = self.enemy.waterEnemyData[self.curEnemy[0]][0]
				ePos = self.curEnemy[1]
			else:
				if custom != None:
					eSprites = self.enemy.customEnemies[custom][1]
					ePos = self.enemy.customEnemies[custom][2]
				else:
					eSprites = self.enemy.enemyData[self.curEnemy[0]][0]
					ePos = self.curEnemy[1]


			# Player and enemy images
			eImage = eSprites[int(self.eFrame)]
			pImage =  self.pSprites[int(self.pFrame)]

			# Add to character frames
			self.eFrame += .07
			self.pFrame += .1
			self.eFrame = 0 if self.eFrame >= len(eSprites) else self.eFrame
			self.pFrame = 0 if self.pFrame >= len(self.pSprites) else self.pFrame

			def drawCharacters(shake=False):
				""" Draws characters """
				global eImage 
				# Reset image to first frame during attack animation
				try:
					if shake:
						eImage = eSprites[0]
					else:
						eImage = eSprites[int(self.eFrame)]
				except: pass
				# Blit the artwork :)
				display.update(self.screen.blit(eImage, ePos))
				display.update(self.screen.blit(pImage, (805,255)))
				# Get the positions from the enemy class thingy
				if custom != None:
					self.screen.blit(self.eHealthBar, self.enemy.customEnemies[custom][3])
				else:
					self.screen.blit(self.eHealthBar, self.curEnemy[3])
				# Draw the sliced up health bar
				if self.enemyHealth > 0:
					if custom != None:
						self.screen.blit(self.healthPercent[self.enemyHealth-1], (self.enemy.customEnemies[custom][3][0]+4, self.enemy.customEnemies[custom][3][1]+4))
						# Draw enemy health
						self.screen.blit(self.font.render("%d / %d"%
							(self.enemyHealth, self.maxEnemyHealth), True, (255,255,255)), (self.enemy.customEnemies[custom][3][0]+120, self.enemy.customEnemies[custom][3][1]-8))

					else:
						self.screen.blit(self.healthPercent[self.enemyHealth-1], (self.curEnemy[3][0]+4, self.curEnemy[3][1]+4))
						# Draw enemy health
						self.screen.blit(self.font.render("%d / %d"%
							(self.enemyHealth, self.maxEnemyHealth), True, (255,255,255)), (self.curEnemy[3][0]+120, self.curEnemy[3][1]-8))

			def pause(length):
				""" Pauses screen """
				display.flip()
				time.delay(length)

			# Initial scene rendering
			drawCharacters()
			self.treasure.render(self.screen, True, maps.sceneName=="mainWorld", False, self.message)

			if not self.enemyStatsShowing:
				self.enemyStatsShowing = False
				# Allow player and enemy to perform attack action
				# if "sword" in self.treasure.collectedItems:
				# 	self.power = 5
				# if "flameSword" in self.treasure.collectedItems:
				# 	self.power = 7
				# else:
				# 	print(self.treasure.collectedItems)
				for weapon in self.treasure.weapons:
					if weapon in self.treasure.collectedItems:
						# Set player power to highest possible in collected items
						self.power = max(self.power, self.treasure.items[weapon][5])

				# Check selected action
				if self.message.attackConfirm(click) == "attack" and not self.attacked:
					self.attacked = True
					# Set enemy frame to 0
					self.eImage = eSprites[0]

					# Player action
					if self.checkDeath() == "alive":						
						self.playerAttack(self.power, scene, custom)
					else:
						self.killFight = True

					# Player attack animation
					self.screen.blit(self.backgrounds[scene], (0,0))
					display.update(self.screen.blit(self.pAttackSprites[0], (805,255)))
					time.delay(200)
					self.screen.blit(self.backgrounds[scene], (0,0))
					display.update(self.screen.blit(self.pAttackSprites[1], (805,255)))
					time.delay(200)
					self.screen.blit(self.backgrounds[scene], (0,0))
					display.update(self.screen.blit(self.pAttackSprites[2], (805,255)))

					# Weapon throwing animation
					x = 750
					# Set the boundary
					while x > 200:
						self.screen.blit(self.backgrounds[scene], (0,0))
						self.screen.blit(self.pAttackWeapon, (x,255))
						self.message.attackConfirm(False)
						self.treasure.render(self.screen, True, maps.sceneName=="mainWorld", False, self.message)
						drawCharacters(True)
						display.flip()
						# Move the weapon
						x -= 6
						time.delay(10)

					# Render all other content
					self.message.attackConfirm(False)
					drawCharacters()

					# Enemy attack animation
					x, eBlit = 0, ePos[0]
					end = 0
					# Set the bound
					while end < 40:
						self.screen.blit(self.backgrounds[scene], (0,0))
						drawCharacters()
						self.screen.blit(eSprites[0], (eBlit+x,ePos[1]))
						self.message.attackConfirm(False)
						self.treasure.render(self.screen, True, maps.sceneName=="mainWorld", False, self.message)
						display.flip()
						# Move enemy back and forth by 10 pixels
						x += 10
						end += 1
						if eBlit+x > eBlit+10:
							x = -10
						else:
							x=10
						time.delay(10)

					# Redraw scene
					self.screen.blit(self.backgrounds[scene], (0,0))
					drawCharacters()
					self.message.attackConfirm(False)

					# Explain attack and wait 1 second
					self.message.quickMessage("You attacked with %s!"%str(self.power))
					self.treasure.render(self.screen, True, maps.sceneName=="mainWorld", False, self.message)
					pause(1300)

					# Keep track of deaths
					if self.enemyHealth <= 0:
						self.killFight = True
					if self.treasure.health <= 0:
						self.killFight = True
						self.playerDied = True

					# Enemy action
					if not self.checkDeath() == "enemy":
						# Allow enemy to attack
						if self.fighting:
							attack = randint(0, self.curEnemy[2])
							if attack == 0:
								self.message.quickMessage("Enemy missed!")
							else:
								self.enemyAttack(attack)
								# Check if enemy killed player
								if self.checkDeath() == "player":
									self.killFight = True
									self.playerDied = True
								# Display enemy attack stats
								self.message.quickMessage("Enemy attacked with %s!"%str(self.curEnemy[2]))
							# Render display and wait 1 second
							pause(1300)

					# End the battle
					if self.killFight:
						# Different message if player died or not
						if self.playerDied:
							self.message.quickMessage("You died!")
							pause(1300)
							self.player.isAlive = False
						else:
							self.message.quickMessage("Enemy defeated!")
							pause(1300)
							# Reward player with random prize (money or health)
							if custom == "broth":
								prize = "water gem"
							else:
								prize = randint(10,25)
							# Award the water gem
							if prize == "water gem":
								self.message.quickMessage("You have been rewarded with the water gem!")
								self.treasure.gems["water"] = True
							else:
								if choice(["money", "health"]) == "money":
									self.message.quickMessage("You have been rewarded with %s coins!"%(str(prize)))
									self.treasure.money += prize
								else:
									self.message.quickMessage("You have been rewarded with %s health!"%str(prize))
									self.treasure.health = min(100, self.treasure.health+prize)
							pause(1300)

						self.enemyStatsShowing = False
						# Add fadeout / fadein effect
						self.finish(fade)
						# Fade back to the scene
						if maps.scrollingCamera:
							if scene == "mainWorldSea":
								fade.fadeDark(maps.allScenes["mainWorld"][0], self.screen, (self.player.mapx,self.player.mapy))
							else:
								fade.fadeDark(maps.allScenes[scene][0], self.screen, (self.player.mapx,self.player.mapy))
						else:
							fade.fadeDark(maps.allScenes[scene][0], self.screen, (0,0))
						fade.alpha = 1
						# Reset enemies
						if self.player.inBoat:
							self.curEnemy = self.newEnemy("water")
						else:
							self.curEnemy = self.newEnemy("earth")

				# Keep track of player attack cycles to avoid duplicate attacks
				if not self.message.attackConfirm(click) == "attack": 
					self.attacked = False

				# Display inventory
				if self.message.attackConfirm(click) == "stats":
					self.message.quickMessage("Your attack power is %s"%self.power)
					self.treasure.render(self.screen, True, maps.sceneName=="mainWorld", False, self.message)
					pause(1000)

				# Player flees fight
				if self.message.attackConfirm(click) == "run":
					self.fled = True

				if self.fled:
					# Enemy fights one last time
					if not self.checkDeath() == "enemy":
						attack = randint(0, self.curEnemy[2])
						if attack == 0:
							self.message.quickMessage("Enemy missed!")
						else:
							# Enemy attack sequence
							self.enemyAttack(attack)
							# Player death config
							if self.checkDeath() == "player":
								self.killFight = True
								self.playerDied = True
							self.message.quickMessage("Enemy attacked with %s!"%str(self.curEnemy[2]))
					pause(1300)

					if self.killFight:
						# Different message if player died or not
						if self.playerDied:
							self.message.quickMessage("You died!")
							pause(1300)
							self.player.isAlive = False

					if not self.killFight and not self.playerDied:
						self.treasure.render(self.screen, True, maps.sceneName=="mainWorld", False, self.message)
						self.message.quickMessage("You fled!")
						pause(1300)

						if maps.sceneName == "mainWorld":
							if not mac:
								mixer.music.fadeout(500)
								mixer.music.load(self.sound.getMusic("mainWorldTheme"))
								mixer.music.play(loops=-1)

					# Change screen state and finish fight sequence
					self.enemyStatsShowing = False
					self.finish(fade)

					# Fade back to screen
					if maps.scrollingCamera:
						if scene == "mainWorldSea":
							fade.fadeDark(maps.allScenes["mainWorld"][0], self.screen, (self.player.mapx,self.player.mapy))
						else:
							fade.fadeDark(maps.allScenes[scene][0], self.screen, (self.player.mapx,self.player.mapy))
					else:
						fade.fadeDark(maps.allScenes[scene][0], self.screen, (0,0))
					fade.alpha = 1
					if self.player.inBoat:
						self.curEnemy = self.newEnemy("water")
					else:
						self.curEnemy = self.newEnemy("earth")

				# Render treasure items so player can go through inventory while fighting
				self.treasure.render(self.screen, True, maps.sceneName=="mainWorld", False, self.message)

			# Display random enemy statistics
			else:
				if custom != None:
					self.message.enemyStats("You encountered %s..."%self.enemy.customEnemies[custom][0],
									"with a max attack power of %d!"%self.enemy.customEnemies[custom][-1], enter)
				else:
					self.message.enemyStats("You encountered %s..."%self.curEnemy[0],
										"with a max attack power of %d!"%self.curEnemy[2], enter)
				# Hide enemy stats
				if enter: 
					self.enemyStatsShowing = False

