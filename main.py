from random import randint
import pygame
from pygame.sprite import spritecollide as sc
import sys

# Velikost okna
SIRINA = 600
VISINA = 400
pygame.init()

class Igralec(pygame.sprite.Sprite):
	""" Razred, ki opisuje enega igralca. Notri so njegove dimenzije, njegova
	barva, katere tipke uporablja za premikanje,...
	"""

	# Metoda __init__ je funkcija, ki se zazene ob kreairanju novega igralca.
	# V njej nastavimo vse osnovne lastnosti igralca
	def __init__(self, up=pygame.K_UP, down=pygame.K_DOWN,
				 left=pygame.K_LEFT, right=pygame.K_RIGHT, ovire=None):
		super().__init__()

		self.ziv=100
		# Shranimo si vse ovire v levelu
		self.ovire = ovire

		# Shranimo vse tipke za kasnejso uporabo
		self.up = up
		self.down = down
		self.left = left
		self.right = right

		# Ustvari sliko igralca, ki je nakljucne barve
		self.image = pygame.Surface((50, 50))
		self.barva=(randint(0, 255), randint(0, 255), randint(0, 255))
		self.image.fill(self.barva)
		self.rect = self.image.get_rect()

		# hitrosti igralca
		self.vx = 0
		self.vy = 0

		# Predpostavimo, da so vse tipke spuscene ob zacetku igre
		self.smeri = {
			self.up: False,
			self.down: False,
			self.right: False,
			self.left: False,
		}
	def narisi_me(self):
		self.image.fill(self.barva)
		font = pygame.font.SysFont("comicsansms", 30)
		text = font.render(str(self.ziv), True, (0,0,0))
		self.image.blit(text, (0,10))

	# Ali Igralec stoji na oviri (Tako vemo, ali lahko skoči)
	def na_oviri(self):
		prejsnje_dno = self.rect.bottom
		if self.rect.bottom >= VISINA:
			# Lahko stoji tudi na dnu ekrana
			return True
		elif self.ovire is None:
			# Če nismo dobili ovir, potem ne more stati na njih
			return False
		else:
			self.rect.y += 1
			rezultat = sc(self, self.ovire, False)
			self.rect.y -= 1
			for ov in rezultat:
				if prejsnje_dno <= ov.rect.top:
					return True

			return False

	# ko uporabnik pritisne ali spusti neko tipko ustrezno popravimo hitrosti
	def oznaci_pritisk(self, smer, status):
		# Najprej si zabeležimo smer premika
		self.smeri[smer] = status

		hitrost = 10

		# Tipka dol ne naredi nič
		if self.smeri[self.down]:
			pass
		# S tipko gor skočimo
		if self.smeri[self.up] and self.na_oviri():
			self.vy = -17

		# če držimo levo ali desno se premikamo levo, ali desno, sicer se ne
		self.vx = 0
		if self.smeri[self.left]:
			self.vx = -hitrost
		if self.smeri[self.right]:
			self.vx = hitrost

	# Vsak frame igre moramo premakniti igralca. To dela metoda update, ki jo
	# klicemo v vsakem prehodu
	def update(self):
		# Najprej poglejmo premik v x smeri
		self.premik(self.vx, 0)

		# Naj se zgodi gravitacija
		self.vy += 1
		# Sedaj porihtajmo še premik v y smeri
		prejsnje_dno = self.rect.bottom
		self.premik(0, self.vy)
		# Če se zabijemo v kakšno oviro se ustavimo
		for ov in sc(self, self.ovire, False):

			if ov.tip==3:
				print("zmagal si")
				sys.exit(0)

			if self.vy > 0 and prejsnje_dno <= ov.rect.top:
				self.rect.bottom = ov.rect.top
				self.vy = 0
			if ov.tip==1:
				self.ziv-=2

		self.narisi_me()
		if self.ziv <= 0:
			self.umri()


	# Pomozna funkcija, ki premakne igralca in poskrbi, da ne gre iz ekrana
	def premik(self, x, y):
		self.rect.x += x
		self.rect.y += y
		self.rect.x = max(self.rect.x, 0)
		self.rect.right = min(self.rect.right, SIRINA)
		if self.rect.bottom > VISINA:
			self.rect.bottom = VISINA
			self.vy = 0

	def umri(self):
		self.ziv=100
		self.rect.left=0
		self.rect.bottom= VISINA
		self.vx=0
		self.vx=0

