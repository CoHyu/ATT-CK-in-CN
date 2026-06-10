# ATT&CK in CN

MITRE ATT&CK 知识库的完整中文汉化版，支持本地离线浏览。

## 内容

- 所有 14 个战术（Tactics）
- 所有 846 个技术/子技术（Techniques/Sub-techniques）
- 所有 189 个威胁组织（Groups）
- 所有 728 个恶意软件（Malware）
- 所有 95 个工具（Tools）
- 所有 44 个缓解措施（Mitigations）

全部内容均已翻译为中文，同时保留英文原文可展开查看。

## 使用

直接打开 `index.html` 即可在浏览器中使用，无需服务器或构建步骤。

也可通过 GitHub Pages 访问：`https://cohyu.github.io/ATT-CK-in-CN/`

## 重建

如需从 MITRE STIX 数据重建：

1. 下载 [enterprise-attack.json](https://github.com/mitre-attack/attack-stix-data) 放入项目目录
2. 运行 `python3 build.py`
3. `data.js` 将被重新生成

## 数据来源

- [MITRE ATT&CK STIX Data](https://github.com/mitre-attack/attack-stix-data)
