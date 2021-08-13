# Solitaire.

import pygame, random

WIDTH, HEIGHT = 800, 600

class Card:
	def __init__(self, card, center, home):
		""" 
			Basic Card Class.

			Arguments:
				- num: a string containing a number or letter
				- suit: a string containing the suit (capitalised)
				- center: position tuple 
		"""
		self.revealed = False
		self.home = home
		self.card = card

		if self.card[-1] == 'A':
			self.value = 1
		elif self.card[-1] == 'K':
			self.value = 13
		elif self.card[-1] == 'Q':
			self.value = 12
		elif self.card[-1] == 'J':
			self.value = 11
		elif self.card[-1] == '0':
			self.value = 10
		else:
			self.value = int(self.card[-1])

		image_direc = 'images/cards/card' + card + '.png'
		self.image = pygame.image.load(image_direc)
		self.image = pygame.transform.scale(self.image, (70, 95))

		self.rect = self.image.get_rect()
		self.rect.center = center
		self.old_pos = center

class Pile:
	def __init__(self, x):
		"""
			A class for each of the piles, or bases or whatever with which one plays solitaire
		"""
		self.rect = pygame.Rect(x, 200, 80, 1200)
		self.cards = []

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

cardBack = pygame.image.load('images/cards/cardBack.png')
cardBack = pygame.transform.scale(cardBack, (70,95)) # Card images are too large

def setup():
	global piles, deck, stock, shuffled_deck, foundations, revealed_stock, held_cards, foundation_rects

	piles = []

	#generating deck of cards
	deck = {
		'Hearts': [],
		'Spades': [],
		'Clubs': [],
		'Diamonds': []
	}
	for suit in deck:
		for num in range(13):
			if num < 10:
				if num != 0: 
					deck[suit].append(str(num + 1))
				else:
					deck[suit].append('A')
			else:
				if num == 10: deck[suit].append('J')
				elif num == 11: deck[suit].append('Q')
				elif num == 12: deck[suit].append('K')

	#shuffling deck
	shuffled_deck = []
	for i in range(52):
		shuffled_deck.append(None)

	forbidden = [] # An array of card numbers that have already been used and should not be overwritten
	for suit in deck:
		for card in deck[suit]:
			card_name = suit + card
			deck_index = random.randint(0, len(shuffled_deck))
			while deck_index in forbidden:
				deck_index = random.randint(0, len(shuffled_deck))
			forbidden.append(deck_index)
			shuffled_deck[deck_index-1] = card_name

	# There was always one remaining 'None', so we replace it here
	for suit in deck:
		for card in deck[suit]:
			if suit + card not in shuffled_deck:
				missing_card = suit + card

	try:
		shuffled_deck[shuffled_deck.index(None)] = missing_card
	except NameError:
		print('No missing cards!')

	held_cards = []	#array that holds the cards that are currently being moved

	# Generating bases
	x = 50
	for i in range(7):
		pile = Pile(x)
		piles.append(pile)
		x += 100

	# Assign cards to piles
	for card in shuffled_deck:
		for pile in piles:
			if len(pile.cards) < piles.index(pile) + 1:
				pile.cards.append(Card(card, (pile.rect.center[0], 200 + ((95/4) * len(pile.cards))), pile))
				break

	# Find cards that arent assigned to piles yet and put them in the stock
	stock = []
	for card in shuffled_deck:
		in_pile = False
		for pile in piles:
			for card2 in pile.cards:
				if card == card2.card:
					in_pile = True
		
		if not in_pile:
			stock.append(card)

	revealed_stock = []

	for pile in piles:
		pile.cards[-1].revealed = True

	foundations = {
		'Hearts': [],
		'Spades': [],
		'Clubs': [],
		'Diamonds': []
	}

	foundation_rects = {
		'Hearts': pygame.Rect(piles[3].rect.x, 20, 70, 95),
		'Spades': pygame.Rect(piles[4].rect.x, 20, 70, 95),
		'Clubs': pygame.Rect(piles[5].rect.x, 20, 70, 95),
		'Diamonds': pygame.Rect(piles[6].rect.x, 20, 70, 95),
	}

