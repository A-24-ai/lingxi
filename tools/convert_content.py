# -*- coding: utf-8 -*-
"""
将《胡珂的想法》知识库内容批量转换为站点文章。
只做机械清理（剥离内部元信息头尾、保留原文正文），不改写内容。
"""
import pathlib, re

SRC = pathlib.Path("E:/胡珂的想法")
OUT = pathlib.Path("src/content/posts")
OUT.mkdir(parents=True, exist_ok=True)

# 每篇配置：
#  src, slug, title, cat, date, desc, tags
#  from_marker: 正文起点（保留该标记所在行起的内容）；None=从标题后正文开始
#  to_markers:  正文终点（遇到任一标记行即截断，去掉其后含该行）
posts = [
    dict(src="02-深度思考/个人价值成长论-成稿.md",
         slug="personal-value-growth-theory",
         title="个人价值成长论：从盯钱到提供价值，再到认知觉醒",
         cat="赚钱与生意", date="2026-08-18",
         desc="金钱的本质是提供价值的交换。如何借平台放大价值、分清运气与本事，把认知真正落地成赚钱的能力。",
         tags=["价值","认知","赚钱"],
         from_marker="## 缘起",
         to_markers=["*本文由"]),
    dict(src="02-深度思考/AI时代的情绪价值-成稿.md",
         slug="emotional-value-in-ai-era",
         title="AI时代的情绪价值：从功能稀缺到情绪稀缺",
         cat="情绪价值", date="2026-08-18",
         desc="当功能不再稀缺，情绪就成了稀缺品。从拉布布到商业造节，看清情绪价值如何成为AI时代的新生态位。",
         tags=["情绪价值","AI","商业"],
         from_marker="## 缘起",
         to_markers=["*本文由"]),
    dict(src="03-主题专题/行业分析/做大底层逻辑-跨行业总结.md",
         slug="how-to-scale-a-business",
         title="做大的底层逻辑：跨行业通用规律",
         cat="赚钱与生意", date="2026-08-18",
         desc="任何行业能不能做大，取决于能否把靠个人、靠手艺升级为靠系统、靠复制。附软件/AI/餐饮/美业/中医/便利店六行业验证。",
         tags=["生意","复制","系统"],
         from_marker="## 一、五个行业的验证",
         to_markers=["## 附：与个人认知的关联"]),
    dict(src="03-主题专题/行业分析/2026-08-20 顺着人性做生意.md",
         slug="business-along-human-nature",
         title="顺着人性做生意",
         cat="赚钱与生意", date="2026-08-20",
         desc="需求端顺人性（有人想要）+ 供给端可复制（能做大）= 大生意。看透人性的六大驱动力，看懂一类生意。",
         tags=["人性","需求","生意"],
         from_marker="## 一、人性是什么",
         to_markers=["## 与本专题","## 相关"]),
    dict(src="03-主题专题/个人价值与成长/2026-08-18 赚钱的本质-把自己搞明白重复做.md",
         slug="essence-of-making-money",
         title="赚钱的本质：把自己搞明白，然后重复的事重复做",
         cat="赚钱与生意", date="2026-08-18",
         desc="卖课式的情绪价值是画饼，不可持续。真正的赚钱，是把自己搞明白、知道自己价值在哪，然后把重复的事重复做好。",
         tags=["赚钱","价值","落地"],
         from_marker="## 想法正文",
         to_markers=["## 与本专题","## 后续动作"]),
    dict(src="03-主题专题/个人价值与成长/2026-08-18 从盯钱到提供价值.md",
         slug="from-chasing-money-to-providing-value",
         title="从盯着钱到为别人提供价值：价值才是金钱的本质",
         cat="个人成长", date="2026-08-18",
         desc="金钱=为他人提供价值的交换结果。别问怎么赚钱，要问我能为谁、解决什么问题、提供什么价值。",
         tags=["价值","金钱","思维"],
         from_marker="## 想法正文",
         to_markers=["## 延伸思考"]),
    dict(src="03-主题专题/个人价值与成长/2026-08-26 别一味深耕产品-先去了解用户.md",
         slug="understand-users-before-product",
         title="别一味深耕产品：先去了解用户",
         cat="个人成长", date="2026-08-26",
         desc="价值的定义权在用户手里，不在你手里。产品是答案，用户是题目，先读懂题目再写答案。",
         tags=["用户","产品","价值"],
         from_marker=None,
         to_markers=["## 与本专题"]),
    dict(src="03-主题专题/个人价值与成长/2026-08-26 想不通就去睡一觉-适当的休息也是一种工作.md",
         slug="rest-is-also-work",
         title="想不通就去睡一觉：适当的休息，也是一种工作",
         cat="个人成长", date="2026-08-26",
         desc="大脑在你休息的时候还在后台运行。想不通就硬想是最亏的做法，停下来让大脑换挡，问题往往就松动了。",
         tags=["休息","效率","成长"],
         from_marker=None,
         to_markers=["## 与本专题"]),
    dict(src="03-主题专题/个人价值与成长/2026-08-26 人不是AI-摆烂也是一种生活态度.md",
         slug="humans-are-not-ai",
         title="人不是AI：摆烂也是一种生活态度",
         cat="个人成长", date="2026-08-26",
         desc="AI靠电源一直执行，人靠本能会停下。别学AI一直转，人要给自己留个关机键，会摆烂的人才能走得更远。",
         tags=["生活态度","休息","节奏"],
         from_marker=None,
         to_markers=["## 与本专题"]),
    dict(src="03-主题专题/情绪价值/2026-08-19 商业造节案例.md",
         slug="commercial-festival-marketing",
         title="商业造节案例：给日子一个故事，然后贩卖它",
         cat="情绪价值", date="2026-08-19",
         desc="商业需要某个意义，就造一个节、讲一个故事、给日子一个说法。拆解双11、520、女神节的造节逻辑。",
         tags=["造节","情绪价值","消费"],
         from_marker="## 案例汇总",
         to_markers=["## 与专题主线的关联","## 与本专题"]),
    dict(src="03-主题专题/行业分析/行业分析方法框架.md",
         slug="industry-analysis-framework",
         title="行业分析方法框架：五步看懂一个行业",
         cat="行业分析", date="2026-08-18",
         desc="一套既含经典方法论、又贴合实战派视角的行业分析框架：不只看表面格局，更看底层决策逻辑。",
         tags=["行业分析","方法","框架"],
         from_marker="## 分析五步法",
         to_markers=["## 与本专题","## 相关"]),
]

