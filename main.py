from rich import align
from textual.app import App
from textual.reactive import Reactive
from textual.views import GridView, WindowView, DockView
from textual.layouts.vertical import VerticalLayout
from textual.widgets import Footer, Header, Placeholder
from textual.widget import Widget
from textual import events

from textual.app import App

from ck_widgets.widgets import ProgressBarChange
from ck_widgets.widgets import ProgressBarV, ProgressBarH
from ck_widgets.widgets import create_gradient
from ck_widgets.widgets import StatusWidget, DebugStatus


def create_horizontal():
    gradient = create_gradient("red", "green", 28)
    gradient2 = create_gradient("rgb(39, 75, 123)", "rgb(200, 100, 10)", 119)
    l = {
        "r1": ProgressBarH(color=["white", "black"]),
        "r2": ProgressBarH(
            color=gradient,
            label="test",
            label_align="left",
            border_style="red",
            height=5,
            width=30,
        ),
        "r3": ProgressBarH(
            color=gradient2,
            label="Another Test",
            label_align="right",
            border_style="blue",
            height=5,
        ),
        "r4": ProgressBarH(),
        "r5": ProgressBarH(),
    }
    return l


def create_vertical():
    gradient = create_gradient("red", "green", 28)
    gradient2 = create_gradient("rgb(39, 75, 123)", "rgb(200, 100, 10)", 28)
    l = {
        "c1": ProgressBarV(color=["white", "black"]),
        "c2": ProgressBarV(
            color=gradient,
            label="test",
            label_align="left",
            border_style="red",
            height=5,
            width=30,
        ),
        "c3": ProgressBarV(
            color=gradient,
            label="Another Test",
            label_align="right",
            border_style="blue",
            height=5,
        ),
        "c4": ProgressBarV(),
        "c5": ProgressBarV(),
    }
    return l


class Layout(GridView):
    def __init__(
        self,
        status,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.status = status

    async def on_mount(self) -> None:
        # Attributes to store the current calculation
        self.grid.set_gap(2, 1)
        self.grid.set_gutter(1)
        self.grid.set_align("center", "center")

        # Create rows / columns / areas
        self.grid.add_column("col", fraction=10)
        self.grid.add_column("cl", repeat=6, fraction=1)
        self.grid.add_row("row", fraction=3)
        self.grid.add_row("rw", fraction=1, repeat=5)

        self.grid.add_areas(st="col,row")
        self.grid.place(st=self.status)

        for i in range(1, 7):
            self.grid.add_areas(**{f"r{i}": f"col,rw{i}"})
        for i in range(1, 6):
            self.grid.add_areas(**{f"c{i}": f"cl{i},row-start|rw3-end"})

        self.grid.place(**create_horizontal())
        self.grid.place(**create_vertical())
        # self.grid.place(r1=Placeholder())


class SimpleApp(App):
    debug: Reactive[dict] = Reactive({})

    async def on_load(self, _: events.Load) -> None:
        await self.bind("q", "quit", "Quit")
        await self.bind("r", "reset()", "Reset")

    async def on_mount(self) -> None:

        self.status = StatusWidget()
        self.layout = Layout(self.status)
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.layout, edge="left")

    async def handle_debug_status(self, message: DebugStatus):
        self.status.debug = message.mes

    async def handle_progress_bar_change(self, message: ProgressBarChange):
        self.debug[message.sender.name] = (
            message.fill,
            message.value,
            message.max_value,
        )
        self.status.debug = self.debug
        self.status.refresh()


if __name__ == "__main__":
    SimpleApp.run()
