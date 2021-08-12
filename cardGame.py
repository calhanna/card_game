import pygame

WIDTH, HEIGHT = 800, 600

class Card:
	def __init__(self, num, suit, center):
		""" 
			Basic Card Class.

			Arguments:
				- num: a string containing a number or letter
				- suit: a string containing the suit (capitalised)
				- center: position tuple 
		"""
		self.num = num
		self.suit = suit
		self.revealed = False

		image_direc = 'images/cards/card' + suit + num + '.png'
		self.image = pygame.image.load(image_direc)
		self.image = pygame.transform.scale(self.image, (70, 95))

		self.rect = self.image.get_rect()
		self.rect.center = center
		self.old_pos = center

class Pile:
	def __init__(self, x):
		self.rect = pygame.Rect(x, 200, 80, HEIGHT-200)
		self.cards = []

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

cardBack = pygame.image.load('images/cards/cardBack.png')
cardBack = pygame.transform.scale(cardBack, (70,95))

piles = []

held_cards = []

x = 50
for i in range(7):
	pile = Pile(x)
	y = 200
	for c in range(i + 1):
		pile.cards.append(Card('A', 'Spades', (x + 40, y)))
		y += 95/2
	pile.cards[-1].revealed = True
	piles.append(pile)
	x += 100

def draw():
	screen.fill((0,100,0))

	for pile in piles:
		for card in pile.cards:
			if card.revealed:
				screen.blit(card.image, card.rect)
			else:
				screen.blit(cardBack, card.rect)

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
							for card2 in pile.cards:
								if pile.cards.index(card2) >= pile.cards.index(card):
									held_cards.append(card2)

		if event.type == pygame.MOUSEBUTTONUP and len(held_cards) > 0:
			held_card = held_cards[0]
			if event.button == pygame.BUTTON_LEFT and held_card != None:
				collision = False
				for pile in piles:
					if pile.rect.collidepoint(event.pos) and len(pile.cards) > 0:
						for home_pile in piles:
							for card in held_cards:
								if card in home_pile.cards: 
									home_pile.cards.remove(card)
								break
						
						if held_card != pile.cards[-1]:
							held_card.rect.center = (pile.cards[-1].rect.center[0], pile.cards[-1].rect.center[1] + 95/2)
							held_card.old_pos = held_card.rect.center

							for card in held_cards:
								pile.cards.append(card)

							held_cards.remove(held_card)
							collision = True
				if not collision:
					held_card.rect.center = held_card.old_pos
					held_cards.remove(held_card)

				for card in held_cards:
					card.rect.center = (held_card.rect.center[0], held_card.rect.y + ((held_cards.index(card)+2) * 95/2))
					held_cards.remove(card)

	if done: break

	if len(held_cards) > 0:
		held_cards[0].rect.center = pygame.mouse.get_pos()
		for card in held_cards:
			if card != held_cards[0]:
				card.rect.center = (held_cards[0].rect.center[0], held_cards[0].rect.y + ((held_cards.index(card)+1) * 95/2))

	draw()

	clock.tick(60)