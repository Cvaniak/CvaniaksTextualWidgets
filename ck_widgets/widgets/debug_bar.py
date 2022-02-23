from __future__ import annotations

import sys
from rich.console import RenderableType
import textual
from textual.reactive import Reactive
from textual.widget import Widget

from rich.align import Align
from rich.panel import Panel
from rich.pretty import Pretty
from textual.message import Message


class DebugStatus(Message):
    def __init__(self, sender: Widget, mes: str):
        super().__init__(sender)
        self.mes = mes


class StatusWidget(Widget):
    last_info: Reactive = Reactive("")
    debug: Reactive = Reactive({})

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def render(self) -> RenderableType:
        # OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]

        return Panel(
            Pretty(self.debug),
            title="Status",
            style="yellow",
        )
