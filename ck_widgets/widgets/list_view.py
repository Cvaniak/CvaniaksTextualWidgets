from __future__ import annotations

from rich.console import RenderableType

from textual.geometry import Size, SpacingDimensions
from textual.layouts.vertical import VerticalLayout
from textual.views._window_view import WindowChange
from textual.reactive import Reactive
from textual.widgets import ScrollView
from textual.widget import Widget
from textual.view import View
from textual import messages
from textual.widgets import Static
from textual import events

from typing import List


class MultipleWidgetsWindowView(View, layout=VerticalLayout):
    layout: Reactive[VerticalLayout]

    def __init__(
        self,
        widgets: List[RenderableType | Widget] | None = None,
        *,
        auto_width: bool = False,
        gutter: SpacingDimensions = (0, 0),
        name: str | None = None
    ) -> None:
        layout = VerticalLayout(gutter=gutter, auto_width=auto_width)
        super().__init__(name=name, layout=layout)
        self.set_widgets(widgets)
        for widget in self._widgets:
            layout.add(widget)

    async def update(self, widgets: List[Widget | RenderableType] | None) -> None:
        layout = self.layout
        assert isinstance(layout, VerticalLayout)
        self.set_widgets(widgets)
        await self.arrange_widgets()

    def set_widgets(self, widgets: List[Widget | RenderableType] | None) -> None:
        if widgets is None:
            return
        self._widgets: List[Static | Widget] = [
            w if isinstance(w, Widget) else Static(w) for w in widgets
        ]

    async def arrange_widgets(self):
        self.layout.clear()
        for widget in self._widgets:
            self.layout.add(widget)
        self.layout.require_update()
        self.refresh(layout=True)
        await self.emit(WindowChange(self))

    async def handle_update(self, message: messages.Update) -> None:
        message.prevent_default()
        await self.emit(WindowChange(self))

    async def handle_layout(self, message: messages.Layout) -> None:
        self.log("TRANSLATING layout")
        self.layout.require_update()
        message.stop()
        self.refresh()

    async def watch_virtual_size(self, size: Size) -> None:
        await self.emit(WindowChange(self))

    async def watch_scroll_x(self, value: int) -> None:
        self.layout.require_update()
        self.refresh()

    async def watch_scroll_y(self, value: int) -> None:
        self.layout.require_update()
        self.refresh()

    async def on_resize(self, event: events.Resize) -> None:
        await self.emit(WindowChange(self))

    async def add_widget(
        self, widget: Widget | RenderableType, index: int | None = None
    ):
        if index is None:
            index = len(self._widgets)
        index = min(len(self._widgets), max(0, index))
        self._widgets.insert(
            index, widget if isinstance(widget, Widget) else Static(widget)
        )
        await self.arrange_widgets()

    async def remove_widget_by_index(self, index: int = 0):
        if not self._widgets:
            return 
        index = min(len(self._widgets)-1, max(0, index))
        self._widgets.pop(index)
        await self.arrange_widgets()

    async def remove_widget(self, widget: Widget):
        if not self._widgets:
            return 
        self._widgets.remove(widget)
        await self.arrange_widgets()


class ListViewUo(ScrollView):
    def __init__(
        self, widgets: List[Widget | RenderableType] | None = None, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.widgets_list = widgets
        self.window = MultipleWidgetsWindowView(self.widgets_list)

    def refresh_all(self):
        self.window.layout.require_update()
        self.layout.require_update()
        self.window.refresh()
        self.vscroll.refresh()
        self.hscroll.refresh()

    async def add_widget(self, widget:Widget, index:int|None = None):
        await self.window.add_widget(widget, index)
        self.refresh_all()

    async def remove_widget_by_index(self, index: int=0):
        await self.window.remove_widget_by_index(index)
        self.refresh_all()

    async def remove_widget(self, widget: Widget):
        await self.window.remove_widget(widget)
        self.refresh_all()

