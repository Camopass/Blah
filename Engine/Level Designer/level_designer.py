import pygame
import os
import json
import base64

from Engine.Window import Window
from Engine.Maths import Vec2
from tkinter import Tk, filedialog

global dark_gray
dark_gray = (25, 25, 35)
global light_gray
light_gray = (45, 45, 55)

# TODO: Draggable Dialogs
# TODO: Move Save/Load into a dialog
# TODO: Add more File options like New
# TODO: Tile Names
# TODO: Scale Down the bottom info panel


Tk().withdraw()

os.chdir(r"E:\Games\Slime")

pygame.init()


class Button:
    """
    Button Class
    x, y, width, height : You probably can guess this.
    button_id, title : button_id is the ID you will use for the button and will be usually the one returned by functions
    and used to retrieve from the window. This should be unique.
    The title is the text rendered by the engine.

    To use this, you call button = Button(x, y, width, height)
    and then use button.on_click = button_click_function
    This function should have the parameters self, window with window being the window it is currently in.
    This will trigger whenever the mouse is released on the button. If for some reason you want it to trigger when the
    mouse goes down, use button.on_mouse_down = button_click_function instead.

    You will also have to use window.buttons.append(button) for the window to register the buttons.

    This class will not actually render the button, however it will manage the button's shape and the window will
    automatically manage click events in the order they are added to the window.

    """

    def __init__(self, x, y, width, height, button_id, title):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = button_id
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title

    def on_mouse_down(self, window):
        pass

    def on_click(self, window):
        pass

    def resize(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)


class Dialog:
    """
    Dialog class for dialogs
    x, y, width, height : self explanatory
    title : the title rendered on the dialog
    dialog_id : the ID used for the dialog
    window : the window the dialog will be rendered on

    This class is meant to have buttons on it. To do this, create a button from the Button class. The x, y, width, and
    height will be automatically set by the dialog when added, so therefore it does not matter. The other parameters do.
    Next, use dialog.add_button(button). This is important as the button needs to be registered and have the size
    manipulated. Example:

    dialog = Dialog(500, 500, 250, 500, "Example Dialog", "example_dialog", window)
    example_button = Button(1, 1, 1, 1, "example_button", "Example Button")
    dialog.add_button(example_button)

    WINDOW COORDINATES

    """

    def __init__(self, x, y, width, height, title, dialog_id, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.id = dialog_id
        self.font = pygame.font.Font(r"assets/fonts/vcr.ttf", 15)
        drag_pos = self.font.size(title)[0] + 3
        self.is_dragging = False
        self.drag_offset = Vec2(0, 0)
        self.render_x = x
        self.render_y = y
        self.last_drag_offset = Vec2(0, 0)
        self.drag_button = Button(self.x + drag_pos, self.y, self.width - 27 - drag_pos, 25,
                                  f'{dialog_id}Dialog:drag', f'{dialog_id} Drag')
        self.drag_pos = Vec2(0, 0)

        def on_drag_clickd(d_window):
            self.drag_pos = -Vec2(*self.window.get_mouse_pos())
            self.is_dragging = True

        def on_drag_clicku(d_window):
            self.last_drag_offset = (self.drag_pos - -Vec2(*self.window.get_mouse_pos())) + self.drag_offset
            o = self.last_drag_offset.to_tuple()
            self.x += o[0]
            self.y += o[1]
            for button in self.buttons:
                button.x += o[0]
                button.y += o[1]
            self.render_x, self.render_y = self.x, self.y
            self.is_dragging = False
            self.drag_pos = Vec2(0, 0)

        self.close_button = Button(self.x + self.width - 25, self.y, 25, 25,
                                   f'{dialog_id}Dialog:close', f'{dialog_id} Close')
        self.drag_button.on_click = on_drag_clicku
        self.drag_button.on_mouse_down = on_drag_clickd

        self.close_button.on_click = lambda w: self.close()
        self.buttons = [self.drag_button, self.close_button]
        self.is_open = False
        self.window = window
        window.buttons += self.buttons

    def open(self):
        self.is_open = True

    def close(self):
        self.window.dialogs.remove(self)
        for button in self.buttons:
            self.window.buttons.remove(button)
        del self

    def add_button(self, button):
        button.resize(self.x + 10, self.y + (len(self.buttons) - 2) * (self.font.get_height() + 12) + 29,
                      self.width - 20, 25)
        self.buttons.append(button)
        if (len(self.buttons) - 2) * (self.font.get_height() + 4) > self.height:
            self.height += self.font.get_height() + 4
        button.id = f'{self.id}Dialog:{button.id}'
        self.window.buttons.append(button)

    def render(self):
        if self.is_dragging:
            self.render_x, self.render_y = (
                        (self.drag_pos - -Vec2(*self.window.get_mouse_pos())) + self.drag_offset).to_tuple()
        if (not self.window.left_click) and self.is_dragging:
            self.drag_button.on_click(self.window)
        pygame.draw.rect(self.window.screen, light_gray, (self.render_x, self.render_y, self.width, self.height + 25))
        pygame.draw.rect(self.window.screen, dark_gray, (self.render_x, self.render_y, self.width, 25))
        self.window.screen.blit(self.font.render(self.title, True, (255, 255, 255)),
                                (self.render_x + 2, self.render_y + 2))
        for ind, button in enumerate(self.buttons[2:]):
            y_offset = ind * (self.font.get_height() + 12) + 29
            pygame.draw.rect(self.window.screen, dark_gray,
                             (self.render_x + 10, self.render_y + y_offset, self.width - 20, 25))
            self.window.screen.blit(self.font.render(button.title, True, (255, 255, 255)),
                                    (self.render_x + 15, self.render_y + y_offset + 2))
        pygame.draw.circle(self.window.screen, (230, 20, 5), (self.render_x + self.width - 12, self.render_y + 12), 7)

    def get_hovered_button(self, m_x, m_y):
        for button in self.buttons:
            if button.x <= m_x <= button.x + button.width:
                if button.y <= m_y <= button.y + button.height:
                    return button
        return None

    def on_click(self, window):
        button = self.get_hovered_button(*window.get_mouse_pos())
        if button is not None:
            button.on_click(window)

    def on_mouse_down(self, window):
        button = self.get_hovered_button(*window.get_mouse_pos())
        if button is not None:
            button.on_mouse_down(window)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Level:
    def __init__(self, name, length, height, tile_size):
        self.name = name
        self.tile_size = tile_size
        self.piece_dict = {0: None, 1: pygame.image.load("assets/Tiles/dirt.png").convert(),
                           2: pygame.image.load("assets/Tiles/grass.png").convert()}
        self.image_dict = {0: None, 1: encode_image(self.piece_dict[1]), 2: encode_image(self.piece_dict[2])}
        self.length = length
        self.height = height
        self.floor_pieces = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 0,
            0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        ]


