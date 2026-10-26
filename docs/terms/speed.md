# 社区俚语（四）：放置飞升、投皮、等效 BPM

## 1. 放置飞升

&emsp;&emsp;一段时间没有玩游戏之后实力突飞猛进。充足的休息确实对实力提升有很大帮助。

&emsp;&emsp;概率比较高，但每个人都不太一样。

## 2. 投皮 / 投机取巧皮

&emsp;&emsp;用修改皮肤图片文件的方式得到面条尾部较短的皮肤，具体方法操作可见 [osu!mania 的投机取巧皮肤中面条的机制简述与修改 - 哔哩哔哩](https://www.bilibili.com/opus/734958888388919331)；此类皮肤在减少读谱难度的同时又不会损失太多准度，故得名**投机取巧皮**。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-165-1.png" width="200" alt="no cheat skin"></td>
<td><img src="/VSRG-4K-wiki/images/2-165-2.png" width="300" alt="cheat skin"></td>
</tr></table>
<figcaption>图 2-165 左图为无投皮，右图为一种投皮<sup>[1]</sup></figcaption>
</figure>

<div style="text-align: right;color: lightgray;"><i><sup>[1]</sup> 除此之外还有非常多种类的投皮，<a href="https://www.bilibili.com/opus/734958888388919331">osu!mania 的投机取巧皮肤中面条的机制简述与修改 - 哔哩哔哩</a>有详细介绍；左图为玩家 Jakads 的皮肤，右图为玩家 cheewee10 的皮肤。</i></div>

## 3. 等效 BPM

<figure>
<table>
  <thead>
    <tr>
      <th align="center">键型 &amp; 排列</th>
      <th align="center">常见分度</th>
      <th align="center">音符时值</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>叠键，切换，纵连，锚</td><td>16</td><td>1/4</td></tr>
    <tr><td>乱键</td><td>32</td><td>1/8</td></tr>
    <tr><td>在切换中看做纵连的锚键</td><td>8</td><td>1/2</td></tr>
  </tbody>
</table>
<figcaption>表 2-10 键型 &amp; 排列的常见分度和音符时值</figcaption>
</figure>

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-166.png" width="420" alt="anchor as jack"></td>
</tr></table>
<figcaption>图 2-166 锚看做纵连(FUTURE DOMINATORS[NB5 Hard 54235] by IcyWorld)</figcaption>
</figure>

&emsp;&emsp;仅观察切换中的锚键，它们的分度为 8 分，音符时值为 $\dfrac{1}{2}$，社区有时直接将其当做锚键的 BPM，此时根据分度以及 BPM 可直接计算出单指 KPS。

&emsp;&emsp;当我们讨论某键型的 BPM 时，常将其转化为等效 BPM，即

&emsp;&emsp;**$\text{等效BPM}=\text{实际BPM}\times\dfrac{\text{实际分度}}{\text{常见分度}}$**

&emsp;&emsp;如下图，已知乱常见分度为 32 分，该谱面 BPM133、实际分度为 48，则

&emsp;&emsp;**$133\times\dfrac{48}{32}=199.5$**

&emsp;&emsp;为等效 BPM，即该乱为 133BPM 48 分，等效 199.5 乱。

<figure>
<table><tr>
<td><img src="/VSRG-4K-wiki/images/2-167.png" width="300" alt="Qualia"></td>
</tr></table>
<figcaption>图 2-167 Qualia (Choukyorisou)[Easy] by Xingyue</figcaption>
</figure>

---

