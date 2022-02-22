from __future__ import annotations

import sys
from rich.console import RenderableType
from rich.style import StyleType, Style
from rich.color import Color, blend_rgb
from rich.align import AlignMethod
from rich.text import TextType, Text

from textual.reactive import Reactive
from textual.widget import Widget
from textual import events
from textual.message import Message, MessageTarget

from rich.panel import Panel
from rich.box import Box, ROUNDED

from typing import Optional
from typing import List
from . import DebugStatus

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


def minmax(a, mn, mx):
    return max(min(mx, a), mn)


# TODO: Emit
# Horizontal or Vertical
# Box or without box
# With label or without label
# Display value outside
# Display value inside
# Height from value or map value
# Style
# Gradient color
# Full custom color
# border color
# Text color
# On hover color change

# style
# # Box type or none
# # Border color
# # Text
# label
# label_position
# height
# width
# value == size
# size == value


LabelPosition = Literal["top", "bottom"]


def create_gradient(color_a: Color | str, color_b: Color | str, n) -> List[Color]:
    if isinstance(color_a, str):
        a = Color.parse(color_a)
        a = a.get_truecolor()
    else:
        a = color_a.get_truecolor()
    if isinstance(color_b, str):
        b = Color.parse(color_b)
        b = b.get_truecolor()
    else:
        b = color_b.get_truecolor()

    return [Color.from_triplet(blend_rgb(a, b, x / n)) for x in range(n)]


class ProgressBarChange(Message):
    def __init__(self, sender: MessageTarget) -> None:
        super().__init__(sender)


class _ProgressBar(Widget):
    is_mouse_down: Reactive = Reactive(False)
    value: Reactive = Reactive(0)
    fill: Reactive = Reactive(0)

    def __init__(
        self,
        start_value: int = 0,
        color: Optional[str | Color | List[Color | str]] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        label: Optional[TextType] = None,
        label_align: AlignMethod = "center",
        label_position: LabelPosition = "top",
        border_style: Optional[StyleType] = "none",
        box: Box = ROUNDED,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.color = color
        self.value = start_value
        self.fill = start_value
        self._width = width
        self._height = height
        self.label = label
        self.label_align: AlignMethod = label_align
        self.label_position = label_position
        self.border_style = border_style
        self.box = box

    @property
    def width(self) -> int:
        return self._width or self._size.width

    @property
    def height(self) -> int:
        return self._height or self._size.height

    @property
    def _max_width(self) -> int:
        return min(self._size.width, self.width) - 4

    @property
    def _max_height(self) -> int:
        return min(self._size.height, self.height) - 2

    @property
    def _fill_width(self) -> int:
        return self._max_width

    @property
    def _fill_height(self) -> int:
        return self.fill

    @property
    def _max_fill(self):
        return self._max_height

    def _color_xy(self, x, y):
        if isinstance(self.color, list):
            w = y % len(self.color)
            return self.color[w]
        else:
            return self.color

    def _mouse_axis(self, event) -> int:
        return event.y

    def update(self, value):
        self.value = value
        self.fill = value * self._size.height // 255

    def render_fill(self) -> Text:
        text = Text()
        for h in range(self._fill_height):
            for w in range(self._fill_width):
                color = self._color_xy(w, h)
                text.append("█", style=Style(color=color))
            text.append("\n")
        return text

    def render(self) -> RenderableType:
        bar = ""
        for _ in range(self._fill_height):
            for _ in range(self._fill_width):
                bar += "█"
            bar += "\n"
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
            border_style=self.border_style,
            box=self.box,
            height=self.height,
            width=self.width,
        )

    async def on_mouse_down(self, event: events.MouseDown) -> None:
        self.fill = minmax(self._mouse_axis(event) - 1, 0, self._max_fill)
        self.value = self.fill
        self.is_mouse_down = True
        await self.emit(ProgressBarChange(self))

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        if self.is_mouse_down:
            self.fill = minmax(self._mouse_axis(event) - 1, 0, self._max_fill)
            await self.emit(ProgressBarChange(self))
        await self.emit(DebugStatus(self, self.color))

    async def on_mouse_up(self, event: events.MouseUp):
        if self.is_mouse_down:
            self.fill = minmax(self._mouse_axis(event) - 1, 0, self._max_fill)
            self.value = self.fill
            self.is_mouse_down = False
            await self.emit(ProgressBarChange(self))

    async def on_leave(self, event: events.Leave):
        self.value = self.fill
        self.is_mouse_down = False
        await self.emit(ProgressBarChange(self))


class ProgressBarV(_ProgressBar):
    ...


class ProgressBarH(_ProgressBar):
    @property
    def _fill_width(self) -> int:
        return self.fill

    @property
    def _fill_height(self) -> int:
        return self._max_height

    def _mouse_axis(self, event) -> str:
        return event.x

    @property
    def _max_fill(self):
        return self._max_width

    def _color_xy(self, x, y):
        if isinstance(self.color, list):
            w = x % len(self.color)
            return self.color[w]
        else:
            return self.color
