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
LONG_COPY_LANGUAGES = ["zh-CN", "en-GB", "ja-JP", "ko-KR"]
LENGTH_EXCLUDED_CATEGORIES = {"短文本", "长难句"}
LENGTH_CATEGORIES = [c for c in ALL_CATEGORIES if c not in LENGTH_EXCLUDED_CATEGORIES]

LONG_COPY = {
    "zh-CN": {
        "常规文案": [
            "社区物业管理处近期对小区的公共设施进行了一次全面巡检，重点排查了电梯运行状况、消防通道畅通情况以及地下车库的照明系统。巡检过程中发现三号楼电梯存在轻微异响，维保人员已在当天下午完成更换配件并测试运行，目前电梯已恢复正常使用。针对消防通道被占用的问题，物业已在楼道内张贴提示，并计划联合社区居委会开展专项清理。地下车库的照明系统也进行了升级，原有老旧灯具全部更换为节能型LED灯，夜间照明效果明显改善。物业表示，后续会将巡检结果和处理进度定期公布在业主群和公告栏，方便居民随时了解维护情况，也欢迎大家继续反馈问题。",
            "本周末的社区义卖活动吸引了不少家庭参与，现场设置了图书交换角、手工艺品展台和儿童游戏区，整体氛围轻松热闹。义卖所得款项将全部捐赠给街道助老基金，用于购买老年活动中心的健身器材和阅读设备。许多居民提前整理了家中闲置的旧书、玩具和手工饰品，摆在摊位上供大家挑选。孩子们对手工体验区格外感兴趣，志愿者老师现场指导制作皮具和陶艺小件，排队队伍一直没有断过。社区工作人员介绍，这类活动今后会定期举办，既能盘活闲置资源，也能增进邻里交流，让社区关系更加融洽。",
        ],
        "数字日期": [
            "根据最新统计数据，本季度（2026年4月1日至6月30日）公司整体营收达到人民币3.87亿元，同比增长14.6%，环比增长5.2%。其中，华东区域贡献最大，占总营收38.5%，达到1.49亿元；华南区域占比27.3%；其余区域合计占比34.2%。从产品线看，主力产品A系列销售额为2.1亿元，同比提升9.8%；新推出的B系列产品自3月上线以来，累计销售额突破6800万元。运营成本方面，本季度总支出为2.65亿元，其中原材料采购占比52%，人力成本占比28%，其余为物流与营销费用。财务团队预计，若市场需求保持当前趋势，下季度营收有望突破4.2亿元。",
            "本次活动排期已经确认，将于2026年8月15日星期六上午9点在市中心会展中心举行，预计持续到下午6点，共设置三个平行会场。签到时间为上午8点至8点50分，请参会人员提前到达并完成身份核验。上午9点到11点30分为主题演讲，共安排五位嘉宾发言，每位发言时长控制在25分钟以内。午餐时间为11点30分到下午1点，会展中心一楼餐厅将提供自助餐。下午1点到4点为分会场专题讨论，参会者可根据兴趣选择A、B、C三个分会场，每个分会场限额150人，建议提前预约座位。",
        ],
        "特殊字符": [
            "在多语种输入框兼容性测试中，测试人员构造了一批包含混合符号的样本文本，用来验证系统在不同渠道下的展示效果。例如某条记录写道：【重要】用户反馈整理——评分★★★★☆（4.5/5.0），涉及金额约￥1,280.00，占比约35%，处理进度████████░░ 80%。另一条记录包含数学与化学公式混排：能量公式E=mc²中c≈3×10⁸ m/s，而某化学反应式为2H₂+O₂→2H₂O。还有样本专门测试表情符号与文字混排，例如“本次促销力度空前🔥🔥🔥，参与用户领取888元礼包🎁，活动进度✅已完成，⚠️请注意仅限前100名”。",
            "为了验证富文本编辑器对特殊字符的兼容能力，测试团队设计了一系列包含罕见符号组合的文本样例。其中一段内容是：会议纪要摘要——议题一「预算调整方案」讨论结果：通过✓；议题二〈人员编制优化〉讨论结果：待定○；议题三《跨部门协作机制》讨论结果：驳回×。文本中还穿插带圈数字与计量单位混排，例如①号方案预计节省成本约¥45,000，②号方案占地面积约128.5㎡，③号方案预计耗电量约320kWh/月。整体样例用于提前暴露系统在保存、展示、复制和导出复杂符号时的边界缺陷。",
        ],
        "边界场景": [
            "本次边界场景测试重点关注系统在极端输入条件下的稳定性表现，测试用例覆盖从空输入到超长文本的多个层级。测试首先验证空字符串和纯空白字符输入的处理逻辑，系统需要正确识别并给出提示，而不是直接报错或静默失败。随后测试团队构造了一段长度接近系统上限的连续文本，用来验证系统在处理超长字符串时是否出现明显卡顿或内存占用异常。另外还测试了包含大量连续换行符和制表符的文本，观察系统展示时能否保持排版可读性。测试过程中还加入零宽空格和方向控制符混入正常文字的样本，验证系统是否会产生显示异常或复制粘贴后的内容变化。",
            "边界场景测试的另一个重点是验证系统对高频重复操作的容错能力。测试人员模拟用户在短时间内连续点击同一个提交按钮的场景，观察系统是否会因为重复请求产生数据重复写入。测试还包括在网络延迟较高或中途断开连接时提交表单，验证系统能否正确保留已填写内容，并在网络恢复后提示用户重新提交，而不是直接丢弃全部输入。此外，测试团队构造了包含潜在注入风险的文本样例，用来验证输入过滤和转义机制是否完善，确保这类内容只会被当作普通文本处理。",
        ],
        "专业术语": [
            "本次模型评估报告围绕图像分类任务的核心性能指标展开分析，重点考察模型在标准数据集上的准确率、召回率以及推理效率。评估结果显示，该模型在验证集上的Top-1准确率达到87.3%，Top-5准确率达到96.8%，在同类模型中处于领先水平。推理延迟方面，在A100 GPU单卡环境下，单张图片的平均推理耗时为2.1毫秒，满足实时性要求较高的应用场景。评估过程中还针对小样本类别和长尾分布问题进行了专项分析，发现模型在样本量较少的类别上准确率有所下降，建议后续通过数据增强和类别重加权策略优化。",
            "根据本次法律合规审查结论，公司现行数据处理流程在个人信息收集环节基本符合相关法规要求，但在授权同意表述和留存期限设定上仍有改进空间。审查团队重点核查了用户协议和隐私政策条款，发现部分表述过于笼统，未清晰说明数据使用场景和第三方共享范围，建议进一步细化并增加可勾选的分项授权。在数据留存方面，现行策略对不同类型数据的保存期限没有区分处理，建议根据数据敏感程度分级设定留存周期，并建立到期自动清理机制。",
        ],
        "口语俚语": [
            "说真的，这次新品体验属实有点出乎意料。一开始看包装和宣传图，感觉就是普通日用品，价格也不算便宜，心里多少有点犹豫。但真正上手用了几天之后，发现细节做得比想象中用心，很多小设计都是真的在考虑日常场景，不是那种只为了噱头的东西。比如收纳部分，一开始没觉得有什么特别，用了才发现日常拿取顺手很多，基本不用多想就能完成操作。当然也不是完全没有槽点，包装盒子设计得有点大，快递到手那一刻还以为买错了尺寸。总体来说，这次体验算是超出预期，虽然不是一眼惊艳，但胜在够实用。",
            "昨天去朋友聚会真是又好笑又有点emo。本来说好六点集合，结果一半人堵在路上，硬是拖到七点半才凑齐，服务员都问了好几次要不要先上菜。等大家终于坐下后，气氛倒是很快热起来，聊着聊着就开始互相吐槽最近工作上的破事，谁又被临时加活，谁的项目又被砍，感觉大家都是“惨”字当头，但笑点也一个接一个。中间还有朋友非要点特辣的菜，结果辣到原地社死，边喝水边说好吃，把大家笑得不行。这种朋友局虽然折腾，但每次聚完都感觉能量被重新充满。",
        ],
    },
    "en-GB": {
        "常规文案": [
            "The residents' association has completed its monthly review of shared facilities across the estate, with particular attention given to lift maintenance, corridor safety and the lighting in the underground car park. During the inspection, the team identified a minor fault in the lift serving Block C and arranged for an engineer to replace the affected component the same afternoon. The car park lighting has also been upgraded to energy-efficient LED fittings, improving visibility during evening hours. Notices will be posted in the lobby and sent by email so that residents can follow the progress of each maintenance item and report any further concerns promptly.",
            "The local library will extend its weekend opening hours throughout August in response to increased demand from families and students. The children's reading area will open from 9 a.m. on Saturdays, while the study rooms on the second floor can now be booked in two-hour slots through the online reservation system. Staff will also run a small programme of workshops covering digital research, creative writing and basic coding for teenagers. The council expects the changes to make the library more useful during the summer holiday period and will review visitor numbers at the end of the trial.",
        ],
        "数字日期": [
            "According to the latest quarterly report, total revenue for the period from 1 April to 30 June 2026 reached GBP 38.7 million, representing a year-on-year increase of 14.6% and a quarter-on-quarter increase of 5.2%. The London region accounted for 41.3% of sales, while the North West contributed 18.9%. Product line A remained the largest contributor with GBP 21.4 million in revenue, but product line B grew fastest after its March launch, reaching GBP 6.8 million by the end of the quarter. Operating costs totalled GBP 26.5 million, with procurement, staffing and logistics making up the majority of expenditure.",
            "The conference schedule has now been finalised. Registration will open at 08:00 on Saturday, 15 August 2026, and the main programme will begin at 09:00 in Hall A of the City Exhibition Centre. Five keynote speakers are scheduled between 09:00 and 11:30, each with a 25-minute presentation and a short Q&A session. Lunch will be served from 11:30 to 13:00, followed by three parallel workshops running until 16:00. Each workshop is limited to 150 participants, so attendees are encouraged to reserve a seat in advance through the event portal.",
        ],
        "特殊字符": [
            "The compatibility test for the rich-text field includes a deliberately mixed sample containing symbols, ratings, currency values and emoji. One entry reads: [URGENT] Customer feedback summary — score ★★★★☆ (4.5/5), value approximately £1,280.00, completion ████████░░ 80%. Another sample includes scientific notation and formulae such as E=mc², CO₂ emissions, H₂O concentration and 3×10⁸ m/s. The same test batch also contains hashtags, user mentions, arrows, brackets, quotation marks and emoji like ✅, ⚠️, 🔥 and 🎁 to confirm that saving, rendering, copying and exporting preserve every character correctly.",
            "A separate text sample is designed to test how the editor handles punctuation-heavy content. It includes paired quotation marks, nested brackets, slashes, pipes, currency symbols and mathematical signs: item ① costs £45.00, item ② covers 128.5㎡, item ③ consumes 320kWh/month, and item ④ is marked as pending ○. The aim is not to produce a readable announcement but to simulate the messy material that users often paste from spreadsheets, reports and chat tools. The system should treat all of it as plain text, avoid unwanted formatting, and keep the output stable in both CSV and Excel exports.",
        ],
        "边界场景": [
            "The boundary-condition test focuses on how the application behaves when users submit unusually long or empty input. The first scenario uses a blank value, a string made entirely of spaces, and a message containing only line breaks, expecting the interface to show a clear validation prompt instead of failing silently. The second scenario uses a long block of repeated characters close to the maximum supported length, allowing testers to observe rendering speed, memory usage and export reliability. A final scenario inserts invisible characters such as zero-width spaces and direction markers into ordinary text, checking whether copying, saving and displaying the content changes the user's intended message.",
            "Another boundary test examines repeated actions and unstable network conditions. Testers click the submit button several times in quick succession to ensure that the back end prevents duplicate records and that the front end disables repeated submissions at the right moment. They also simulate a slow connection, a request timeout and a browser refresh during form submission. In each case, the expected behaviour is that user-entered text remains available, the system explains what happened, and the user can retry without starting from scratch. These cases are rare in controlled demos but common enough in production to justify dedicated testing.",
        ],
        "专业术语": [
            "This model evaluation report reviews the core metrics for an image-classification system deployed in a production-like environment. On the validation set, the model achieved a Top-1 accuracy of 87.3% and a Top-5 accuracy of 96.8%, while average inference latency on a single A100 GPU was measured at 2.1 milliseconds per image. The analysis also examined performance on long-tail classes, where accuracy dropped by approximately 6.2 percentage points compared with high-frequency classes. The report recommends targeted data augmentation, class reweighting and additional calibration checks before the model is used in high-risk decision flows.",
            "The compliance review found that the current data-processing workflow broadly satisfies the requirements for lawful collection and storage of personal information, but several policy statements remain too general. In particular, the privacy notice does not clearly separate analytics, marketing and operational use cases, making it difficult for users to grant informed consent for each purpose. The review also recommends assigning different retention periods to different categories of data, with shorter retention for sensitive identifiers and automated deletion once the retention period expires. Cross-border transfer records should be expanded to include risk assessments and approval evidence.",
        ],
        "口语俚语": [
            "Honestly, the new product turned out better than I expected. When I first saw the photos, it looked like another ordinary everyday item with slightly ambitious pricing, so I was not convinced. After using it for a few days, though, the small details started to make sense. The storage layout is simple, the main parts are easy to reach, and the whole thing feels designed for real daily use rather than just for marketing pictures. It is not perfect: the packaging is bigger than it needs to be, and the first impression is a bit underwhelming. Still, it is the kind of product that quietly wins you over because it does the basic things well.",
            "Last night's catch-up with friends was chaotic in the best possible way. We said we would meet at six, but half the group got stuck in traffic, so dinner did not really start until half past seven. Once everyone arrived, the conversation jumped straight from work complaints to old stories, and somehow every serious topic turned into a joke within two minutes. Someone ordered a dish that was far too spicy, insisted it was delicious while drinking water non-stop, and gave the rest of us the biggest laugh of the evening. It was one of those nights that leaves you tired but oddly recharged.",
        ],
    },
    "ja-JP": {
        "常规文案": [
            "地域の管理組合は、今月の共有設備点検を終え、エレベーターの運転状況、廊下の安全性、地下駐車場の照明を中心に確認しました。点検では三号棟のエレベーターに軽い異音が見つかり、当日の午後に保守担当者が部品を交換して試運転を行いました。地下駐車場では古い照明を省エネ型LEDに入れ替え、夜間の視認性が大きく改善されています。管理組合は今後、対応状況を掲示板と住民向けメールで定期的に共有し、追加の不具合があれば早めに連絡してほしいと案内しています。",
            "市立図書館は夏休み期間中の利用増加に合わせ、週末の開館時間を延長することを発表しました。土曜日は午前九時から児童閲覧室を開放し、二階の学習室はオンライン予約で二時間単位の利用が可能になります。館内では中高生向けに調べ学習、文章作成、基礎的なプログラミングを扱う小規模な講座も行われる予定です。市は今回の変更により、図書館が家族連れや学生にとってより使いやすい場所になることを期待しており、試験期間後に利用者数と満足度を確認する方針です。",
        ],
        "数字日期": [
            "最新の四半期報告によると、2026年4月1日から6月30日までの売上高は38億7,000万円となり、前年同期比14.6%、前期比5.2%の増加を記録しました。関東エリアが全体の41.3%を占め、関西エリアは22.8%でした。主力商品のAシリーズは21億4,000万円の売上を維持し、3月に発売されたBシリーズは四半期末までに6億8,000万円を達成しました。営業費用は26億5,000万円で、仕入れ、人件費、物流費が大部分を占めています。",
            "イベントの開催日程が確定し、2026年8月15日土曜日の午前9時から市内展示センターで実施されることになりました。受付は午前8時に開始し、参加者は8時50分までに本人確認を済ませる必要があります。午前9時から11時30分までは基調講演が行われ、五名の登壇者がそれぞれ25分間発表します。昼食休憩は11時30分から13時までで、午後は三つの分科会が16時まで同時進行します。各分科会の定員は150名のため、事前予約が推奨されています。",
        ],
        "特殊字符": [
            "リッチテキスト入力欄の互換性テストでは、記号、評価、通貨、絵文字を混在させたサンプルを使用します。たとえば「【重要】フィードバック集計——評価★★★★☆（4.5/5）、金額約￥128,000、進捗████████░░ 80%」という内容を保存し、表示、コピー、CSV出力で崩れないか確認します。別のサンプルにはE=mc²、CO₂、H₂O、3×10⁸ m/sのような数式や化学式を含め、さらに✅、⚠️、🔥、🎁などの絵文字を加えて、文字化けや不要な変換が起きないことを検証します。",
            "別の検証用テキストでは、括弧、引用符、スラッシュ、縦線、丸数字、単位記号を意図的に多く含めています。例として、①案は費用45,000円、②案は面積128.5㎡、③案は消費電力量320kWh/月、④案は状態○保留といった情報を一つの段落内に混在させます。ユーザーが表計算ソフトやチャットから複雑な内容を貼り付けた場合でも、システムはそれを通常のテキストとして扱い、保存後の表示やエクスポート時に意味が変わらないようにする必要があります。",
        ],
        "边界场景": [
            "境界条件テストでは、空文字、空白だけの文字列、改行だけの入力、そして上限に近い長文入力を順番に確認します。空入力の場合は明確なエラーメッセージを表示し、処理が途中で止まったり無言で失敗したりしないことが重要です。長文入力では、画面表示の遅延、保存処理の時間、エクスポート時の欠落を重点的に観察します。さらに、ゼロ幅スペースや文字方向制御記号を通常の文章に混ぜ、コピーや保存後に見た目と内容が意図せず変化しないかを確認します。",
            "もう一つの境界テストでは、短時間に同じ送信ボタンを連続して押す状況を再現します。フロントエンドは重複送信を防ぎ、バックエンドも同じ内容が複数回登録されないように処理する必要があります。また、通信が遅い状態、リクエストのタイムアウト、送信中の画面更新も検証対象になります。期待される動作は、入力済みの内容が失われず、何が起きたのかユーザーに分かる形で表示され、必要に応じて再送信できることです。",
        ],
        "专业术语": [
            "本モデル評価レポートでは、画像分類システムの主要指標としてTop-1精度、Top-5精度、推論レイテンシを確認しました。検証データセットにおけるTop-1精度は87.3%、Top-5精度は96.8%であり、A100 GPU単体での平均推論時間は画像一枚あたり2.1ミリ秒でした。一方で、サンプル数の少ないロングテールカテゴリでは高頻度カテゴリに比べて精度が約6.2ポイント低下しており、データ拡張、クラス重み付け、追加キャリブレーションが推奨されます。",
            "コンプライアンスレビューの結果、現在の個人情報処理フローは収集と保管に関する基本要件を満たしているものの、利用目的の説明には改善余地があると判断されました。プライバシーポリシーでは、分析、マーケティング、運用保守の目的が十分に分離されておらず、ユーザーが個別に同意しにくい構成になっています。また、データの種類ごとに保存期間を分け、機微情報については短い保持期間と自動削除の仕組みを設けることが望ましいとされています。",
        ],
        "口语俚语": [
            "正直なところ、この新商品は思っていたよりかなり良かったです。写真だけ見たときは、よくある日用品に少し強気な価格を付けただけかなと思っていました。でも実際に数日使ってみると、細かい部分が意外と考えられていて、毎日の使い勝手がかなり楽になります。収納の位置や取り出しやすさも自然で、派手ではないけれど地味に助かるタイプです。もちろん完璧ではなく、箱が少し大きすぎるとか、第一印象が弱いとか気になる点はあります。それでも、使い続けるほど良さが分かる商品だと思いました。",
            "昨日の友人との集まりは、良い意味でかなりカオスでした。六時集合のはずが半分くらい遅れて、結局ちゃんと始まったのは七時半過ぎです。全員そろってからは仕事の愚痴、昔の失敗談、最近ハマっているものの話でずっと盛り上がりました。誰かが激辛料理を頼んで、辛いと言いながらもおいしいと言い張っていたのが一番面白かったです。帰る頃にはかなり疲れていたのに、妙に気持ちは軽くなっていて、こういう集まりはやっぱり必要だなと思いました。",
        ],
    },
    "ko-KR": {
        "常规文案": [
            "아파트 관리사무소는 이번 달 공용 시설 점검을 마치고 엘리베이터 운행 상태, 복도 안전, 지하 주차장 조명 상태를 중심으로 결과를 정리했습니다. 점검 과정에서 3동 엘리베이터에서 가벼운 소음이 확인되어 당일 오후 유지보수 담당자가 부품을 교체하고 시운전을 완료했습니다. 지하 주차장에는 노후 조명을 에너지 효율이 높은 LED 조명으로 교체해 야간 시야가 크게 개선되었습니다. 관리사무소는 앞으로 처리 현황을 게시판과 입주민 안내 메시지로 공유하고, 추가 불편 사항이 있으면 즉시 접수해 순차적으로 처리하겠다고 밝혔습니다.",
            "시립도서관은 여름방학 기간 이용객 증가에 맞춰 주말 운영 시간을 연장한다고 안내했습니다. 토요일에는 어린이 자료실이 오전 9시부터 개방되며, 2층 학습실은 온라인 예약을 통해 두 시간 단위로 이용할 수 있습니다. 도서관은 중고등학생을 대상으로 자료 조사, 글쓰기, 기초 코딩을 다루는 소규모 프로그램도 운영할 예정입니다. 시는 이번 운영 시간 조정이 가족 단위 방문객과 학생들에게 더 실질적인 도움이 될 것으로 보고 있으며, 시범 운영이 끝난 뒤 이용자 수와 만족도를 종합적으로 검토할 계획입니다.",
        ],
        "数字日期": [
            "최신 분기 보고서에 따르면 2026년 4월 1일부터 6월 30일까지의 전체 매출은 387억 원으로 전년 동기 대비 14.6%, 전 분기 대비 5.2% 증가했습니다. 수도권 지역은 전체 매출의 41.3%를 차지했으며, 부산과 경남 지역은 18.9%를 기록했습니다. 주력 제품 A 시리즈는 214억 원의 매출을 유지했고, 3월 출시된 B 시리즈는 분기 말 기준 68억 원을 달성했습니다. 운영 비용은 총 265억 원으로 집계되었으며, 원자재 구매, 인건비, 물류비가 주요 항목을 차지했습니다.",
            "행사 일정이 최종 확정되어 2026년 8월 15일 토요일 오전 9시부터 시내 전시컨벤션센터에서 진행됩니다. 등록은 오전 8시에 시작되며, 참가자는 8시 50분까지 본인 확인을 마쳐야 합니다. 오전 9시부터 11시 30분까지는 다섯 명의 연사가 각각 25분씩 기조 발표를 진행하고, 발표 사이에는 짧은 질의응답 시간이 마련됩니다. 점심시간은 11시 30분부터 오후 1시까지이며, 오후에는 세 개의 분과 세션이 4시까지 동시에 운영됩니다. 각 세션 정원은 150명으로 제한되어 사전 예약이 권장됩니다.",
        ],
        "特殊字符": [
            "리치 텍스트 입력창의 호환성 테스트에는 기호, 평점, 통화, 이모지를 섞은 샘플 문장을 사용합니다. 예를 들어 한 기록에는 '[중요] 고객 피드백 요약——평점 ★★★★☆(4.5/5), 금액 약 ₩1,280,000, 진행률 ████████░░ 80%'라는 내용이 포함됩니다. 다른 샘플에는 E=mc², CO₂, H₂O, 3×10⁸ m/s와 같은 수식과 화학식이 포함되며, ✅, ⚠️, 🔥, 🎁 같은 이모지도 함께 들어갑니다. 이 테스트의 목적은 저장, 표시, 복사, CSV 또는 Excel 내보내기 과정에서 모든 문자가 그대로 유지되는지 확인하는 것입니다.",
            "별도의 검증 문장에는 괄호, 따옴표, 슬래시, 세로줄, 원문자, 단위 기호를 의도적으로 많이 포함했습니다. 예를 들어 ①안은 비용 45,000원, ②안은 면적 128.5㎡, ③안은 전력 사용량 320kWh/월, ④안은 상태 ○보류로 표시됩니다. 사용자가 스프레드시트나 메신저에서 복잡한 내용을 붙여넣는 경우에도 시스템은 이를 일반 텍스트로 처리해야 하며, 저장 후 화면 표시나 파일 내보내기 과정에서 의미가 바뀌거나 문자가 누락되어서는 안 됩니다.",
        ],
        "边界场景": [
            "경계 조건 테스트는 빈 문자열, 공백만 있는 문자열, 줄바꿈만 포함된 입력, 그리고 허용 길이에 가까운 장문 입력을 순서대로 확인합니다. 빈 입력의 경우 시스템은 명확한 안내 문구를 보여줘야 하며, 조용히 실패하거나 예외 화면으로 넘어가서는 안 됩니다. 장문 입력에서는 화면 렌더링 속도, 저장 처리 시간, 내보내기 결과의 누락 여부를 집중적으로 확인합니다. 또한 일반 문장 안에 제로 폭 공백이나 방향 제어 문자를 섞어 넣고, 복사하거나 저장한 뒤 내용이 의도치 않게 달라지지 않는지도 점검합니다.",
            "또 다른 경계 테스트는 짧은 시간 안에 같은 제출 버튼을 여러 번 누르는 상황을 재현합니다. 프런트엔드는 중복 클릭을 막아야 하고, 백엔드는 동일한 요청이 여러 번 저장되지 않도록 멱등성을 보장해야 합니다. 느린 네트워크, 요청 시간 초과, 제출 중 새로고침도 함께 검증합니다. 기대되는 동작은 사용자가 입력한 내용이 사라지지 않고, 현재 상태가 이해하기 쉽게 표시되며, 필요할 때 다시 제출할 수 있는 것입니다. 이런 상황은 데모 환경에서는 드물지만 실제 서비스에서는 충분히 발생할 수 있습니다.",
        ],
        "专业术语": [
            "이번 모델 평가 보고서는 이미지 분류 시스템의 핵심 지표인 Top-1 정확도, Top-5 정확도, 추론 지연 시간을 중심으로 작성되었습니다. 검증 데이터셋에서 모델의 Top-1 정확도는 87.3%, Top-5 정확도는 96.8%였으며, A100 GPU 단일 장비에서 이미지 한 장당 평균 추론 시간은 2.1밀리초로 측정되었습니다. 다만 샘플 수가 적은 롱테일 클래스에서는 고빈도 클래스보다 정확도가 약 6.2%포인트 낮아지는 경향이 확인되었습니다. 보고서는 배포 전 데이터 증강, 클래스 가중치 조정, 추가 보정 검사를 수행할 것을 권고합니다.",
            "이번 컴플라이언스 검토 결과, 현재 개인정보 처리 흐름은 수집과 보관에 관한 기본 요건을 대체로 충족하지만 이용 목적 설명에는 개선 여지가 있는 것으로 확인되었습니다. 개인정보 처리방침은 분석, 마케팅, 운영 유지보수 목적을 명확히 구분하지 않아 사용자가 각 목적에 대해 충분히 이해하고 동의하기 어렵습니다. 또한 데이터 유형별 보관 기간을 다르게 설정하고, 민감한 식별 정보에는 더 짧은 보관 기간과 자동 삭제 절차를 적용하는 것이 바람직합니다. 국외 이전 기록에는 위험 평가와 승인 근거도 함께 보완되어야 합니다.",
        ],
        "口语俚语": [
            "솔직히 이번 신제품은 생각보다 괜찮았습니다. 처음 사진만 봤을 때는 그냥 평범한 생활용품에 가격만 살짝 높은 느낌이라 큰 기대가 없었습니다. 그런데 며칠 써보니 작은 부분들이 꽤 잘 설계되어 있다는 게 느껴졌습니다. 수납 위치도 자연스럽고 필요한 부분을 바로 꺼내기 쉬워서 일상에서 은근히 편합니다. 물론 완벽한 제품은 아닙니다. 포장이 조금 과하고 첫인상이 강하지 않다는 점은 아쉽습니다. 그래도 계속 사용할수록 장점이 보이는 타입이라, 가격만 조금 더 합리적이면 재구매 의사도 충분히 있을 것 같습니다.",
            "어제 친구들 모임은 좋은 의미로 정말 정신없었습니다. 여섯 시에 만나기로 했는데 절반이 길에서 막혀서 제대로 시작한 건 일곱 시 반이 넘어서였습니다. 다 모이고 나서는 회사 이야기, 예전 실수담, 요즘 빠진 것들까지 주제가 계속 바뀌면서도 분위기는 계속 좋았습니다. 누군가 너무 매운 음식을 시켜놓고 맵다고 물을 계속 마시면서도 맛있다고 우기는 바람에 다 같이 한참 웃었습니다. 집에 갈 때는 꽤 피곤했지만 이상하게 기분은 가벼웠습니다. 이런 모임은 번거로워도 가끔 꼭 필요하다는 생각이 들었습니다.",
        ],
    },
}


