#!/usr/bin/env python3
"""
SEO Analyzer - 网站 SEO 健康度检测脚本
分析 HTML 页面并输出 JSON 格式的 SEO 检测结果
"""

import sys
import json
import re
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin
from collections import Counter


def detect_site_region(url: str, html_content: str = "") -> str:
    """
    检测网站是中国站还是国际站
    返回: 'china' 或 'international'
    """
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    # 检测中国域名
    china_tlds = ['.cn', '.com.cn', '.net.cn', '.org.cn', '.gov.cn']
    for tld in china_tlds:
        if domain.endswith(tld):
            return 'china'
    
    # 检测常见中国网站域名关键词
    china_keywords = ['baidu', 'taobao', 'tmall', 'jd', 'qq', 'weibo', 
                      'alibaba', 'aliyun', '163', '126', 'sina', 'sohu']
    for keyword in china_keywords:
        if keyword in domain:
            return 'china'
    
    # 检测 HTML 中的语言标记
    if html_content:
        # 检查 lang 属性
        if 'lang="zh' in html_content.lower() or 'lang=\'zh' in html_content.lower():
            # 如果有 zh-CN 或 zh-Hans，很可能是中国站
            if 'zh-cn' in html_content.lower() or 'zh-hans' in html_content.lower():
                return 'china'
    
    return 'international'


class SEOHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.meta_keywords = ""
        self.meta_robots = ""
        self.canonical = ""
        self.h1_tags = []
        self.h2_tags = []
        self.h3_tags = []
        self.images = []
        self.links = {"internal": [], "external": [], "nofollow": []}
        self.scripts = []
        self.stylesheets = []
        self.text_content = []
        self.og_tags = {}
        self.twitter_tags = {}
        self.structured_data = []
        self.lang = ""
        self.viewport = ""
        
        self._current_tag = None
        self._current_attrs = {}
        self._in_title = False
        self._in_h1 = False
        self._in_h2 = False
        self._in_h3 = False
        self._in_script = False
        self._in_style = False
        self._in_body = False
        self._script_content = ""
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._current_tag = tag
        self._current_attrs = attrs_dict
        
        if tag == "html":
            self.lang = attrs_dict.get("lang", "")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            # 获取 name 和 property 属性，忽略大小写
            name = attrs_dict.get("name", "")
            prop = attrs_dict.get("property", "")
            content = attrs_dict.get("content", "")
            
            # 标准化处理，避免大小写问题
            name_lower = name.lower() if name else ""
            prop_lower = prop.lower() if prop else ""
            
            # 检测 description - 支持多种写法
            if name_lower == "description" or prop_lower == "description":
                if content and not self.meta_description:  # 只取第一个
                    self.meta_description = content
            # 检测 keywords
            elif name_lower == "keywords":
                if content and not self.meta_keywords:
                    self.meta_keywords = content
            # 检测 robots
            elif name_lower == "robots":
                if content and not self.meta_robots:
                    self.meta_robots = content
            # 检测 viewport
            elif name_lower == "viewport":
                if content and not self.viewport:
                    self.viewport = content
            # 检测 Open Graph 标签
            elif prop_lower.startswith("og:"):
                self.og_tags[prop_lower] = content
            # 检测 Twitter 标签
            elif name_lower.startswith("twitter:"):
                self.twitter_tags[name_lower] = content
        elif tag == "link":
            rel = attrs_dict.get("rel", "")
            href = attrs_dict.get("href", "")
            if rel == "canonical":
                self.canonical = href
            elif rel == "stylesheet":
                self.stylesheets.append(href)
        elif tag == "h1":
            self._in_h1 = True
        elif tag == "h2":
            self._in_h2 = True
        elif tag == "h3":
            self._in_h3 = True
        elif tag == "img":
            self.images.append({
                "src": attrs_dict.get("src", ""),
                "alt": attrs_dict.get("alt", ""),
                "loading": attrs_dict.get("loading", "")
            })
        elif tag == "a":
            href = attrs_dict.get("href", "")
            rel = attrs_dict.get("rel", "")
            if href:
                link_info = {"href": href, "rel": rel}
                if "nofollow" in rel:
                    self.links["nofollow"].append(link_info)
                elif href.startswith(("http://", "https://", "//")):
                    self.links["external"].append(link_info)
                else:
                    self.links["internal"].append(link_info)
        elif tag == "script":
            self._in_script = True
            self._script_content = ""
            src = attrs_dict.get("src", "")
            if src:
                self.scripts.append({"type": "external", "src": src})
            script_type = attrs_dict.get("type", "")
            if script_type == "application/ld+json":
                self._in_script = True
        elif tag == "style":
            self._in_style = True
        elif tag == "body":
            self._in_body = True
            
    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "h2":
            self._in_h2 = False
        elif tag == "h3":
            self._in_h3 = False
        elif tag == "script":
            if self._script_content.strip():
                if "application/ld+json" in str(self._current_attrs.get("type", "")):
                    try:
                        self.structured_data.append(json.loads(self._script_content))
                    except:
                        pass
            self._in_script = False
            self._script_content = ""
        elif tag == "style":
            self._in_style = False
        elif tag == "body":
            self._in_body = False
            
    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self._in_h1:
            self.h1_tags.append(data.strip())
        elif self._in_h2:
            self.h2_tags.append(data.strip())
        elif self._in_h3:
            self.h3_tags.append(data.strip())
        elif self._in_script:
            self._script_content += data
        elif self._in_body and not self._in_style:
            text = data.strip()
            if text:
                self.text_content.append(text)