setup()

def find_pile(held_cards):
	global stock_image
	if pygame.mouse.get_pos()[1] > 200:
		dest_pile = None
		for pile in piles:
			if pile.rect.move(0,-95/2).collidepoint(pygame.mouse.get_pos()):
				dest_pile = pile
				break

		
		
		home = False
		if dest_pile == None:
			home = True
		else:
			if len(dest_pile.cards) > 0:
				front_card = dest_pile.cards[-1]
				if 'Spades' in front_card.card or 'Clubs' in front_card.card:
					if 'Spades' in held_cards[0].card or 'Clubs' in held_cards[0].card:
						home = True

				elif 'Hearts' in front_card.card or 'Diamonds' in front_card.card:
					if 'Hearts' in held_cards[0].card or 'Diamonds' in held_cards[0].card:
						home = True

				if front_card.value != held_cards[0].value + 1:
					home = True
			elif 'K' not in held_cards[0].card:
				home = True

		if home:
			if held_cards[0].home != 'Stock' and held_cards[0].home not in foundations:
				dest_pile = held_cards[0].home
			elif held_cards[0].home == 'Stock':
				revealed_stock.append(held_cards[0].card)
				held_cards = []
				stock_image = pygame.image.load('images/cards/card' + revealed_stock[-1] + '.png')
				stock_image = pygame.transform.scale(stock_image, (70, 95))
			else:
				foundations[held_cards[0].home].append(held_cards[0])
				held_cards = []

		if len(held_cards) > 0:
			if len(dest_pile.cards) < 1:
				held_cards[0].rect.x, held_cards[0].rect.y = dest_pile.rect.x, 200 - 95/2 
				dest_pile.cards.append(held_cards[0])
				held_cards[0].home = dest_pile
				held_cards.remove(held_cards[0])
			
			for card in held_cards:
				card.rect.center = (dest_pile.cards[-1].rect.center[0], dest_pile.cards[-1].rect.center[1] + 95/4)
				dest_pile.cards.append(card)
				card.home = dest_pile
				held_cards.remove(card)

	else:
		found_foundation = False
		if len(held_cards) == 1:
			for rect in foundation_rects:
				if foundation_rects[rect].collidepoint(pygame.mouse.get_pos()):
					foundation = foundations[rect]
					if rect in held_cards[-1].card:
						if len(foundation) > 0:
							if held_cards[-1].value == foundation[-1].value + 1:
								foundations[rect].append(held_cards[0])
								foundations[rect][-1].home = rect
								held_cards = []
								found_foundation = True
						else:
							if held_cards[-1].card[-1] == 'A':
								foundations[rect].append(held_cards[0])
								foundations[rect][-1].home = rect
								held_cards = []
								found_foundation = True
			if not found_foundation:
				if held_cards[0].home != 'Stock' and held_cards[0].home not in foundations:
					dest_pile = held_cards[0].home # Copypasted logic
					if len(dest_pile.cards) < 1:
						held_cards[0].rect.x, held_cards[0].rect.y = dest_pile.rect.x, 200 - 95/4
						dest_pile.cards.append(held_cards[0])
						held_cards[0].home = dest_pile
						held_cards.remove(held_cards[0])
				
					for card in held_cards:
						card.rect.center = (dest_pile.cards[-1].rect.center[0], dest_pile.cards[-1].rect.center[1] + 95/4)
						dest_pile.cards.append(card)
						card.home = dest_pile
						held_cards.remove(card)
				elif held_cards[0].home == 'Stock':
					revealed_stock.append(held_cards[0].card)
					held_cards = []
					stock_image = pygame.image.load('images/cards/card' + revealed_stock[-1] + '.png')
					stock_image = pygame.transform.scale(stock_image, (70, 95))
				else:
					foundations[held_cards[0].home].append(held_cards[0])
					held_cards = []
		else:
			if held_cards[0].home != 'Stock' and held_cards[0].home not in foundations:
				dest_pile = held_cards[0].home # Copypasted logic
				if len(dest_pile.cards) < 1:
					held_cards[0].rect.x, held_cards[0].rect.y = dest_pile.rect.x, 200 - 95/4
					dest_pile.cards.append(held_cards[0])
					held_cards[0].home = dest_pile
					held_cards.remove(held_cards[0])
			
				for card in held_cards:
					card.rect.center = (dest_pile.cards[-1].rect.center[0], dest_pile.cards[-1].rect.center[1] + 95/4)
					dest_pile.cards.append(card)
					card.home = dest_pile
					held_cards.remove(card)
			elif held_cards[0].home == 'Stock':
				revealed_stock.append(held_cards[0].card)
				held_cards = []
				stock_image = pygame.image.load('images/cards/card' + revealed_stock[-1] + '.png')
				stock_image = pygame.transform.scale(stock_image, (70, 95))
			else:
				foundations[held_cards[0].home].append(held_cards[0])
				held_cards = []
		
	for pile in piles:
		if len(pile.cards) > 0:
			if not pile.cards[-1].revealed:
				pile.cards[-1].revealed = True

	return held_cards

