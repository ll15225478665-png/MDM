# Playwright get_by_role 速查表

## 最常用（90% 场景够用）

| role | 对应元素 | role 定位 | placeholder 定位 | locator 定位 |
|------|----------|-----------|------------------|--------------|
| `button` | `<button>`, `<input type="button/submit">` | `get_by_role("button", name="登录")` | — | `locator("button:has-text('登录')")` |
| `textbox` | `<input>`, `<textarea>` | `get_by_role("textbox", name="用户名")` | `get_by_placeholder("用户名")` | `locator("input[placeholder='用户名']")` |
| `link` | `<a>` | `get_by_role("link", name="忘记密码")` | — | `locator("a:has-text('忘记密码')")` |
| `checkbox` | `<input type="checkbox">` | `get_by_role("checkbox", name="记住我")` | — | `locator("input[type='checkbox']")` |
| `heading` | `<h1>`~`<h6>` | `get_by_role("heading", level=1)` | — | `locator("h1")` |
| `img` | `<img>` | `get_by_role("img", name="Logo")` | — | `locator("img[alt='Logo']")` |
| `dialog` | 弹窗容器 | `get_by_role("dialog")` | — | `locator(".el-dialog")` |
| `alert` | 提示信息 | `get_by_role("alert")` | — | `locator(".el-message")` |
| `table` | `<table>` | `get_by_role("table")` | — | `locator("table")` |
| `tab` | 标签页 | `get_by_role("tab", name="基本信息")` | — | `locator(".el-tab-pane")` |

---

## 表单类

| role | 对应元素 | role 定位 | placeholder 定位 | locator 定位 |
|------|----------|-----------|------------------|--------------|
| `textbox` | 文本输入框 | `get_by_role("textbox", name="账号")` | `get_by_placeholder("账号")` | `locator("input[type='text']")` |
| `searchbox` | 搜索框 | `get_by_role("searchbox")` | `get_by_placeholder("搜索")` | `locator("input[type='search']")` |
| `spinbutton` | 数字步进器 | `get_by_role("spinbutton")` | — | `locator("input[type='number']")` |
| `slider` | 滑块（范围选择/音量调节） | `get_by_role("slider")` | — | `locator(".el-slider")` |
| `step` | 步骤条中的单个步骤 | `get_by_role("step")` | — | `locator(".el-step")` |
| `combobox` | 下拉框本体（Element UI / Ant Design 等框架） | `get_by_role("combobox", name="状态")` | `get_by_placeholder("状态")` | `locator(".el-select")` |
| `listbox` | 下拉列表容器（弹出层） | — | — | `locator("[role='listbox']")` |
| `option` | 下拉框单个选项 | `get_by_role("option", name="启用")` | — | `locator(".el-select-dropdown__item")` |
| `checkbox` | 复选框 | `get_by_role("checkbox", name="同意")` | — | `locator("input[type='checkbox']")` |
| `radio` | 单选框 | `get_by_role("radio", name="男")` | — | `locator("input[type='radio']")` |
| `switch` | 开关（Switch 组件） | `get_by_role("switch", name="启用")` | — | `locator(".el-switch")` |
| `button` | 按钮 | `get_by_role("button", name="提交")` | — | `locator("button:has-text('提交')")` |
| `separator` | 分割线/分隔符 | `get_by_role("separator")` | — | `locator(".el-divider")` |

---

## 导航类

| role | 对应元素 | role 定位 | text 定位 | locator 定位 |
|------|----------|-----------|-----------|--------------|
| `link` | 链接 | `get_by_role("link", name="首页")` | `get_by_text("首页")` | `locator("a:has-text('首页')")` |
| `tab` | 标签页（Tab） | `get_by_role("tab", name="设置")` | `get_by_text("设置")` | `locator(".el-tab-pane")` |
| `tablist` | 标签页列表容器 | `get_by_role("tablist")` | — | `locator(".el-tabs__header")` |
| `tabpanel` | 标签页面板内容区 | `get_by_role("tabpanel")` | — | `locator(".el-tabs__content")` |
| `menu` | 右键菜单 / 下拉菜单容器 | `get_by_role("menu")` | — | `locator(".el-dropdown-menu")` |
| `menuitem` | 菜单项 | `get_by_role("menuitem", name="导出")` | `get_by_text("导出")` | `locator(".el-dropdown-menu__item")` |
| `menubar` | 顶部导航菜单栏 | `get_by_role("menubar")` | — | `locator(".el-menu")` |
| `tree` | 树形控件 | `get_by_role("tree")` | — | `locator(".el-tree")` |
| `treeitem` | 树节点 | `get_by_role("treeitem", name="部门A")` | `get_by_text("部门A")` | `locator(".el-tree-node")` |
| `navigation` | 侧边栏导航区域 | `get_by_role("navigation")` | — | `locator(".el-aside")` |

