# CvaniaK's Widgets for Textual TUI (`ck_widgets`)

This is list of Widgets for [Textual](https://github.com/Textualize/textual) framework, created from my personal need.

> ⚠ **NOTE:** This project widgets names, arguments, etc. can vary along diffrent versions.

# Install

# ValueBar
![CoolBarGif](https://raw.githubusercontent.com/Cvaniak/CvaniaksTextualWidgets/master/documentation/NiveValueBar.gif)  
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
![Example with many arguments](https://raw.githubusercontent.com/Cvaniak/CvaniaksTextualWidgets/master/documentation/ValueBarArguments.png)  
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
![LotOfValueBars](https://raw.githubusercontent.com/Cvaniak/CvaniaksTextualWidgets/master/documentation/ValueBarArguments.png)  
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


# Change Log

## [0.1.0] - 2022-02-26

### Added
* ValueBar
* Test version of DebugWidget


