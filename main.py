from typing import List
from rich import align
from textual.app import App
from textual.reactive import Reactive
from textual.views import GridView, WindowView, DockView
from textual.layouts.vertical import VerticalLayout
from textual.widgets import Footer, Header, Placeholder
from textual.widget import Widget
from textual import events

from textual.app import App
from rich import box
from rich.color import Color


from ck_widgets.widgets import ValueBarChange
from ck_widgets.widgets import ValueBarV, ValueBarH
from ck_widgets.widgets import DebugWindow, DebugStatus
from ck_widgets.color import CustomColor, create_gradient


def create_horizontal():
    red_green_40 = CustomColor.gradient("red", "green")
    blue_orange_121 = CustomColor.gradient("rgb(39, 75, 123)", "rgb(200, 100, 10)")
    red_and_white_black_100 = create_gradient("white", "black", 100)
    red_and_white_black_100[:5] = ["red"] * 5
    black_blue_121 = CustomColor.gradient("black", "blue", 121)
    l = {
        "r1": ValueBarH(max_value=30),
        "r2": ValueBarH(
            label="Heavy box, two colors, one after another, reversed",
            color=["white", "black"],
            bg_color=["green", "blue"],
            max_value=80,
            start_value=40,
            box=box.HEAVY,
            reversed=True,
        ),
        "r3": ValueBarH(
            color=red_green_40,
            bg_color="yellow",
            start_value=20,
            label="short",
            label_align="left",
            border_style="red",
            height=3,
            width=40,
        ),
        "r4": ValueBarH(
            color=blue_orange_121,
            label="Reversed and instant",
            instant=True,
            label_align="right",
            label_position="bottom",
            border_style="blue",
            start_value=55,
            width=70,
            reversed=True,
        ),
        "r5": ValueBarH(
            color=red_and_white_black_100,
            label="Ugly but with background",
            label_align="center",
            label_position="bottom",
            border_style="black on white",
            start_value=80,
            width=200,
            max_value=100,  # Max value overide width
            padding=(0, 3),
        ),
        "r6": ValueBarH(
            color=black_blue_121,
            label="Full range",
            label_align="right",
            label_position="top",
            border_style="rgb(11,100,33)",
            start_value=121,
            max_value=121,
        ),
    }
    return l


def create_vertical():
    color_list = [
        "rgb(10, 120, 10)",
        "black",
        "green",
        "blue",
        Color.from_rgb(10, 50, 100),
    ]
    green_black_30 = CustomColor.gradient(Color.from_rgb(30, 200, 30), "black")
    red_black_30 = CustomColor.gradient(Color.from_rgb(200, 30, 30), "black")
    l = {
        "c1": ValueBarV(max_value=30),
        "c2": ValueBarV(
            color=["white", "black"],
            bg_color=["red", "black"],
            start_value=10,
            max_value=20,
            padding=(0, 1),
        ),
        "c3": ValueBarV(
            height=10,
            start_value=30,
            border_style="blue",
            box=box.SQUARE,
            width=5,
            padding=(2, 0),
        ),
        "c4": ValueBarV(
            color=color_list,
            start_value=30,
            max_value=25,
            border_style="yellow on black",
            padding=(4, 1),
        ),
        "c5": ValueBarV(
            color=green_black_30,
            bg_color=red_black_30,
            height=120,
            max_value=30,
            start_value=15,
        ),
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
        self.grid.add_column("col", fraction=10, min_size=121)
        self.grid.add_column("cl", repeat=6, fraction=1)
        self.grid.add_row("row", fraction=3)
        self.grid.add_row("rw", fraction=1, repeat=6)

        self.grid.add_areas(st="col,row")
        self.grid.place(st=self.status)

        for i in range(1, 7):
            self.grid.add_areas(**{f"r{i}": f"col,rw{i}"})
        for i in range(1, 6):
            self.grid.add_areas(**{f"c{i}": f"cl{i},row-start|rw6-end"})

        self.grid.place(**create_horizontal())
        self.grid.place(**create_vertical())
        # self.grid.place(r1=Placeholder())


class SimpleApp(App):
    debug: Reactive[dict] = Reactive({})

    async def on_load(self, _: events.Load) -> None:
        await self.bind("q", "quit", "Quit")
        await self.bind("r", "reset()", "Reset")

    async def on_mount(self) -> None:

        self.status = DebugWindow()
        self.layout = Layout(self.status)
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.layout, edge="left")

    async def handle_debug_status(self, message: DebugStatus):
        self.status.debug = message.mes

    async def handle_value_bar_change(self, message: ValueBarChange):
        self.debug[message.sender.name] = (
            f"[blue]Fill: [green]{message.fill}[/green] "
            f"Value: [yellow]{message.value}[/yellow]/[red]{message.max_value}[/red][/blue]"
        )
        t = str(self.debug).replace(", ", "\n")[1:-1]
        self.status.debug = t
        self.status.refresh()


if __name__ == "__main__":
    SimpleApp.run()
