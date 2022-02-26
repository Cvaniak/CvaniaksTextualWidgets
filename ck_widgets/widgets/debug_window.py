from __future__ import annotations

import sys
from rich.console import RenderableType
from rich.segment import Segment
import textual
from textual.reactive import Reactive
from textual.widget import Widget

from rich import box
from rich.align import Align
from rich.panel import Panel
from rich.pretty import Pretty
from rich.text import Text
from textual.message import Message


class DebugStatus(Message):
    def __init__(self, sender: Widget, mes: str):
        super().__init__(sender)
        self.mes = mes


class DebugWindow(Widget):
    last_info: Reactive = Reactive("")
    debug: Reactive = Reactive("")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def render(self) -> RenderableType:
        # OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]

        return Panel(
            self.debug,
            title="Debug Window",
            style="yellow",
            box=box.HEAVY,
            border_style="red",
        )
