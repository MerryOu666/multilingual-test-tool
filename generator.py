import random
from templates import ALL_LANGUAGES

CATEGORY_WEIGHTS = {
    "常规文案": 0.40,
    "长难句": 0.15,
    "短文本": 0.10,
    "数字日期": 0.10,
    "特殊字符": 0.05,
    "边界场景": 0.10,
    "专业术语": 0.05,
    "口语俚语": 0.05,
}

ALL_CATEGORIES = list(CATEGORY_WEIGHTS.keys())
LENGTH_OPTIONS = [100, 500, 1000, 2000]
NO_SPACE_JOIN_LANGS = {"zh-CN", "ja-JP", "ko-KR", "th-TH"}

ZH_LONG_COPY = {
    "常规文案": {
        "topics": ["社区服务调整", "公共交通安排", "校园活动通知", "企业内部协作", "门店运营更新"],
        "openings": [
            "为保证{topic}能够平稳推进，相关负责人已对当前情况进行了梳理，并结合用户反馈制定了后续安排。",
            "围绕{topic}的实际执行需求，项目组在前期调研的基础上形成了较为完整的工作方案。",
            "近期，{topic}受到较多关注，相关部门正在按照既定节奏协调资源、完善流程并同步信息。",
        ],
        "details": [
            "本次安排将优先处理影响范围较大的事项，同时保留必要的缓冲时间，避免短时间内集中调整给使用者带来不便。",
            "现场工作人员会根据实际客流、设备状态和反馈记录持续优化执行细节，并通过公告、短信或系统消息及时提醒。",
            "对于已经提交的问题，后台会按照时间顺序进行归类，必要时安排专人复核，确保处理结果清晰、可追踪。",
        ],
        "closings": [
            "后续如有新的变化，将通过正式渠道继续发布，请以最新通知为准。",
            "请相关人员提前做好准备，并在执行过程中保持沟通，以便问题能够及时解决。",
        ],
    },
    "长难句": {
        "topics": ["跨部门协同项目", "长期服务升级计划", "复杂审批流程", "区域资源整合", "多阶段产品改版"],
        "openings": [
            "尽管{topic}在推进过程中涉及多个系统、多个角色以及若干需要反复确认的业务规则，但只要各环节能够按照既定标准持续校验，整体进度仍然可以保持稳定。",
            "由于{topic}既包含前期调研、方案评估，也包含执行跟踪和结果复盘，因此任何一个阶段的判断都不能脱离完整背景单独作出。",
        ],
        "details": [
            "如果只关注单一指标而忽略上下游之间的依赖关系，就很容易在表面数据看似正常的情况下遗漏潜在风险。",
            "在实际落地时，团队需要同时考虑人员排期、系统承载、沟通成本和异常回滚方案，以免临时调整影响最终效果。",
            "即便短期内存在反馈不一致的情况，也应通过样本复核、场景拆分和责任边界确认来逐步收敛问题。",
        ],
        "closings": [
            "只有当规则、数据和执行路径都能相互印证时，最终结论才具有足够的参考价值。",
            "因此，后续评估不应停留在单点判断上，而应结合完整链路进行持续观察。",
        ],
    },
    "短文本": {
        "topics": ["移动端设置页", "订单确认页", "消息中心", "支付结果页", "会员权益页"],
        "openings": [
            "在{topic}中，短文本需要同时承担提示、确认和引导作用，因此每一个按钮、标签和状态说明都应保持简洁明确。",
            "针对{topic}的界面文案设计，团队将信息拆分为标题、操作入口、状态反馈和错误提示四类内容。",
        ],
        "details": [
            "主要按钮使用直接动词，次要操作避免制造歧义；当用户完成关键动作后，页面应立即给出可理解的反馈。",
            "空状态文案不宜过长，应说明当前没有内容的原因，并提供下一步可以执行的操作。",
            "错误提示应指出问题所在，而不是简单展示失败或异常，必要时还需要补充恢复方式。",
        ],
        "closings": [
            "整体文案应服务于快速理解和低成本操作，而不是堆砌说明。",
            "最终目标是让用户无需反复猜测，也能顺利完成当前任务。",
        ],
    },
    "数字日期": {
        "topics": ["季度经营报告", "活动排期", "账单结算", "库存盘点", "跨境订单统计"],
        "openings": [
            "本次{topic}覆盖2026年1月1日至2026年3月31日的数据，统计口径包含订单数量、金额变化、完成率和异常占比。",
            "围绕{topic}，系统已按照日期、地区和业务类型完成初步汇总，并对关键数字进行了二次校验。",
        ],
        "details": [
            "截至2026年4月5日18:30，累计记录为12,458条，环比增长7.6%，其中高优先级事项占比约为13.2%。",
            "金额字段统一保留两位小数，人民币、美元和欧元分别按CNY 7.12、USD 1.00、EUR 0.92的参考汇率展示。",
            "日期格式同时覆盖YYYY-MM-DD、DD/MM/YYYY和本地化长日期，便于验证不同区域的显示效果。",
        ],
        "closings": [
            "后续统计将继续保留原始明细，便于审计、回溯和跨系统比对。",
            "如口径发生调整，应在报告页显著位置说明版本号和生效时间。",
        ],
    },
    "特殊字符": {
        "topics": ["富文本输入框", "搜索关键词", "消息推送内容", "用户昵称", "多格式备注"],
        "openings": [
            "在{topic}的测试中，需要覆盖中文、英文、emoji、数学符号、货币符号以及全角半角字符混排的情况。",
            "本轮{topic}校验重点关注特殊字符的输入、保存、展示、复制和导出链路是否保持一致。",
        ],
        "details": [
            "例如文本中可能同时出现@用户、#话题#、￥128.00、50%、A/B测试、√确认、×取消以及😀🔥等表情符号。",
            "系统在处理引号、括号、斜杠、换行、制表符和连续空格时，不应出现截断、转义错误或样式错乱。",
            "如果内容包含HTML片段、Markdown标记或类似<script>的字符串，也应作为普通文本安全展示。",
        ],
        "closings": [
            "最终结果应保证所见即所得，并避免因字符集差异造成数据丢失。",
            "所有导出文件也应保留原始字符，方便后续人工核对。",
        ],
    },
    "边界场景": {
        "topics": ["超长输入校验", "弱网络提交", "重复点击操作", "空数据展示", "异常恢复流程"],
        "openings": [
            "针对{topic}，测试需要模拟用户在极端条件下的真实操作，而不是只验证理想路径。",
            "在{topic}场景中，系统应能够处理异常输入、延迟响应和状态回退等复杂情况。",
        ],
        "details": [
            "当输入内容接近上限时，页面应清楚提示剩余长度，并避免保存后内容被静默截断。",
            "如果网络请求超时，系统应保留用户已经填写的信息，并提供重试入口，而不是直接清空页面。",
            "连续点击同一个按钮时，前端应避免重复提交，后端也需要通过幂等机制保证结果唯一。",
        ],
        "closings": [
            "边界场景的价值在于暴露真实使用中的脆弱环节，因此验证结果应被纳入发布前检查。",
            "只有这些异常路径稳定，核心流程的可靠性才更有保障。",
        ],
    },
    "专业术语": {
        "topics": ["模型评估报告", "财务披露材料", "法律合规审查", "云服务架构说明", "医学研究摘要"],
        "openings": [
            "本次{topic}围绕核心指标、执行口径和风险控制展开，重点说明关键结论背后的数据依据。",
            "在{topic}中，所有术语均按照行业通用定义使用，并尽量保持指标、参数和结论之间的一致性。",
        ],
        "details": [
            "评估过程需要关注样本规模、置信区间、基线对照、异常值处理和可复现性，避免单一结果被过度解读。",
            "如果涉及合同、审计或监管要求，应明确责任主体、适用范围、生效日期和证据留存方式。",
            "技术方案还应说明系统吞吐、延迟、容灾等级、权限边界和数据脱敏策略。",
        ],
        "closings": [
            "最终文本应在专业性和可读性之间取得平衡，使非技术读者也能理解主要风险。",
            "相关结论仍需结合原始材料复核，不宜脱离上下文单独引用。",
        ],
    },
    "口语俚语": {
        "topics": ["新品体验", "活动现场", "朋友聚会", "线上讨论", "日常吐槽"],
        "openings": [
            "说实话，这次{topic}一开始看着挺普通，真用起来才发现细节还挺多。",
            "聊到{topic}，大家的第一反应可能都不一样，但真正体验过之后，感觉还是有不少可以说道的地方。",
        ],
        "details": [
            "有些地方确实很顺手，基本不用想就能完成操作；也有些小细节让人忍不住想吐槽两句。",
            "如果只是随便看一眼，可能觉得没什么特别，但多用几次之后，就能感受到它到底适不适合日常场景。",
            "大家讨论的时候也挺直接，喜欢的点会马上夸，不舒服的地方也会立刻被拎出来。",
        ],
        "closings": [
            "整体来说，它不是那种一眼惊艳的东西，但胜在够实用，后续再打磨一下会更稳。",
            "要是能把几个明显的小问题处理掉，体验应该会舒服很多。",
        ],
    },
}


