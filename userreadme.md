# 当前支持的功能 和 支持的服务器

+ 马娘新闻播报【已支持台/日/B服】

+ 马娘模拟抽卡【已支持台/日/韩/B服】

+ 马娘基础数据库【台/日/韩/B服通用】

+ 支援卡节奏榜【已支持台/日/B服】

+ 相性计算器【台/日/韩/B服通用】

+ 马娘黄历【台/日/韩/B服通用】

+ 马娘耐力计算器【台/日/韩/B服通用】

+ 马娘表情包【台/日/韩/B服通用】

+ 马娘漫画【台/日/韩/B服通用】

+ 马娘限时任务【台/日/韩/B服通用】

+ 马娘技能查询【台/日/韩/B服通用】

+ 育成目标查询【台/日/韩/B服通用】

（具体命令请看本页面下方功能命令和描述）

## 功能命令和描述

### 注：群内查看功能帮助可以发送：“马娘帮助”

+ 维护组的所有命令

|  子模块   |      命令       |
|:------:|:-------------:|
| 马娘数据库  |   手动更新马娘数据    |
|  马娘相性  |   手动更新相性信息    |
|  马娘抽卡  |    更新马娘卡池     |
| 马娘表情包  |   手动更新马娘表情包   |
|  马娘漫画  |   手动更新马娘漫画    |
| 马娘限时任务 |   手动更新限时任务    |
|  马娘技能  |   手动更新马娘技能    |
|  马娘新闻  | 马娘新闻翻译转发模式on  |
|  马娘新闻  | 马娘新闻翻译转发模式off |

+ 马娘基础数据库模块

|       功能命令       |              介绍               |        功能命令         |   介绍    | 
|:----------------:|:-----------------------------:|:-------------------:|:-------:|
|     查今天生日马娘      |       看看今天哪只马娘生日(仅限马娘)        |      查角色cv xx       | xx为角色名字 |   
|     查马娘生日 xx     |   xx为马娘名字，查询这只马娘是哪天生日(仅限马娘)   |      查角色身高 xx       | xx为角色名字 |     
|    查生日马娘 m-d     | m-d就是 m月d日 ，查询这天有哪些马娘生日(仅限马娘) |      查角色体重 xx       | xx为角色名字 |       
|     查角色id xx     |            xx为角色名字            |      查角色三围 xx       | xx为角色名字 |
|    查角色日文名 xx     |            xx为角色名字            |      查角色制服 xx       | xx为角色名字 |    
|    查角色中文名 xx     |            xx为角色名字            |      查角色决胜服 xx      | xx为角色名字 |    
|    查角色英文名 xx     |            xx为角色名字            |      查角色原案 xx       | xx为角色名字 |    
|     查角色分类 xx     |            xx为角色名字            |      查角色适应性 xx      | xx为角色名字 |     
|     查角色语音 xx     |            xx为角色名字            |      手动更新马娘数据       | 功能限维护组  |
|     查角色头像 xx     |            xx为角色名字            |    
| (每天1:31自动更新马娘数据) |            该功能没有命令            | (每天9:31自动推送该日生日的马娘) | 该功能没有命令 |

+ 相性计算器

|                  功能命令                  |                                                                         介绍                                                                          |
|:--------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------:|
|                 马娘相性帮助                 |                                                                      看看详细帮助内容                                                                       |   
| 查相性 本体 父母1 祖父母1 祖父母2 父母2 祖父母3 祖父母4 胜鞍数 | 1.直接按照下面的指令写马名即可，请按顺序写，注意空格别漏<br>2.胜鞍数为胜鞍+金牌的总个数，类型为整数，且可写可不写<br>3.判断胜鞍：(父母1和祖父母1相同的重赏胜场数)+(父母1和祖父母2相同的重赏胜场数)+(父母2和祖父母3相同的重赏胜场数)+(父母2和祖父母4相同的重赏胜场数) |   
|   查相性 本体 父母1 祖父母1 祖父母2 父母2 祖父母3 祖父母4   |                                                                     同上，表示可以不加胜鞍                                                                     |
|              查相性 马娘1 马娘2               |                                                                 查两只马娘之间的相性，这里不可以加胜鞍                                                                 |
|                 相性榜 马娘                 |                                                               相性榜是指生成对这只马娘相性最好的马娘排行榜                                                                |  