def _text_length(text):
    return len("".join(text.split()))


def _weighted_category(categories):
    weights = [CATEGORY_WEIGHTS.get(category, 0.01) for category in categories]
    return random.choices(categories, weights=weights, k=1)[0]


# 拼接多个底稿仍不足以在小字数（如100字）下产生100条不重复文本，
# 因此额外提供了带编号/场景标记的前缀，用于制造真实存在差异的变体，
# 而不是简单复制粘贴同一段素材。标记本身不改变文本所属的类别语义。
VARIANT_MARKERS = {
    "zh-CN": [
        "场景A：", "场景B：", "场景C：", "场景D：", "场景E：", "场景F：", "场景G：", "场景H：",
        "回归用例一：", "回归用例二：", "灰度环境记录：", "线上复现记录：", "验收样例：", "压力样例：",
    ],
    "en-GB": [
        "Scenario A: ", "Scenario B: ", "Scenario C: ", "Scenario D: ", "Scenario E: ", "Scenario F: ",
        "Regression case one: ", "Regression case two: ", "Staging note: ", "Production sample: ", "Acceptance sample: ",
    ],
    "ja-JP": [
        "ケースA：", "ケースB：", "ケースC：", "ケースD：", "ケースE：", "回帰テスト一：", "検収サンプル：", "本番想定：",
    ],
    "ko-KR": [
        "시나리오 A: ", "시나리오 B: ", "시나리오 C: ", "시나리오 D: ", "회귀 사례 1: ", "검수 샘플: ", "운영 환경 예시: ",
    ],
}