def _text_length(text):
    return len("".join(text.split()))


def _join_texts(texts, lang_code):
    sep = "" if lang_code in NO_SPACE_JOIN_LANGS else " "
    return sep.join(texts)


def _natural_trim(text, target_length):
    if _text_length(text) <= target_length:
        return text.strip()

    chars = []
    visible = 0
    for ch in text:
        chars.append(ch)
        if not ch.isspace():
            visible += 1
        if visible >= target_length:
            break

    candidate = "".join(chars).rstrip()
    min_visible = max(20, int(target_length * 0.85))
    for idx in range(len(candidate) - 1, -1, -1):
        if candidate[idx] in "。！？.!?":
            trimmed = candidate[: idx + 1].rstrip()
            if _text_length(trimmed) >= min_visible:
                return trimmed

    return candidate.rstrip("，,；;、 ") + "。"


def _weighted_category(cats):
    weights = [CATEGORY_WEIGHTS.get(cat, 0.01) for cat in cats]
    return random.choices(cats, weights=weights, k=1)[0]


def _choose_length_category(templates, category):
    available_cats = [c for c in ALL_CATEGORIES if c in templates and templates[c]]
    if not available_cats:
        return None
    if category != "全部" and category in available_cats:
        return category
    return _weighted_category(available_cats)