+ 支援卡节奏榜

|           功能命令           |     介绍     | 
|:------------------------:|:----------:|
|          速卡节奏榜           |   对应速度卡    |  
|          耐卡节奏榜           |   对应耐力卡    | 
|          力卡节奏榜           |   对应力量卡    | 
|          根卡节奏榜           |   对应根性卡    |  
|          智卡节奏榜           |   对应智力卡    | 
| 台服只需在前面加上前缀<kbd>台服</kbd> | 例如：台服速卡节奏榜 |
| B服只需在前面加上前缀<kbd>B服</kbd> | 例如：B服速卡节奏榜 |
  
+ 马娘新闻播报

|   功能命令   |               介绍                | 
|:--------:|:-------------------------------:|
|   马娘新闻   |            查看最近五条新闻             | 
|  台服马娘新闻  |           查看最近五条台服新闻            | 
|  B服马娘新闻  |           查看最近五条B服新闻            | 
|   新闻翻译   |     查看翻译命令和新闻编号（限近5条）[仅限日服]     |    
|  新闻翻译 1  | 翻译第1条新闻，编号可选值(1/2/3/4/5) [仅限日服] | 
| (马娘新闻推送) |             该功能没有命令             | 

+ 马娘模拟抽卡

| 功能命令          | 介绍           | 功能命令          | 介绍                            |
|---------------|--------------|---------------|-------------------------------| 
| 查看马娘卡池        | 看马娘当前的池子     | @bot支援卡抽满破    | 支援卡抽一张UP至满破                   |
| @bot马娘单抽      | 马娘池子单抽       | 查看马娘卡池        | 查看本群设置的服务器和池子信息               |
| @bot马娘十连      | 马娘池子十连       | 切换马娘服务器       | 限群管，命令后加服务器名                  |
| @bot马之井       | 马娘池子抽一井      | 切换马娘卡池        | 限群管，命令后加卡池ID                  |
| @bot育成卡单抽     | 育成卡池子单抽      | 更新马娘卡池        | 限维护组，更新数据                     |   
| @bot育成卡十连     | 育成卡池子十连      | 重载赛马娘卡池       | 仅刷新马娘当前UP卡池的信息（不含图片数据），功能限维护组 |
| @bot育成卡井      | 育成卡池子抽一井     | @bot支援卡选择满破目标 | 支援卡抽满破的时候选择目标，池子刷新会清除         |
| @bot支援卡查询满破目标 | 查询自己抽满破的选择目标 | @bot支援卡清除满破目标 | 清除抽满破目标选择                     |

|                       注意事项                        |
|:-------------------------------------------------:|
| 切换卡池后仅一天可用，因为自动更新会覆盖为该服最新的卡池信息，命令后什么也不加会提示卡池ID的由来 |
|     切换服务器后会自动使用改服务器的最新卡池，命令后什么也不加会提示支持的服务器列表      |
|         开服无UP的卡池ID为00000000，未开服的服务器默认为该卡池         |

+ 马娘黄历

| 功能命令 |    介绍    | 
|:----:|:--------:|  
| 马娘签到 | 看看今日的黄历？ |   

+ 马娘耐力计算器

|                                               功能命令                                               |    介绍    |
|:------------------------------------------------------------------------------------------------:|:--------:|
|                                              马娘耐力帮助                                              | 看看详细帮助内容 | 
| 举个例子:<br>算耐力<br>属性:1200 600 1200 600 700<br>适应性:逃马-A 芝-A 1600-A<br>干劲:绝好调 状况:良<br>固回:0 普回:0 金回:1 | 计算最低耐力需求 |   

|                  注意事项                   |
|:---------------------------------------:|
| 中英文冒号均可  适性大小写均可  空格别漏，记得换行  没反应就是你指令错了 |

