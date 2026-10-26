"""mkdocs-font-switch：构建时自动给站点加上「正文字体切换」控件。

插件做三件事，全部在构建阶段完成，不需要手改主题模板或 docs/ 下的样式：

1. 按 ``fonts`` 配置生成 ``@font-face`` 声明和 ``html[data-site-font="…"]`` 覆盖规则，
   写入 ``stylesheets/font-switch.css``；
2. 生成 ``javascripts/font-switch.js``：在页眉挂一个按钮，点击循环切换、选择存 localStorage；
3. 在每页 ``</head>`` 前插入一小段内联脚本，在首次绘制前把上次的选择写回 ``<html>``，
   避免刷新时先闪一下默认字体。
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from mkdocs.config import config_options
from mkdocs.config.base import Config
from mkdocs.exceptions import ConfigurationError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files

CSS_ASSET = "stylesheets/font-switch.css"
JS_ASSET = "javascripts/font-switch.js"
BUTTON_CLASS = "vsrg-font-switch"

# Material 在 body 上写的是
#   --md-text-font-family: var(--md-text-font, _), -apple-system, …
# 所以真正要覆盖的是可继承的 --md-text-font，再给 body 补一条同值声明兜底。
_SYSTEM_STACK = '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'

_FORMAT_BY_EXT = {
    ".woff2": "woff2",
    ".woff": "woff",
    ".otf": "opentype",
    ".ttf": "truetype",
}

_BUTTON_CSS = """/* 页眉里的切换按钮，沿用 .md-header__button 的位置与配色 */
.md-header__button.{cls} {{
  width: auto;
  min-width: 2.4rem;
  padding: 0 .5rem;
  border: 0;
  background: none;
  font-family: var(--md-text-font-family, sans-serif);
  font-size: .8rem;
  font-weight: 600;
  text-align: center;
  color: inherit;
}}

.md-header__button.{cls}:hover {{
  opacity: .7;
}}

