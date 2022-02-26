from rich.color import Color, blend_rgb
from typing import List, Union
from functools import lru_cache

from rich.color_triplet import ColorTriplet

CColor = Union[Color, str]

def ccolor_to_color_triplet(color: CColor) -> ColorTriplet :
    if isinstance(color, str):
        tri = Color.parse(color)
        tri = tri.get_truecolor()
    else:
        tri = color.get_truecolor()
    return tri


def create_gradient(color_a: CColor, color_b: CColor, n) -> List[CColor]:
    a = ccolor_to_color_triplet(color_a)
    b = ccolor_to_color_triplet(color_b)

    return [Color.from_triplet(blend_rgb(a, b, x / n)) for x in range(n)]


class CustomColor:
    __auto_size: bool = False
    def __init__(self, color_list: List[CColor], repeat = True):
        self.color_list = color_list
        self.repeat = repeat

    def __getitem__(self, index:int):
        return self.color_list[index]

    def __setitem__(self, index:int, value:CColor):
        self.color_list[index] = value

    def __get__(self, instance, owner):
        return self.color_list

    @lru_cache
    def get_color(self, index, max_size: Union[int,None] = None):
        if self.__auto_size and len(self.color_list) == 2: 
            a, b = self.color_list
            a, b = ccolor_to_color_triplet(a), ccolor_to_color_triplet(b)
            return Color.from_triplet(blend_rgb(a, b, index/max_size))
        if self.repeat:
            return self.color_list[index%len(self.color_list)]
        else:
            mx = max(index, len(self.color_list))
            return self.color_list[mx]

    @classmethod
    def gradient(
        cls,
        color_a: CColor,
        color_b: CColor,
        n: Union[int,None] = None,
        repeat: bool = True
    ) -> "CustomColor":
        
        if n is None:
            auto_size = True
            color_list: List[CColor] = [color_a, color_b]
        else:
            auto_size = False
            color_list: List[CColor] = create_gradient(color_a, color_b, n)


        new_obj =  cls(
            color_list,
            repeat = repeat
        )
        new_obj.__auto_size = auto_size
        return new_obj


