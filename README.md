# SEO Checker - Claude Skill

> 🔍 一键检测网站 SEO 健康度 + 关键词排名的 Claude 技能

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blue.svg)](https://claude.ai)

一个用于 Claude 的专业 SEO 健康度检测工具，支持全面的网站分析、关键词排名检测和智能搜索引擎适配。

## ✨ 主要功能

- ✅ **五大维度评估** - 可爬取性、性能、内容优化、内容质量、权威性
- ✅ **智能区域识别** - 自动识别中国站/国际站，使用对应搜索引擎
- ✅ **关键词排名分析** - 提取目标关键词并检测搜索排名
- ✅ **专业报告生成** - 包含评分、问题列表和优化建议
- ✅ **免费使用** - 完全免费，无需付费 SEO 工具

## 🚀 快速开始

### 1. 下载 Skill

点击下载 [seo-checker.skill](./seo-checker.skill) 文件

### 2. 导入到 Claude

1. 打开 [Claude.ai](https://claude.ai) 或 Claude App
2. 点击设置 ⚙️ → Skills → Import Skill
3. 选择下载的 `seo-checker.skill` 文件
4. 等待导入完成 ✅

### 3. 开始使用

在 Claude 中输入：

```
检测 https://example.com 的 SEO
```

30 秒后，生成专业 SEO 报告！

## 📊 检测内容

### 五大维度

| 维度 | 权重 | 检测项 |
|------|------|--------|
| 🔍 可爬取性 | 20% | robots.txt、meta robots、canonical、sitemap |
| ⚡ 页面性能 | 20% | HTML大小、资源数量、压缩状态 |
| 📝 内容优化 | 25% | title、description、h1、关键词密度、图片alt |
| 📊 内容质量 | 20% | 字数、结构化程度、可读性 |
| 🔗 权威性 | 15% | 外链数量、社交标签、结构化数据 |

### 搜索引擎适配

- 🇨🇳 **中国站**（.cn 域名或中文网站）
  - 使用：百度 + Bing 国内版
  
- 🌍 **国际站**（.com/.org 等）
  - 使用：Google

### 关键词排名

- 自动提取 3-5 个目标关键词
- 检测在搜索引擎中的排名位置
- 提供排名优化建议

## 📖 使用示例

### 示例 1：基础检测

```
检测 https://www.taobao.com 的 SEO
```

**输出**：
- 总体评分（0-100）
- 五大维度详细分析
- 百度收录状态
- 具体问题和改进建议

### 示例 2：批量分析

```
帮我检测这几个页面的 SEO：
1. https://page1.com
2. https://page2.com
3. https://page3.com
```

### 示例 3：竞品对比

```
对比分析我的网站和竞品：
我的：https://mysite.com
竞品：https://competitor.com
```

## 📁 项目结构

```
seo-checker/
├── SKILL.md                    # 技能主文件
├── scripts/
│   └── seo_analyzer.py        # SEO 分析脚本
├── references/
│   ├── report_template.md     # 报告模板
│   └── usage_example.md       # 使用示例
├── seo-checker.skill          # 打包文件
└── README.md                   # 项目说明
```

## 🎯 适用场景

### 1. 独立站卖家
- 新品上线前检测产品页
- 定期监控 SEO 健康度
- 优化搜索排名

### 2. 内容创作者
- 博客文章 SEO 检测
- 关键词排名追踪
- 内容质量优化

### 3. 营销人员
- 竞品 SEO 分析
- 市场机会发现
- 优化策略制定

### 4. 网站管理员
- 全站健康检查
- 技术问题排查
- 持续优化跟踪

## 💡 核心优势

### vs 付费 SEO 工具

| 功能 | SEO Checker | Ahrefs/SEMrush |
|------|-------------|----------------|
| 页面技术分析 | ✅ 免费 | ✅ $99+/月 |
| 关键词排名 | ✅ 基础版 | ✅ 完整版 |
| 外链分析 | ⚠️ 简单版 | ✅ 专业版 |
| 竞品分析 | ✅ 手动 | ✅ 自动 |
| 历史数据 | ❌ | ✅ |

**结论**：日常检测和基础分析完全够用，省下数千元工具费！

## 📝 更新日志

### v2.0 (2025-02-01) - 当前版本

- ✅ 修复 meta 描述检测 bug（支持大小写不敏感）
- ✅ 新增网站区域自动识别（中国站/国际站）
- ✅ 新增关键词排名检测功能
- ✅ 新增自然搜索表现分析
- ✅ 优化工作流程，步骤更清晰
- ✅ 新增完整使用示例文档

### v1.0 (初始版本)

- 基础 SEO 技术指标检测
- 五大维度评分系统
- 改进建议生成

## ❓ 常见问题

### Q: 需要 Claude Pro 吗？

不需要！免费版就能用，Pro 版会更快一些。

### Q: 检测准确吗？

- 技术指标（title、meta 等）：100% 准确
- 收录数量：估算值，仅供参考
- 关键词排名：实时数据，可能波动

### Q: 可以检测哪些网站？

任何公开网站都可以！包括独立站、电商平台、博客等。

### Q: 检测需要多长时间？

通常 30-60 秒，取决于页面大小和网络速度。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 如何贡献

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 💬 反馈与支持

如果你：
- 发现 Bug 🐛
- 有改进建议 💡
- 需要帮助 🙋‍♀️

欢迎：
- 提交 [Issue](../../issues)
- 发起 [Discussion](../../discussions)

## 🌟 致谢

感谢所有使用和支持这个项目的朋友！

如果觉得有用，欢迎：
- ⭐ Star 本仓库
- 🔄 分享给朋友
- 💬 留下你的使用反馈

---

**Made with ❤️ by [Your Name]**

*最后更新：2025-02-01*