---

## 结构类

| role | 对应元素 | 示例 |
|------|----------|------|
| `heading` | 标题（h1~h6） | `get_by_role("heading", level=1)` |
| `paragraph` | 段落文本 | `get_by_role("paragraph")` |
| `region` | 独立功能区域 | `get_by_role("region")` |
| `banner` | 页面顶部 Header | `get_by_role("banner")` |
| `navigation` | 侧边栏/顶部导航 | `get_by_role("navigation")` |
| `main` | 主内容区域 | `get_by_role("main")` |
| `complementary` | 侧边栏/辅助信息区 | `get_by_role("complementary")` |
| `contentinfo` | 页脚（Footer） | `get_by_role("contentinfo")` |
| `form` | 表单容器 | `get_by_role("form")` |
| `search` | 搜索区域 | `get_by_role("search")` |
| `article` | 文章/卡片内容块 | `get_by_role("article")` |
| `section` | 章节/分区 | `get_by_role("section")` |

---

## 表格类

| role | 对应元素 | role 定位 | text 定位 | locator 定位 |
|------|----------|-----------|-----------|--------------|
| `table` | 数据表格 | `get_by_role("table")` | — | `locator("table")` |
| `row` | 表格行 | — | — | `locator("tbody tr")` |
| `rowgroup` | 行组（thead/tbody/tfoot） | — | — | `locator("thead")` / `locator("tbody")` |
| `columnheader` | 列头（可排序/筛选） | `get_by_role("columnheader", name="企业")` | `get_by_text("企业")` | `locator("thead th")` |
| `rowheader` | 行头 | — | — | `locator("th[scope='row']")` |
| `cell` | 数据单元格 | — | — | `locator("tbody td")` |
| `grid` | 可编辑网格表格 | `get_by_role("grid")` | — | `locator(".el-table")` |
| `gridcell` | 网格单元格 | — | — | `locator(".el-table__body td")` |
| `treegrid` | 树形表格（可展开） | `get_by_role("treegrid")` | — | `locator(".el-table--tree")` |
| `checkbox` | 表格行复选框（批量选择） | `get_by_role("checkbox", name="全选")` | — | `locator(".el-table__header .el-checkbox")` |

---

## 反馈类

| role | 对应元素 | role 定位 | text 定位 | locator 定位 |
|------|----------|-----------|-----------|--------------|
| `alert` | 消息提示（Message/Toast） | `get_by_role("alert")` | `get_by_text("操作成功")` | `locator(".el-message")` |
| `alertdialog` | 确认对话框（二次确认弹窗） | `get_by_role("alertdialog")` | — | `locator(".el-message-box")` |
| `dialog` | 弹窗/抽屉容器 | `get_by_role("dialog")` | — | `locator(".el-dialog")` / `locator(".el-drawer")` |
| `status` | 状态提示条 | `get_by_role("status")` | — | `locator(".el-notification")` |
| `log` | 日志输出区域 | `get_by_role("log")` | — | `locator(".log-container")` |
| `progressbar` | 进度条（上传/加载进度） | `get_by_role("progressbar")` | — | `locator(".el-progress")` |
| `tooltip` | 文字提示气泡 | `get_by_role("tooltip")` | — | `locator(".el-tooltip")` |
| `timer` | 倒计时/计时器 | `get_by_role("timer")` | — | `locator(".timer")` |

---
**常见框架下拉框的 role 映射**：
| 组件 | role |
|------|------|
| 下拉框本体 | `combobox` |
| 下拉列表容器 | `listbox` |
| 单个选项 | `option` |
## 其他

| role | 对应元素 | 示例 |
|------|----------|------|
| `img` | 图片 | `get_by_role("img", name="二维码")` |
| `figure` | 图文组合 | `get_by_role("figure")` |
| `caption` | 说明文字 | `get_by_role("caption")` |
| `code` | 代码块 | `get_by_role("code")` |
| `separator` | 分隔线 | `get_by_role("separator")` |

---

## 使用原则

1. **优先级**：`get_by_role` > `get_by_text/label/placeholder` > `locator`
2. **name 参数**：用页面上用户能看到的文字（按钮文字、输入框 label、链接文字）
3. **不指定 name**：`get_by_role("button")` 会返回所有按钮，配合 `.first` / `.nth(0)` 使用
4. **大小写**：role 名称全小写，name 区分大小写（需与页面文字完全一致）

---

## 附录：浏览器自动分配的 ARIA role 完整清单

**Playwright 的 `get_by_role()` 只能定位有 ARIA role 的元素。**