class LevelDesigner(Window):
    def __init__(self, width, height, caption: str = "PyGame Engine", icon=None):
        super().__init__(width, height, caption, icon)
        self.mouse_pan_pos = Vec2(0, 0)
        self.view_offset = Vec2(0, 0)
        self.view_zoom = 1
        self.panning = False
        self.level = Level("Test Level", 25, 15, 32)
        self.viewport = None
        self.buttons = []
        self.active_piece = 2
        self.dialogs = []

    def get_viewport_mouse(self):
        pos = list(self.get_mouse_pos())
        pos[0] -= self.screen.get_width() - self.viewport.get_width()
        pos[1] -= 25
        return pos

    def mouse_down(self, button):
        if button == pygame.BUTTON_MIDDLE:
            self.mouse_pan_pos = -Vec2(*self.get_mouse_pos())
            self.panning = True
        if button == pygame.BUTTON_LEFT:
            for button in self.buttons:
                if button.rect.collidepoint(self.get_mouse_pos()):
                    print(button.id)
                    return button.on_mouse_down(self)

    def mouse_up(self, button):
        if button == pygame.BUTTON_MIDDLE:
            self.view_offset = (self.mouse_pan_pos - -Vec2(*self.get_mouse_pos())) + self.view_offset
            self.panning = False
            self.mouse_pan_pos = Vec2(0, 0)
        if button == pygame.BUTTON_LEFT:
            for button in self.buttons:
                if button.rect.collidepoint(self.get_mouse_pos()):
                    print(button.id)
                    return button.on_click(self)

    def mouse_scroll(self, amount):
        if amount < 0:
            amount *= -1
            amount = amount ** -1
        self.view_zoom *= amount

    def get_offset(self):
        if self.panning:
            return (self.mouse_pan_pos - -Vec2(*self.get_mouse_pos())) + self.view_offset
        else:
            return self.view_offset

    def get_hovered_button(self):
        for button in self.buttons:
            if button.rect.collidepoint(self.get_mouse_pos()):
                return button
        return None

    def get_button_by_id(self, b_id):
        for button in self.buttons:
            if button.id == b_id:
                return button
        return None