def analyze_seo(url: str, html_content: str) -> dict:
    """分析页面 SEO 并返回结果"""
    
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # 检测网站区域
    site_region = detect_site_region(url, html_content)
    
    # 解析 HTML
    parser = SEOHTMLParser()
    try:
        parser.feed(html_content)
    except Exception as e:
        pass
    
    # 计算文本统计
    full_text = " ".join(parser.text_content)
    word_count = len(full_text.split())
    char_count = len(full_text)
    
    # 分析结果
    results = {
        "url": url,
        "domain": domain,
        "site_region": site_region,  # 新增：网站区域
        "html_size_kb": round(len(html_content) / 1024, 2),
        
        # 可爬取性检测
        "crawlability": {
            "has_meta_robots": bool(parser.meta_robots),
            "meta_robots": parser.meta_robots,
            "is_noindex": "noindex" in parser.meta_robots.lower() if parser.meta_robots else False,
            "is_nofollow": "nofollow" in parser.meta_robots.lower() if parser.meta_robots else False,
            "has_canonical": bool(parser.canonical),
            "canonical_url": parser.canonical,
            "has_lang": bool(parser.lang),
            "lang": parser.lang,
        },
        
        # 页面性能指标
        "performance": {
            "html_size_kb": round(len(html_content) / 1024, 2),
            "external_scripts": len([s for s in parser.scripts if s.get("type") == "external"]),
            "stylesheets": len(parser.stylesheets),
            "total_images": len(parser.images),
            "images_with_lazy_loading": len([i for i in parser.images if i.get("loading") == "lazy"]),
            "has_viewport": bool(parser.viewport),
        },
        
        # 内容优化检测
        "content_optimization": {
            "title": parser.title.strip(),
            "title_length": len(parser.title.strip()),
            "title_ok": 30 <= len(parser.title.strip()) <= 60,
            "meta_description": parser.meta_description,
            "meta_description_length": len(parser.meta_description),
            "meta_description_ok": 120 <= len(parser.meta_description) <= 160,
            "has_meta_keywords": bool(parser.meta_keywords),
            "h1_count": len(parser.h1_tags),
            "h1_tags": parser.h1_tags[:5],
            "h2_count": len(parser.h2_tags),
            "h3_count": len(parser.h3_tags),
            "images_without_alt": len([i for i in parser.images if not i.get("alt")]),
            "images_with_alt": len([i for i in parser.images if i.get("alt")]),
        },
        
        # 内容质量指标
        "content_quality": {
            "word_count": word_count,
            "char_count": char_count,
            "word_count_ok": word_count >= 300,
            "has_headings_structure": len(parser.h1_tags) > 0 and len(parser.h2_tags) > 0,
            "heading_hierarchy_ok": len(parser.h1_tags) == 1,
        },
        
        # 权威性与社交
        "authority": {
            "internal_links": len(parser.links["internal"]),
            "external_links": len(parser.links["external"]),
            "nofollow_links": len(parser.links["nofollow"]),
            "has_og_tags": bool(parser.og_tags),
            "og_tags": parser.og_tags,
            "has_twitter_tags": bool(parser.twitter_tags),
            "twitter_tags": parser.twitter_tags,
            "has_structured_data": bool(parser.structured_data),
            "structured_data_types": [sd.get("@type", "unknown") for sd in parser.structured_data if isinstance(sd, dict)],
        },
        
        # 评分
        "scores": calculate_scores(parser, html_content, word_count),
    }
    
    # 生成问题列表和建议
    results["issues"] = generate_issues(results)
    results["recommendations"] = generate_recommendations(results)
    
    return results


