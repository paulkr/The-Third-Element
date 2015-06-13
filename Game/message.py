# message.py
# Paul Krishnamurthy 2015
# Class to display messages

# The Last Element
# ICS3U Final Project

from pygame import *

class Message(object):
	""" Display message dialogues """
	
	def __init__(self, screen):
		self.screen = screen
		self.background = image.load("resources/graphics/misc/msgBanner.png").convert_alpha()
		self.optionsBg = transform.scale(image.load("resources/graphics/misc/optionsBox.png").convert_alpha(),(200,150))
		self.select = transform.scale(image.load("resources/graphics/misc/choose.png").convert_alpha(),(70,12))
		self.font = font.Font("resources/fonts/Cardinal.ttf", 40)
		self.enterFont = font.Font("resources/fonts/Cardinal.ttf", 20)
		self.black = (0,0,0)
		self.showing = True
		self.enemyStatsShowing = True
		# Current sentance index for narration
		self.sent = 0
		self.done = False

	def narration(self, story, next, location):
		""" Takes list of text as an argument and displays the text """
		length = len(story)
		# If user presses enter, change text or hide message box
		if next:
			if self.sent+1 != length:
				self.sent += 1
			else:
				self.showing = False
				self.done = True
				self.sent = 0
		# Render current sentence
		self.render(story[self.sent], location, length!=1)

	def enemyStats(self, l1, l2, done):
		if self.enemyStatsShowing:
			self.screen.blit(self.background, (130,430))
			self.screen.blit(self.font.render(l1, True, self.black), (160,450))
			self.screen.blit(self.font.render(l2, True, self.black), (425,507))
			self.screen.blit(self.enterFont.render("[Enter]", True, self.black), (860,550))
		if done:
			self.enemyStatsShowing = False

	def topMessage(self, text, enterShow):
		""" Display message on top of self.screen """
		self.screen.blit(self.background, (130,30))
		self.screen.blit(self.font.render(text, True, self.black), (160,50))
		if enterShow:
			self.screen.blit(self.enterFont.render("[Enter]", True, self.black), (860,150))

	def botMessage(self, text, enterShow):
		""" Display message on bottom of self.screen """
		self.screen.blit(self.background, (130,430))
		self.screen.blit(self.font.render(text, True, self.black), (160,450))
		if enterShow:
			self.screen.blit(self.enterFont.render("[Enter]", True, self.black), (860,550))

	def quickMessage(self, text):
		""" Quick message display """
		self.screen.blit(self.background, (50,430))
		self.screen.blit(self.font.render(text, True, self.black), (75,483))

	def attackConfirm(self, click):
		""" Checks if player wants to run, attack or use item """
		# Blit the background and options
		self.screen.blit(self.background, (50,430))
		self.screen.blit(self.optionsBg, (867,429))
		self.screen.blit(self.font.render("Attack", True, self.black), (945,438))
		self.screen.blit(self.font.render("[Stats]", True, self.black), (945,483))
		self.screen.blit(self.font.render("Run", True, self.black), (945,528))
		pos = mouse.get_pos()
		# Check action selected and return it
		if Rect(945,438,100,50).collidepoint(pos):
			if click:
				return "attack"
			self.screen.blit(self.select, (875,448))
		elif Rect(945,483,100,50).collidepoint(pos):
			if click:
				return "stats"
			self.screen.blit(self.select, (875,498))
		elif Rect(945,528,90,55).collidepoint(pos):
			if click:
				return "run"
			self.screen.blit(self.select, (875,544))

	def reset(self):
		""" Reset variables """
		self.showing = True
		self.enemyStatsShowing = True
		self.sent = 0
		self.done = False

	def render(self, text, location, enterShow):
		""" Display one message at a time """
		if self.showing:
			# Render message based on location
			if location == "top":
				self.topMessage(text, enterShow)
			else:
				self.botMessage(text, enterShow)
