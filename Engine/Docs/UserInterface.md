# User Interface
> User Interface Classes for easy UI stuff.

### render_text_in_rect
> `def render_text_in_rect(font: pygame.font.Font, text: str, dim: typing.Tuple[int, int], *, line_spacing=3, color=(255, 255, 255)): -> pygame.Surface`
> **font** determines the font renderer used
> 
> **text** is the text that is being rendered.
> 
> **dim** is the width and height the text is constrained to.
> 
> **line_spacing** determines the width of line spaces.
> 
> **color** is the text color

> This will render text with auto wrapping into a certain width and height. This returns a `pygame.Surface` object with the text on it.

### UIElement
> `UIElement` is a UI Background renderer. This will take an image such as ![UIE Image](https://github.com/Camopass/Blah/raw/master/assets/UI/Button.png)
> and stretch it in a way that looks nice. You would create one like this:
> ```
> ui = UIElement(image, 30)  # Image is a pygame surface, 30 is the size of the image. Image must be 1:1 AR with a width divisible by 3
> window.screen.blit(ui.render(3, 5, 10), (200, 500))  # 3, 5 is the size of the UI element. This will be the width and height.
> # The UIElement.render() method takes 2 required args, width and height, which determines the amount of tiles used.
> Scaling determines what it should upscale the image by. The return will be a pygame Surface with the dimensions equal to
> ((size / 3) * width * scaling, (size / 3) * height * scaling)
> ```

### Notice
> A notice is a UIElement with text.

> `def __init__(self, image, length, text):`
> **image** is the image used to create the background. This is the same as in `UIElement`.
> **length** is also the same as in `UIElement`.
> **text** is the text rendered in the notice.
> ```
> notice = Notice(image, 30, "Hello, World!")
> 
> ...
> 
> window.screen.blit(notice.render(5, 3, font, scaling=10)
> ```

### Base Button
> Base button is a button class that is used to create simple buttons.
> There is no manager yet, examples for a basic one will be shown below.
> `def __init__(self, rect, image):`
> **rect** is a `pygame.Rect` that describes the position and size of the button.
> **image** is the `pygame.Surface` that is displayed.
> ```
> button = BaseButton(pygame.Rect(20, 50, 60, 40), image)
> 
> def on_click(window):
>     print("Button Pressed!")
> 
> button.on_click = on_click
> 
> # Detecting Clicks
> 
> def mouse_up(self, button):
>     if button == pygame.BUTTON_LEFT:
>         for button in self.buttons:
>             if button.rect.collidepoint(self.window.get_mouse_pos()):
>                 button.on_click(self.window)
> ```
