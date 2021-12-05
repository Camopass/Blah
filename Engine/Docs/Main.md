# Compass Engine

> Compass Engine, a game framework made in Python and Pygame designed for Blah.
> Compass Engine has many helpful features such as the Window class. 


### Windows in Compass Engine

> `def __init__(self, width, height, caption: str = "PyGame Engine", icon_path=None):`
> 
> **Width** and **Height** parameters determine the default width and height of the window.
> In Compass Engine, the windows are automatically resized while maintaining aspect ratio.
> This also determines the base resolution that will be resized to fit the window.
> 
> **Caption** is a parameter determining the Window Title. This is the text displayed at the top of the window.
> 
> **icon_path** is a path to the icon used for the window. This cannot be an image, as the display mode must be set first.

**Examples:**
```
window = Window(500, 800, "Example Window!", "icon.png")
```
From this, you would simply use this like a normal pygame application.

**Blit to display**
> To blit to the display using Compass Engine, you use `window.screen.blit()` instead of `pygame.display.get_surface()`.
> This blits to the window's **screen** surface instead of directly to the display.
> This is resized to fit the window size allowing any size window with little effort.
> You must call `window.render()` before `pygame.display.update()` 

**Fullscreen**
> To set the display mode to fullscreen, simply use `window.fullscreen()` and `window.windowed()` to revert back.
>  **screen** resolution will stay constant. All resizing is managed by Compass Engine.

**Mouse Position**
> Compass Engine does not work with the normal `pygame.mouse.get_pos()`. This returns an incorrect value for the mouse position due to window resizing.
> You can use `window.get_mouse_pos()` to return the correct mouse position on the **screen**. This will always be within the dimensions of the **screen**
> You can also use `window.get_transforms()` to transform a display position to a **screen** position.

**Entity and Object managers**
> Entity Managers will be explained later, but when you are using them, you can use `window.render_managers()` to render them to the **screen**.

### Scenes in Compass Engine
> Scenes are a nice way to contain different areas of your game. This is most likely to be used for things like a Title Screen and the Main Game.
> Scenes allow you to have different rendering, tick, and setup methods.
> While these are mostly nonfunctional, it is nice to separate them.
> 
> Render is for rendering things, tick is a per-frame update. Basically what you would put in the `while True` loop.
> Setup is any setup done before running the scene's code.
> 
> _TO SWITCH SCENES, USE `scene.next_scene = Scene(self.window, self.clock)`_

**Examples:**
```
clock = pygame.time.Clock()

class TitleScreen(Scene):
    def setup(self):
        self.text = "Hi!"
        
    def tick(self):
        pass
    
    def render(self):
        self.window.screen.blit(pygame.font.render(self.text, True, (255, 255, 255)), (20, 20))
        
scene = TitleScreen(window, clock)
```

### EXAMPLE OF EVENT LOOP

This stuff must be done manually.

```
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        p.close()
        running = False
    if event.type == pygame.VIDEORESIZE:
        window.window_surface = pygame.display.set_mode(size=(event.w, event.h), flags=pygame.RESIZABLE)
        window.update_resize()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == pygame.BUTTON_RIGHT:
            window.right_click = True
        if event.button == pygame.BUTTON_LEFT:
            window.left_click = True
        window.mouse_down(event.button)
        scene.mouse_up(event.button)
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == pygame.BUTTON_RIGHT:
            window.right_click = False
        if event.button == pygame.BUTTON_LEFT:
            window.left_click = False
        window.mouse_up(event.button)
        scene.mouse_up(event.button)
    if event.type == pygame.KEYDOWN:  # Fullscreen by pressing F11
        if event.key == pygame.K_F11:
            window.windowed() if window.is_fullscreen else window.fullscreen()
        if event.key == pygame.K_F12:
            dir = os.environ["USERPROFILE"] + f"/Desktop/{datetime.date.today()}.png"
            pygame.image.save(window.screen, dir)
```
