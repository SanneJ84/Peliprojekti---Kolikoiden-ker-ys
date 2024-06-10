import pygame
from random import randint

class Rahasade:
    paras_tulos = 0 

    def __init__(self):  
        pygame.init()
        self.naytto = pygame.display.set_mode((640, 480))
        self.fontti1 = pygame.font.SysFont("Arial", 30)
        self.fontti2 = pygame.font.SysFont("Arial", 25)
        self.robo = pygame.image.load("robo.png")
        self.kolikko = pygame.image.load("kolikko.png")
        self.hirvio = pygame.image.load("hirvio.png")
        self.alusta_peli()

    # Alustetaan peli
    def alusta_peli(self):
        self.robo_x = 0
        self.robo_y = 480 - self.robo.get_height()
        self.oikealle = False
        self.vasemmalle = False
        self.hyppy = False
        self.hypyn_korkeus = 0
        self.nopeus = 3
        self.pisteet = 0
        self.game_over = False
        self.kolikot = [(randint(0, 640 - self.kolikko.get_width()), 0) for _ in range(5)]
        self.kolikko_nopeus = 0.8
        self.hirvio1_x = randint(0, 640 - self.hirvio.get_width())
        self.hirvio1_y = 0
        self.hirvio1_nopeus = 0.5
        self.hirvio2_x = randint(0, 640 - self.hirvio.get_width())
        self.hirvio2_y = 0
        self.hirvio2_nopeus = 1
        self.hirvio3_x = 480
        self.hirvio3_y = 0, 480 - self.hirvio.get_width()  
        self.hirvio3_nopeus = 0.5

        pygame.display.set_caption("Rahasade")
        self.aloita_peli()

    # Pelin aloitusnäyttö
    def aloita_peli(self):      
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_RETURN:
                        self.pelaa()
                if tapahtuma.type == pygame.QUIT:
                    exit()

            # Aloitusnäytön tekstit
            self.naytto.fill((50,50,50))
            aloitusviesti = self.fontti1.render("KERÄÄ KOLIKOITA JA VÄISTELE HIRVIÖITÄ", True, (200,200,200))
            self.naytto.blit(aloitusviesti, ((640 - aloitusviesti.get_width()) / 2, (480 - aloitusviesti.get_height()) / 2 + aloitusviesti.get_height() - 100))

            aloitusviesti_2 = self.fontti2.render("Käynnistä peli painamalla ENTER", True, (200,200,200))
            self.naytto.blit(aloitusviesti_2, ((640 - aloitusviesti_2.get_width()) / 2, (480 - aloitusviesti_2.get_height()) / 2 + aloitusviesti.get_height() - 30))

            aloitusviesti_3 = self.fontti2.render("Ohjaa robottia nuolinäppäimillä \u2190 \u2192", True, (200,200,200))
            self.naytto.blit(aloitusviesti_3, ((640 - aloitusviesti_2.get_width()) / 2, (480 - aloitusviesti_3.get_height()) / 2 + aloitusviesti.get_height() + 20))
        
            aloitusviesti_4 = self.fontti2.render("Hyppää painamalla VÄLILYÖNTIÄ", True, (200,200,200))
            self.naytto.blit(aloitusviesti_4, ((640 - aloitusviesti_2.get_width()) / 2, (480 - aloitusviesti_4.get_height()) / 2 + aloitusviesti.get_height() + 70))
            
            pygame.display.flip()

    # Robottin liikuttaminen ja hyppääminen
    def liikuta_robottia(self):
        if self.vasemmalle and self.robo_x > 0:                             # robotti liikkuu vasemmalle 
            self.robo_x -= self.nopeus
        if self.oikealle and self.robo_x < 640 - self.robo.get_width():     # robotti liikkuu oikealle
            self.robo_x += self.nopeus
        if self.hyppy:                                                 
            if self.hypyn_korkeus < 200:                                    # jos hypyn korkeus on alle 200, robottia nostetaan ylöspäin             
                self.robo_y -= 4                                            # nostetaan robottia (koska y-koordinaatisto on alhaalta ylöspäin, vähennetään y-koordinaattia)
                self.hypyn_korkeus += 4                                     # hypyn korkeus kasvaa 
            else:  
                self.robo_y += 2.7                                          # kun hypyn korkeus on 200, robottia lasketaan alaspäin
                if self.robo_y > 480 - self.robo.get_height():              
                    self.robo_y = 480 - self.robo.get_height()          
                    self.hyppy = False                                      
                    self.hypyn_korkeus = 0                           

    # Kolikoiden liikuttaminen
    def liikuta_kolikoita(self):
        for i in range(len(self.kolikot)):                  
            kolikko_x, kolikko_y = self.kolikot[i]
            self.kolikot[i] = (kolikko_x, kolikko_y + self.kolikko_nopeus)
            if kolikko_y > 480:
                self.kolikot[i] = (randint(0, 640 - self.kolikko.get_width()), 0) 

    # Hirviöiden liikuttaminen
    def liikuta_hirvioita(self):  
        self.hirvio1_y += self.hirvio1_nopeus
        if self.hirvio1_y > 480:
            self.hirvio1_x = randint(0, 640 - self.hirvio.get_width())
            self.hirvio1_y = 0

        self.hirvio2_y += self.hirvio2_nopeus
        if self.hirvio2_y > 480:
            self.hirvio2_x = randint(0, 640 - self.hirvio.get_width())
            self.hirvio2_y = 0

        self.hirvio3_y = 480 - self.hirvio.get_height()
        self.hirvio3_x -= self.hirvio3_nopeus
        if self.hirvio3_x < 0:
            self.hirvio3_x = 640
            self.hirvio3_y = 480 - self.hirvio.get_height()

    # Tarkistetaan, osuuko robotti kolikkoon ja lisätään pisteitä                          
    def tarkista_kolikot(self): 
        for i in range(len(self.kolikot)): 
            kolikko_x, kolikko_y = self.kolikot[i]
            if self.robo_tormaa_kolikkoon(kolikko_x, kolikko_y):
                self.pisteet += 1
                if self.pisteet % 15 == 0:                      # Kun on kerätty 20 kolikkoa, nopeutetaan hirviöitä
                    self.hirvio3_nopeus += 0.2
                    if self.hirvio3_nopeus > 3:                 # Jotta ei mennä liian nopeaksi, rajoitetaan nopeus 3:een
                        self.hirvio3_nopeus = 3
                if self.pisteet > Rahasade.paras_tulos:         # Päivitetään paras tulos
                    Rahasade.paras_tulos = self.pisteet  
                self.kolikot[i] = (randint(0, 640 - self.kolikko.get_width()), 0)   
    
    # Tarkistetaan, onko robotti törmännyt hirviöön, jos on, peli päättyy
    def tarkista_hirviot(self):
        if self.robo_tormaa_hirvioon(self.hirvio1_x, self.hirvio1_y) or self.robo_tormaa_hirvioon(self.hirvio2_x, self.hirvio2_y) or self.robo_tormaa_hirvioon(self.hirvio3_x, self.hirvio3_y):
            self.game_over = True

    # Tarkistetaan, osuuko robotti kolikkoon
    def robo_tormaa_kolikkoon(self, kolikko_x, kolikko_y):              
        return self.robo_x < kolikko_x + self.kolikko.get_width() and \
               self.robo_x + self.robo.get_width() > kolikko_x and \
               self.robo_y < kolikko_y + self.kolikko.get_height() and \
               self.robo_y + self.robo.get_height() > kolikko_y
    
    # Tarkistetaan, osuuko robotti hirviöön
    def robo_tormaa_hirvioon(self, hirvio_x, hirvio_y):
        pelivara = 12      
        return (self.robo_x + self.robo.get_width() - pelivara) >= hirvio_x and \
            (hirvio_x + self.hirvio.get_width() - pelivara) >= self.robo_x and \
            (self.robo_y + self.robo.get_height() - pelivara) >= hirvio_y and \
            (hirvio_y + self.hirvio.get_height() - pelivara) >= self.robo_y

    def tarkista_tormaykset(self):  
        self.tarkista_kolikot()
        self.tarkista_hirviot()

    def pelaa(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasemmalle = True
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = True
                    if tapahtuma.key == pygame.K_SPACE:
                        self.hyppy = True
                if tapahtuma.type == pygame.KEYUP:
                    if tapahtuma.key == pygame.K_LEFT:
                        self.vasemmalle = False
                    if tapahtuma.key == pygame.K_RIGHT:
                        self.oikealle = False
                if tapahtuma.type == pygame.QUIT:                   
                    exit()

            self.liikuta_robottia() 
            self.liikuta_kolikoita() 
            self.liikuta_hirvioita() 
            self.tarkista_tormaykset()

            if self.game_over:
                teksti = self.fontti1.render("GAME OVER!", True, (255, 0, 0))
                self.naytto.blit(teksti, ((640 - teksti.get_width()) / 2, (480 - teksti.get_height()) / 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                self.alusta_peli()      
                return

            # Päivitetään näyttö 
            self.naytto.fill((50,50,50))
            for kolikko_x, kolikko_y in self.kolikot:
                self.naytto.blit(self.kolikko, (kolikko_x, kolikko_y))
            self.naytto.blit(self.hirvio, (self.hirvio1_x, self.hirvio1_y))
            self.naytto.blit(self.hirvio, (self.hirvio2_x, self.hirvio2_y))
            self.naytto.blit(self.hirvio, (self.hirvio3_x, self.hirvio3_y))
            self.naytto.blit(self.robo, (self.robo_x, self.robo_y))
            teksti = self.fontti1.render("Pisteet: " + str(self.pisteet), True, (200,200,200))            
            teksti_paras_tulos = self.fontti1.render("Paras tulos: " + str(Rahasade.paras_tulos), True, (200,200,200))
            self.naytto.blit(teksti, (10, 10))
            self.naytto.blit(teksti_paras_tulos, (10, 30))
            pygame.display.flip()     
            pygame.time.delay(5)

if __name__ == "__main__":
    Rahasade()