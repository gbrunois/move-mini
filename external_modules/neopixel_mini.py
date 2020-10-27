from neopixel import NeoPixel as AdaNeoPixel
import time

ColorRGB = (int, int, int)

class NeoPixel:

    def __init__(self, pixels: AdaNeoPixel) -> None:
        self._pixels = pixels
        self.num_pixels = len(pixels)

    def set_all_color(self, color: ColorRGB):
        for i in range(self.num_pixels):
            self._pixels[i] = color

    def show_color(self, color: ColorRGB):
        self.set_all_color(color)
        self._pixels.show()

    def set_pixel_color(self, position: int, color: ColorRGB):
        self._pixels[position] = color
        
    def show(self) -> None:
        self._pixels.show()


class NeoPixelEffects:

    def __init__(self, neopixel: NeoPixel) -> None:
        self._neopixel = neopixel

    @staticmethod
    def wheel(pos) -> ColorRGB:
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return r, g, b

    def rainbow_cycle(self, wait: float):
        for j in range(256):
            for i in range(self._neopixel.num_pixels):
                pixel_index = (i * 256 // self._neopixel.num_pixels) + j
                self._neopixel.set_pixel_color(i, self.wheel(pixel_index & 255))
            self._neopixel.show()
            time.sleep(wait)

    @staticmethod
    def hsl(h: int, s: int, l: int) -> ColorRGB:
        """
        :param h: Hue from 0 to 359
        :param s: Saturation from 0 to 99
        :param l: Luminance from 0 to 99
        """
        def hsl2rgb(_h: float, _x: float, _c: float):
            if 0 <= _h < 60:
                return _c, _x, 0
            if 60 <= _h < 120:
                return _x, _c, 0
            if 120 <= _h < 180:
                return 0, _c, _x
            if 180 <= _h < 240:
                return 0, _x, _c
            if 240 <= _h < 300:
                return _x, 0, _c
            if 300 <= _h < 360:
                return _c, 0, _x

        s = s / 100.0
        l = l / 100.0

        chroma = (1.0 - abs(2.0 * l - 1.0)) * s
        x = chroma * (1.0 - abs((h/60.0) % 2.0 - 1.0))
        m = l - chroma / 2.0

        r, g, b = hsl2rgb(h, x, chroma)
        return round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)

    # TODO Add ease quadratic functions
