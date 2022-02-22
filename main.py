from rich import align
from textual.app import App
from textual.views import GridView
from textual.widgets import Footer, Header, Placeholder
from textual import events

from textual.app import App

from pixelart_tui.my_messages import DebugStatus
from pixelart_tui.my_widgets import (
    StatusWidget,
)
from ck_widgets import ProgressBarV, ProgressBarH
from ck_widgets import create_gradient


class Layout(GridView):
    def __init__(
        self,
        w: int,
        h: int,
        status: StatusWidget,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.w = w
        self.h = h
        self.status = status

    def on_mount(self) -> None:
        # Attributes to store the current calculation
        self.grid.set_gap(2, 1)
        self.grid.set_gutter(1)
        self.grid.set_align("center", "center")

        # Create rows / columns / areas
        self.grid.add_column("col", repeat=2)
        self.grid.add_row("row", repeat=2)
        self.grid.add_areas(status="col1,row1")
        self.grid.add_areas(pb_h="col1,row2")
        self.grid.add_areas(pb_v="col2,row1")
        self.grid.add_areas(pb_h1="col2,row2")
        gradient = create_gradient("red", "green", 28)
        gradient2 = create_gradient("rgb(39, 75, 123)", "rgb(200, 100, 10)", 28)

        pb_h = ProgressBarH(color=["white", "black"])
        pb_v = ProgressBarV(color=gradient2, width=7)
        p1 = ProgressBarH(
            color=gradient,
            label="test",
            label_align="left",
            border_style="red",
            height=5,
            width=30,
        )
        a1 = Placeholder(height=5)
        self.status.debug = str(gradient)
        # Place out widgets in to the layout
        self.grid.place(status=self.status)
        self.grid.place(pb_v=pb_v)
        self.grid.place(pb_h=pb_h)
        self.grid.place(pb_h1=p1)


class SimpleApp(App):
    async def on_load(self, _: events.Load) -> None:
        await self.bind("q", "quit", "Quit")
        await self.bind("r", "reset()", "Reset")

    async def on_mount(self) -> None:
        w, h = 64, 64
        self.status = StatusWidget()

        self.layout = Layout(
            w,
            h,
            self.status,
        )

        style_fh = "white on rgb(111,22,44)"
        await self.view.dock(Header(style=style_fh), edge="top")
        # Fix style of footer
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.layout, edge="left")

    async def handle_debug_status(self, message: DebugStatus):
        self.status.debug = message.mes


if __name__ == "__main__":
    SimpleApp.run()
