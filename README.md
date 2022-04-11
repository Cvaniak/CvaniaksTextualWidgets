# CvaniaK's Widgets for Textual TUI (`ck_widgets`)

This is list of Widgets for [Textual](https://github.com/Textualize/textual) framework, created from my personal need.

> ⚠ **NOTE:** This project widgets names, arguments, etc. can vary along diffrent versions.

# Install
This is pip package so you can install it using command below:
```bash
pip3 install ck-widgets
# or 
python3 -m pip install ck-widgets
```

# ValueBar
![CoolBarGif](https://github.com/Cvaniak/CvaniaksTextualWidgets/blob/progress-bar/documentation/NiceValueBar.gif?raw=true)  
<details>
<summary>Examples</summary>

The simples example:

```python
# Simples value bar
from ck_widgets.widgets import ValueBarH, ValueBarV
vbar_horizontal = ValueBarH(max_value=50)
# or 
vbar_vertical = ValueBarV(max_value=50)
```  

And here is example with almost all arguments:

![Example with many arguments](https://github.com/Cvaniak/CvaniaksTextualWidgets/blob/progress-bar/documentation/ValueBarArguments.png?raw=true)

```python
# Example with almost all arguments
from ck_widgets.widgets import ValueBarH, CColor, CustomColor
from rich import box

background_color: List[CColor] = ["rgb(0,0,0)", "rgb(0,0,0)", "yellow"]
ValueBarH(
    name="name_to_catch_in_event",
    label="Almost all arguments",
    label_align="left",
    label_position="bottom",
    start_value=25,
    max_value=50,
    height=6,
    instant=True,
    reversed=True,
    color=CustomColor.gradient("green", "rgb(0, 100, 250)"),
    bg_color=background_color,
    border_style="yellow",
    padding=(1,1),
    box=box.DOUBLE_EDGE,
)
```  

And this example:  
![LotOfValueBars](https://github.com/Cvaniak/CvaniaksTextualWidgets/blob/progress-bar/documentation/FullUglyDemo.png?raw=true)

you can check code in this file `ck_widgets/exmples/value_bar.py` or test it by using command below:  

```bash
python3 -m ck_widgets.examples.value_bar
```

</details>

<details>
<summary>Known Limitations</summary>

* You need to force size of layout to be not smaller than maximum size of of ValueBar (otherwise it will behave badly)
* ...

</details>

<details>
<summary>TODO</summary>

* Reactive version (so it gives values from 0 to 1 and can be resized/'squashed')  
* Be sure that provide all arguments  
* Test edge cases  
* Clean up how to provide color  
* Label on left or right site  
* ...

</details>


# ListViewUo
![Image](https://github.com/Cvaniak/CvaniaksTextualWidgets/blob/progress-bar/documentation/ListViewDemo.gif?raw=true)  
While waiting for [ticket](https://github.com/Textualize/textual/projects/1#card-66941810) (also mentioned [here](https://github.com/Textualize/textual/discussions/196)) and official `ListView`, you can use this dirty version that allows you to scroll thrue list of widgets.  

<details>
<summary>Examples</summary>
You can use it this way:

```python
from ck_widgets_lv import ListViewUo

class TestListView(App):
    async def on_mount(self, event: events.Mount) -> None:
        await self.view.dock(ListViewUo([Placeholder(height=10) for _ in range(20)]))

if __name__ == "__main__":
    TestListView.run()
```

or more complex example (from gif demo above):
```python
from textual.widgets import Placeholder
from textual.widget import Widget
from textual.events import Message
from textual.app import App
from textual import events

from ck_widgets_lv import ListViewUo

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
```

</details>

# Change Log

## [0.2.0] - 2022-04-11

### Added
* ListViewUo from previous [repo](https://github.com/Cvaniak/TextualListViewUnofficial)

## [0.1.0] - 2022-02-26

### Added
* ValueBar
* Test version of DebugWidget