### 1. 浏览器自动分配的 role（原生 HTML 元素）

| HTML 元素 | 浏览器分配的 role | Playwright 定位写法 |
|-----------|------------------|---------------------|
| `<button>` | `button` | `get_by_role("button", name="xx")` |
| `<input type="text">` | `textbox` | `get_by_role("textbox", name="xx")` |
| `<input type="password">` | `textbox` | `get_by_role("textbox", name="xx")` |
| `<input type="email">` | `textbox` | `get_by_role("textbox", name="xx")` |
| `<input type="search">` | `searchbox` | `get_by_role("searchbox")` |
| `<input type="number">` | `spinbutton` | `get_by_role("spinbutton")` |
| `<input type="range">` | `slider` | `get_by_role("slider")` |
| `<input type="checkbox">` | `checkbox` | `get_by_role("checkbox", name="xx")` |
| `<input type="radio">` | `radio` | `get_by_role("radio", name="xx")` |
| `<input type="submit">` | `button` | `get_by_role("button", name="xx")` |
| `<input type="reset">` | `button` | `get_by_role("button", name="xx")` |
| `<textarea>` | `textbox` | `get_by_role("textbox", name="xx")` |
| `<select>` | `combobox` | `get_by_role("combobox")` |
| `<option>` | `option` | `get_by_role("option", name="xx")` |
| `<a href="...">` | `link` | `get_by_role("link", name="xx")` |
| `<h1>`~`<h6>` | `heading` | `get_by_role("heading", level=1)` |
| `<img alt="xx">` | `img` | `get_by_role("img", name="xx")` |
| `<img alt="">` | 无 | — |
| `<table>` | `table` | `get_by_role("table")` |
| `<th scope="col">` | `columnheader` | `get_by_role("columnheader", name="xx")` |
| `<th scope="row">` | `rowheader` | `get_by_role("rowheader", name="xx")` |
| `<td>` | `cell` | `get_by_role("cell")` |
| `<caption>` | `caption` | `get_by_role("caption")` |
| `<nav>` | `navigation` | `get_by_role("navigation")` |
| `<main>` | `main` | `get_by_role("main")` |
| `<header>` | `banner` | `get_by_role("banner")` |
| `<footer>` | `contentinfo` | `get_by_role("contentinfo")` |
| `<aside>` | `complementary` | `get_by_role("complementary")` |
| `<section>` | `region` | `get_by_role("region")` |
| `<article>` | `article` | `get_by_role("article")` |
| `<form>` | `form` | `get_by_role("form")` |
| `<search>` | `search` | `get_by_role("search")` |
| `<menu>` | `menu` | `get_by_role("menu")` |
| `<menuitem>` | `menuitem` | `get_by_role("menuitem", name="xx")` |
| `<ul>` / `<ol>` 内的 `<li>` | `listitem` | `get_by_role("listitem", name="xx")` |
| `<progress>` | `progressbar` | `get_by_role("progressbar")` |
| `<output>` | `status` | `get_by_role("status")` |
| `<details>` | `group` | `get_by_role("group")` |
| `<summary>` | 无 | — |
| `<fieldset>` | `group` | `get_by_role("group")` |
| `<dialog>` | `dialog` | `get_by_role("dialog")` |
| `<figure>` | `figure` | `get_by_role("figure")` |

### 2. 没有 role 的情况

| 情况 | 原因 | 替代定位方式 |
|------|------|-------------|
| `<input readonly>` | 只读输入框，浏览器不知道算什么 | `get_by_placeholder()` / `locator()` |
| `<input disabled>` | 禁用输入框，浏览器不分配 role | `locator()` |
| `<div>` / `<span>` | 通用容器，无语义 | `locator()` / `get_by_text()` |
| `<li>` 不在 `<ul/ol>` 内 | 无父级列表 | `locator()` |
| Element UI 下拉选项 | 自定义 `<li>` 无 role 属性 | `locator(".el-select-dropdown__item")` |
| Element UI 表格列头 | 无 `scope` 属性 | `get_by_text("列名", exact=True)` |

### 3. 如何查看元素的 role

**不要猜测，用浏览器开发者工具查看：**

1. **F12 打开开发者工具**
2. **Elements 面板选中元素**（点击 HTML 标签）
3. **右侧找到 Accessibility 标签**
4. **看 Computed Properties → Role 字段**

| Role 值 | 含义 |
|---------|------|
| `button` / `textbox` / `link` / `listitem` 等 | 有 role，可用 `get_by_role()` 定位 |
| `generic` | 没有语义 role（选中了 div/span），往上找父元素 |

**注意：要选中语义化元素（button/input/a/select），不要选中内部的 div/span。**
