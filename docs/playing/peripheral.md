# 外设 / peripheral

&emsp;&emsp;显示器够用就行，有条件可追求高刷；游戏卡顿可以试试更改帧数限制解决。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-135.png" alt="frame limiter"></td>
</tr></table>
<figcaption>图 2-135 osu 设置 - 画面 - 渲染器 - 帧数限制</figcaption>
</figure>

&emsp;&emsp;不同类型键盘的 PCB / printed circuit board / 印制电路板和轴体不能互通，更换配件时注意自己使用的键盘类型；这些键盘都有不同的轴体、品牌等，电子产品水很深，连实时更新的键盘推荐视频也不能 100% 做到让玩家不踩坑，笔者能力有限，在此不做键盘推荐，可自行查找适合自己的键盘。

## 1. 磁轴键盘<sup>[1]</sup>

&emsp;&emsp;基于霍尔效应，通过按键下压时磁铁与传感器距离改变引起的磁场变化来触发信号；无接触延迟，触发速度比机械轴快；没有物理磨损，寿命可达 1 亿次以上；可通过驱动软件精细设定触发点。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-136.png" width="280" alt="magnetic switch"></td>
</tr></table>
<figcaption>图 2-136 磁轴轴体结构</figcaption>
</figure>

&emsp;&emsp;音游最常用的功能是 RT / rapid trigger / 快速触发：基于磁轴可自定义触发电位的特性松开极短距离即可重置按键。<br />
&emsp;&emsp;也是大多数顶尖音游玩家的键盘。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-137.png" alt="magnetic polarity"></td>
</tr></table>
<figcaption>图 2-137 磁极朝向</figcaption>
</figure>

&emsp;&emsp;注意，磁轴的磁极朝向分为 N 极朝灯，N 极朝下，N 极朝上三种，不同类型互不兼容，部分支持多种方案，购买时注意区别。

<div style="text-align: right;color: lightgray;"><i><sup>[1]</sup> 在 mania 几乎用不上的功能可自行查阅资料，包括但不限于：DKS / 动态键程、MT / 双效点击、SOCD / 瞬时释放、TK / 切换开关、ANA IN / 模拟输入，下同；其中 DKS / 动态键程可极大提升 std 模式水平，存在争议；部分功能可提高 FPS 游戏水平。</i></div>

## 2. 机械键盘

&emsp;&emsp;每个按键都使用独立机械开关（称为轴）进行触发的键盘。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-138.png" width="280" alt="mechanical switch"></td>
</tr></table>
<figcaption>图 2-138 机械轴轴体结构</figcaption>
</figure>

&emsp;&emsp;市面上除某些特殊轴体外均可视为以下轴体的各种子类型<sup>[2]</sup>。<br />
&emsp;&emsp;**青轴**：具有强烈的段落感和清脆的按键声，但声音较大，可能影响他人。<br />
&emsp;&emsp;**茶轴**：有轻微的段落感，声音比青轴安静。<br />
&emsp;&emsp;**红轴**：手感直上直下，没有段落感，触发力度轻。既能兼顾长时间打字，又能满足游戏快速反应。<br />
&emsp;&emsp;**黑轴**：手感直上直下，但按压需要的力度更大，回弹更有力。较重的压力可能让长时间使用感到疲劳。<br />
&emsp;&emsp;**银轴**：极短触发键程和快速响应为主要特点的轴体，容易误触。<br />
&emsp;&emsp;使用寿命在 5000 万次左右。

<div style="text-align: right;color: lightgray;"><i><sup>[2]</sup> 商品介绍写类茶轴、类红轴即类似于茶轴或红轴的轴体。</i></div>

## 3. 薄膜键盘

&emsp;&emsp;带有导电触点的上下两层电路被中间带有开孔的隔离层分开，电路处于断开状态。当你按下键帽时，力量会传递到底部的硅胶或橡胶帽，使其变形，从而推动上电路层穿过隔离层的开孔与下电路层接触，形成通路，键盘控制器检测到这个信号后，就完成了一次按键输入。<br />
&emsp;&emsp;手感比较随机；整体比较轻；使用寿命在 100 万 - 300 万之间，较短；薄膜容易因各种原因老化，用力敲击会加速此过程，手感逐渐变差。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-139.png" alt="membrane keyboard"></td>
</tr></table>
<figcaption>图 2-139 薄膜键盘结构</figcaption>
</figure>

&emsp;&emsp;**火山口结构**：键帽的键柱直接套在橡胶帽上。这种结构键程较长，但按键可能不够稳定，容易晃动。<br />
&emsp;&emsp;**剪刀脚结构 / X 结构**：在键帽和橡胶帽之间增加了一个类似剪刀的支架。这使得按键受力更均匀，稳定性好，键程较短，常见于笔记本电脑和超薄键盘。

## 4. 静电容键盘

&emsp;&emsp;通过按压导致轴体内电容值变化实现触发，无物理触点接触。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-140.png" alt="capacitive keyboard"></td>
</tr></table>
<figcaption>图 2-140 静电容键盘结构</figcaption>
</figure>

&emsp;&emsp;由于触发依赖于电容值变化量而非固定的触点通断，一些键盘支持通过软件或快捷键调整触发点；一些传统静电容键盘采用分区压力设计，即不同区域的按键采用不同的触发压力。<br />
&emsp;&emsp;寿命可达 1 亿次以上；触发稳定；噪音较小；部分产品支持可调触发键程。

## 5. 光轴键盘

&emsp;&emsp;利用红外光线通断进行光学感应。和机械轴一样分为段落轴和线性轴。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-141.png" alt="optical switch"></td>
</tr></table>
<figcaption>图 2-141 光轴键盘结构</figcaption>
</figure>

&emsp;&emsp;寿命可达 1 亿次以上；响应快；噪音较小；环境抗性高。

## 6. 模拟光轴键盘

&emsp;&emsp;通过测量穿过轴体的光通量来检测按压深度。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-142.png" alt="analog optical switch"></td>
</tr></table>
<figcaption>图 2-142 模拟光轴结构和原理</figcaption>
</figure>

&emsp;&emsp;可调节触发与快速触发；响应快；寿命长。

---
