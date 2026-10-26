# mkdocs-font-switch

给 MkDocs Material 站点加一个页眉字体切换按钮。构建时自动注入 CSS / JS，不需要手改主题模板。

## 用法

```bash
pip install -e ./mkdocs-font-switch
```

```yaml
plugins:
  - search
  - font-switch:
      storage_key: vsrg-font          # localStorage 键名
      fonts:
        - id: uuz                     # 对应 <html data-site-font="uuz">
          label: 隶                   # 按钮上显示的文字
          title: 隶灵黑               # 悬浮提示里的名字
          src: fonts/uuz.woff2        # 相对 docs/ 的路径，优先使用
          fallback: fonts/uuz.otf     # 可选，老浏览器兜底
```

字体文件仍放在 `docs/fonts/` 下由 MkDocs 正常拷贝；插件只负责生成 `@font-face`、覆盖规则和按钮。

## 选项

| 选项 | 默认值 | 说明 |
|---|---|---|
| `fonts` | `[]` | 除“默认字体”以外的可选字体，每项含 `id` / `label` / `title` / `src` / `fallback` / `family` |
| `storage_key` | `vsrg-font` | 记住用户选择的 localStorage 键名 |
| `button_anchor` | `<div class="md-header__source` | 按钮插入位置；找不到时由 JS 兜底挂载 |

## 它是怎么生效的

Material 的字体变量定义在 `body` 上：

```css
--md-text-font-family: var(--md-text-font, _), -apple-system, BlinkMacSystemFont, …
```

所以插件覆盖的是可继承的 `--md-text-font`（在 `<html>` 上设一次，`body` 会自动拼进自己的字体栈），
再给 `body` 补一条同值声明兜底。切换时只改一个属性，整页排版自动重算，不刷新、不丢阅读位置。
