# fade.py
# Paul Krishnamurthy 2015
# Transitions from scene to scene

# The Third Element
# ICS3U Final Project

from pygame import *
from random import *

class Fade:
	""" Fade from one scene into another """
	
	def __init__(self):
		# Initial alpha value
		self.alpha = 1
		# New surface
		self.alphaSurf = Surface((1086,600))

	def fadeDark(self, surf, screen, coords):
		""" Fade to dark screen """
		while self.alpha != "done":
			self.alphaSurf.set_alpha(self.alpha)
			# Blit the alpha surface
			screen.blit(self.alphaSurf, (0,0))
			# Add to alpha value (3 gives a cooler effect than 1)
			self.alpha += 3

			if self.alpha > 50:
				self.alpha = "done"
			if self.alpha == "done":
				self.fadeLight(surf, screen, coords)

			# Render
			time.wait(10)
			display.flip()
	
	def fadeLight(self, surf, screen, coords):
		""" Fade from dark to scene """
		self.alpha = 255
		while self.alpha != "done":
			screen.blit(surf, coords)
			# Blit the alpha surface
			self.alphaSurf.set_alpha(self.alpha)
			screen.blit(self.alphaSurf, (0,0))
			# Subtract from alpha value
			self.alpha -= 5

			if self.alpha < 1:
				self.alpha = "done"
			if self.alpha == "done":
				screen.blit(surf, coords)

			# Render
			time.wait(10)
			display.flip()

	def reset(self):
		""" Reset """
		self.alpha = 1