def _generate_zh_long_copy(category, target_length):
    profile = ZH_LONG_COPY[category]
    topic = random.choice(profile["topics"])
    sections = [
        random.choice(profile["openings"]).format(topic=topic),
        random.choice(profile["details"]),
        random.choice(profile["details"]),
        random.choice(profile["closings"]),
    ]

    text = "\n\n".join(sections)
    while _text_length(text) < target_length:
        extra = random.choice(profile["details"] + profile["closings"])
        text = f"{text}\n\n{extra}"

    return _natural_trim(text, target_length)


def _generate_structured_from_templates(templates, lang_code, category, target_length):
    # 非中文语种没有内置规则长文案库；这里保持同一类别、同一段落结构，避免跨类别随机拼接。
    pool = templates[category]
    ordered = pool[:]
    random.shuffle(ordered)
    paragraphs = []
    cursor = 0

    while _text_length("\n\n".join(paragraphs)) < target_length:
        if cursor >= len(ordered):
            random.shuffle(ordered)
            cursor = 0
        chunk_size = 2 if target_length <= 500 else 3
        chunk = ordered[cursor : cursor + chunk_size]
        cursor += chunk_size
        paragraphs.append(_join_texts(chunk, lang_code))

    return _natural_trim("\n\n".join(paragraphs), target_length)


def generate_by_length(lang_code, target_length, category="全部", count=1):
    mod = ALL_LANGUAGES.get(lang_code)
    if mod is None:
        return []

    templates = mod.TEMPLATES
    results = []
    for idx in range(1, int(count) + 1):
        selected_category = _choose_length_category(templates, category)
        if selected_category is None:
            return []

        if lang_code == "zh-CN" and selected_category in ZH_LONG_COPY:
            text = _generate_zh_long_copy(selected_category, target_length)
        else:
            text = _generate_structured_from_templates(templates, lang_code, selected_category, target_length)

        results.append({
            "序号": idx,
            "类别": selected_category,
            "语种": mod.LANG_NAME,
            "语种代码": mod.LANG_CODE,
            "目标字数": target_length,
            "实际字数": _text_length(text),
            "测试用例": text,
        })
    return results


def generate(lang_code, count, category="全部"):
    mod = ALL_LANGUAGES.get(lang_code)
    if mod is None:
        return []

    templates = mod.TEMPLATES

    if category != "全部" and category in templates:
        pool = [(category, t) for t in templates[category]]
        if len(pool) >= count:
            selected = random.sample(pool, count)
        else:
            selected = pool[:]
            while len(selected) < count:
                selected.append(random.choice(pool))
            random.shuffle(selected)
    else:
        selected = []
        remaining = count
        cats = [c for c in ALL_CATEGORIES if c in templates and templates[c]]
        if not cats:
            return []

        for i, cat in enumerate(cats):
            weight = CATEGORY_WEIGHTS.get(cat, 1.0 / len(cats))
            if i == len(cats) - 1:
                n = remaining
            else:
                n = max(1, int(count * weight))
                n = min(n, remaining)
            remaining -= n
            for _ in range(n):
                selected.append((cat, random.choice(templates[cat])))
            if remaining <= 0:
                break
        random.shuffle(selected)
        selected = selected[:count]

    results = []
    for idx, (cat, text) in enumerate(selected, 1):
        results.append({
            "序号": idx,
            "类别": cat,
            "语种": mod.LANG_NAME,
            "语种代码": mod.LANG_CODE,
            "测试用例": text,
        })

    return results
