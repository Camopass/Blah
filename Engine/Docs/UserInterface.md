### User Interface
> User Interface Classes for easy UI stuff.

# render_text_in_rect
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

# UIElement
> UI Element is a UI Background renderer. This will take an image such as ![UIE Image](https://github.com/Camopass/Blah/raw/master/assets/UI/Button.png)
> and stretch it in a way that looks nice. You would create one like this:
```
ui = UIElement(image, 30)  # Image is a pygame surface, 30 is the size of the image. Image must be 1:1 AR with a width divisible by 3
window.screen.blit(ui.render(3, 5, 10), (200, 500))  # 3, 5 is the size of the UI element. This will be the width and height.
# The UIElement.render() method takes 2 required args, width and height, which determines the amount of tiles used.
Scaling determines what it should upscale the image by. The return will be a pygame Surface with the dimensions equal to
((size / 3) * width * scaling, (size / 3) * height * scaling)
```

# Notice
> A notice is a UIElement with text.

# I WILL FINISH THIS TOMORROW