def calculate_scores(parser, html_content, word_count) -> dict:
    """计算各维度评分"""
    
    # 可爬取性评分 (20%)
    crawl_score = 100
    if "noindex" in parser.meta_robots.lower() if parser.meta_robots else False:
        crawl_score -= 50
    if not parser.canonical:
        crawl_score -= 20
    if not parser.lang:
        crawl_score -= 10
    crawl_score = max(0, crawl_score)
    
    # 性能评分 (20%)
    perf_score = 100
    html_size = len(html_content) / 1024
    if html_size > 200:
        perf_score -= 30
    elif html_size > 100:
        perf_score -= 15
    if len(parser.scripts) > 10:
        perf_score -= 20
    if not parser.viewport:
        perf_score -= 20
    lazy_ratio = len([i for i in parser.images if i.get("loading") == "lazy"]) / max(len(parser.images), 1)
    if lazy_ratio < 0.5 and len(parser.images) > 5:
        perf_score -= 15
    perf_score = max(0, perf_score)
    
    # 内容优化评分 (25%)
    opt_score = 100
    title_len = len(parser.title.strip())
    if title_len < 30 or title_len > 60:
        opt_score -= 15
    if not parser.title:
        opt_score -= 25
    desc_len = len(parser.meta_description)
    if desc_len < 120 or desc_len > 160:
        opt_score -= 15
    if not parser.meta_description:
        opt_score -= 25
    if len(parser.h1_tags) != 1:
        opt_score -= 20
    images_no_alt = len([i for i in parser.images if not i.get("alt")])
    if images_no_alt > 0:
        opt_score -= min(20, images_no_alt * 5)
    opt_score = max(0, opt_score)
    
    # 内容质量评分 (20%)
    quality_score = 100
    if word_count < 300:
        quality_score -= 30
    elif word_count < 500:
        quality_score -= 15
    if len(parser.h1_tags) == 0 or len(parser.h2_tags) == 0:
        quality_score -= 20
    if len(parser.h1_tags) > 1:
        quality_score -= 15
    quality_score = max(0, quality_score)
    
    # 权威性评分 (15%)
    auth_score = 100
    if not parser.og_tags:
        auth_score -= 25
    if not parser.twitter_tags:
        auth_score -= 15
    if not parser.structured_data:
        auth_score -= 30
    if len(parser.links["external"]) == 0:
        auth_score -= 10
    auth_score = max(0, auth_score)
    
    # 总分（加权平均）
    total_score = round(
        crawl_score * 0.20 +
        perf_score * 0.20 +
        opt_score * 0.25 +
        quality_score * 0.20 +
        auth_score * 0.15
    )
    
    return {
        "total": total_score,
        "crawlability": crawl_score,
        "performance": perf_score,
        "content_optimization": opt_score,
        "content_quality": quality_score,
        "authority": auth_score,
    }


