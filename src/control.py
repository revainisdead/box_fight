from typing import Any, Dict

import sys
import time

import pygame as pg

from . import binds
from . import const
from . import setup
from . components import user_interface, util


class Control:
    def __init__(self, caption) -> None:
        self.quit = False
        self.current_time = 0
        self.fps = const.FPS
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()

        self.screen_surface = pg.display.get_surface()

        self.state = None # type: State
        self.state_name = None # type: Dict[const.MainState, State]
        self.state_dict = {}


    def game_loop(self) -> None:
        while not self.quit:
            dt = self.clock.tick(self.fps)/1000
            self.event_loop()
            self.update(dt)
            pg.display.update()

            binds.INPUT.reset()

        # Game loop is quit by checking for when the quit
        # is set to True, when game loop exist end gracefully
        # but unloading pygame and using a system exit.
        pg.quit()
        sys.exit()


    def event_loop(self) -> None:
        for event in pg.event.get():
            binds.INPUT.update(event)


    def update(self, dt: float) -> None:
        """Connects to the main game loop.
        Do any updates needed.
        """
        self.current_time = pg.time.get_ticks()
        if self.state.quit:
            self.quit = True
        elif self.state.state_done:
            self.flip_state()

        self.state.update(self.screen_surface, self.current_time, dt)

        # In Game User Interface.
        #self.game_ui.update(self.screen_surface, self.current_time, self.state_name)


    def setup_states(self, state_dict, start_state) -> None:
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        print("Initial state in control object: {}".format(self.state_name))


    def setup_game_ui(self) -> None:
        #self.game_ui = user_interface.GameUI()
        pass


    def flip_state(self) -> None:
        previous, self.state_name = self.state_name, self.state.next
        # Get game_info before setting new state
        game_info = self.state.dump_game_info()
        self.state = self.state_dict[self.state_name]

        # Startup state when switching to it
        self.state.startup(game_info)
        print("Main state switched to: {}".format(self.state_name))

        self.state.previous = previous


class State:
    def __init__(self) -> None:
        # Quit everything
        self.quit = False

        # Quit this state
        self.state_done = False

        self.next = None # type: const.MainState
        self.previous = None # type: const.MainState

        # XXX Make game info it's own object.
        self.game_info = {} # type: Dict[str, Any]


    def dump_game_info(self) -> Dict[str, Any]:
        return self.game_info


    def startup(self) -> None:
        raise NotImplementedError


    def update(self) -> None:
        raise NotImplementedError
