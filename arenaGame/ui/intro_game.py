import pygame
from settings import settings


class IntroScreen:
    """Zeigt Story-Seiten im Retro-Terminal-Stil.
    Enter/Space = Text sofort komplett zeigen, dann nochmal = naechste Seite.
    Esc = ueberspringen (falls skippable=True)."""

    # Anzahl Zeichen, die pro Sekunde "getippt" werden
    CHARS_PER_SECOND = 15
    # wie schnell der Cursor blinkt (Sekunden pro Zustand an/aus)
    CURSOR_BLINK_INTERVAL = 0.5

    def __init__(self, pages, on_finished=None, font=None, bg_texture=None, skippable=True):
        self.pages = pages
        self.on_finished = on_finished or (lambda: None)
        self.index = 0
        self.skippable = skippable
        self.bg_texture = bg_texture

        # Retro-Font laden. Falls die .ttf-Datei fehlt, faellt es automatisch
        # auf Pygames eingebaute Default-Font zurueck (kein Crash, keine fc-list Warnung).
        self.font = font or self._load_retro_font(28)
        self.hint_font = self._load_retro_font(18)

        # NEU: Tastatur-Tipp-Sound laden (kurzer Klick, wird bei jedem Buchstaben abgespielt)
        self.type_sound = self._load_type_sound()

        # Typewriter-State
        self.char_timer = 0.0
        self.chars_shown = 0
        self.cursor_timer = 0.0
        self.cursor_visible = True

    def _load_retro_font(self, size):
        font_path = settings.ASSET_DIR / "fonts" / "VT323-Regular.ttf"
        try:
            return pygame.font.Font(str(font_path), size)
        except (FileNotFoundError, pygame.error):
            # Fallback: eingebaute Pygame-Font, kein Systemfont-Lookup noetig
            return pygame.font.Font(None, size)

    def _load_type_sound(self):
        # NEU: WICHTIG - dieser Pfad muss EXAKT zu deinem Ordner passen.
        # Passe "sounds" hier an, falls dein Ordner anders heisst (z.B. "sound_effekt").
        sound_path = settings.ASSET_DIR / "sounds" / "type_click.wav"
        print("Suche Sound unter:", sound_path, "| existiert:", sound_path.exists())
        try:
            sound = pygame.mixer.Sound(str(sound_path))
            sound.set_volume(0.35)
            return sound
        except (FileNotFoundError, pygame.error) as e:
            print("Sound konnte nicht geladen werden:", e)
            return None

    def reset(self):
        self.index = 0
        self.chars_shown = 0
        self.char_timer = 0.0

    def _current_full_text(self):
        if self.index >= len(self.pages):
            return ""
        return self.pages[self.index]

    def _is_page_fully_shown(self):
        return self.chars_shown >= len(self._current_full_text())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if not self._is_page_fully_shown():
                    # erstes Enter waehrend des Tippens: Text sofort komplett anzeigen
                    self.chars_shown = len(self._current_full_text())
                else:
                    # Text ist schon komplett da: zur naechsten Seite
                    self.index += 1
                    self.chars_shown = 0
                    self.char_timer = 0.0
                    if self.index >= len(self.pages):
                        self.on_finished()
            elif event.key == pygame.K_ESCAPE and self.skippable:
                self.on_finished()

    def update(self, dt):
        # Buchstaben nach und nach "eintippen"
        if not self._is_page_fully_shown():
            self.char_timer += dt
            step = 1.0 / self.CHARS_PER_SECOND
            while self.char_timer >= step and not self._is_page_fully_shown():
                self.char_timer -= step
                self.chars_shown += 1

                # NEU: Tipp-Sound abspielen, aber nicht bei Leerzeichen
                full_text = self._current_full_text()
                just_revealed_char = full_text[self.chars_shown - 1] if self.chars_shown > 0 else ""
                if self.type_sound and just_revealed_char != " ":
                    self.type_sound.play()

        # Cursor blinken lassen
        self.cursor_timer += dt
        if self.cursor_timer >= self.CURSOR_BLINK_INTERVAL:
            self.cursor_timer -= self.CURSOR_BLINK_INTERVAL
            self.cursor_visible = not self.cursor_visible

    def draw(self, surface: pygame.Surface):
        if self.bg_texture:
            surface.blit(self.bg_texture, (0, 0))
        else:
            surface.fill((10, 10, 10))

        if self.index >= len(self.pages):
            return

        full_text = self._current_full_text()
        visible_text = full_text[: self.chars_shown]

        lines = self._wrap_text(visible_text, settings.SCREEN_WIDTH - 180)
        y = settings.SCREEN_HEIGHT // 2 - (len(lines) * 34) // 2

        for i, line in enumerate(lines):
            rendered = self.font.render(line, True, (255, 255, 255))
            rect = rendered.get_rect(center=(settings.SCREEN_WIDTH // 2, y))
            surface.blit(rendered, rect)

            # blinkender Cursor nur an der letzten Zeile, nur solange Seite noch nicht fertig getippt
            if i == len(lines) - 1 and not self._is_page_fully_shown() and self.cursor_visible:
                cursor_x = rect.right + 4
                cursor_rect = pygame.Rect(cursor_x, rect.top, 12, rect.height)
                pygame.draw.rect(surface, (255, 255, 255), cursor_rect)

            y += 34

        # Hinweistext unten, je nachdem ob Seite fertig getippt ist oder nicht
        if self._is_page_fully_shown():
            hint_text = "[Enter] weiter"
        else:
            hint_text = "[Enter] ueberspringen"

        hint = self.hint_font.render(hint_text, True, (255, 255, 255))
        surface.blit(hint, hint.get_rect(midbottom=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 20)))

    def _wrap_text(self, text, max_width):
        words, lines, current = text.split(" "), [], ""
        for word in words:
            test = (current + " " + word).strip()
            if self.font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines