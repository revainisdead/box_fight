from . import const
from . import control
from . import setup

from . states import arena
from . states import mainmenu


def main():
    setup.start()

    state_dict = {
        const.MainState.mainmenu: mainmenu.MainMenu(),
        const.MainState.arena: arena.Arena(),
    }

    game = control.Control(const.CAPTION)
    game.setup_states(state_dict, const.MainState.mainmenu)
    game.setup_game_ui()

    game.game_loop()


if __name__ == "__main__":
    main()
