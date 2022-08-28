<p align="center">
  <a href="https://github.com/azmiao/uma_plugin/">
    <img src="https://img.gejiba.com/images/dab0cfe092c1f5f77ae54cd3b488a0d4.png" width="200" height="200" alt="uma_plugin">
  </a>
</p>

<div align="center">

# 赛马娘QQ机器人插件

### ★ 纯粹用爱发电，如果你喜欢的话，请给仓库点一个star支持一下2333 ★

#### 如有魔改版请遵守本插件的GPL3.0开源协议并保持开源！！最好注明来源支持一下作者hhh

#### 如果想快速从零开始搭建一个这样的机器人，可以看我的教程哦：[让我栞栞](https://www.594594.xyz/2022/03/05/uma_bot/)

[![image](https://img.shields.io/badge/license-GPL3.0-blue.svg)](https://raw.githubusercontent.com/azmiao/uma_plugin/main/LICENSE)
[![image](https://img.shields.io/badge/release-2.6.6-orange.svg)](https://github.com/azmiao/uma_plugin)
[![image](https://img.shields.io/badge/auther-AZMIAO-blue.svg)](https://github.com/azmiao/uma_plugin)

</div>

<p align="center">
  <a href="https://github.com/azmiao/uma_plugin/blob/main/README.md">文档</a>
  ·
  <a href="https://github.com/azmiao/uma_plugin/discussions">讨论</a>
  ·
  <a href="https://github.com/azmiao/uma_info_data">基础数据库</a>
</p>

<details>
<summary>插件说明</summary>

这是一个适用[hoshinobot](https://github.com/Ice-Cirno/HoshinoBot)的赛马娘功能插件，数据来自：

 + [马娘官网](https://github.com/azmiao/uma_info_data)
 + [bwiki](https://wiki.biligame.com/umamusume)
 + [马娘基础数据库](https://github.com/azmiao/uma_info_data)
 + [台服马娘官网](https://uma.komoejoy.com/)
 + [乌拉拉大胜利](https://urarawin.com/#/)

</details>

<details>
<summary>反馈说明</summary>

 + 有空的话建议先看看已关闭的历史issue有没有类似的参考一下
 + 可直接在本仓库提交issue，但请带上报错的日志完整截图，并说明清楚哦
 + 如果按照我的教程搭建机器人遇到的问题可以前往 [Discussions](https://github.com/azmiao/uma_plugin/discussions) 进行讨论

</details>

<details>
<summary>当前支持的功能 和 支持的服务器</summary>

（具体命令请看本页面下方功能命令和描述）

+ 马娘新闻播报【已支持台/日服】
+ 马娘模拟抽卡v2【已支持台/日/韩/B服】
+ 马娘基础数据库【台/日通用】
+ 支援卡节奏榜【已支持台/日服】
+ 相性计算器【台/日通用】
+ 马娘黄历【台/日通用】
+ 马娘耐力计算器【台/日通用】
+ 马娘表情包【台/日通用】
+ 马娘漫画【台/日通用】
+ 马娘限时任务
+ 马娘技能查询【已支持台/日服】
+ 育成目标查询【台/日差不多通用】

</details>

<details>
<summary>版本号的编号方式</summary>

 + v2.5.1为例：
 + v2为大版本号，除非有超级有益的重构类大更新，一般不会更新
 + 5为功能迭代版本号，有新功能或者某一功能重写了就会更新
 + 1为BUG修复/数据更新版本号，有关键性的BUG修复或者重要的数据更新就更新
 + 其余不刷版本号的更新，一般来说为不影响大局的BUG修复或小数据更新

</details>

## 本仓库链接

https://github.com/azmiao/uma_plugin/

## 最近的更新日志

 + 22-08-28     v2.6.6  临时改变节奏榜的内容为bwiki上巅峰杯歌姬杯分开的节奏榜，新增可选设置插件默认服务器，配置方法在本文末。注意：本次更新需要使用命令`git pull -f`来更新，并且`properties.json`的配置可能回到默认状态

 + 22-28-28     v2.6.5  修复耐力计算的BUG，修复方案来自[@aaaaaaria](https://github.com/aaaaaaria)，[issue #36](https://github.com/azmiao/uma_plugin/issues/36)

 + 22-08-22     v2.6.4  常规数据更新，新增红宝石和凯斯的别名，更新后记得“手动更新马娘数据”或者等半夜自动更新

 + 22-08-18     v2.6.3  新增图片可选发送形式`properties.json`，配置方法在本文末, [issue #37](https://github.com/azmiao/uma_plugin/issues/37)

</details>

<details>
<summary>◆ 更以前的更新日志</summary>

 + 22-08-15     v2.6.2  修复台服节奏命名规则修改后产生的BUG

 + 22-08-08     v2.6.1  修复卡池界面更新的BUG

 + 22-08-02     v2.6.0  完全重写马娘抽卡功能，减少人为BUG率，且能切换服务器支持日台韩B服，且能切换卡池，缩减抽卡结果长度防刷屏，[issue #27](https://github.com/azmiao/uma_plugin/issues/27)，[issue #32](https://github.com/azmiao/uma_plugin/issues/32)

 + 22-07-27     v2.5.2  同步官网更新马娘：谋勇兼备，敏锐奇才，北港火山，更新完插件后请使用命令“手动更新马娘数据”

 + 22-07-20     v2.5.1  临时兼容一下最新的卡池，有BUG讲究一下吧，后续打算重写，不然实在不好整

 + 22-07-17     v2.5.0  新增一个小功能“马娘速查”，方便萌新

 + 22-07-16     v2.4.0  美化帮助界面，同时方便autohelp服务模式显示，详情本文末尾

 + 22-07-16     v2.3.1  修复技能查询BUG同时新增繁中技能查询 by[@Yui-xy](https://github.com/Yui-xy)，[issue #28](https://github.com/azmiao/uma_plugin/issues/28)

 + 22-07-08     v2.3.0  新增查询赛程的育成目标功能，使用命令 “查目标 角色名” 即可，结果图片仿自bwiki，[issue #25](https://github.com/azmiao/uma_plugin/issues/25)

 + 22-07-06     v2.2.2  修复台服支援卡命名方式变化后的BUG，更新后请务必手动删除uma_support_chart文件夹下的`sup_config_tw.json`再重启hoshino

 + 22-07-05     v2.2.1  修复支援卡节奏榜网页更新后的BUG，更新后请务必手动删除uma_support_chart文件夹下的`sup_config.json`再重启hoshino，[issue #24](https://github.com/azmiao/uma_plugin/issues/24)

 + 22-06-30     v2.2.0  新增台服马娘新闻功能，整进了“马娘新闻帮助”里

 + 22-06-30     v2.1.0  新增台服支援卡节奏榜功能，整进了“支援卡节奏榜帮助”里

 + 22-06-24     v2.0.4  请务必更新！同步translators更新，以便修复马娘新闻翻译显示不全的BUG

 + 22-06-23     v2.0.3  马娘新闻修复不具合翻译不了的BUG和其他遇不到的BUG，且现在支持配置代理，已添加进本文档的食用教程里

 + 22-06-19     v2.0.2  马娘新闻部分代码改进优化，并且翻译结果默认采用转发消息发送，可以自行更换

 + 22-05-05     v2.0.1  优化更新逻辑，当更新失败自动回退防止再次更新时出错，同时更换数据镜像站提高更新速度

 + 22-04-25     v2.0    大版本更新！！！强烈推荐，之后可无需APIKEY，注意：更新后需要更新安装依赖，并重新“手动更新马娘数据”

 + 22-04-24     v1.7    新增马娘技能查询功能

 + 22-04-15     v1.6    新增马娘限时任务功能，并修复一些描述，此版本开始需要更新依赖

 + 22-04-11     v1.5.3  修复图片文件夹的问题，并修复由于也文摄辉背景图分辨率过高导致OCR无结果的问题

 + 22-04-10     v1.5.2  将所有的图片文件夹移动至umamusume文件夹下

 + 22-03-30     v1.5.1  重构支援卡节奏榜代码，理论上性能更好，冗余更低

 + 22-03-28     v1.5    新增马娘一格漫画功能

 + 22-03-28     v1.4    新增马娘表情包功能

 + 22-03-20     v1.3.3    节奏榜新增了 友人卡节奏榜

 + 22-03-19     v1.3.2  新增了更新数据时自动下载语音文件，更新到此版本后需要手动更新一下数据，当然等半夜的自动更新也行

 + 22-03-18     v1.3.1  调整了自动更新策略，将在更新时生成一个缓存文件，更新完再复制过去，以防止更新期间部分功能不能用，顺便新增手动更新相性信息功能

 + 22-03-09     v1.3    新增了“马娘耐力计算器”功能，但数据为 根性与下坡 改版前的数据，且为非常理想的数值

 + 22-03-09     v1.2    一些调整，以及修改部分文件使之规范化github储存库，方便 git pull, [pull #4](https://github.com/azmiao/uma_plugin/pull/4)

 + 22-03-06     v1.1    新增了“马娘签到”功能

 + 22-03-04     v1.0    first commit

</details>

## 更新

### 1.如何更新

> 在你的 `hoshino/modules/uma_plugin` 文件夹里，打开powershell输入 `git pull` ，运行完重启hoshinobot即可

如果报错如下：
```
error: Your local changes to the following files would be overwritten by merge: 
Please, commit your changes or stash them before you can merge
```
一般是有因为你修改了部分代码导致的，删了它提示的那些文件再`git pull`就好了

### 2.想要推送更新提醒？

可以使用我之前的插件 [github_reminder](https://github.com/azmiao/github_reminder) 添加 本仓库网址 即可监控本仓库commit，以便跟随功能更新和BUG修复

</details>

## 功能命令和描述

<details>
<summary><font size = 4>维护组的命令</font></summary>

| 子模块 | 命令 |
|  ----  | ----  |
| 马娘数据库 | 手动更新马娘数据 |
| 马娘相性 | 手动更新相性信息 |
| 马娘抽卡 | 更新马娘卡池 |
| 马娘表情包 | 手动更新马娘表情包 |
| 马娘漫画 | 手动更新马娘漫画 |
| 马娘限时任务 | 手动更新限时任务 |
| 马娘技能 | 手动更新马娘技能 |
| 马娘新闻 | 马娘新闻翻译转发模式on |
| 马娘新闻 | 马娘新闻翻译转发模式off |

</details>

<details>
<summary><font size = 4>子模块的图片版帮助</font></summary>

![](https://img.gejiba.com/images/14656fafe6c33ac7f0429c572a251808.png)
![](https://img.gejiba.com/images/3aff9b9882954e3f8206328444627a93.png)
![](https://img.gejiba.com/images/9b012de7f710229bea2fa7e867b031bc.png)
![](https://img.gejiba.com/images/ca1e78b1faf8a2a58bfbe62d04cff247.png)
![](https://img.gejiba.com/images/4d0aa3a260363002bb4edabb689c141e.png)
![](https://img.gejiba.com/images/63c84910b6117c7eb5d8f7a706f2ff9a.png)
![](https://img.gejiba.com/images/90d76cb9ac80c7cbe0d01e0403954a29.png)
![](https://img.gejiba.com/images/881d1f7010c79b8cfcc6b3dad8c17028.png)
![](https://img.gejiba.com/images/2bef2337722582aa066899258c8c94c0.png)
![](https://img.gejiba.com/images/9c429aa7be4a6f997b22c54f11eda3c6.png)
![](https://img.gejiba.com/images/58fadc7fba87e876ea67c4c9e89c4668.png)

</details>

### 汇总命令 (群里发送“马娘帮助”也可查看)

![汇总命令](https://img.gejiba.com/images/1d987330ad0a9e041321cdf433e5c7c4.png)

## 插件安装

<details>
<summary>点我展开</summary>

1. git clone本插件（注：一定要git clone，不要下载压缩包，另外请确保git环境变量正常）：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/azmiao/uma_plugin
    ```

2. 安装依赖：

    到HoshinoBot\hoshino\modules\uma_plugin目录下，管理员方式打开powershell
    ```
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
    ```

3. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'uma_plugin'

    然后重启 HoshinoBot

    装完插件后首次启动时会更新马娘各种数据，按带宽的大小可能需要3-10分钟不等，请耐心等待，您可以看着控制台看他有没有报错。

4. 额外功能：（自动提醒）

    在某个群里发消息输入下文以开启马娘生日提醒（提醒当天哪知马娘生日）
    ```
    开启 uma_bir_push
    ```

    在某个群里发消息输入下文以开启马娘新闻播报，一个日服，一个台服（推送新闻更新）
    ```
    开启 umamusume-news-poller
    ```
    ```
    开启 umamusume-news-poller-tw
    ```

    可以通过发消息输入"lssv"查看这个功能前面是不是⚪来确认是否开启成功

5. 马娘新闻配置代理（可选）

    > Q经常连不上马娘官网咋办：

    A：现在受各种影响导致的连不上马娘官网，建议配置代理，请先自购代理，然后吧umamusume_news文件夹里的 `news_spider.py` 的第15行换成：
    (注意1081请换成你自己的代理端口号)
    ```
    proxy = {
        "http": "http://localhost:1081",
        "https": "http://localhost:1081"
    }
    ```
    更换后台服和日服官网都会走代理。
    如果不需要代理就换回原来默认的：
    ```
    proxy = {}
    ```

</details>

## 额外定制配置（可选）

<details>
<summary>点我展开</summary>

### 该功能的所有配置均在插件目录下的 `properties.json` 里

> 可选图片发送形式：

如果你使用docker，且hoshino和gocqhttp不在一个容器里，可选base64，默认file
```
    "image_send_form": {
        "notes": "图片发送形式，可选值有 [ file | base64 ]",
        "current": "file"
    },
```

> 可选默认服务器

如果你主要玩的不是日服，可以将所有子模块修改至你玩的服务器，可选[ jp | tw | ko | bili ]
```
    "default_server": {
        "notes": "一键切换所有子的模块的服务器，可选值有 [ jp | tw | ko | bili ]",
        "current": "jp"
    },
```

> 其他定制功能还在画饼阶段

</details>

## [Autohelp](https://github.com/SonderXiaoming/autohelp)推荐配置(可选)

<details>
<summary>点我展开</summary>

安装 [autohelp](https://github.com/SonderXiaoming/autohelp) 即可，可显示更好看的帮助界面

关于本马娘插件推荐添加的`black.json`：

```
{
    "uma_bir_push",
    "umamusume-news-poller",
    "umamusume-news-poller-tw",
}
```

推荐添加的`replace.json`：

```
{
    "uma_almanac": "马娘黄历",
    "uma_comic": "马娘漫画",
    "uma_compatibility": "马娘相性",
    "uma_endurance": "马娘耐力",
    "uma_face": "马娘表情包",
    "uma_gacha_v2": "马娘抽卡V2",
    "uma_info": "马娘基础数据查询",
    "uma_skills": "马娘技能查询",
    "uma_support_chart": "马娘支援卡节奏榜",
    "uma_target": "马娘育成目标查询",
    "uma_tasks": "马娘限时任务查询",
    "umamusume_news": "马娘新闻",
    "uma_help": "马娘帮助汇总",
}
```
</details>