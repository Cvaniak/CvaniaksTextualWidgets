from __future__ import annotations

import sys
from rich.console import RenderableType
import textual
from textual.reactive import Reactive
from textual.widget import Widget

from rich.align import Align
from rich.panel import Panel
from textual.message import Message


class DebugStatus(Message):
    def __init__(self, sender: Widget, mes: str):
        super().__init__(sender)
        self.mes = mes


class StatusWidget(Widget):
    alive: Reactive = Reactive(True)
    points: Reactive = Reactive(0)
    pos: Reactive = Reactive((0, 0))
    debug: Reactive = Reactive("")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def render(self) -> RenderableType:
        w = (
            f"Alive: [b red]{self.alive}[/b red] :red_heart:"
            f"\n\n"
            f"Points: [b red]{self.points}[/b red] :glowing_star:"
            f"\n\n"
            f"Pos: [b red]{self.pos}[/b red]"
            f"\n\n"
            f"[b blue]{self.debug}[/b blue]"
        )
        return Panel(
            Align.center(
                w,
                vertical="middle",
            ),
            title="Status",
            style="yellow",
        )