/* 字体文件正在下载时的反馈 */
.md-header__button.{cls}[data-state="loading"] {{
  cursor: progress;
  opacity: .4;
}}
""".format(cls=BUTTON_CLASS)

_BUTTON_HTML = (
    '<button type="button" class="md-header__button ' + BUTTON_CLASS + '"'
    ' title="切换正文字体" aria-label="切换正文字体" data-state="">__LABEL__</button>'
)

# 注意：这段 JS 里有花括号，不能用 str.format，统一走 __KEY__ 占位符替换
_BOOTSTRAP = """<script>
(function () {
  try {
    var font = localStorage.getItem(__KEY__);
    if (font && font !== "default") {
      document.documentElement.setAttribute("data-site-font", font);
    }
  } catch (e) {}
})();
</script>
"""

_JS_TEMPLATE = """/* 由 mkdocs-font-switch 生成，请勿手改 */
(function () {
  "use strict";

  var CONFIG = __CONFIG__;
  var FONTS = CONFIG.fonts;
  var STORAGE_KEY = CONFIG.storageKey;

  function read() {
    var id = null;
    try {
      id = localStorage.getItem(STORAGE_KEY);
    } catch (e) {}
    for (var i = 0; i < FONTS.length; i++) {
      if (FONTS[i].id === id) return i;
    }
    return 0;
  }

  function save(id) {
    try {
      localStorage.setItem(STORAGE_KEY, id);
    } catch (e) {}
  }

  function apply(font) {
    var root = document.documentElement;
    if (font.id === "default") {
      root.removeAttribute("data-site-font");
    } else {
      root.setAttribute("data-site-font", font.id);
    }
  }

  function render(btn, index) {
    var font = FONTS[index];
    btn.textContent = font.label;
    btn.title = "切换正文字体（当前：" + font.title + "）";
    btn.setAttribute("aria-label", btn.title);
  }

  function onClick(btn) {
    var next = (read() + 1) % FONTS.length;
    var font = FONTS[next];

    save(font.id);
    apply(font);
    render(btn, next);

    // 首次切到自定义字体时文件才真正开始下载，加载期间给个反馈
    if (font.family && document.fonts && document.fonts.load) {
      btn.dataset.state = "loading";
      var done = function () {
        delete btn.dataset.state;
      };
      document.fonts.load('1em "' + font.family + '"').then(done, done);
    }
  }

  function bind(btn) {
    if (btn.dataset.bound === "1") return;
    btn.dataset.bound = "1";
    btn.addEventListener("click", function () {
      onClick(btn);
    });
    render(btn, read());
  }

  // 插件已经把按钮写进了 HTML，这里只负责绑定；万一模板变了就补一个
  function mount() {
    var btn = document.querySelector(".__CLS__");
    if (!btn) {
      var inner = document.querySelector(".md-header__inner");
      if (!inner) return;
      btn = document.createElement("button");
      btn.type = "button";
      btn.className = "md-header__button __CLS__";
      var anchor =
        inner.querySelector(".md-header__source") || inner.querySelector(".md-search");
      inner.insertBefore(btn, anchor);
    }
    bind(btn);
  }

  // Material 的即时导航只换内容、不重建页眉，用它的 document$ 保证每次导航后都绑上
  var documentDollar = window["document$"];
  if (documentDollar && documentDollar.subscribe) {
    documentDollar.subscribe(mount);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
""".replace("__CLS__", BUTTON_CLASS)


class FontSwitchPlugin(BasePlugin):
    """构建时注入字体切换控件。"""

    config_scheme = (
        ("fonts", config_options.Type(list, default=[])),
        ("storage_key", config_options.Type(str, default="vsrg-font")),
        ("button_anchor", config_options.Type(str, default='<div class="md-header__source')),
    )

    def __init__(self) -> None:
        self._fonts: List[Dict[str, Any]] = []
        self._assets_dir: Optional[Path] = None

    # ------------------------------------------------------------------ 配置
    @staticmethod
    def _collect_sources(item: Dict[str, Any]) -> List[Dict[str, str]]:
        raw: List[str] = []
        for key in ("src", "fallback"):
            value = item.get(key)
            if not value:
                continue
            if isinstance(value, (list, tuple)):
                raw.extend(str(v) for v in value)
            else:
                raw.append(str(value))

        sources: List[Dict[str, str]] = []
        for path in raw:
            fmt = _FORMAT_BY_EXT.get(Path(path).suffix.lower())
            if fmt is None:
                raise ConfigurationError(
                    "font-switch: 不认识的字体格式 %s（支持 %s）"
                    % (path, "、".join(sorted(_FORMAT_BY_EXT)))
                )
            sources.append({"path": path.lstrip("./"), "format": fmt})
        return sources

    def _normalize(self, config: Config) -> List[Dict[str, Any]]:
        fonts: List[Dict[str, Any]] = [{"id": "default", "label": "Aa", "title": "默认字体"}]
        seen = {"default"}

        for item in self.config.get("fonts") or []:
            if not isinstance(item, dict):
                raise ConfigurationError("font-switch: fonts 里每一项都得是字典")

            fid = str(item.get("id") or "").strip()
            if not fid:
                raise ConfigurationError("font-switch: fonts 里缺少 id")
            if fid in seen:
                raise ConfigurationError("font-switch: 字体 id 重复：%s" % fid)
            seen.add(fid)

            sources = self._collect_sources(item)
            if not sources:
                raise ConfigurationError("font-switch: 字体 %s 缺少 src" % fid)

            docs_dir = Path(config.docs_dir)
            for src in sources:
                if not (docs_dir / src["path"]).is_file():
                    raise ConfigurationError(
                        "font-switch: 字体 %s 的文件 %s 不存在" % (fid, src["path"])
                    )

            fonts.append(
                {
                    "id": fid,
                    "label": str(item.get("label") or fid.upper()[:2]),
                    "title": str(item.get("title") or fid),
                    "family": str(item.get("family") or fid),
                    "sources": sources,
                }
            )
        return fonts

    @staticmethod
    def _font_css(font: Dict[str, Any]) -> str:
        sources = ", ".join(
            'url("../%s") format("%s")' % (src["path"], src["format"]) for src in font["sources"]
        )
        return "\n".join(
            [
                "@font-face {",
                '  font-family: "%s";' % font["family"],
                "  src: %s;" % sources,
                "  font-display: swap;",
                "  font-weight: normal;",
                "  font-style: normal;",
                "}",
                "",
                'html[data-site-font="%s"] {' % font["id"],
                '  --md-text-font: "%s";' % font["family"],
                "}",
                "",
                'html[data-site-font="%s"] body {' % font["id"],
                '  --md-text-font-family: "%s", %s;' % (font["family"], _SYSTEM_STACK),
                "}",
                "",
            ]
        )

    # ------------------------------------------------------------------ 资源
    def _write_assets(self) -> None:
        assert self._assets_dir is not None
        (self._assets_dir / "stylesheets").mkdir(parents=True, exist_ok=True)
        (self._assets_dir / "javascripts").mkdir(parents=True, exist_ok=True)

        chunks = ["/* 由 mkdocs-font-switch 在构建时生成，请勿手改 */", ""]
        for font in self._fonts:
            if font["id"] != "default":
                chunks.append(self._font_css(font))
        chunks.append(_BUTTON_CSS)
        (self._assets_dir / CSS_ASSET).write_text("\n".join(chunks), encoding="utf-8")

        payload = {
            "storageKey": self.config["storage_key"],
            "fonts": [
                {
                    "id": font["id"],
                    "label": font["label"],
                    "title": font["title"],
                    "family": font.get("family"),
                }
                for font in self._fonts
            ],
        }
        js = _JS_TEMPLATE.replace("__CONFIG__", json.dumps(payload, ensure_ascii=False))
        (self._assets_dir / JS_ASSET).write_text(js, encoding="utf-8")

    # ------------------------------------------------------------------ events
    def on_config(self, config: Config) -> Config:
        self._fonts = self._normalize(config)
        self._assets_dir = Path(tempfile.mkdtemp(prefix="mkdocs-font-switch-"))
        self._write_assets()

        config.extra_css = list(config.extra_css or []) + [CSS_ASSET]
        config.extra_javascript = list(config.extra_javascript or []) + [JS_ASSET]
        return config

    def on_files(self, files: Files, config: Config) -> Files:
        assert self._assets_dir is not None
        for asset in (CSS_ASSET, JS_ASSET):
            files.append(
                File(
                    path=asset,
                    src_dir=str(self._assets_dir),
                    dest_dir=config.site_dir,
                    use_directory_urls=config.use_directory_urls,
                )
            )
        return files

    def on_post_page(self, output: str, page: Any, config: Config) -> str:
        # 1) 首绘前恢复上次选择，避免闪一下默认字体
        if "</head>" in output:
            bootstrap = _BOOTSTRAP.replace("__KEY__", json.dumps(self.config["storage_key"]))
            output = output.replace("</head>", bootstrap + "</head>", 1)

        # 2) 把按钮直接写进页眉（JS 里还有一层兜底，模板变了也能挂上）
        if BUTTON_CLASS not in output:
            anchor = self.config["button_anchor"]
            index = output.find(anchor) if anchor else -1
            if index != -1:
                button = _BUTTON_HTML.replace("__LABEL__", self._fonts[0]["label"])
                output = output[:index] + button + "\n" + output[index:]
        return output
