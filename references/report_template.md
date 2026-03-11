# SEO 报告模板

使用此模板生成最终的 SEO 检测报告。

## 报告结构

```markdown
# SEO 健康度检测报告

**检测网址**: {url}  
**检测时间**: {timestamp}  

---

## 📊 总体评分：{total_score}/100

| 维度 | 评分 | 状态 |
|------|------|------|
| 🔍 可爬取性 | {crawl_score}/100 | {status_emoji} |
| ⚡ 页面性能 | {perf_score}/100 | {status_emoji} |
| 📝 内容优化 | {opt_score}/100 | {status_emoji} |
| 📊 内容质量 | {quality_score}/100 | {status_emoji} |
| 🔗 权威性 | {auth_score}/100 | {status_emoji} |

> 评分说明：🟢 80+ 优秀 | 🟡 60-79 良好 | 🔴 <60 需改进

---

## 🔍 详细检测结果

### 1. 可爬取性与索引

- **Meta Robots**: {meta_robots_status}
- **Canonical URL**: {canonical_status}
- **语言标记**: {lang_status}

### 2. 页面性能

- **HTML 大小**: {html_size} KB
- **外部脚本数**: {scripts_count}
- **图片数量**: {images_count}（懒加载: {lazy_count}）
- **Viewport 设置**: {viewport_status}

### 3. 内容优化

- **页面标题**: "{title}" ({title_length} 字符) {title_status}
- **Meta 描述**: "{description}" ({desc_length} 字符) {desc_status}
- **H1 标签**: {h1_count} 个 {h1_status}
- **图片 Alt**: {alt_status}

### 4. 内容质量

- **内容字数**: {word_count} 词 {word_status}
- **标题层级**: H1({h1_count}) → H2({h2_count}) → H3({h3_count})

### 5. 权威性与社交

- **Open Graph**: {og_status}
- **Twitter Cards**: {twitter_status}
- **结构化数据**: {schema_status}
- **外链数量**: {external_links}

---

## 🔎 搜索引擎表现

### 收录状态

- **检测引擎**: {search_engines}
- **索引页面数**: {indexed_pages}
- **收录状态**: {indexing_status}

### 关键词排名

| 关键词 | 排名位置 | 状态 |
|--------|----------|------|
{keyword_rankings}

**排名说明**: 前10名 🟢 优秀 | 11-30名 🟡 良好 | 30名后 🔴 需提升 | 未上榜 ❌

### 自然搜索可见度

{organic_visibility_summary}

---

## ⚠️ 发现的问题

### 🔴 严重问题
{critical_issues}

### 🟡 警告
{warnings}

### 🔵 建议
{info_issues}

---

## ✅ 改进建议（按优先级，标注影响维度）

### 高优先级
| 建议 | 影响维度 |
|------|----------|
{high_priority_actions}

### 中优先级
| 建议 | 影响维度 |
|------|----------|
{medium_priority_actions}

### 低优先级
| 建议 | 影响维度 |
|------|----------|
{low_priority_actions}

---

## 📈 重点提升维度

根据当前评分，以下维度需要重点关注：

{weak_dimensions_summary}

---

## 📌 下一步行动

1. 首先解决所有严重问题
2. 优化页面加载性能
3. 完善内容结构和标签
4. 添加结构化数据提升富媒体展示

---

*报告由 SEO Checker 自动生成*
```

## 状态 Emoji 规则

- 评分 >= 80: 🟢
- 评分 60-79: 🟡  
- 评分 < 60: 🔴
- 存在/通过: ✅
- 缺失/未通过: ❌
- 部分通过: ⚠️

## 改进建议格式

每条建议需包含：
- `action`: 具体操作建议
- `affects_display`: 影响的维度显示文本（如 "🔗 权威性"）

表格格式示例：
```
| 添加 og:title, og:description 等社交分享标签 | 🔗 权威性 |
| 添加 JSON-LD 格式的结构化数据标记 | 🔗 权威性 |
```

## 重点提升维度总结规则

当某维度评分 < 60 时，输出：
```
### 🔴 {维度名} ({分数}/100) - 需重点改进

可通过以下操作提升此维度分数：
- {对应建议1}
- {对应建议2}
...
```