+ 马娘表情包

|    功能命令    |            介绍             |
|:----------:|:-------------------------:|  
|  马娘表情包帮助   |         看看详细帮助内容          |   
|   马娘表情包    |       随机一张马娘游戏内的表情包       |   
|   xxx表情包   | xxx为角色名字，没有该角色的表情包就不会有反应  |   
|   x号表情包    | x为数字，是表情包的编号，编号不是整数就不会有反应 |  
| 查表情包含义 xxx | xxx为角色名字，没有该角色的表情包就不会有反应  |
| 查表情包含义 x号  | x为数字，是表情包的编号，编号不是整数就不会有反应 |

+ 马娘漫画

|   功能命令   |             介绍             |
|:--------:|:--------------------------:|
|  马娘漫画帮助  |          看看详细帮助内容          | 
|   马娘漫画   |       随机一张马娘游戏内的一格漫画       |   
| 马娘漫画 xxx | xxx为角色名字，没有该角色的一格漫画就不会有反应  |  
| 马娘漫画 x号  | x为数字，是一格漫画的编号，编号不是整数就不会有反应 |
 
+ 马娘限时任务

|   功能命令   |         介绍         | 
|:--------:|:------------------:|
| 马娘限时任务帮助 |      看看详细帮助内容      |   
|  限时任务列表  |  查看所有的限定任务标题对应编号   |  
|  限时任务x   | x为列表中的编号，查看限时任务的内容 |  
| 手动更新限时任务 |    强制刷新列表，限维护组     |   

+ 马娘技能查询

|               功能命令               |                                                                                    介绍                                                                                     | 
|:--------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|              马娘技能帮助              |                                                                                 看看详细帮助内容                                                                                  |   
|             查技能 xxx              |                                                        xxx为中/日文技能名<br>注意继承后的固有名为 "继承技/(固有名)"<br>例如"继承技/113転び114起き"                                                        |    
|        查技能 (条件1) (条件2)...        |                                                           查技能后面可以加任意1个或多个条件，用空格隔开<br>例如"查技能 通用 妨害（速度）"，条件可选项如下                                                            | 
| TIP:不需要的可不选，另外由于存在复合技能，因此技能类型可多选 |                                                                          (输入时不用加单引号<kbd>'</kbd>)                                                                          |
|              稀有度可选               |                                                              '普通', '传说', '独特', '普通·继承', '独特·继承', '剧情', '活动'                                                               |   
|              条件限制可选              |                                                       '通用', '短距离', '英里', '中距离', '长距离', '泥地', '逃马', '先行', '差行', '追马'                                                       | 
|              技能颜色可选              |                                                                       '绿色', '紫色', '黄色', '蓝色', '红色'                                                                        |  
|             技能类型可多选              | '被动（速度）', '被动（耐力）', '被动（力量）', '被动（毅力）', '被动（智力）',<br>'耐力恢复', '速度', '加速度', '出闸', '视野', '切换跑道',<br>'妨害（速度）', '妨害（加速度）', '妨害（心态）', '妨害（智力）', '妨害（耐力恢复）', '妨害（视野）',<br>'(未知)' |    

+ 马娘速查

| 功能命令 |       介绍        | 
|:----:|:---------------:|
| 马娘速查 | 查询马娘官网、种马库等相关网站 |

+ 育成目标帮助

|   功能命令    |           介绍            | 
|:---------:|:-----------------------:|
|   马娘速查    |     查询马娘官网、种马库等相关网站     |
|  查目标 xxx  | xxx是马娘名，查该马娘在URA剧本的育成目标 |
| 查目标 xxx-f |     末尾加上-f为强制重新生成图片     |

+ 其他

|  功能命令  |    介绍    |
|:------:|:--------:| 
| 马娘插件-v | 查看当前插件版本 |

| 现插件已自带跟踪新版更新，只要确保bot能访问Github即可，如不能访问请配置代理 |
|:------------------------------------------:|

*by--int-PP、AZMIAO*
