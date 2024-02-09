
import logging
from PIL import Image, ImageDraw
import board
import adafruit_ssd1306

i2c = board.I2C()

class OLEDDisplay:
    """ Display info on the I2C OLED screen """
    def __init__(self):
        self.pixels_size = (128, 64)
        ...
        self.app_logo = Image.open("bunny.png").convert('1')
        if adafruit_ssd1306 is not None and i2c is not None:
            self.oled = adafruit_ssd1306.SSD1306_I2C(self.pixels_size[0],
                                                     self.pixels_size[1],
                                                     i2c)
        else:
            self.oled = None        

    def add_line(self, text: str):
        """ Add new line with scrolling """

    def add_tokens(self, text: str):
        """ Add new tokens with or without extra line break """

    def draw_record_screen(self, text: str):
        """ Draw logo and text """
        logging.debug(f"Draw_record_screen: \033[0;31m{text}\033[0m")
        if self.oled is None:
            return

        image = Image.new("1", self.pixels_size)
        img_pos = (self.pixels_size[0] - self.image_logo.size[0])//2
        image.paste(self.image_logo, (img_pos, 0))
        draw = ImageDraw.Draw(image)
        text_size = self._get_text_size(text)
        txt_pos = (self.pixels_size[0]//2 - text_size[0]//2,
                   self.pixels_size[1] - text_size[1])
        draw.text(txt_pos, text, font=self.font, fill=255, align="center")

        self._draw_image(image)

    def _get_text_size(self, text):
        """ Get size of the text """
        _, descent = self.font.getmetrics()
        text_width = self.font.getmask(text).getbbox()[2]
        text_height = self.font.getmask(text).getbbox()[3] + descent
        return (text_width, text_height)

    def _draw_image(self, image: Image):
        """ Draw image on display """