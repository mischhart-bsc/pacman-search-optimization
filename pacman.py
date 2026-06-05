import sys
from model.board_definition import BoardDefinition
from model.level_config import LevelConfig
from settings import *
from levels.level_content_initializer import LevelContentInitializer
from model.direction import Direction


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.timer = pygame.time.Clock()
        self.game_engine = self.init()
        self.game_start_sfx = pygame.mixer.Sound("media/game_start.wav")

    def init(self):
        board = BOARD.copy()
        board_definition = BoardDefinition(board)
        level_1 = LevelConfig(
            wall_color="blue",
            gate_color="white",
            board_definition=board_definition,
            power_up_limit=POWER_UP_LIMIT,
        )
        level_init = LevelContentInitializer(level_1, self.screen)
        return level_init.init_game_engine()

    def update(self):
        self.timer.tick(FPS)
        self.game_engine.tick()
        pygame.display.flip()

    def draw(self):
        self.screen.fill([12, 2, 25])

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.game_engine.game_over:
                    if not self.game_engine.name_submitted:
                        if event.key == pygame.K_RETURN and self.game_engine.player_name:
                            self.game_engine.submit_score()
                        elif event.key == pygame.K_BACKSPACE:
                            self.game_engine.player_name = self.game_engine.player_name[:-1]
                        elif event.unicode.isprintable() and len(self.game_engine.player_name) < 12:
                            self.game_engine.player_name += event.unicode
                    elif event.key == pygame.K_SPACE:
                        pygame.init()
                        self.game_start_sfx.play()
                        self.game_engine = self.init()
                else:
                    if event.key == pygame.K_LEFT:
                        self.game_engine.queued_direction = Direction.LEFT
                    if event.key == pygame.K_RIGHT:
                        self.game_engine.queued_direction = Direction.RIGHT
                    if event.key == pygame.K_DOWN:
                        self.game_engine.queued_direction = Direction.DOWN
                    if event.key == pygame.K_UP:
                        self.game_engine.queued_direction = Direction.UP
   
            if event.type == GHOST_EATEN_EVENT:
                self.game_engine.play_ghost_runsaway_sound()
            if event.type == PLAYER_EATEN_EVENT:
                self.game_engine.play_player_eaten_sound()

    def run(self):
        self.game_start_sfx.play()
        while True:
            self.check_events()
            self.draw()
            self.update()


if __name__ == "__main__":
    game = Game()
    game.run()