def _natural_trim(text, target_length):
    text = text.strip()
    if _text_length(text) <= target_length:
        return text

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


def _extend_copy(order, target_length):
    """按给定顺序拼接底稿，直到达到目标字数（不足时循环复用顺序列表）。"""
    parts = []
    idx = 0
    while _text_length(" ".join(parts)) < target_length:
        parts.append(order[idx % len(order)])
        idx += 1
    return " ".join(parts)


def _select_length_category(lang_code, category):
    available = [c for c in LENGTH_CATEGORIES if c in LONG_COPY.get(lang_code, {})]
    if not available:
        return None
    if category in available:
        return category
    return _weighted_category(available)


def _apply_variant(text, lang_code, variant_index):
    """在文本前加入编号/场景标记，在不破坏类别语义的前提下制造可辨识差异。"""
    markers = VARIANT_MARKERS.get(lang_code, [])
    if not markers:
        return text
    marker = markers[variant_index % len(markers)]
    return marker + text


def _build_unique_text(pool, lang_code, target_length, seen_texts, variant_index):
    """从底稿池中拼出一条尚未出现过的文本；拼接顺序、变体标记和截断位置共同保证多样性。"""
    max_attempts = 30
    candidate = ""
    for _ in range(max_attempts):
        order = pool[:]
        random.shuffle(order)
        combined = _extend_copy(order, target_length)
        candidate = _natural_trim(combined, target_length)
        text = _apply_variant(candidate, lang_code, variant_index)
        if text not in seen_texts:
            return text
        variant_index += 1

    # 极端情况下（底稿池过小、目标字数过短、变体标记也用尽）仍未找到新组合，
    # 追加序号后缀兜底，确保绝不会返回完全相同的文本。
    fallback_index = variant_index
    while True:
        text = f"{candidate} #{fallback_index}"
        if text not in seen_texts:
            return text
        fallback_index += 1


def generate_by_length(lang_code, target_length, category="全部", count=1):
    mod = ALL_LANGUAGES.get(lang_code)
    if mod is None or lang_code not in LONG_COPY_LANGUAGES:
        return []

    results = []
    seen_texts = set()
    for idx in range(1, int(count) + 1):
        selected_category = _select_length_category(lang_code, category)
        if selected_category is None:
            return []

        pool = LONG_COPY[lang_code][selected_category]
        text = _build_unique_text(pool, lang_code, target_length, seen_texts, idx - 1)
        seen_texts.add(text)

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