def generate_issues(results: dict) -> list:
    """生成问题列表"""
    issues = []
    
    # 可爬取性问题
    if results["crawlability"]["is_noindex"]:
        issues.append({"severity": "critical", "category": "crawlability", "message": "页面设置了 noindex，无法被搜索引擎索引"})
    if not results["crawlability"]["has_canonical"]:
        issues.append({"severity": "warning", "category": "crawlability", "message": "缺少 canonical 标签，可能导致重复内容问题"})
    if not results["crawlability"]["has_lang"]:
        issues.append({"severity": "info", "category": "crawlability", "message": "缺少 lang 属性，影响国际化 SEO"})
    
    # 性能问题
    if results["performance"]["html_size_kb"] > 200:
        issues.append({"severity": "warning", "category": "performance", "message": f"HTML 文件过大 ({results['performance']['html_size_kb']}KB)，影响加载速度"})
    if not results["performance"]["has_viewport"]:
        issues.append({"severity": "critical", "category": "performance", "message": "缺少 viewport 设置，移动端体验差"})
    
    # 内容优化问题
    if not results["content_optimization"]["title"]:
        issues.append({"severity": "critical", "category": "optimization", "message": "缺少页面标题"})
    elif not results["content_optimization"]["title_ok"]:
        issues.append({"severity": "warning", "category": "optimization", "message": f"标题长度 ({results['content_optimization']['title_length']} 字符) 不在最佳范围 (30-60)"})
    if not results["content_optimization"]["meta_description"]:
        issues.append({"severity": "critical", "category": "optimization", "message": "缺少 meta description"})
    elif not results["content_optimization"]["meta_description_ok"]:
        issues.append({"severity": "warning", "category": "optimization", "message": f"描述长度 ({results['content_optimization']['meta_description_length']} 字符) 不在最佳范围 (120-160)"})
    if results["content_optimization"]["h1_count"] == 0:
        issues.append({"severity": "critical", "category": "optimization", "message": "缺少 H1 标签"})
    elif results["content_optimization"]["h1_count"] > 1:
        issues.append({"severity": "warning", "category": "optimization", "message": f"存在多个 H1 标签 ({results['content_optimization']['h1_count']} 个)，建议只使用 1 个"})
    if results["content_optimization"]["images_without_alt"] > 0:
        issues.append({"severity": "warning", "category": "optimization", "message": f"{results['content_optimization']['images_without_alt']} 张图片缺少 alt 属性"})
    
    # 内容质量问题
    if not results["content_quality"]["word_count_ok"]:
        issues.append({"severity": "warning", "category": "quality", "message": f"内容较少 ({results['content_quality']['word_count']} 词)，建议增加到 300+ 词"})
    
    # 权威性问题 - 详细拆分
    if not results["authority"]["has_og_tags"]:
        issues.append({"severity": "warning", "category": "authority", "message": "缺少 Open Graph 标签，影响社交分享效果和品牌曝光"})
    if not results["authority"]["has_twitter_tags"]:
        issues.append({"severity": "info", "category": "authority", "message": "缺少 Twitter Cards 标签，影响 Twitter 分享展示"})
    if not results["authority"]["has_structured_data"]:
        issues.append({"severity": "warning", "category": "authority", "message": "缺少结构化数据 (Schema.org)，影响富媒体搜索结果展示"})
    if results["authority"]["external_links"] == 0:
        issues.append({"severity": "info", "category": "authority", "message": "缺少外部链接引用，适当添加高质量外链可增强内容可信度"})
    
    return issues


