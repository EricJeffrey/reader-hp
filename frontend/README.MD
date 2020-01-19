# My Harry Potter Reader

哈利波特英文版阅读网站前端:

- 显示单词发音释义
- 记录单词释义到服务器
- 显示一个句子的翻译
- 记录一个句子到服务器

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
- 选中文本弹出菜单
  > 使用`document.onselectionchange`搭配`onmouseup`, `onmousedown`实现
- 记录阅读进度
  > `LocalStorage`中的`getItem, setItem`

## Todo

- 鼠标可以移动到翻译框内部（而不是在移动到target外部后翻译框就消失）
  > 通过mousedown事件判断目标对象是不是翻译框内部
- 文章API实现
- 翻译后端实现

## 问题记录

- `window.scroll`不起作用
  > 设置`body`的`overflow-y: hidden`
- 替换文档中的单词为span标签
  > 正则: `[",\.?!]{0,} ["']{0,}`, `[a-zA-Z0-9'-]{1,}<`
- 隐藏滚动条
  - 隐藏并禁用滚动: `body{overflow-x: hidden;}`
  - 隐藏但不禁用: `body:-webkit-scrollbar{display: none}`
- 横向滚动实现:
  > 子元素固定高度，父元素禁止Y轴滚动。同时父元素需要手动设置宽度以保证子元素的宽度比例正常。
  - 子元素: `#content{display: flex; width: 300%; height: 100%; overflow-y: hidden}`
  - 父元素: `body{width: 100%; height: 100%; overflow-y: hidden}`
- 固定宽度、高度
  > 使用`div{width: 100%; height: 100%}`时需要同时制定父元素(包括`body`与`html`)的宽高
- `clientWidth` 为0
  > 对于能够滚动的元素，可能需要查看 `offsetWidth` 的值确定其宽度
- 鼠标移动到其它地方，`setTimeOut` 仍然触发
  > 根本原因在于: 鼠标移动到其它非 `<span class="word">` 时未清除已经设置的 timeout，可以通过如下方式解决
  > - 在 word 上的 `mousemove` 在捕获阶段处理并结束分发: `{capture: true}, event.stopPropagation()`
  > - 在 window 上的 `mousemove` 在，若翻译未显示，就清除已经设置的 timeout
- 鼠标点击翻译盒子触发翻页
  > 原因: 鼠标点击翻页的监听器设置到了 window 上  
  > 解决: 设置到 contentdiv 上即可
- 渐显动画在仅更改`visibility`的时候不起作用，更改`display`时起作用
  > 原因: CSS动画默认仅在第一次加载时启动，和`display=none -> display=block`类似  
  > 解决: 使用如下JavaScript代码手动触发，即手动添加/移除动画属性，动画见下
  ```javascript
  show(){
      box.style.visibility = "visible";
      box.style.animation = "boxanimation_show 0.2s";
      box.style.opacity = "1"; 
  }
  hide(){
      box.style.visibility = "hidden";
      box.style.animation = "none";
      box.style.opacity = "0";
  }
  ```
  ```css
  @keyframes boxanimation_show {
      0% { opacity: 0; }
      30% { opacity: 0.75; }
      100% { opacity: 1; }
  }
  ```
- ~~网页一次性无法加载过多内容~~
- 父`div`添加超过一定数量的子元素时，子元素的`width`属性的效果发生变化
  > 原因是`display: flex`布局未明确指定每个子元素的`flex`属性，设置子元素 `flex: 1` 之后即可
- 进度条实现
  > 使用html5的`<progress value="" max="">`标签即可
- 使用动画实现类似edge的滚动效果
  > edge的滚动效果可以通过三次贝塞尔曲线实现: `cubic-bezier(0.12, 1, 0.1, 1)`，设置动画时间为 `0.6s` 左右即可