def get_grid_pos(x, y, tile_size, window):
    pos = Vec2(x, y) - window.get_offset() * Vec2(window.view_zoom, window.view_zoom)
    tile_size = Vec2(tile_size, tile_size)
    tile_pos = pos // (tile_size * Vec2(window.view_zoom, window.view_zoom))
    return tile_pos.to_tuple()


def get_screen_pos(x, y, tile_size, window):
    pos = Vec2(x, y)
    tile_size = Vec2(tile_size, tile_size)
    pos *= tile_size
    return (pos + window.get_offset()).to_tuple()


def encode_image(image):
    return base64.b64encode(pygame.image.tostring(image, "RGBA")).decode('ascii')


def decode_image(image_str, size):
    return pygame.image.fromstring(base64.b64decode(image_str), size, "RGBA")


def directory_prompt():
    return filedialog.asksaveasfilename(title='Save Mungus 2 Level To', filetypes=[('Mungus 2 Level', '*.m2l')])


def main():
    window = LevelDesigner(1900, 1007, "Slime Level Designer", 'assets/icons/16-hacker.png')
    grid_size = 32

    clock = pygame.time.Clock()

    viewport = pygame.Surface((1600, 960))
    window.viewport = viewport

    running = True

    font = pygame.font.Font('assets/fonts/vcr.ttf', 15)

    def func_fact(p_id):
        def on_click(func_fact_window):
            func_fact_window.active_piece = p_id

        return on_click

    def add_tile_buttons(window_b):
        for button in window_b.buttons:
            if button.id.startswith('LDButton'):
                window_b.buttons.remove(button)
        for index_buttons, temp in enumerate(window.level.piece_dict.items()):
            p_id, button = temp
            b = Button(10, 85 * index_buttons + 30, grid_size, grid_size, f'LDButton{p_id}', 'Tile Select')

            b.on_click = func_fact(p_id)
            window_b.buttons.append(b)

    add_tile_buttons(window)

    save_button = Button(0, 0, 45, 25, 'save', 'Save')

    def save(save_window):
        level = save_window.level
        directory = directory_prompt()
        print(level.image_dict)
        obj = {"LevelLength": level.length, "LevelHeight": level.height, "LevelName": level.name,
               "LevelPieces": level.image_dict, "LevelData": level.floor_pieces, "TileSize": level.tile_size}
        print(obj)
        json_data = json.dumps(obj)
        with open(directory + '.m2l' if not directory.endswith('.m2l') else directory, 'w') as file:
            file.write(json_data)

    save_button.on_click = save
    window.buttons.append(save_button)

    load_button = Button(45, 0, 45, 25, 'load', 'Load')

    def load(load_window):
        directory = filedialog.askopenfilename(filetypes=[('Mungus 2 Level', '*.m2l')])
        if directory == '':
            return
        with open(directory, 'r') as file:
            map_data = json.loads(file.read())
        l = Level(map_data["LevelName"], map_data["LevelLength"], map_data["LevelHeight"], map_data["TileSize"])
        piece_dict = {}
        for p_id, piece in map_data["LevelPieces"].items():
            if piece is None:
                piece_dict[p_id] = None
                continue
            piece_dict[p_id] = piece
        true_data = {}
        for p_id, item in piece_dict.items():
            if item is None:
                true_data[int(p_id)] = None
                continue
            true_data[int(p_id)] = decode_image(item, (grid_size, grid_size))
        l.piece_dict = true_data
        l.floor_pieces = map_data["LevelData"]
        load_window.level = l

    load_button.on_click = load
    window.buttons.append(load_button)

    edit_button = Button(90, 0, 45, 25, 'edit', 'Edit')

    def load_tile(load_window):
        directory = filedialog.askopenfilename(filetypes=[('Image File (recommended)', '*.png'), ('All Files', '*')])
        if directory == '':
            return
        tile = pygame.image.load(directory).convert_alpha()
        if tile.get_size() != (grid_size, grid_size):
            print(tile.get_size())
            return -1
        p_dict = load_window.level.piece_dict
        index = max(p_dict.keys()) + 1
        p_dict[index] = tile
        load_window.level.image_dict[index] = encode_image(tile)
        add_tile_buttons(load_window)
        return 0

    def open_edit_dialog(edit_dialog_window):
        if len(edit_dialog_window.dialogs) != 1:
            edit_dialog = Dialog(edit_dialog_window.screen.get_width() / 2 - 250,
                                 edit_dialog_window.screen.get_height() / 2 - 125, 500, 250,
                                 "Edit Dialog", "edit", edit_dialog_window)
            add_tile = Button(edit_dialog.x, edit_dialog.y + 25, edit_dialog.width, 25,
                              'add_tile', 'Add Tile')
            undo = Button(edit_dialog.x, edit_dialog.y + 52, edit_dialog.width, 25, 'undo', 'Undo')
            add_tile.on_click = load_tile
            edit_dialog.add_button(add_tile)
            edit_dialog.add_button(undo)
            edit_dialog.open()
            edit_dialog_window.dialogs.append(edit_dialog)
        else:
            edit_dialog_window.dialogs[0].close()

    edit_button.on_click = open_edit_dialog
    window.buttons.append(edit_button)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                window.window_surface = pygame.display.set_mode(size=(event.w, event.h), flags=pygame.RESIZABLE)
                window.update_resize()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    window.windowed() if window.is_fullscreen else window.fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_RIGHT:
                    window.right_click = True
                if event.button == pygame.BUTTON_LEFT:
                    window.left_click = True
                if event.button == pygame.BUTTON_MIDDLE:
                    window.middle_click = True
                window.mouse_down(event.button)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_RIGHT:
                    window.right_click = False
                if event.button == pygame.BUTTON_LEFT:
                    window.left_click = False
                if event.button == pygame.BUTTON_WHEELDOWN:
                    window.view_zoom += 0.01
                if event.button == pygame.BUTTON_WHEELUP:
                    window.view_zoom -= 0.01
                window.mouse_up(event.button)
            if event.type == pygame.BUTTON_WHEELUP:
                window.mouse_scroll(-10)
            if event.type == pygame.BUTTON_WHEELDOWN:
                window.mouse_scroll(10)

        viewport.fill((11, 12, 13))
        window.screen.fill(dark_gray)
        # We do a little rendering

        pygame.draw.rect(window.screen, light_gray, (0, 0, window.screen.get_width(), 25))
        window.screen.blit(font.render('SAVE', True, (255, 255, 255)), (5, 3))
        window.screen.blit(font.render('LOAD', True, (255, 255, 255)), (50, 3))
        window.screen.blit(font.render('EDIT', True, (255, 255, 255)), (95, 3))
        pygame.draw.rect(window.screen, light_gray,
                         (0, window.screen.get_height() - 25, window.screen.get_width(), 25))
        window.screen.blit(font.render(
            f'Mouse Position: {window.get_mouse_pos()} Tile Position:"'
            f' {get_grid_pos(*window.get_viewport_mouse(), grid_size, window)} Active Tile: {window.active_piece}'
            f' Zoom Level: {window.view_zoom}',
            True, (255, 255, 255)), (5, window.screen.get_height() - 25))

        target_res = grid_size * window.view_zoom
        for ind, i in enumerate(window.level.floor_pieces):
            if window.level.piece_dict[i] is not None:
                pos = ((((ind % window.level.length) * grid_size) + window.get_offset().x) * window.view_zoom,
                       (((ind // window.level.length) * grid_size) + window.get_offset().y) * window.view_zoom)
                piece = pygame.transform.scale(window.level.piece_dict[i], (target_res, target_res))
                viewport.blit(piece, pos)

        for ind, x in enumerate(window.level.piece_dict.items()):
            pid, i = x

            if i is None:
                i = pygame.image.load('assets/Tiles/EraserIcon.png').convert_alpha()
            window.screen.blit(i, (10, 85 * ind + 30))
            window.screen.blit(font.render(str(pid), True, (255, 255, 255)), (10, 85 * ind + 95))

        window.screen.blit(viewport, (window.screen.get_width() - viewport.get_width(), 25))

        for dialog in window.dialogs:
            dialog.render()

        # Debug Render Here
        pos = get_grid_pos(*window.get_viewport_mouse(), grid_size, window)
        pygame.draw.rect(viewport, (255, 255, 255),
                         list(get_screen_pos(*pos, grid_size, window)) + [target_res, target_res], 0)
        hovered_button = window.get_hovered_button()
        if hovered_button is not None:
            pygame.draw.rect(window.screen, (255, 255, 255), hovered_button.rect, 3)
        else:
            pygame.draw.rect(window.screen, (255, 255, 255),
                             window.get_button_by_id(f'LDButton{window.active_piece}').rect, 3)

        # Controls
        if window.left_click:
            pos = get_grid_pos(*window.get_viewport_mouse(), grid_size, window)
            if -1 < pos[0] < window.level.length and -1 < pos[1] < window.level.height \
                    and window.get_hovered_button() is None:
                window.level.floor_pieces[pos[0] + pos[1] * window.level.length] = window.active_piece

        clock.tick(60)

        window.render()
        pygame.display.update()


if __name__ == "__main__":
    main()
