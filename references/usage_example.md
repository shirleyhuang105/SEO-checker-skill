# SEO Checker 使用示例

## 完整工作流程示例

### 示例 1: 检测中国站网站

**用户请求**: "帮我检测一下 https://www.example.cn 的 SEO"

**执行步骤**:

1. 获取页面内容
```python
# 使用 web_fetch 获取页面
web_fetch("https://www.example.cn")
# 保存 HTML 到临时文件
```

2. 运行分析脚本
```bash
python3 /mnt/skills/user/seo-checker/scripts/seo_analyzer.py "https://www.example.cn" /tmp/page.html
```

3. 检查脚本输出的 `site_region` 字段
```json
{
  "site_region": "china"  // 确认是中国站
}
```

4. 使用百度和 Bing 进行搜索
```
# 百度收录检测
site:example.cn

# 关键词排名检测（提取自 title/h1）
"示例关键词"
"示例关键词" example.cn
```

5. 生成报告，包含:
   - 技术分析结果
   - 百度/Bing 收录状态
   - 关键词在百度的排名
   - 改进建议

### 示例 2: 检测国际站网站

**用户请求**: "分析 https://example.com 的搜索排名"

**执行步骤**:

1-2. 同上获取和分析

3. 检查 site_region
```json
{
  "site_region": "international"  // 确认是国际站
}
```

4. 使用 Google 进行搜索
```
# Google 收录检测
site:example.com

# 关键词排名检测
"target keyword"
"target keyword" example.com
```

5. 生成报告，使用 Google 数据

## 关键词提取示例

**页面信息**:
- Title: "Python Web 开发教程 - 从零开始学 Flask | DevTutorial"
- H1: "Python Flask Web 开发完全指南"
- Meta Description: "学习 Python Flask 框架，掌握现代 Web 开发技术"

**提取的关键词**:
1. "Python Flask 开发" (title + h1 核心词)
2. "Flask Web 开发" (title + description 共现)
3. "Python Web 教程" (title 核心)

**搜索策略**:
```
"Python Flask 开发"           # 检测通用排名
"Flask Web 开发" site:devtutorial.com  # 精确定位
"Python Web 教程"             # 检测长尾排名
```

## 排名判断规则

从搜索结果中找到目标网站的位置：

- **第 1-3 位**: 🟢 优秀排名，高可见度
- **第 4-10 位**: 🟢 首页排名，良好可见度
- **第 11-20 位**: 🟡 第二页，可见度中等
- **第 21-30 位**: 🟡 第三页，可见度较低
- **30 位之后**: 🔴 需要优化
- **未找到**: ❌ 未上榜

## 报告生成要点

1. **搜索引擎表现部分**必须包含:
   - 使用的搜索引擎（根据 site_region）
   - 索引页面数（从 site: 搜索结果估算）
   - 关键词排名表格（至少 3 个关键词）
   - 整体可见度评估

2. **关键词排名表格格式**:
```markdown
| 关键词 | 排名位置 | 状态 |
|--------|----------|------|
| Python Flask 开发 | 第 5 名 | 🟢 |
| Flask Web 开发 | 未上榜 | ❌ |
| Python Web 教程 | 第 18 名 | 🟡 |
```

3. **自然搜索可见度总结**:
```markdown
**整体评估**: 目标关键词中有 1 个进入首页前 10，展现效果良好。
但核心关键词"Flask Web 开发"未上榜，建议加强该关键词的优化。

**建议**:
- 在页面中增加"Flask Web 开发"关键词密度
- 创建更多与"Flask Web 开发"相关的内部链接
- 获取包含该关键词的外部链接
```

## 常见问题处理

### Q1: 如果 meta description 检测不到？

**可能原因**:
- HTML 格式问题（已修复：现在支持大小写不敏感）
- 使用了非标准属性名
- 内容在 JavaScript 中动态生成

**解决方案**:
- 检查原始 HTML 是否真的包含 meta description
- 如果是 SPA 应用，可能需要渲染后的 HTML

### Q2: site_region 判断错误？

**检查**:
- 查看 HTML 中的 lang 属性
- 检查域名后缀
- 必要时手动指定搜索引擎

### Q3: 搜索排名找不到网站？

**原因**:
- 网站可能真的没有被索引
- 关键词选择不当
- 网站是新站，尚未建立排名

**建议**:
- 先用 site: 确认是否被收录
- 尝试用品牌词 + 关键词搜索
- 检查是否有 noindex 标签
