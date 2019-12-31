# My Harry Potter Reader

哈利波特英文版阅读网站:

- 显示单词发音释义
- 记录单词释义到文件/服务器
- 显示一个句子的翻译
- 记录一个句子到文件/服务器

## 核心功能实现

- 高度固定两栏显示
   > 固定高度，设置`overflow-y: hidden;`禁用上下滚动，设置宽度为200%，设置`overflow-x: auto`，启用左右滚动  
   > 父组件宽高也需要设置
- 翻页，上下页
  > 通过不断在容器中添加子元素，然后滚动到子元素实现
- 类似于edge的翻页动画
   > 使用edge-chromium浏览器阅读
- 鼠标悬浮/快捷键显示单词释义
  > 使用有道API，添加一个固定位置的元素即可
- 显示句子翻译
  > 同上
- 选中文本弹出菜单
  > 使用`document.onselectionchange`搭配`onmouseup`, `onmousedown`实现

## Todo

- 鼠标可以移动到翻译框内部（而不是在移动到target外部后翻译框就消失）
  > 通过mousedown事件判断目标对象是不是翻译框内部

## 问题与解决

- `window.scroll`不起作用
  > 设置`body`的`overflow-y: hidden`
