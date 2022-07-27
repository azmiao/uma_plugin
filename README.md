## uma_info

这是一个适用hoshinobot的赛马娘功能插件，数据来自马娘官网和bwiki，所有功能的数据均可自动更新

这里包含了之前开源了的功能以及新开发的一大堆功能，其他功能仍在锐意开发中，有问题请在本仓库提交issue，请务必带上报错的日志完整截图，并说明清楚即可

如遇问题可以先看看已关闭的历史issue有没有类似的参考一下。

### ★ 纯粹用爱发电，如果你喜欢的话，请给仓库点一个star支持一下23333 ★

<details>
<summary>点我查看主要的几个功能模块</summary>

（具体命令请看本页面下方功能命令和描述）

+ [马娘新闻播报](https://github.com/azmiao/umamusume_news) 【已支持台/日服】

+ [马娘模拟抽卡](https://github.com/azmiao/uma_gacha)

+ 马娘基础数据库

+ 支援卡节奏榜【已支持台/日服】

+ 相性计算器【台/日通用】

+ 马娘黄历【台/日通用】

+ 马娘耐力计算器【台/日通用】

+ 马娘表情包【台/日通用】

+ 马娘漫画【台/日通用】

+ 马娘限时任务

+ 马娘技能查询

+ 育成目标查询【台/日差不多通用】

</details>

<details>
<summary>点我查看独立版和整合版的区别</summary>

+ 图片文件夹目录不一致，因此和独立版的马娘抽卡稍有不一致，但是删除独立版马娘抽卡后再装本整合版插件，理论上可以直接使用之前的图片文件，反之需重新下载数据

+ [马娘新闻播报](https://github.com/azmiao/umamusume_news) 和 [马娘模拟抽卡](https://github.com/azmiao/uma_gacha) 的代码以及功能性均与本整合版不同，后续将仅维护本整合版

+ 其他所有整合版里功能都不能单独拿出来直接用，不然必报错

</details>

## 本项目地址：
https://github.com/azmiao/uma_plugin/

## 最近的更新日志

22-07-27    v2.5.2  同步官网更新马娘：谋勇兼备，敏锐奇才，北港火山，更新完插件后请使用命令“手动更新马娘数据”

22-07-20    v2.5.1  临时兼容一下最新的卡池，有BUG讲究一下吧，后续打算重写，不然实在不好整

22-07-17    v2.5.0  新增一个小功能“马娘速查”，方便萌新

22-07-16    v2.4.0  美化帮助界面，同时方便autohelp服务模式显示，详情本文末尾

</details>

<details>
<summary>更以前的更新日志</summary>

22-07-16    v2.3.1  修复技能查询BUG同时新增繁中技能查询 by[@Yui-xy](https://github.com/Yui-xy)，[issue #28](https://github.com/azmiao/uma_plugin/issues/28)

22-07-08    v2.3.0  新增查询赛程的育成目标功能，使用命令 “查目标 角色名” 即可，结果图片仿自bwiki，[issue #25](https://github.com/azmiao/uma_plugin/issues/25)

22-07-06    v2.2.2  修复台服支援卡命名方式变化后的BUG，更新后请务必手动删除uma_support_chart文件夹下的`sup_config_tw.json`再重启hoshino

22-07-05    v2.2.1  修复支援卡节奏榜网页更新后的BUG，更新后请务必手动删除uma_support_chart文件夹下的`sup_config.json`再重启hoshino，[issue #24](https://github.com/azmiao/uma_plugin/issues/24)

22-06-30    v2.2.0  新增台服马娘新闻功能，整进了“马娘新闻帮助”里

22-06-30    v2.1.0  新增台服支援卡节奏榜功能，整进了“支援卡节奏榜帮助”里

22-06-24    v2.0.4  请务必更新！同步translators更新，以便修复马娘新闻翻译显示不全的BUG

22-06-23    v2.0.3  马娘新闻修复不具合翻译不了的BUG和其他遇不到的BUG，且现在支持配置代理，已添加进本文档的食用教程里

22-06-19    v2.0.2  马娘新闻部分代码改进优化，并且翻译结果默认采用转发消息发送，可以自行更换

22-05-05    v2.0.1  优化更新逻辑，当更新失败自动回退防止再次更新时出错，同时更换数据镜像站提高更新速度

22-04-25    v2.0    大版本更新！！！强烈推荐，之后可无需APIKEY，注意：更新后需要更新安装依赖，并重新“手动更新马娘数据”

22-04-24    v1.7    新增马娘技能查询功能

22-04-15    v1.6    新增马娘限时任务功能，并修复一些描述，此版本开始需要更新依赖

22-04-11    v1.5.3  修复图片文件夹的问题，并修复由于也文摄辉背景图分辨率过高导致OCR无结果的问题

22-04-10    v1.5.2  将所有的图片文件夹移动至umamusume文件夹下

22-03-30    v1.5.1  重构支援卡节奏榜代码，理论上性能更好，冗余更低

22-03-28    v1.5    新增马娘一格漫画功能

22-03-28    v1.4    新增马娘表情包功能

22-03-20    v1.3.3    节奏榜新增了 友人卡节奏榜

22-03-19    v1.3.2  新增了更新数据时自动下载语音文件，更新到此版本后需要手动更新一下数据，当然等半夜的自动更新也行

22-03-18    v1.3.1  调整了自动更新策略，将在更新时生成一个缓存文件，更新完再复制过去，以防止更新期间部分功能不能用，顺便新增手动更新相性信息功能

22-03-09    v1.3    新增了“马娘耐力计算器”功能，但数据为 根性与下坡 改版前的数据，且为非常理想的数值

22-03-09    v1.2    一些调整，以及修改部分文件使之规范化github储存库，方便 git pull, [pull #4](https://github.com/azmiao/uma_plugin/pull/4)

22-03-06    v1.1    新增了“马娘签到”功能

22-03-04    v1.0    first commit

</details>

## 注意事项

### 如何更新

#### 如何监控更新：建议使用 RSS 或者我之前的插件 [github_reminder](https://github.com/azmiao/github_reminder) 添加[本仓库链接](https://github.com/azmiao/uma_plugin/)监控本仓库commit，以便跟随功能更新和BUG修复

> 若是从 v1.2 版本之后(包括 v1.2)的版本更新到最新版，直接在你的 `hoshino/modules/uma_plugin文件夹里，打开powershell输入下方命令，运行完重启hoshinobot即可：

（注：v2.0开始请删除您的APIKEY.txt后再使用命令）

```
git pull
```
git pull不成功的请自行百度解决，一般是有文件冲突导致的，删了那个文件再git pull就好了

> 若是从 v1.2 版本之前(不包括 v1.2)的版本更新到最新版，建议直接把 `uma_plugin` 文件夹删了，再按照本页面最底下的安装教程重新安装一遍。并且建议删除前，把文件 `/uma_info/config.json` 备份出来，这样重新安装完就不用再手动更新马娘数据了。否则重装后需要重新使用群命令："手动更新马娘数据" 更新基础数据

</details>

## 功能命令和描述

### 维护组的命令

<details>
<summary><font size = 4>点我展开</font></summary>

马娘数据库的：

 - 手动更新马娘数据

马娘相性的：

 - 手动更新相性信息

马娘抽卡的：

 - 更新马娘信息

 - 重载赛马娘卡池

马娘表情包的：

 - 手动更新马娘表情包

马娘漫画的：

 - 手动更新马娘漫画

马娘限时任务的：

 - 手动更新限时任务

马娘技能的：

 - 手动更新马娘技能

马娘新闻的：

 - 马娘新闻翻译转发模式on/off

</details>

### 注：发送“马娘帮助”可以查看马娘插件所有的帮助汇总

### 没有图片版的【马娘黄历】只有一个命令：马娘签到

![](https://img.gejiba.com/images/1d987330ad0a9e041321cdf433e5c7c4.png)

<details>
<summary><font size = 4>其他功能的图片版帮助</font></summary>

![](https://img.gejiba.com/images/14656fafe6c33ac7f0429c572a251808.png)
![](https://img.gejiba.com/images/3aff9b9882954e3f8206328444627a93.png)
![](https://img.gejiba.com/images/9b012de7f710229bea2fa7e867b031bc.png)
![](https://img.gejiba.com/images/ca1e78b1faf8a2a58bfbe62d04cff247.png)
![](https://img.gejiba.com/images/b7fe400d61fbefc8cfa52f87683ce507.png)
![](https://img.gejiba.com/images/63c84910b6117c7eb5d8f7a706f2ff9a.png)
![](https://img.gejiba.com/images/90d76cb9ac80c7cbe0d01e0403954a29.png)
![](https://img.gejiba.com/images/881d1f7010c79b8cfcc6b3dad8c17028.png)
![](https://img.gejiba.com/images/2bef2337722582aa066899258c8c94c0.png)
![](https://img.gejiba.com/images/9c429aa7be4a6f997b22c54f11eda3c6.png)
![](https://img.gejiba.com/images/58fadc7fba87e876ea67c4c9e89c4668.png)

</details>

</details>

## 食用教程：

<details>
<summary>点我展开</summary>

1. git clone本插件（注：一定要git clone，不要下载压缩包，另外请确保git环境变量正常）：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
    ```
    git clone https://github.com/azmiao/uma_plugin
    ```

2. 如果之前装过独立版的 [马娘新闻播报](https://github.com/azmiao/umamusume_news) 和 [马娘模拟抽卡](https://github.com/azmiao/uma_gacha) 的，请先删除那两个文件夹，没有就跳过这一步

3. 安装依赖：

    到HoshinoBot\hoshino\modules\uma_plugin目录下，管理员方式打开powershell
    ```
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
    ```

4. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'uma_plugin'

    然后重启 HoshinoBot

    装完插件后首次启动时会更新马娘各种数据，按带宽的大小可能需要3-10分钟不等，请耐心等待，您可以看着控制台看他有没有报错，除了在首次启动本插件的时候会在更新马娘基础数据库（要下好多语音文件和图片）的时候更新一段时间和马娘抽卡（要下好多图片）的时候更新一段时间，其他和再次启动的时候都会很快的。

6. 额外功能：（自动提醒）

    在某个群里发消息输入下文以开启马娘生日提醒
    ```
    开启 uma_bir_push
    ```

    在某个群里发消息输入下文以开启马娘新闻播报，一个日服，一个台服
    ```
    开启 umamusume-news-poller
    ```
    ```
    开启 umamusume-news-poller-tw
    ```

    可以通过发消息输入"lssv"查看这个功能前面是不是⚪来确认是否开启成功

7. 马娘新闻配置代理（可选）

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

8. 更好看的帮助界面，见本文末尾（可选）

</details>

## 另有图片预览，请看：

https://www.594594.xyz/2022/03/04/uma_plugin/

## 支持[autohelp](https://github.com/SonderXiaoming/autohelp)

<details>
<summary>点我展开</summary>

可显示更好看的帮助界面

推荐添加的`black.json`：

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
    "uma_gacha": "马娘抽卡",
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
