# StepMania

&emsp;&emsp;[Dance Dance Revolution (DDR) Wiki | Fandom](https://dancedancerevolution.fandom.com/wiki/Dance_Dance_Revolution_(DDR)_Wiki)　[Stepmania / ffr history thread - Flash Flash Revolution](https://www.flashflashrevolution.com/vbz/showthread.php?t=149106)　[StepMania | StepMania Wiki | Fandom](https://stepmania.fandom.com/wiki/StepMania)

&emsp;&emsp;2001 年开发用于在桌面端模拟街机音游 DDR 的 StepMania 于 2016 年 8 月 14 日完成了最后一次更新 v5.0.12，分裂出无数分支音游，其中玩家群体最大的音游是 Etterna。

&emsp;&emsp;Etterna 于 2016 年 12 月 4 日诞生，详情可见[音游界的扛把子游戏——细说 Etterna 的历史，发展与展望_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Pf4y127eY/)。

&emsp;&emsp;DDR 模拟器历史详情可见 [DDR 与模拟器历史 - 哔哩哔哩](https://www.bilibili.com/opus/545471584016919913)；其中 FFR 是现在许多熟知谱师曾经入坑的论坛，如 IcyWorld / icontrolyourworld，Shoegazer / Wiosna，Fullerene / rCaliverGX，Wh1teh，Staiain 等。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-189.png" alt="IcyWorld FFR"></td>
</tr></table>
<figcaption>图 2-189 IcyWorld 在 FFR 的主页</figcaption>
</figure>

## 1. 多押合并 / chord cohesion

&emsp;&emsp;多押合并（chord cohesion，也叫和弦粘连），指同一时间点上的多个 note 只产生**一个**判定：整行的结果由这一行里最后按下的那个键决定，先按下的键自己的判定被直接丢弃。这是 SM 系引擎的默认行为，在 osu!mania 这类原生 4K 里并不存在。<br />
&emsp;&emsp;举个四押的例子：四个键分别落在「早 40ms」「早 15ms」「准」「晚 16ms」。osu!mania 会给出四个判定（Perfect、Marvelous、Marvelous、Marvelous）；StepMania 只给一个 Marvelous，由最晚落下的那个（晚 16ms）决定，早 40ms 那个 Perfect 直接消失<sup>[1]</sup>。

### 1.1 代码里的实现

&emsp;&emsp;逻辑集中在 `src/Player.cpp`，分三步<sup>[2]</sup>：

1. **逐键记录**。`Player::Step()` 每按一个键，只把判定写进该列那个 note 的 `result.tns` 和 `fTapNoteOffset`，不动整行。
2. **等整行判完**。`Player::UpdateJudgedRows()` 用 `IsRowCompletelyJudged()` 判断，一行里所有 note 都有结果了才往下走。
3. **整行取最后**。非分离模式下只调用一次 `SetJudgment()`，值来自 `NoteDataWithScoring::LastTapNoteWithResult()`；它内部走 `LastTapNoteScoreTrack()`，按真实时间挑出最晚落下的键，**但只要行里有一个键是 Miss 或未判定，就立刻返回那个键**，所以漏键永远整行 Miss。

&emsp;&emsp;接着 `ScoreKeeperNormal::HandleTapRowScore()` 结算这一行：判定计数（`HandleTapNoteScoreInternal`）和分数（`AddTapRowScore`，源码注释就写着 only score once per row）都只做一次。但 **combo 走的是另一条路**——`HandleRowComboInternal()` 拿 `iNumTapsInRow` 去累加，只有当 theme metric `ComboIsPerRow` 为真时才把它截断成 1，而这个 metric 默认取 `ComboPerRow()`，只有 pump 与 Oni 模式返回 true<sup>[3]</sup>。

### 1.2 三个直接后果

&emsp;&emsp;最直观的是**判定总数不再等于谱面 note 数**：四押只记一个判定，acc 的分母也跟着按行算，所以同一张谱在 SM 系里判定数更少，而 acc 反而容易更高——一个准键就能带走整行。同时 combo 依然按 note 涨，于是「combo 涨了 4、判定只加了 1」这种错位是常态，也是不少人第一次看 SM 结算页时觉得数字对不上的原因。<br />
&emsp;&emsp;反过来说，**四押可以扫过去**：只要每个键都落在自己的判定窗里、最后落下的那个键在 ±22.5ms 内，整行就是最高判定。这是 SM 系 acc 普遍偏高、观感偏宽容的一个结构性原因，也是它与其他 4K 游戏成绩难以横向比较的根源之一。

| | StepMania 默认 | Etterna（0.55 起） | osu!mania |
|:-----:|:-----:|:-----:|:-----:|
| 4 押产生的判定数 | 1 | 4 | 4 |
| 判定取值来源 | 该行最后按下的键 | 各键独立 | 各键独立 |
| 漏掉一个键 | 整行 1 个 Miss | 1 个 Miss + 3 个正常判定 | 同左 |
| combo 增长 | 每键 +1（pump / Oni 除外） | 每键 +1 | 每键 +1 |
| 判定总数与 note 数 | 判定数更少 | 相等 | 相等 |
| 拆键 / 扫键容错 | 高 | 低 | 低 |

<div style="text-align: left;">多押合并判定对比（编者补）</div>

### 1.3 Etterna 为什么关掉它

&emsp;&emsp;Etterna 的变更日志写得很直接<sup>[4]</sup>：**0.55.0（2017 / 9 / 8）**标为「Chord Cohesion Off is official」，同版本里「Chord Cohesion is disabled by default」，并声明「Chord Cohesion enabled scores are invalid」；**0.56.2** 起评级也只认关闭合并的成绩。<br />
&emsp;&emsp;动机是评级（MSD、SSR）要能跟谱面逐键对齐：合并判定会让四押多的谱在同样实际精度下拿到更高 acc，跟 osu!mania 这类原生 4K 的成绩没法互相参照。关闭之后，Etterna 的判定总数与判定取值方式都与 osu!mania 一致了。

&emsp;&emsp;SM5 自身并没有面向玩家的开关。`m_bCountNotesSeparately` 只是游戏模式（GameType）上的字段，仅 beat、popn 这类模式会设置它。2015 年就有 issue 要求加开关<sup>[5]</sup>，至今没做，理由也很实在：引擎里有大量代码都假设「一行只有一个判定」。

<div style="text-align: right;color: lightgray;"><i><sup>[1]</sup> 判定档位名称依主题而定，SM5 默认主题是 Fantastic / Excellent / Great / Decent / Way Off，Etterna 用 Marvelous / Perfect / Great / Good / Bad；对应的判定窗（Judge 4）为 ±22.5ms / ±45ms / ±90ms / ±135ms / ±180ms。<br /><sup>[2]</sup> 以 SM5 master 分支为准，涉及 <code>src/Player.cpp</code>、<code>src/NoteDataWithScoring.cpp</code>、<code>src/ScoreKeeperNormal.cpp</code>。<br /><sup>[3]</sup> <code>Themes/_fallback/metrics.ini</code> 的 <code>[Gameplay]</code> 段：<code>ComboIsPerRow=ComboPerRow()</code>；<code>ComboPerRow()</code> 定义在 <code>Themes/_fallback/Scripts/03 Gameplay.lua</code>。<br /><sup>[4]</sup> Etterna 仓库 <code>CHANGELOG.md</code> 与 <code>.changelog/Release_0-55-0.md</code>。<br /><sup>[5]</sup> StepMania issue #605「Chord cohesion」。</i></div>

---

&emsp;&emsp;本节为编者补充：原书 2.6 只写到 StepMania 与 Etterna 的分裂，未涉及多押合并，此处依两者的开源实现整理；表格为新增，沿用原书表格样式，故不占原书表号。

&emsp;&emsp;押、叠键、交互等键型的定义见[键型 / 排列](/VSRG-4K-wiki/pattern/pailie/)，Rice 键型的分级见[键型 / 常规](/VSRG-4K-wiki/pattern/rice/)。