def draw():
	screen.fill((0,100,0))

	if len(stock) > 0:
		screen.blit(cardBack, (piles[0].rect.x,20))

	if len(revealed_stock) > 0:
		screen.blit(stock_image, (piles[0].rect.x + 95, 20))

	for foundation in foundations:
		if len(foundations[foundation]) > 0:
			screen.blit(foundations[foundation][-1].image, foundation_rects[foundation])
		else:
			pygame.draw.rect(screen, (50,150,50), foundation_rects[foundation])

	for pile in piles:
		for card in pile.cards:
			if card.revealed:
				screen.blit(card.image, card.rect)
			else:
				screen.blit(cardBack, card.rect)
	
	for card in held_cards:
		screen.blit(card.image, card.rect)

	pygame.display.flip()

done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

			break

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == pygame.BUTTON_LEFT:
				for pile in piles:
					for card in pile.cards:
						if card.rect.collidepoint(event.pos) and card.revealed:
							held_cards.append(card)
							for card2 in pile.cards:
								if card.rect.y < card2.rect.y:
									held_cards.append(card2)
							break

					for card in held_cards:
						if card in pile.cards:
							pile.cards.remove(card)
				
				rect = pygame.Rect(100 - 70/2, 20, 70, 95)
				if rect.collidepoint(pygame.mouse.get_pos()):
					if len(stock) > 0:
						revealed_stock.append(stock[-1])
						stock.pop()
						stock_image = pygame.image.load('images/cards/card' + revealed_stock[-1] + '.png')
						stock_image = pygame.transform.scale(stock_image, (70, 95))
					else:
						for i in range(len(revealed_stock)):
							stock.append(revealed_stock[-1])
							revealed_stock.pop()

				rect = pygame.Rect(piles[0].rect.x + 95, 20, 70, 95)
				if rect.collidepoint(pygame.mouse.get_pos()) and len(revealed_stock) > 0:
					held_cards = [Card(revealed_stock[-1], pygame.mouse.get_pos(), 'Stock')]
					revealed_stock.pop()
					if len(revealed_stock) > 0:
						stock_image = pygame.image.load('images/cards/card' + revealed_stock[-1] + '.png')
						stock_image = pygame.transform.scale(stock_image, (70, 95))

				for rect in foundation_rects:
					if foundation_rects[rect].collidepoint(pygame.mouse.get_pos()):
						held_cards = [foundations[rect][-1]]
						foundations[rect].pop()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				setup()

	if done: break

	if not pygame.mouse.get_pressed()[0] and len(held_cards) > 0:
		held_cards = find_pile(held_cards)

	if len(held_cards) > 0:
		held_cards[0].rect.center = pygame.mouse.get_pos()
		for card in held_cards:
			if card != held_cards[0]:
				card.rect.center = (held_cards[0].rect.center[0], held_cards[0].rect.y + ((held_cards.index(card)+1) * (95/3)))

	draw()

	clock.tick(60)