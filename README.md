# Abstract_Words

#### 介绍
一个根据文字自动生成抽象话的脚本

#### 软件架构

1. ab.py是程序最终生成的脚本
2. genemoji.py用来手动生成表情包数据
3. genab.py用来根据数据生成ab.py
4. emoji存放表情数据
5. Asa_PinYin存放拼音数据
6. EmojiUtf8存放utf8字符与表情对应关系

#### 安装教程

```
python setup.py sdist
python setup.py install
```

#### 使用说明

```
import ab
ab.str2abs('那你是真滴牛皮')
```

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request
