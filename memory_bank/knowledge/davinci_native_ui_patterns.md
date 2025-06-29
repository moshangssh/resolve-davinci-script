# DaVinci Resolve 原生UI框架模式

本文档记录了使用 DaVinci Resolve 的 `fusion.UIManager` 创建原生脚本UI的核心模式。

## 1. 初始化

所有UI操作都需要 `Fusion`, `UIManager`, 和 `UIDispatcher` 对象。

```python
import fusionscript as bmd

# 获取 Fusion 对象
fu = bmd.scriptapp('Fusion')
if not fu:
    print("无法连接到 Fusion")
    # 应当在此处处理错误

# 获取 UI 管理器和分发器
ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
```

## 2. 声明式UI布局

UI布局通过嵌套的Python列表和字典来定义，这是一种声明式的方法。

- **`ui.VGroup({}, [])`**: 垂直容器。
- **`ui.HGroup({}, [])`**: 水平容器。
- 第一个参数（字典）用于定义容器属性，如 `{"Spacing": 10}`。
- 第二个参数（列表）包含子UI元素。

## 3. UI组件定义

每个组件都通过一个字典来定义，其中必须包含一个唯一的 `ID`。

- **标签 (Label):**
  `ui.Label({"ID": "MyLabel", "Text": "这是一个标签"})`

- **单行输入 (LineEdit):**
  `ui.LineEdit({"ID": "MyLineEdit", "PlaceholderText": "请输入文本..."})`

- **按钮 (Button):**
  `ui.Button({"ID": "MyButton", "Text": "点击我"})`

- **下拉框 (ComboBox):**
  `ui.ComboBox({"ID": "MyComboBox"})`
  *内容通过 `itm['MyComboBox'].AddItem("选项")` 动态添加。*

- **数字输入 (SpinBox/IntEdit 的替代方案):**
  原生UI中没有直接对应的 `SpinBox`。通常使用 `ui.LineEdit` 替代，并在代码中处理字符串到数字的转换。
  `ui.LineEdit({"ID": "MyNumberInput", "Text": "0"})`

## 4. 窗口创建与显示

使用 `disp.AddWindow()` 来创建窗口。

```python
# 假设 layout 是一个定义好的UI布局列表
layout = [
    ui.VGroup({}, [
        ui.Label({"ID": "MyLabel", "Text": "示例"}),
        ui.Button({"ID": "MyButton", "Text": "确定"})
    ])
]

# 创建窗口
dlg = disp.AddWindow({
    "WindowTitle": "我的工具",
    "ID": "MyToolWin",
    "Geometry": [ 600, 300, 400, 200 ], # X, Y, Width, Height
}, layout)
```

## 5. 访问组件和处理事件

- **访问组件:**
  `itm = dlg.GetItems()` 返回一个包含所有UI元素的字典，键是元素的ID。
  `my_button = itm['MyButton']`
  `text_value = itm['MyLineEdit'].Text`

- **事件绑定:**
  事件处理函数在窗口显示前绑定。
  ```python
  def handle_button_click(ev):
      print("按钮被点击了!")
      # 可以通过 itm 访问其他控件
      print(f"输入框内容: {itm['MyLineEdit'].Text}")

  def handle_window_close(ev):
      disp.ExitLoop()

  # 绑定事件
  dlg.On.MyButton.Clicked = handle_button_click
  dlg.On.MyToolWin.Close = handle_window_close
  ```

## 6. 运行UI

显示窗口并启动事件循环来让UI响应用户操作。

```python
dlg.Show()
disp.RunLoop()
dlg.Hide() # 事件循环结束后隐藏窗口