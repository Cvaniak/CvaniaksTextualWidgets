from __future__ import annotations

import sys
from rich.console import RenderableType
from rich.style import StyleType, Style
from rich.color import Color, blend_rgb
from rich.align import AlignMethod
from rich.text import TextType, Text
from textual.geometry import Size

from textual.reactive import Reactive
from textual.widget import Widget
from textual import events
from textual.message import Message, MessageTarget

from rich.panel import Panel
from rich.box import Box, ROUNDED
from rich.repr import Result

from typing import Optional
from typing import List, Tuple, Union

from ck_widgets.color import CColor, CustomColor

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


def minmax(a, mn, mx):
    return max(min(mx, a), mn)


LabelPosition = Literal["top", "bottom"]


class ValueBarChange(Message):
    def __init__(self, sender: _ValueBar) -> None:
        super().__init__(sender)
        self.value = sender.value
        self.fill = sender.fill
        self.max_value = sender._max_value


class _ValueBar(Widget):
    """
    ValueBar Base classc
    """

    is_mouse_down: Reactive = Reactive(False)
    value: Reactive = Reactive(0)
    fill: Reactive = Reactive(0)

    def __init__(
        self,
        name: str | None = None,
        start_value: int = 0,
        max_value: int | None = None,
        reversed: bool = False,
        instant: bool = False,
        color: Optional[Union[CColor, List[CColor], CustomColor]] = None,
        bg_color: Optional[Union[CColor, List[CColor], CustomColor]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        label: Optional[TextType] = None,
        label_align: AlignMethod = "center",
        label_position: LabelPosition = "top",
        padding: Tuple[int, int] = (0, 0),
        border_style: StyleType = "none",
        box: Box = ROUNDED,
    ) -> None:
        """ValueBar constructor

        ValueBar in two flavours -> Horizontal `ValueBarH` and Vertical `ValueBarV`.
        It needs at lest max_value or width/height. `max_value` have bigger priority.

        Args:
            name: Widget uniqe name
            start_value: Value that will appears after widget initialization
            max_value: Maximal value that also defines size of widget
            (it overides width for Horizontal and hight for Vertical)
            reversed: Reverse direction of progress
            instant: If update should be after mouse release or not
            color: Color of progress in bar. Can be setup as list of colors
            bg_color: Background color of progress in bar. Can be setup as (`List[Color]`)
            width: Width of widget
            height: Height of widget
            label: Text displayed in Panel's border
            label_align: Alignment of label -> left, center, right
            label_postion: Top or Bottom for now
            padding: Padding between value part and border
            border_style: Border style
            box: Rich's box type

        """
 
        super().__init__(name=name)
        self.color = color
        self.bg_color = bg_color
        self.label = label
        self.label_align: AlignMethod = label_align
        self.label_position = label_position
        self._border_style = border_style
        self.box = box
        self.reversed = reversed
        self.instant = instant
        self._padding: Tuple[int, int] = padding

        self._set_size_and_values(start_value, max_value, width, height)

    def __rich_repr__(self) -> Result:
        yield self.name
        yield self.fill, self.value, self._max_value

    def __repr__(self):
        return f"{self.fill}, {self.value}"

    def _set_size_and_values(self, start_value, max_value, width, height):
        if max_value:
            self._height = max_value+self._padding[0]*2+2
        elif height:
            self._height = height
        else:
            raise KeyError("max_value or height must be filled")

        self.value = minmax(start_value, 0, self._max_value)
        self.fill = self.value
        self._width = width

    @property
    def width(self) -> int:
        return self._width or self._size.width

    @property
    def height(self) -> int:
        return self._height or self._size.height

    @property
    def _max_width(self) -> int:
        return self.width - 2 - self._padding[1] * 2

    @property
    def _max_height(self) -> int:
        return self.height - 2 - self._padding[0] * 2

    @property
    def _fill_width(self) -> int:
        return self._max_width

    @property
    def _fill_height(self) -> int:
        return self.fill

    @property
    def _max_value(self):
        return self._max_height

    def _color_direction(self, _, y):
        return y

    def _color_xy(self, x, y, bg=False):
        if bg:
            color = self.bg_color
        else:
            color = self.color

        if isinstance(color, list):
            w = self._color_direction(x, y) % len(color)
            return color[w]
        elif isinstance(color, CustomColor):
            w = self._color_direction(x, y)
            return color.get_color(w, self._max_value)
        else:
            return color

    def _mouse_axis(self, event) -> int:
        y = event.y
        pad = self._padding[0]
        if y < pad: 
            return 0
        if y >= self._max_value + pad:
            return self._max_value
        return y-pad

    def update(self, value):
        self.value = value
        self.fill = value * self._size.height // 255

    def render_fill(self) -> Text:
        text = Text()
        r1 = self._fill_height
        first = "█"
        second = " "
        if self.reversed:
            r1 = self._max_value - r1
            first, second = second, first

        for h in range(r1):
            for w in range(self._fill_width):
                color = self._color_xy(w, h)
                bg_color = self._color_xy(w, h, bg=True)
                text.append(first, style=Style(color=color, bgcolor=bg_color))
            text.append("\n")
        for h in range(r1, self._max_value):
            for w in range(self._fill_width):
                bg_color = self._color_xy(w, h, bg=True)
                text.append(second, style=Style(bgcolor=bg_color))
            text.append("\n")
        return text

    def render(self) -> RenderableType:
        bar = self.render_fill()

        title = None
        subtitle = None
        if self.label_position == "top":
            title = self.label
        elif self.label_position == "bottom":
            subtitle = self.label

        return Panel(
            bar,
            title=title,
            title_align=self.label_align,
            subtitle=subtitle,
            subtitle_align=self.label_align,
            style=self._border_style,
            box=self.box,
            height=self.height,
            width=self.width,
            padding=self._padding,
            expand=False,
        )

    def set_fill(self, event):
        mouse_axis = self._mouse_axis(event)
        mn_mx = minmax(mouse_axis, 0, self._max_value)
        if self.reversed:
            self.fill = self._max_value - mn_mx
        else:
            self.fill = mn_mx

    async def on_mouse_down(self, event: events.MouseDown) -> None:
        self.set_fill(event)
        self.value = self.fill
        self.is_mouse_down = True
        await self.emit(ValueBarChange(self))

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        if self.is_mouse_down:
            self.set_fill(event)
            if self.instant:
                self.value = self.fill
            await self.emit(ValueBarChange(self))

    async def on_mouse_up(self, event: events.MouseUp):
        if self.is_mouse_down:
            self.set_fill(event)
            self.value = self.fill
            self.is_mouse_down = False
            await self.emit(ValueBarChange(self))

    async def on_leave(self, event: events.Leave):
        self.value = self.fill
        self.is_mouse_down = False
        await self.emit(ValueBarChange(self))


class ValueBarV(_ValueBar):
    """
    ValueBar Vertical
    """
    ...


class ValueBarH(_ValueBar):
    """
    ValueBar Horizontal
    """

    def _set_size_and_values(self, start_value, max_value, width, height):
        if max_value:
            self._width = max_value
        elif width:
            self._width = width
        else:
            raise KeyError("max_value or width must be filled")
        self._size = Size(self._width, self._size.height)

        self.value = min(start_value, self._max_width)
        self.fill = self.value
        self._height = height

    @property
    def _fill_width(self) -> int:
        return self.fill

    @property
    def _fill_height(self) -> int:
        return self._max_height

    def _mouse_axis(self, event) -> int:
        x = event.x
        pad = self._padding[1]
        if x < pad: 
            return 0
        if x >= self._max_value + pad:
            return self._max_value
        return x-pad


    @property
    def _max_value(self):
        return self._max_width

    def _color_direction(self, x, _):
        return x

    def render_fill(self) -> Text:
        text = Text()
        r1 = self._fill_width
        first = "█"
        second = " "
        if self.reversed:
            r1 = self._max_value - r1
            first, second = second, first
        for h in range(self._fill_height):
            for w in range(0, r1):
                color = self._color_xy(w, h)
                bg_color = self._color_xy(w, h, True)
                text.append(first, style=Style(color=color, bgcolor=bg_color))
            for w in range(r1, self._max_value):
                color = self._color_xy(w, h)
                bg_color = self._color_xy(w, h, True)
                text.append(second, style=Style(color=color, bgcolor=bg_color))
            text.append("\n")
        return text
