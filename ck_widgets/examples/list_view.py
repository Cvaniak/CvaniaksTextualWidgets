from __future__ import annotations

from textual.widgets import Placeholder
from textual.widget import Widget
from textual.events import Message
from textual.app import App
from textual import events

from ck_widgets.widgets import ListViewUo


if __name__ == "__main__":
    from textual.widgets import Footer

    class DeleteStatus(Message):
        def __init__(self, sender: Widget):
            super().__init__(sender)
            self.to_delete = sender

    class DeletablePlaceholder(Placeholder):
        async def on_click(self, event: events.Click) -> None:
            await self.emit(DeleteStatus(self))

    class TestListView(App):
        async def action_add(self) -> None:
            await self.list_view.add_widget(DeletablePlaceholder(height=10))
            self.refresh()

        async def action_add_index_2(self) -> None:
            await self.list_view.add_widget(DeletablePlaceholder(height=10), index=2)
            self.refresh()

        async def action_remove(self) -> None:
            await self.list_view.remove_widget_by_index()
            self.refresh()

        async def action_remove_index_2(self) -> None:
            await self.list_view.remove_widget_by_index(index=2)
            self.refresh()

        async def on_load(self, _: events.Load) -> None:
            await self.bind("a", "add()", "Add Widget")
            await self.bind("s", "add_index_2()", "Add Widget in index 2")
            await self.bind("r", "remove()", "Remove Widget")
            await self.bind("e", "remove_index_2()", "Remove Widget in index 2")
            await self.bind("Click Widget", "_()", "To delete it")

        async def on_mount(self, event: events.Mount) -> None:
            self.list_view = ListViewUo(
                [DeletablePlaceholder(height=10) for _ in range(7)]
            )

            await self.view.dock(Footer(), edge="bottom")
            await self.view.dock(self.list_view)

        async def handle_delete_status(self, message: DeleteStatus):
            await self.list_view.remove_widget(message.to_delete)

    TestListView.run()