class Plato(pygame.sprite.Sprite):
	""" Ravna podlaga po kateri lahko igralci skacejo.

	0: navaden Plato (zelen)
	1: nevaren plato (rdeč)
	2: neprehoden plato ()
	3: cilj
	"""

	# Vse kar potrebujemo so položaj (x, y) in dimenzije (w, h)
	def __init__(self, x=100, y=300, w=200, h=10, tip=0):
		super().__init__()
		self.image = pygame.Surface((w, h))
		self.image.fill((0, 255, 0))
		if tip==1:
			self.image.fill((255, 0, 0))
		if tip==3:
			self.image.fill((255, 255, 0))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.tip = tip
# Naredimo nekaj odskočišč za igralce in jih poimenujemo "level"
level = pygame.sprite.Group()
level.add(Plato(10, 10, 10, 10, 3))
level.add(Plato(200, 395, 400, 10, 1))
level.add(Plato(200, 300, 50, 10, 1))

level.add(Plato(250, 300, 50, 10))
level.add(Plato(500, 200, 50, 10))
level.add(Plato(300, 100, 50, 10))
level.add(Plato(10, 100, 100, 10))
# Spodaj dodamo še: level.draw(ekran)

# Ustvarimo dva igralca, vsakega s svojim setom ukaznih tipk
igralec = Igralec(pygame.K_w, pygame.K_s,
				  pygame.K_a, pygame.K_d, ovire=level)
igralec2 = Igralec(ovire=level)
igralec.rect.bottom = VISINA
igralec2.rect.bottom = VISINA

# Oba igralca dodamo v skupino, da ju lazje skupaj risemo in posodabljamo
igra_skupina = pygame.sprite.Group()
igra_skupina.add(igralec)
igra_skupina.add(igralec2)

# Ustvarimo prazno okno definirane sirine in visine
ekran = pygame.display.set_mode([SIRINA, VISINA])
# Ura bo poskrbela, da se bo nasa igra predvajala pri 60 slikah na sekundo
ura = pygame.time.Clock()

# Definiramo spemenljivko s katero bomo spremljali, ali se vedno igramo igro
igramo = True
while igramo:
	# Poskrbimo, da igra tece pri 60 slikah na sekundo
	ura.tick(60)

	# Preverimo vse dogodke, ki so se zgodili v tem 1/60s
	# To so vsi pritiski tipk na tipkovnici in miski
	for dogodek in pygame.event.get():
		if dogodek.type == pygame.QUIT:
			# Ce uporabnik zapre okno nehajmo igrati
			igramo = False
		elif dogodek.type == pygame.KEYDOWN:
			# Ce uporabnik pritisne katerokoli tipko si to oznacimo
			igralec.oznaci_pritisk(dogodek.key, True)
			igralec2.oznaci_pritisk(dogodek.key, True)
		elif dogodek.type == pygame.KEYUP:
			# Ce uporabnik spusti katerokoli tipko si to oznacimo
			igralec.oznaci_pritisk(dogodek.key, False)
			igralec2.oznaci_pritisk(dogodek.key, False)

	# Premakni oba igralca
	igra_skupina.update()

	# Cel ekran prebarvaj z ozadjem
	ekran.fill((200, 200, 255))
	# Na ekran narisi igralce in level
	level.draw(ekran)
	igra_skupina.draw(ekran)
	# Poskrbi, da se vse skupaj izrise na monitor
	pygame.display.flip()

# Zapri okno pygame
pygame.quit()