def generate_recommendations(results: dict) -> list:
    """生成改进建议，按优先级排序，标注影响的维度"""
    recs = []
    
    # 根据问题生成建议，每个建议包含 affects 字段表明影响的维度
    for issue in results["issues"]:
        if issue["severity"] == "critical":
            priority = "high"
        elif issue["severity"] == "warning":
            priority = "medium"
        else:
            priority = "low"
            
        if "noindex" in issue["message"]:
            recs.append({
                "priority": "high", 
                "action": "移除 noindex 标签或确认是否故意阻止索引",
                "affects": ["crawlability"],
                "affects_display": "🔍 可爬取性"
            })
        elif "canonical" in issue["message"]:
            recs.append({
                "priority": "medium", 
                "action": "添加 <link rel=\"canonical\" href=\"...\"> 指定规范 URL",
                "affects": ["crawlability"],
                "affects_display": "🔍 可爬取性"
            })
        elif "lang" in issue["message"]:
            recs.append({
                "priority": "low",
                "action": "添加 <html lang=\"zh-CN\"> 语言属性",
                "affects": ["crawlability"],
                "affects_display": "🔍 可爬取性"
            })
        elif "viewport" in issue["message"]:
            recs.append({
                "priority": "high", 
                "action": "添加 <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
                "affects": ["performance"],
                "affects_display": "⚡ 页面性能"
            })
        elif "HTML" in issue["message"] and "过大" in issue["message"]:
            recs.append({
                "priority": "medium",
                "action": "压缩 HTML 文件，移除不必要的空白和注释",
                "affects": ["performance"],
                "affects_display": "⚡ 页面性能"
            })
        elif "懒加载" in issue["message"] or "lazy" in issue["message"].lower():
            recs.append({
                "priority": "medium",
                "action": "为图片添加 loading=\"lazy\" 属性实现懒加载",
                "affects": ["performance"],
                "affects_display": "⚡ 页面性能"
            })
        elif "标题" in issue["message"] and "缺少" in issue["message"]:
            recs.append({
                "priority": "high", 
                "action": "添加描述性的 <title> 标签，长度保持在 30-60 字符",
                "affects": ["content_optimization"],
                "affects_display": "📝 内容优化"
            })
        elif "标题长度" in issue["message"]:
            recs.append({
                "priority": "medium",
                "action": "调整标题长度到 30-60 字符的最佳范围",
                "affects": ["content_optimization"],
                "affects_display": "📝 内容优化"
            })
        elif "meta description" in issue["message"] and "缺少" in issue["message"]:
            recs.append({
                "priority": "high", 
                "action": "添加 <meta name=\"description\" content=\"...\">，长度保持在 120-160 字符",
                "affects": ["content_optimization"],
                "affects_display": "📝 内容优化"
            })
        elif "描述长度" in issue["message"]:
            recs.append({
                "priority": "medium",
                "action": "调整 meta description 长度到 120-160 字符的最佳范围",
                "affects": ["content_optimization"],
                "affects_display": "📝 内容优化"
            })
        elif "H1" in issue["message"] and "缺少" in issue["message"]:
            recs.append({
                "priority": "high", 
                "action": "添加一个清晰的 H1 标签描述页面主题",
                "affects": ["content_optimization", "content_quality"],
                "affects_display": "📝 内容优化 | 📊 内容质量"
            })
        elif "多个 H1" in issue["message"]:
            recs.append({
                "priority": "medium",
                "action": "保留一个主要的 H1 标签，将其他改为 H2 或更低级别",
                "affects": ["content_optimization", "content_quality"],
                "affects_display": "📝 内容优化 | 📊 内容质量"
            })
        elif "alt" in issue["message"]:
            recs.append({
                "priority": "medium", 
                "action": "为所有图片添加描述性的 alt 属性",
                "affects": ["content_optimization"],
                "affects_display": "📝 内容优化"
            })
        elif "内容较少" in issue["message"] or "词" in issue["message"]:
            recs.append({
                "priority": "medium",
                "action": "增加页面内容至 300 词以上，提供更丰富有价值的信息",
                "affects": ["content_quality"],
                "affects_display": "📊 内容质量"
            })
        elif "Open Graph" in issue["message"]:
            recs.append({
                "priority": "low", 
                "action": "添加 og:title, og:description, og:image 等社交分享标签",
                "affects": ["authority"],
                "affects_display": "🔗 权威性"
            })
        elif "Twitter" in issue["message"]:
            recs.append({
                "priority": "low",
                "action": "添加 twitter:card, twitter:title, twitter:description 等 Twitter 卡片标签",
                "affects": ["authority"],
                "affects_display": "🔗 权威性"
            })
        elif "结构化数据" in issue["message"]:
            recs.append({
                "priority": "low", 
                "action": "添加 JSON-LD 格式的结构化数据标记 (Schema.org)",
                "affects": ["authority"],
                "affects_display": "🔗 权威性"
            })
        elif "外链" in issue["message"]:
            recs.append({
                "priority": "low",
                "action": "适当添加高质量的外部链接引用，增强内容可信度",
                "affects": ["authority"],
                "affects_display": "🔗 权威性"
            })
    
    # 去重并按优先级排序
    seen = set()
    unique_recs = []
    for rec in recs:
        if rec["action"] not in seen:
            seen.add(rec["action"])
            unique_recs.append(rec)
    
    priority_order = {"high": 0, "medium": 1, "low": 2}
    unique_recs.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    return unique_recs


def main():
    if len(sys.argv) < 3:
        print("Usage: python seo_analyzer.py <URL> <HTML_FILE_PATH>")
        sys.exit(1)
    
    url = sys.argv[1]
    html_file = sys.argv[2]
    
    with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()
    
    results = analyze_seo(url, html_content)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
