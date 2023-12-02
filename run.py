import utils.utils

if __name__ == "__main__":
    from setup import setup_environment
    setup_environment(utils.utils.get_project_root() + "/requirements.txt")

    import argparse
    import sys

    import pygame

    from game import Game
    from render.character_selection import CharacterSelectionScene
    from resources.resources_manager import ResourcesManager


    def determine_scaling_factor(width, height):
        from resources.resources_manager import ResourcesManager
        global_scaling = ResourcesManager.settings["base_scaling"]
        base_width = ResourcesManager.settings["base_width"]
        base_height = ResourcesManager.settings["base_height"]

        width_scaling = width / base_width
        height_scaling = height / base_height

        return global_scaling * min(width_scaling, height_scaling)


    parser = argparse.ArgumentParser(description="Provide width and height for game screen.")
    parser.add_argument('--width', type=int, default=ResourcesManager.settings["base_width"], help="Width of the screen.")
    parser.add_argument('--height', type=int, default=ResourcesManager.settings["base_height"], help='Height of the screen.')

    args = parser.parse_args()

    pygame.init()

    width, height = args.width, args.height

    fps = 1000

    ResourcesManager.settings["base_scaling"] = determine_scaling_factor(width, height)

    import ctypes

    # remove windows DPI scaling
    if sys.platform == 'win32':
        ctypes.windll.user32.SetProcessDPIAware()


    flags = pygame.SCALED | pygame.RESIZABLE | pygame.FULLSCREEN


    screen = pygame.display.set_mode((width, height), flags=flags, vsync=1)

    character_selection = CharacterSelectionScene(screen)

    while True:
        result = character_selection.main_loop()

        if result is False:
            break

        character1, character2 = result

        game = Game(screen, character1, character2, fps=fps, title="RiftBrawl")

        game.run()
