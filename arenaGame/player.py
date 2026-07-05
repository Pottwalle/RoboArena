import pygame
import math
from weapon import Weapon
from inventory_manager import InventoryManager
from stats import Stats
from settings import settings

class Player:
    # Idle-Pose: wird gezeigt, wenn sich der Spieler nicht bewegt
    IDLE_FRAME_PATH = 'assets/character/character1_walk_0.png'

    # Lauf-Zyklus: wird beim Bewegen der Reihe nach durchgeschaltet.
    # Aktuell nur 1 Pose vorhanden -> wechselt einfach zwischen Idle und dieser Pose hin und her.
    # Sobald mehr Frames verfügbar sind, hier einfach weitere Pfade ergänzen.
    WALK_FRAME_PATHS = [
        'assets/character/character1_walk_0.png',
        'assets/character/character1_walk_1.png',
    ]

    # Angriffs-Animation (Axt-Schwung), 10 Frames, wird einmal komplett abgespielt
    ATTACK_FRAME_PATHS = [
        'assets/character/attack_01_idle.png',
        'assets/character/attack_02_ausholen.png',
        'assets/character/attack_03_ausholen_hoch.png',
        'assets/character/attack_04_schwung.png',
        'assets/character/attack_05_mitte_schwung.png',
        'assets/character/attack_06_schwung_ende.png',
        'assets/character/attack_07_nachziehen.png',
        'assets/character/attack_08_nachziehen_tief.png',
        'assets/character/attack_09_zurueckfuehren.png',
        'assets/character/attack_10_zurueck_idle.png',
    ]

    # Wie viele Frames pro Sekunde die Laufanimation abspielt
    ANIMATION_FPS = 6

    # Wie viele Frames pro Sekunde die Angriffsanimation abspielt (schneller = knackiger)
    ATTACK_FPS = 14

    # Wie viel größer die Sprites im Vergleich zum Kollisionsradius (r) gezeichnet werden.
    # r bleibt für Kollision/Bewegung unverändert - nur die Optik wird skaliert.
    # 1.0 entspräche der alten Größe von 40x40px (bei typischem r), höher = größer/erkennbarer
    SPRITE_SCALE = 3.0

    def __init__(self, x, y, r, alpha, base_speed, speed_modifier=1, hp=100, max_hp=100):
        def laden(pfad):
            bild = pygame.image.load(settings.BASE_DIR / pfad).convert_alpha()
            durchmesser = int(r * 2 * self.SPRITE_SCALE)
            return pygame.transform.smoothscale(bild, (durchmesser, durchmesser))

        # Idle-Bild (rechts/links)
        self.idle_bild_rechts = laden(self.IDLE_FRAME_PATH)
        self.idle_bild_links = pygame.transform.flip(self.idle_bild_rechts, True, False)

        # Walk-Zyklus-Bilder (rechts/links)
        self.walk_frames_rechts = [laden(p) for p in self.WALK_FRAME_PATHS]
        self.walk_frames_links = [pygame.transform.flip(b, True, False) for b in self.walk_frames_rechts]

        # Angriffs-Frames (rechts/links)
        self.attack_frames_rechts = [laden(p) for p in self.ATTACK_FRAME_PATHS]
        self.attack_frames_links = [pygame.transform.flip(b, True, False) for b in self.attack_frames_rechts]

        # Aktueller Frame-Index und Timer für die Lauf-Animation
        self.frame_index = 0
        self.frame_timer = 0.0
        self.frame_dauer = 1 / self.ANIMATION_FPS

        # Status der Angriffs-Animation
        self.is_attacking = False
        self.attack_frame_index = 0
        self.attack_timer = 0.0
        self.attack_frame_dauer = 1 / self.ATTACK_FPS
        self.attack_schaut_links = False

        # Merkt sich den Mausstatus vom letzten Frame, um einen "frischen" Klick zu erkennen
        self._maus_links_war_gedrueckt = False

        # Bequemer Zugriff auf das aktuell darzustellende Bild
        self.spieler_bild = self.idle_bild_rechts

        # Merkt sich, in welche Richtung der Charakter zuletzt geschaut hat
        self.schaut_links = False

        self.position = pygame.Vector2(x, y)
        self.r = r
        self.alpha = alpha
        self.direction = pygame.Vector2()
        self.attack_direction = pygame.Vector2()

        self.xp = 0
        self.level = 0
        self.xp_breakpoints = [
            0, 50, 100, 180, 300, 500, 750, 1200,
            922337203685477580
        ]

        self.base_speed = base_speed
        self.speed_modifier = speed_modifier

        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = 800
        self.max_speed = 300
        self.friction = 0.90

        self.weapon: Weapon = None
        self.inventory = InventoryManager(3, 8)
        self.stats = Stats({ # stat bonuses, ontop of the base stats of the weapon / skill
            "max_hp": max_hp,
            "speed": base_speed,
            "damage": 0,
            "attack_range": 0,
            "cone_angle_deg": 0,
            "cooldown": 0 # cooldown counts as cooldown reduction
        }, self.inventory)

        '''handles the updating of all player related methods changing the coordinates accordingly'''
    # backwards compatability for now
    @property
    def max_hp(self):
        return self.stats.get("max_hp")
    
    @property
    def hp(self):
        return self.stats.hp
    
    @hp.setter
    def hp(self, value):
        self.stats.hp = max(0, min(self.max_hp, value))

    def update(self, dt, movement, camera):
        self.input(camera)

        # Blickrichtung NUR ändern, wenn sich der Spieler aktiv bewegt (Tasten gedrückt sind)
        if self.direction.length() > 0:
            # Das Minus vor math.atan2 korrigiert die Drehung für die invertierte Pygame-Y-Achse
            self.alpha = math.degrees(
                math.atan2(-self.direction.y, self.direction.x)
            )

            # Nur horizontal flippen statt drehen, damit der Charakter aufrecht bleibt.
            # Bei reiner vertikaler Bewegung (nur hoch/runter, x == 0) auf die
            # Standardausrichtung zurücksetzen, damit z.B. beim Runterlaufen
            # immer die Seite mit der Axt zu sehen ist, statt eine alte
            # links/rechts-Blickrichtung beizubehalten.
            if self.direction.x < 0:
                self.schaut_links = True
            elif self.direction.x > 0:
                self.schaut_links = False
            else:
                self.schaut_links = False
        
        if self.inventory.update_stats: # handles stat changes on equipment, signal down that change occured
            self.weapon.update_stats()

        if self.is_attacking:
            self._update_attack(dt)
        else:
            self._update_animation(dt)

        self.position = movement.move(self, dt)

    def start_attack(self):
        """Startet die Angriffsanimation von vorne (falls nicht schon aktiv)."""
        if self.is_attacking:
            return
        self.is_attacking = True
        self.attack_frame_index = 0
        self.attack_timer = 0.0
        # Blickrichtung beim Angriff einfrieren = Richtung Maus, nicht Bewegung
        self.attack_schaut_links = self.attack_direction.x < 0

    def _update_attack(self, dt):
        """Spielt die Angriffs-Frames einmal komplett durch und beendet
        danach automatisch den Angriffszustand."""
        self.attack_timer += dt
        if self.attack_timer >= self.attack_frame_dauer:
            self.attack_timer -= self.attack_frame_dauer
            self.attack_frame_index += 1

            if self.attack_frame_index >= len(self.attack_frames_rechts):
                self.is_attacking = False
                self.attack_frame_index = 0
                return

        richtung_frames = self.attack_frames_links if self.attack_schaut_links else self.attack_frames_rechts
        self.spieler_bild = richtung_frames[self.attack_frame_index]

    def _update_animation(self, dt):
        """Zeigt die Idle-Pose im Stillstand. Beim Bewegen wird die
        Walk-Frame-Liste im Kreis durchgeschaltet (funktioniert mit
        beliebig vielen Frames, auch nur 2)."""
        if self.direction.length() > 0:
            self.frame_timer += dt
            if self.frame_timer >= self.frame_dauer:
                self.frame_timer -= self.frame_dauer
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames_rechts)

            richtung_frames = self.walk_frames_links if self.schaut_links else self.walk_frames_rechts
            self.spieler_bild = richtung_frames[self.frame_index]
        else:
            self.frame_index = 0
            self.frame_timer = 0.0
            self.spieler_bild = self.idle_bild_links if self.schaut_links else self.idle_bild_rechts

    def draw(self, screen, camera):
        screen_position = self.position - camera

        # self.spieler_bild wird bereits in _update_animation() passend
        # zu Laufzustand + Blickrichtung gesetzt
        rect = self.spieler_bild.get_rect(
            center=(int(screen_position.x), int(screen_position.y))
        )
        screen.blit(self.spieler_bild, rect)

        # Richtungslinie (darf sich weiterhin frei um 360° drehen)
        rad = math.radians(self.alpha)
        end_x = screen_position.x + math.cos(rad) * self.r
        end_y = screen_position.y - math.sin(rad) * self.r

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (screen_position.x, screen_position.y),
            (int(end_x), int(end_y)),
            2
        )

    def input(self, camera):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1
        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:
            self.direction.x = 1

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        mouse_world_pos = mouse_pos + camera
        to_mouse = mouse_world_pos - self.position

        if to_mouse.length() > 0:
            self.attack_direction = to_mouse.normalize()
        else:
            self.attack_direction = pygame.Vector2(1, 0)

        # Linksklick erkennen (nur beim Übergang "nicht gedrückt" -> "gedrückt",
        # damit gehaltene Maustaste nicht dauerhaft angreift)
        maus_links_gedrueckt = pygame.mouse.get_pressed()[0]
        if maus_links_gedrueckt and not self._maus_links_war_gedrueckt:
            self.start_attack()
        self._maus_links_war_gedrueckt = maus_links_gedrueckt

    def setWeapon(self, weapon):
        self.weapon = weapon

    def add_xp(self, amount):
        if amount >= 0:
            self.xp += amount
            self.update_level()

    def update_level(self):
        if self.xp >= self.xp_breakpoints[self.level + 1]:
            self.level += 1
            self.update_level()

    def get_level_progress(self) -> float:
        current_lvl = self.level
        current_lvl_xp = self.xp_breakpoints[current_lvl]
        next_lvl_xp = self.xp_breakpoints[current_lvl + 1]

        return max(
            0.0,
            min(
                1.0,
                (self.xp - current_lvl_xp) /
                max(1, (next_lvl_xp - current_lvl_xp))
            )
        )