# 通用元信息行（行首），删除
META_PATTERNS = [
    re.compile(r'^-\s*\*\*[^*]+\*\*.*$'),   # "- **日期**：xxx"
    re.compile(r'^-\s*[^\*#].*$'),           # "- 适用：xxx" 等
]

def clean_body(text, fm, tms):
    lines = text.splitlines()
    # 1) 定位正文起点
    start = 0
    if fm:
        for i, ln in enumerate(lines):
            if fm in ln:
                start = i
                break
    else:
        # 从标题行之后开始，跳过元信息行直到正文
        start = 0
        for i, ln in enumerate(lines):
            if ln.startswith('# '):
                start = i + 1
                continue
            # 跳过空行和元信息行
            if not ln.strip() or META_PATTERNS[0].match(ln) or META_PATTERNS[1].match(ln):
                start = i + 1
            else:
                break
        # 若一直滑到末尾，回退
    body = lines[start:]
    # 2) 定位正文终点
    if tms:
        for i, ln in enumerate(body):
            if any(tm in ln for tm in tms):
                body = body[:i]
                break
    return body

def remove_meta_lines(lines):
    # 只删除 "- **键**：值" 形式的元信息行，保留正文列表项
    out = []
    for ln in lines:
        if not ln.strip():
            continue
        if META_PATTERNS[0].match(ln):
            continue
        out.append(ln)
    return out

def build_frontmatter(p):
    return (f'---\ntitle: "{p["title"]}"\ndescription: "{p["desc"]}"\n'
            f'category: "{p["cat"]}"\ndate: {p["date"]}\n'
            f'tags: {str(p["tags"])}\n---\n')

def run():
    for p in posts:
        sp = SRC / p["src"]
        text = sp.read_text(encoding="utf-8")
        body_lines = clean_body(text, p.get("from_marker"), p.get("to_markers", []))
        body_lines = remove_meta_lines(body_lines)
        # 去掉正文中的一级标题行（页面已显示title）
        body_lines = [ln for ln in body_lines if not ln.startswith('# ')]
        # 去掉孤立的分隔线
        body_lines = [ln for ln in body_lines if ln.strip() != '---']
        # 压缩连续空行
        final = []
        prev_blank = False
        for ln in body_lines:
            blank = not ln.strip()
            if blank and prev_blank:
                continue
            final.append(ln)
            prev_blank = blank
        content = build_frontmatter(p) + "\n" + "\n".join(final).strip() + "\n"
        out_path = OUT / f'{p["slug"]}.md'
        out_path.write_text(content, encoding="utf-8")
        print(f"[OK] {p['slug']}  ({len(final)} 行)")

if __name__ == "__main__":
    run()
