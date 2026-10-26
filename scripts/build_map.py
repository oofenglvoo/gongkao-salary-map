# -*- coding: utf-8 -*-
"""生成三级下钻地图：全国 -> 四川省(21市州) -> 成都市(20区县)"""
import os, json, csv

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(OUT, 'data')
ASSETS_DIR = os.path.join(OUT, 'assets')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# ============ 全国 31 省 ============
DATA = {
 '北京市': (17, 15, 20, '中', 3, 3, '普通科员到手约13万+公积金3.6万；公检法约25万'),
 '天津市': (15.5, 13, 18, '中', 3, 5, '公积金按1:1高比例缴存，全包13–18万'),
 '河北省': (9.8, 8, 12, '高', 12, 4, '11地市数据齐全，省直/石家庄约9.6万，多数市8.7–9.2万'),
 '山西省': (8.5, 7, 11, '中', 3, 3, '省直副科纯工资仅5.4万；太原市直约7–9万'),
 '内蒙古自治区': (10.5, 7, 12, '中', 5, 4, '呼和浩特一级科员实测11.1万；区直无绩效约7万；偏远盟市7–9万'),
 '辽宁省': (9.5, 6, 13, '中', 3, 3, '沈阳8年工龄约9–10万；阜新等辽西北偏低约5–6万'),
 '吉林省': (9.5, 7, 12, '高', 11, 4, '9地市+省直数据；省直副科约10万，县域7–8万'),
 '黑龙江省': (9.5, 7, 12, '中', 4, 4, '省直三级主任科员约10.7万；哈尔滨市直科员约12万'),
 '上海市': (17, 14, 19, '中', 3, 3, '转正科员到手15万，副科17万，正科22万；公积金2000–4000/月'),
 '江苏省': (19, 13, 30, '高', 13, 4, '省直/南京20万+，苏州25–30万，苏北县域仅8–11万'),
 '浙江省': (18.5, 13, 25, '高', 10, 3, '11地市数据齐全：杭甬25万，省直20万，舟山13万'),
 '安徽省': (11.5, 7, 18, '高', 17, 5, '16地市数据齐全：合肥18万，省直15万，宿州仅7万'),
 '福建省': (12, 8, 18, '中', 5, 4, '厦门15–18万，省直/南平/龙岩仅7–10万，省内差距大'),
 '江西省': (10, 7, 15, '中', 5, 4, '萍乡市直全包仅6.5万；南昌主城区四主15万'),
 '山东省': (9.5, 7, 13, '高', 12, 5, '16地市数据齐全：省直/青岛13万，济宁/泰安/滨州仅7万'),
 '河南省': (9.5, 6.5, 15, '高', 15, 5, '18地市数据齐全：郑州港区16–18万，县域6–8万，落差极大'),
 '湖北省': (11, 8, 18, '高', 17, 5, '17地市数据齐全：武汉市直24万，区直18万，荆州/黄冈仅8万'),
 '湖南省': (10, 6.5, 20, '高', 8, 4, '长沙12–20万，岳阳/株洲/郴州仅6–8万'),
 '广东省': (20, 13, 30, '中', 6, 4, '深广珠28–30万，惠州18万，粤东西北市直13–16万'),
 '广西壮族自治区': (10.5, 8, 14.5, '中', 7, 4, '区直13–14.5万，南宁12.5–14万，县直仅8–10万'),
 '海南省': (11, 8, 16, '中', 4, 4, '海口市直约11万，省直/三亚更高，东线县级市约8万'),
 '重庆市': (13, 10, 21, '中', 4, 3, '主城/区县约10–13万，市直18–21万，公检法上浮'),
 '四川省': (16, 7, 24, '高', 101, 5, '21市州+成都20区县全覆盖：成都16万（高新/天府新区20–24万），雅安/凉山/内江仅7–8万'),
 '贵州省': (12, 8, 16, '高', 18, 5, '9地州+省直数据齐全：遵义13–16万，铜仁8–10万'),
 '云南省': (10.5, 6, 16, '高', 9, 5, '省直16万，昆明9–13万，普通县仅6–9万，迪庆14–18万'),
 '西藏自治区': (15.5, 13, 20, '中', 4, 4, '高原/岗位/包干路费叠加；乡镇约16万，区直约13万'),
 '陕西省': (9.5, 6, 13, '高', 15, 5, '10地市数据齐全：西安雁塔/灞桥11–13万，咸阳/铜川仅6万'),
 '甘肃省': (8.5, 7, 11, '中', 4, 3, '省直转正约7万，兰州约8.5万，河西约7.5万'),
 '青海省': (12, 10, 18, '中', 5, 3, '西宁市区约12万；州县三类/四类地区14–16万，警监22万'),
 '宁夏回族自治区': (10.5, 8, 13, '低', 2, 3, '银川市直应发12.3万；平罗乡镇全年8.4万，样本少'),
 '新疆维吾尔自治区': (11, 7, 14, '中', 3, 3, '南疆到手8200/月、综合13.6万；喀什乡镇无绩效仅约7万'),
}
NODATA = ['台湾省', '香港特别行政区', '澳门特别行政区']
SHORT = {
 '北京市':'北京','天津市':'天津','河北省':'河北','山西省':'山西','内蒙古自治区':'内蒙古',
 '辽宁省':'辽宁','吉林省':'吉林','黑龙江省':'黑龙江','上海市':'上海','江苏省':'江苏',
 '浙江省':'浙江','安徽省':'安徽','福建省':'福建','江西省':'江西','山东省':'山东',
 '河南省':'河南','湖北省':'湖北','湖南省':'湖南','广东省':'广东','广西壮族自治区':'广西',
 '海南省':'海南','重庆市':'重庆','四川省':'四川','贵州省':'贵州','云南省':'云南',
 '西藏自治区':'西藏','陕西省':'陕西','甘肃省':'甘肃','青海省':'青海',
 '宁夏回族自治区':'宁夏','新疆维吾尔自治区':'新疆',
 '台湾省':'台湾','香港特别行政区':'香港','澳门特别行政区':'澳门',
}

# ============ 四川 21 市州 ============
CITY = [
 ('成都市','成都市', 16.0, 12.0, 24.0, '高', 20, 6, 1, '高新区20–24万；天府新区18–22万；五城区16–18万；二圈层13–16万；三圈层12–13万'),
 ('泸州市','泸州市', 11.5, 10.0, 13.0, '高', 4, 3, 2, '龙马潭/江阳市区约13万，年终绩效5–6万；县域10–12万'),
 ('宜宾市','宜宾市', 11.5, 10.0, 15.0, '高', 4, 3, 2, '三江新区/翠屏区13–15万；市直10–12万，目标奖约5–6万'),
 ('德阳市','德阳市', 11.0, 10.0, 12.0, '高', 3, 3, 2, '市直/区县10–12万，公积金缴纳规范；县级市选调年终1.6–2万'),
 ('眉山市','眉山市', 10.8, 10.0, 12.0, '高', 3, 3, 2, '市直11–12万，年终绩效4–5万；区级略低'),
 ('达州市','达州市', 10.5, 8.5, 12.0, '高', 4, 3, 2, '市直副科12万+；县级8.5–9万；乡镇略低'),
 ('绵阳市','绵阳市', 10.2, 6.0, 12.0, '高', 5, 4, 2, '市直10–12万（四主约11万）；盐亭/梓潼等县域仅约6万'),
 ('广安市','广安市', 10.2, 9.0, 11.0, '高', 4, 4, 2, '城区全包约11万，目标奖基数4.7万；选调试用期约9万'),
 ('自贡市','自贡市', 9.8, 8.0, 11.0, '高', 4, 3, 3, '市直约11万（到手8万+公积金2.3万）；县域约8万'),
 ('乐山市','乐山市', 9.5, 7.0, 10.0, '高', 4, 4, 3, '综合约10万，年到手7–8万；人才引进额外1200元/月'),
 ('阿坝藏族羌族自治州','阿坝州', 9.5, 7.0, 10.0, '中', 3, 3, 3, '目标奖约2.8万，各类补贴完善；高原补贴高'),
 ('南充市','南充市', 9.3, 7.0, 10.0, '高', 4, 3, 3, '市直二级主任科员约10万；顺庆区约8万；年到手7万+'),
 ('攀枝花市','攀枝花市', 8.8, 8.6, 9.5, '高', 3, 3, 3, '年终绩效1.6万；财政相对薄弱，数据集中在8.6–9.5万'),
 ('甘孜藏族自治州','甘孜州', 8.5, 7.0, 12.0, '中', 4, 2, 3, '县级约7万；高海拔约10万+；德格等乡镇可达12万'),
 ('遂宁市','遂宁市', 8.5, 7.5, 9.0, '高', 3, 3, 3, '市直试用期到手5500；年终绩效1.6–3.9万'),
 ('广元市','广元市', 8.5, 6.5, 9.0, '高', 4, 3, 3, '参公约8–9万，年终约3万；青川县级约9万，乡镇仅6.5万'),
 ('巴中市','巴中市', 8.2, 7.0, 9.0, '高', 3, 3, 3, '年终2.2–3万，全年到手7.5–8万；竞争最小'),
 ('资阳市','资阳市', 8.0, 7.0, 8.5, '高', 4, 3, 3, '年到手8–9万；安岳/乐至略低约7万；公安有执勤补助'),
 ('雅安市','雅安市', 7.8, 7.0, 8.0, '高', 4, 4, 4, '试用期到手3700；转正年终约0.9万；公检法较高'),
 ('凉山彝族自治州','凉山州', 7.5, 7.0, 8.0, '中', 3, 2, 4, '州级一级科员公积金双边1300、年终2万；贫困县年终仅1万'),
 ('内江市','内江市', 7.0, 6.7, 8.0, '高', 3, 3, 4, '全年约6.7万，为全省最低档；差旅补贴完善，生活成本低'),
]

# ============ 成都 20 区县 + 3 功能区 ============
# (geojson名/None, 显示名, 代表值, 下限, 上限, 置信度, 样本, 来源, 圈层, 说明)
CD = [
 ('成都高新区', '成都高新区', 21.5, 20.0, 24.0, '中', 4, 5, 1,
  '全市天花板，全包20–24万；月工资4000+绩效4700+车补650，公积金双边3200+，年终考核3万+应休未休0.5万；编制稀缺、竞争1:200+'),
 ('天府新区', '天府新区', 20.0, 18.0, 22.0, '中', 4, 5, 1,
  '与高新区同属第一档，全包18–22万；街道办/乡镇可达25万；竞争比常超30:1'),
 ('东部新区', '东部新区', 19.0, 18.0, 20.0, '中', 2, 3, 1,
  '新区政策倾斜，全包不低于19万；发展潜力大，但配套尚在完善'),
 ('锦江区', '锦江区', 16.5, 16.0, 18.0, '高', 3, 4, 2,
  '五城区之一，全包16–18万；月工资3600+绩效4100+车补650，公积金双边3000，年终绩效2.5万+应休未休0.4万'),
 ('青羊区', '青羊区', 17.0, 16.0, 18.0, '高', 4, 4, 2,
  '五城区之一，到手13万+公积金4万≈17万；省委省政协驻地，教育资源最优'),
 ('金牛区', '金牛区', 17.0, 16.5, 18.0, '高', 4, 4, 2,
  '五城区之一，到手13–14万+公积金3.5–4万≈16.5–18万；火车北站、荷花池商圈'),
 ('武侯区', '武侯区', 16.5, 16.0, 18.0, '高', 3, 4, 2,
  '五城区之一，全包16–18万；一般公共预算收入居五城区首位，财政实力强'),
 ('成华区', '成华区', 17.6, 16.0, 18.0, '高', 3, 4, 2,
  '五城区之一，到手5000/月+公积金3000+年终7–8万≈17.6万；街道办岗位收入偏高'),
 ('龙泉驿区', '龙泉驿区', 15.5, 13.0, 20.0, '中', 3, 4, 3,
  '二圈层，到手12–15万+公积金；汽车产业集中，四级科员可到20万；区局级6年工龄到手12万+'),
 ('双流区', '双流区', 17.0, 16.0, 20.0, '中', 3, 4, 3,
  '二圈层最优之一，全包16–20万；空港经济+高校资源，二圈层中竞争最激烈'),
 ('新都区', '新都区', 16.0, 14.0, 19.0, '中', 3, 4, 3,
  '二圈层，硕士打卡5000+公积金3500+年终9万≈19.2万；也有口径约14万，区间跨度大'),
 ('温江区', '温江区', 15.0, 14.0, 16.0, '中', 2, 3, 3,
  '二圈层，全包约15万；生态环境好，生活成本低于主城'),
 ('郫都区', '郫都区', 13.5, 11.0, 15.0, '中', 4, 4, 3,
  '二圈层偏低，全包11–15万；到手13万左右，税务口约15万；高校集中'),
 ('新津区', '新津区', 14.0, 13.0, 15.0, '中', 2, 3, 3,
  '二圈层（2020撤县设区），全包约14万；花舞人间、天府农博园'),
 ('青白江区', '青白江区', 13.0, 12.5, 14.0, '中', 2, 3, 4,
  '三圈层，全包约13万；中欧班列（成都）始发地，铁路港带来一定财政支撑'),
 ('彭州市', '彭州市', 13.0, 12.5, 13.5, '中', 2, 3, 4,
  '三圈层，全包约13万；年终奖约5万起；百强县，化工新材料产业强'),
 ('金堂县', '金堂县', 13.0, 12.5, 13.5, '中', 2, 3, 4,
  '三圈层，全包约13万；基层补贴较多，部分乡镇9–12万'),
 ('都江堰市', '都江堰市', 12.8, 12.0, 13.5, '中', 2, 3, 4,
  '三圈层（四档），全包约12.8万；旅游业主导，财政季节性明显'),
 ('崇州市', '崇州市', 12.8, 12.0, 13.5, '中', 2, 3, 4,
  '三圈层（四档），全包约12.8万；家具产业+农业，生活成本低'),
 ('邛崃市', '邛崃市', 12.5, 12.0, 13.0, '低', 2, 2, 4,
  '三圈层（四档），全包约12.5万；样本较少，以2025汇总口径估算'),
 ('大邑县', '大邑县', 12.5, 12.0, 13.0, '低', 2, 2, 4,
  '三圈层（四档），全包约12.5万；西岭雪山、安仁古镇；样本较少'),
 ('简阳市', '简阳市', 12.3, 11.5, 13.0, '低', 3, 3, 5,
  '三圈层（五档），全包约12.3万；天府国际机场所在地，事业编约10万；近年增长快'),
 ('蒲江县', '蒲江县', 12.0, 11.5, 13.0, '低', 2, 2, 5,
  '三圈层（五档），全包约12万，为全市最低档；竞争最小，部分乡镇达线即进面'),
]
# geojson 名称映射（功能区无独立行政区划，不在地图上）
CD_GEO = {c[1]: c[0] for c in CD if c[0] is not None}
CD_FUNC = ['成都高新区', '天府新区', '东部新区']

# ============ 成都明细 ============
CD_DETAIL = [
 ('成都高新区','功能区','二级主任科员','4000','3200','3+应休未休0.5','','19-24','有墨/搜狐/金榜','2025'),
 ('成都高新区','功能区','科员(试用期)','','','','17','20','鸿途/知乎','2022'),
 ('成都高新区','功能区','一级科员','','','','','20+','有墨个案','2025'),
 ('天府新区','功能区','二级主任科员','4000','3200','3+应休未休0.5','','18-22','有墨/搜狐','2025'),
 ('天府新区','功能区','科员','','','9+','17-18','20','搜狐/有墨个案','2022'),
 ('东部新区','功能区','二级主任科员','4000','3200','3+应休未休0.5','','18-20','有墨/搜狐','2025'),
 ('锦江区','五城区','二级主任科员','3600','3000','2.5+应休未休0.4','','16-18','有墨/搜狐','2025'),
 ('青羊区','五城区','一级科员','','','','13','17','有墨/鸿途','2025'),
 ('金牛区','五城区','一级科员','','','','13','16.5','有墨个案','2025'),
 ('金牛区','五城区','一级科员','','','','14','18','鸿途/知乎','2022'),
 ('武侯区','五城区','二级主任科员','3600','3000','2.5+应休未休0.4','','16-18','有墨/搜狐','2025'),
 ('成华区','五城区','街道办科员','5000','3000','7-8','14','17.6','有墨/鸿途','2025'),
 ('龙泉驿区','二圈层','四级科员','','','','15','20','有墨个案','2025'),
 ('龙泉驿区','二圈层','区局级(6年)','','1600','','12+','','鸿途/知乎','2022'),
 ('双流区','二圈层','一级科员','','','','','16-20','有墨/搜狐','2025'),
 ('双流区','二圈层','一级科员','','','','','16','有墨个案','2025'),
 ('新都区','二圈层','四级主任科员','5000','3500','9','','19','有墨/鸿途','2025'),
 ('新都区','二圈层','一级科员','','','','','14','有墨汇总','2025'),
 ('温江区','二圈层','一级科员','','','','','15','有墨个案','2025'),
 ('郫都区','二圈层','一级科员','3600','','','13','15','有墨/鸿途','2025'),
 ('郫都区','二圈层','税务','','2000+','','','15','鸿途/知乎','2022'),
 ('新津区','二圈层','一级科员','','','','','14','有墨汇总','2025'),
 ('青白江区','三圈层','二级主任科员','3000','2600','2+应休未休0.3','','13','有墨/搜狐','2025'),
 ('彭州市','三圈层','二级主任科员','3000','2600','2+应休未休0.3','','13','有墨/搜狐','2025'),
 ('金堂县','三圈层','二级主任科员','3000','2600','2+应休未休0.3','','13','有墨/搜狐','2025'),
 ('都江堰市','三圈层','二级主任科员','3000','2600','2+应休未休0.3','','12.8','有墨/搜狐','2025'),
 ('崇州市','三圈层','二级主任科员','3000','2600','2+应休未休0.3','','12.8','有墨/搜狐','2025'),
 ('邛崃市','三圈层','二级主任科员','3000','2600','2+应休未休0.3','','12.5','有墨/搜狐','2025'),
 ('大邑县','三圈层','二级主任科员','3000','2600','2+应休未休0.3','','12.5','有墨/搜狐','2025'),
 ('简阳市','三圈层','二级主任科员','3000','2600','2+应休未休0.3','','12.3','有墨/搜狐','2025'),
 ('简阳市','三圈层','事业编(研究生)','2000','2400','4+补贴2','','10','鸿途/知乎','2022'),
 ('蒲江县','三圈层','二级主任科员','3000','2600','2+应休未休0.3','','12','有墨/搜狐','2025'),
]

# ============ CSV ============
csv_path = os.path.join(DATA_DIR, '各省公务员年综合收入_参考数据.csv')
with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['省份','年综合收入_万元','区间下限','区间上限','置信度','数据点数','来源数','说明'])
    for name, (v, lo, hi, conf, n, ns, note) in DATA.items():
        w.writerow([name, v, lo, hi, conf, n, ns, note])

p1 = os.path.join(DATA_DIR, '四川21市州公务员收入_汇总.csv')
with open(p1, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['城市','年综合收入_万元','区间下限','区间上限','置信度','样本数','来源数','梯队','说明'])
    for c in CITY:
        w.writerow([c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9]])

p2 = os.path.join(DATA_DIR, '四川各地市收入明细数据点.csv')
with open(p2, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['城市','层级/区县','单位/岗位','月到手_元','双边公积金_月_元','年终绩效_万元','全年到手_万元','全年综合_万元','来源','数据年份'])
    for d in [
        ('成都市','省直','省直普通科员','5000+','2000+','3','13','15','有墨/搜狐','2024'),
        ('成都市','高新区','一级科员','4000','3200','3+应休未休0.5','','20+','有墨汇总','2025'),
        ('成都市','天府新区','一级科员','4000','3200','3+','','19+','有墨汇总','2025'),
        ('成都市','东部新区','一级科员','4000','3200','3+','','19+','有墨汇总','2025'),
        ('成都市','五城区','一级科员','3600','3000','2.5+应休未休0.4','','16-18','有墨汇总','2025'),
        ('成都市','金牛区','一级科员','','','','13','16.5','有墨个案','2025'),
        ('成都市','青羊区','一级科员','','','','13','17','有墨个案','2025'),
        ('成都市','成华区','街道办科员','','','','14','17.6','有墨/知乎','2025'),
        ('成都市','武侯区','一级科员','3600','3000','2.5','','16-18','有墨汇总','2025'),
        ('成都市','二圈层','一级科员','3200','2800','','','14','有墨汇总','2025'),
        ('成都市','温江区','一级科员','','','','','15','有墨个案','2025'),
        ('成都市','双流区','一级科员','','','','','16','有墨个案','2025'),
        ('成都市','龙泉驿区','四级科员','','','','15','20','有墨个案','2025'),
        ('成都市','新都区','四级主任科员','5000+','3500','9','','19','有墨/鸿途','2025'),
        ('成都市','郫都区','一级科员','3600','','','13','15','有墨/鸿途','2025'),
        ('成都市','三圈层','一级科员','3000','2600','','','13','有墨汇总','2025'),
        ('成都市','政法系统','一级科员','','','','22-25','','有墨个案','2025'),
        ('自贡市','市直','事业单位','3600','','','8','11','有墨个案','2025'),
        ('自贡市','市直','一级科员','3000+','','4','7.8','11+','有墨个案','2025'),
        ('自贡市','县域','公务员','6000+','','0.77-1','','8','有墨汇总','2025'),
        ('自贡市','全市','公务员','2800+','','3+','','7-8','上岸鸭','2023'),
        ('攀枝花市','市直','一级科员','4000+','','3.5-3.8','','8.6','有墨个案','2025'),
        ('攀枝花市','市直','公务员','6300','2000','1.6','','8.6','有墨汇总','2025'),
        ('攀枝花市','全市','公务员','3000-3500','2200','3.8','','9-10','上岸鸭','2023'),
        ('泸州市','龙马潭区','区级部门','3000+','2000+','6','','12','有墨个案','2025'),
        ('泸州市','县级','县级部门','3400','','6.3','10','','有墨个案','2025'),
        ('泸州市','市区','公务员','6000+','2000','','','13','有墨汇总','2025'),
        ('泸州市','县域','公务员','6000+','1800','1.2-1.5','','10-12','有墨汇总','2025'),
        ('德阳市','市直','一级科员','3000+','2000+','4+','','10','有墨个案','2025'),
        ('德阳市','市直/区县','公务员','6000','2200','','','10-12','有墨汇总','2025'),
        ('德阳市','市直','公务员(2年)','8000','','','9.6','12','搜狐','2022'),
        ('绵阳市','市直','四级主任科员','','','','11','','有墨/知乎','2025'),
        ('绵阳市','市直','事业单位','','','','','10','有墨个案','2025'),
        ('绵阳市','市直','公务员','6000','2500','','','10-12','有墨汇总','2025'),
        ('绵阳市','盐亭/梓潼','县域公务员','3500','800','','','6','有墨汇总','2025'),
        ('广元市','青川县','县级部门','','','','9','','有墨个案','2025'),
        ('广元市','乡镇','一级科员','3700','','2','6.5','','有墨个案','2025'),
        ('广元市','市直','参公','5600','1590','3','','8-9','有墨汇总','2025'),
        ('遂宁市','市直','一级科员','5000+','2000','3.9','','','有墨个案','2025'),
        ('遂宁市','市直','公务员','4000','1600','1.6','','8.6','有墨汇总','2025'),
        ('内江市','市直','一级科员','3000+','','2.4','6.7','','有墨个案','2025'),
        ('内江市','县级','公务员','3000','2000','','','6.7+','有墨汇总','2025'),
        ('乐山市','县级','一级科员','2900','','3.5','','8','有墨个案','2025'),
        ('乐山市','乡镇','公务员','4000','','3.5-4.4','','9.2','有墨个案','2025'),
        ('乐山市','市直','公务员','6600','2100','','','10','有墨汇总','2025'),
        ('南充市','顺庆区','区级公务员','3000+','','3.6','','8','有墨个案','2025'),
        ('南充市','市直','二级主任科员','7600','2600','','7+','10','有墨汇总','2025'),
        ('眉山市','市直','公务员','7000','2300','4-5','','11-12','有墨汇总','2025'),
        ('眉山市','全市','公务员','2500','','6-8','','12','搜狐','2022'),
        ('宜宾市','市直','公务员','3000+','','6','','13','有墨个案','2025'),
        ('宜宾市','翠屏区','一级科员','','','','','13','有墨个案','2025'),
        ('宜宾市','市直','公务员','6000','2500','5','','10-12','有墨汇总','2025'),
        ('广安市','城区','一级科员','','','4.7(基数)','','11','有墨个案','2025'),
        ('广安市','市直','公务员','5000','2000','','','10','有墨汇总','2025'),
        ('达州市','市直','副科','4000','1900','5+','','12','有墨个案','2025'),
        ('达州市','县级','科员','','','','8.5-9','','有墨个案','2025'),
        ('达州市','市直','公务员','5700','2000','','','12+','有墨汇总','2025'),
        ('雅安市','市级','一级科员','','','','7.5','','有墨个案','2025'),
        ('雅安市','市直','公务员(试用期)','3700','1400','0.9','','7.5-8','有墨汇总','2025'),
        ('巴中市','市直','一级科员','','','2','7.5-8','','有墨个案','2025'),
        ('巴中市','市直','公务员','4300-4400','1400','','','7.5-9','有墨汇总','2025'),
        ('资阳市','市直','一级科员','3000+','','2.5','','','有墨个案','2025'),
        ('资阳市','全市','公务员','3000+','2400','','','8','有墨汇总','2025'),
        ('阿坝藏族羌族自治州','县级','科员','','','2.3','4+','7','有墨个案','2025'),
        ('阿坝藏族羌族自治州','州级','公务员','3500','700','2.8','','9-10','有墨汇总','2025'),
        ('甘孜藏族自治州','县级','科员','','','2.3','4+','7','有墨个案','2025'),
        ('甘孜藏族自治州','德格','乡镇公务员','5000-6000','','','12','','有墨个案','2025'),
        ('凉山彝族自治州','贫困县','科员','3100','1360(双边)','1','','7','有墨个案','2025'),
        ('凉山彝族自治州','州级','一级科员','3000+','1300','2','','7.5','有墨个案','2025'),
    ]:
        w.writerow(list(d))

p3 = os.path.join(DATA_DIR, '成都各区县公务员收入_汇总.csv')
with open(p3, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['区县/功能区','年综合收入_万元','区间下限','区间上限','置信度','样本数','来源数','圈层','说明'])
    for c in CD:
        w.writerow([c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9]])

p4 = os.path.join(DATA_DIR, '成都各区县收入明细数据点.csv')
with open(p4, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['区县/功能区','圈层','单位/岗位','月到手_元','双边公积金_月_元','年终绩效_万元','全年到手_万元','全年综合_万元','来源','数据年份'])
    for d in CD_DETAIL:
        w.writerow(list(d))
print('CSV ok')

# ============ JSON ============
nat = [{'name': k, 'gname': SHORT[k], 'value': v[0], 'lo': v[1], 'hi': v[2],
        'conf': v[3], 'n': v[4], 'ns': v[5], 'note': v[6]} for k, v in DATA.items()]
for name in NODATA:
    nat.append({'name': name, 'gname': SHORT[name], 'value': None, 'lo': None, 'hi': None,
                'conf': '—', 'n': 0, 'ns': 0, 'note': '暂无同口径数据'})
city = [{'name': c[0], 'label': c[1], 'value': c[2], 'lo': c[3], 'hi': c[4],
         'conf': c[5], 'n': c[6], 'ns': c[7], 'tier': c[8], 'note': c[9]} for c in CITY]
cdist = [{'gname': c[0], 'label': c[1], 'value': c[2], 'lo': c[3], 'hi': c[4],
          'conf': c[5], 'n': c[6], 'ns': c[7], 'ring': c[8], 'note': c[9]} for c in CD]

echarts_js = open(os.path.join(ASSETS_DIR,'echarts.min.js'), encoding='utf-8').read().replace('</script','<\\/script')
geo = open(os.path.join(ASSETS_DIR,'china.json'), encoding='utf-8').read().replace('</script','<\\/script')
scgeo = open(os.path.join(ASSETS_DIR,'sichuan.json'), encoding='utf-8').read().replace('</script','<\\/script')
cdgeo = open(os.path.join(ASSETS_DIR,'chengdu.json'), encoding='utf-8').read().replace('</script','<\\/script')

NOTE_NAT = (
 '<b>使用说明：</b>鼠标悬停省份可看数值区间、置信度与依据；颜色越红收入越高。'
 '<b>点击「四川」可下钻到 21 个市州，再点「成都」可下钻到 20 个区县。</b><br>'
 '<b>置信度：</b><span class="tag t-high">高</span> 8 条以上地市明细且多源一致；'
 '<span class="tag t-mid">中</span> 3–7 条样本；<span class="tag t-low">低</span> 仅 1–2 条个案。<br>'
 '<b>重要提示：</b>公务员收入与「地区财政 + 单位层级 + 岗位类别 + 职级」强相关，'
 '同省内差异可达数万甚至十倍。本图取「省会/典型地市普通科员」代表值，请勿据此对单个岗位下定论。'
 '台湾、香港、澳门暂无同口径数据。<br>'
 '<b>数据来源：</b><ol>'
 '<li>畅老师公考《公务员薪资排行》（B站，2021–2022，30 省市分档）</li>'
 '<li>《2024 年全国公务员薪资待遇一览》（惠诚律所汇编）</li>'
 '<li>《全国各地公务员薪资大曝光》（搜狐，2022，知乎网友汇总）</li>'
 '<li>《超全！全国各省公务员薪资待遇（含河南 18 地市）》（知乎·河南华图）</li>'
 '<li>《广西公务员待遇概况（一级科员）》（知乎专文，2026）</li>'
 '<li>金标尺 / 华图各省专文（贵州、陕西、湖北、云南、天津、内蒙古、黑龙江等）</li>'
 '<li>《全国各省公务员工资完整梯队排行榜》（今日头条，2026）</li>'
 '<li>四川/成都专项：有墨公考 4 篇、上岸鸭、鸿途教育、搜狐、四川金标尺（2020–2025）</li>'
 '</ol>明细见同目录各 CSV 文件。'
)

NOTE_SC = (
 '<b>梯队说明：</b>'
 '<span class="tag" style="background:#7f1d1d;color:#fca5a5">一档 16万+</span>　'
 '<span class="tag" style="background:#78350f;color:#fdba74">二档 10–12万</span>　'
 '<span class="tag" style="background:#1e3a5f;color:#93c5fd">三档 8–10万</span>　'
 '<span class="tag" style="background:#334155;color:#cbd5e1">四档 7–8万</span><br>'
 '<b>核心规律：</b><ol>'
 '<li><b>成都一城独大</b>：16 万，是第二名（宜宾/泸州 11.5 万）的 1.4 倍。<b>点击成都可下钻到 20 个区县。</b></li>'
 '<li><b>第二梯队</b>：泸州、宜宾、德阳、眉山、达州、绵阳、广安，市直 10–12 万。</li>'
 '<li><b>第三梯队</b>：自贡、乐山、阿坝、南充、攀枝花、甘孜、遂宁、广元、巴中、资阳，8–10 万。</li>'
 '<li><b>第四梯队</b>：雅安、凉山、内江，7–8 万，为全省最低档。</li>'
 '<li><b>城乡落差大</b>：绵阳市直 10–12 万，盐亭/梓潼县域仅约 6 万；广元青川 9 万而乡镇仅 6.5 万。</li>'
 '<li><b>高原/边远补贴</b>：阿坝、甘孜补贴项目多，甘孜德格乡镇可达 12 万，反超多数平原市州。</li>'
 '<li><b>年终绩效是最大变量</b>：成都目标奖 4–9 万，泸州/宜宾 5–6 万，凉山贫困县仅 1 万。</li>'
 '</ol>'
 '<b>数据来源：</b>有墨公考（2025）、上岸鸭（2023）、鸿途教育＋知乎（2022）、搜狐（2022、2025）、四川金标尺（2020）。'
 '明细：<b>四川21市州公务员收入_汇总.csv</b>、<b>四川各地市收入明细数据点.csv</b>'
)

NOTE_CD = (
 '<b>圈层说明（成都官方口径）：</b><br>'
 '<b>一档/一圈层</b>：高新区、天府新区、东部新区（功能区，非行政区，图中以括号标注在对应位置）<br>'
 '<b>二档/五城区</b>：锦江、青羊、金牛、武侯、成华<br>'
 '<b>三档/二圈层</b>：龙泉驿、双流、新都、温江、郫都、新津<br>'
 '<b>四、五档/三圈层</b>：青白江、彭州、金堂、都江堰、崇州、邛崃、大邑、简阳、蒲江<br><br>'
 '<b>核心规律：</b><ol>'
 '<li><b>区县 &gt; 市级 &gt; 省级</b>：这是成都独有的倒挂现象，区县财政分成高、目标奖发得多。省直约 13–15 万，反而不如三圈层区县。</li>'
 '<li><b>高新区是天花板</b>：20–24 万，公积金双边 3500+，但编制稀缺、竞争比常超 1:200（某岗 437 人报 2 人）。</li>'
 '<li><b>主城五区高度均衡</b>：16–18 万，彼此差距不到 1 万。青羊/金牛/成华因个案数据偏高。</li>'
 '<li><b>二圈层内部差距大</b>：双流 16–20 万（最优）＞新都 14–19 万 ＞龙泉驿 13–20 万 ＞温江 15 万 ＞新津 14 万 ＞郫都 11–15 万。</li>'
 '<li><b>三圈层收敛于 12–13 万</b>：青白江/彭州/金堂 13 万，都江堰/崇州 12.8 万，邛崃/大邑 12.5 万，简阳 12.3 万，蒲江 12 万。</li>'
 '<li><b>年终奖是决定性变量</b>：一档年终 10–20 万（高新个别达 15–20 万），三档约 5 万起，五档/省直约 3 万。</li>'
 '<li><b>性价比提示</b>：三圈层（蒲江、大邑、邛崃）全包 12–12.5 万，与主城 16–18 万只差 4–6 万，但房价可能只有主城的 1/3–1/2，竞争比不足 1:30。</li>'
 '</ol>'
 '<b>重要提示：</b>以上为「一级/二级主任科员」口径，取税后全包（含公积金双边）。'
 '功能区（高新/天府/东部新区）无独立行政区划，地图上不单独着色，数值见右侧排行与下方明细表。'
 '公检法另有政法专项津贴，普遍高 2–4 万/年。<br>'
 '<b>数据来源：</b><ol>'
 '<li>《2026 四川省公务员薪资待遇汇总版》（有墨公考，2025-10，含成都区县分层）</li>'
 '<li>《速看！四川公务员真实待遇曝光》（搜狐，2025-07，成都四档明细拆解）</li>'
 '<li>《大揭秘！成都公务员各个区难度》（有墨公考，2025-10，各区薪资+竞争比）</li>'
 '<li>《四川公务员工资：你了解的比你想象的还多！》（有墨公考，2025-02，区县个案）</li>'
 '<li>《成都各地区事业单位待遇的区别》（鸿途教育，2022-03）＋知乎成都公务员待遇讨论</li>'
 '<li>《成都区县公务员收入排行！共分五个档次》（搜狐·四川金标尺，2020-11，五档划分依据）</li>'
 '</ol>明细：<b>成都各区县公务员收入_汇总.csv</b>、<b>成都各区县收入明细数据点.csv</b>'
)

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>全国公务员年综合收入参考地图（全国 → 四川 → 成都）</title>
<style>
  *{box-sizing:border-box;}
  body{margin:0;font-family:"Microsoft YaHei","PingFang SC",system-ui,sans-serif;background:#0f172a;color:#e2e8f0;}
  .wrap{max-width:1440px;margin:0 auto;padding:18px 20px 40px;}
  h1{font-size:22px;margin:6px 0 4px;font-weight:700;letter-spacing:.5px;}
  .sub{font-size:13px;color:#94a3b8;margin-bottom:14px;line-height:1.75;}
  .sub b{color:#f8d477;}
  .stats{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px;}
  .stat{background:#111c33;border:1px solid #1e2f4d;border-radius:9px;padding:8px 14px;font-size:12.5px;color:#94a3b8;}
  .stat b{color:#f8d477;font-size:16px;margin-right:4px;}
  .crumb{display:flex;align-items:center;gap:6px;margin-bottom:12px;font-size:13.5px;flex-wrap:wrap;}
  .crumb a{color:#38bdf8;text-decoration:none;cursor:pointer;padding:5px 12px;border:1px solid #24365c;border-radius:7px;background:#0b1424;transition:.15s;}
  .crumb a:hover{background:#16233d;border-color:#38bdf8;}
  .crumb .cur{color:#f8d477;font-weight:700;font-size:15px;padding:0 2px;}
  .crumb .sep{color:#475569;}
  .crumb .hint{color:#64748b;font-size:12px;margin-left:6px;}
  .main{display:flex;gap:16px;align-items:stretch;}
  .panel{background:#111c33;border:1px solid #1e2f4d;border-radius:12px;}
  #map{flex:1 1 66%;min-width:0;height:660px;}
  #rank{flex:0 0 32%;height:660px;}
  @media (max-width:980px){.main{flex-direction:column;} #map,#rank{width:100%;height:520px;flex:none;}}
  .note{margin-top:16px;font-size:12.5px;color:#94a3b8;line-height:1.95;background:#0b1424;border:1px dashed #243b5c;border-radius:10px;padding:14px 16px;}
  .note b{color:#cbd5e1;}
  .note ol{margin:6px 0 0 20px;padding:0;}
  .tag{display:inline-block;padding:1px 7px;border-radius:5px;font-size:11px;margin-left:4px;}
  .t-high{background:#14532d;color:#86efac;}
  .t-mid{background:#1e3a5f;color:#93c5fd;}
  .t-low{background:#4a2e1a;color:#fbbf24;}
</style>
</head>
<body>
<div class="wrap">
  <h1>全国公务员年综合收入参考地图</h1>
  <div class="sub">
    口径：<b>年综合收入（含月薪、年终绩效/考核奖、十三薪、公积金单位+个人部分等，税后估算）</b>，单位万元。<br>
    数据为网络公开的网友自述 / 培训机构汇总（约 2019–2026），<b>非官方统计</b>，仅作横向参考，不代表具体岗位。
  </div>

  <div class="crumb">
    <a id="btnNat">全国</a>
    <span class="sep" id="sep1" style="display:none">›</span>
    <a id="btnSC" style="display:none">四川省</a>
    <span class="sep" id="sep2" style="display:none">›</span>
    <span class="cur" id="crumbCur">全国</span>
    <span class="hint" id="crumbHint">点击地图上的「四川」可下钻查看 21 个市州</span>
  </div>

  <div class="stats" id="statsBox"></div>

  <div class="main">
    <div id="map" class="panel"></div>
    <div id="rank" class="panel"></div>
  </div>

  <div class="note" id="noteBox"></div>
</div>

<script id="geo" type="application/json">__GEO__</script>
<script id="scgeo" type="application/json">__SCGEO__</script>
<script id="cdgeo" type="application/json">__CDGEO__</script>
<script>__ECHARTS__</script>
<script>
var NAT = __DATA__;
var CITY = __CITY__;
var CD = __CDIST__;

var NOTE_NAT = __NOTE_NAT_JS__;
var NOTE_SC  = __NOTE_SC_JS__;
var NOTE_CD  = __NOTE_CD_JS__;

echarts.registerMap('china', JSON.parse(document.getElementById('geo').textContent));
echarts.registerMap('sichuan', JSON.parse(document.getElementById('scgeo').textContent));
echarts.registerMap('chengdu', JSON.parse(document.getElementById('cdgeo').textContent));

var natMap = {}, cityMap = {}, cdMap = {}, cdLabel = {};
NAT.forEach(function(d){ natMap[d.gname] = d; });
CITY.forEach(function(d){ cityMap[d.name] = d; });
CD.forEach(function(d){
  if(d.gname) cdMap[d.gname] = d;
  cdLabel[d.label] = d;
  cdLabel[d.label+'（功能区）'] = d;
});

var TIER_COLOR = {1:'#ef4444', 2:'#f59e0b', 3:'#3b82f6', 4:'#64748b', 5:'#475569'};
var CONF_COLOR = {高:'#38bdf8', 中:'#6366f1', 低:'#f59e0b'};

var LABEL_OFFSET_CD = {
  '金牛区':[-22,-30]
};
var CORE5 = ['锦江区','青羊区','金牛区','武侯区','成华区'];

var LABEL_OFFSET_SC = {
  '资阳市':[14,10], '内江市':[-2,16], '自贡市':[-16,10], '遂宁市':[-6,-12],
  '南充市':[12,-10], '广安市':[16,2], '眉山市':[-8,12], '德阳市':[4,-14],
  '绵阳市':[-10,-12], '成都市':[2,-2], '乐山市':[-12,6], '雅安市':[-14,2]
};

var chart = echarts.init(document.getElementById('map'), null, {renderer:'canvas'});
var chart2 = echarts.init(document.getElementById('rank'), null, {renderer:'canvas'});
var view = 'national';

function setCrumb(level){
  var bN=document.getElementById('btnNat'), bS=document.getElementById('btnSC');
  var s1=document.getElementById('sep1'), s2=document.getElementById('sep2');
  var cur=document.getElementById('crumbCur'), hint=document.getElementById('crumbHint');
  if(level==='national'){
    bN.style.display='none'; bS.style.display='none'; s1.style.display='none'; s2.style.display='none';
    cur.textContent='全国';
    hint.innerHTML='点击地图上的「四川」可下钻查看 21 个市州';
  } else if(level==='sichuan'){
    bN.style.display='inline-block'; bS.style.display='none'; s1.style.display='inline'; s2.style.display='none';
    cur.textContent='四川省 · 21 市州';
    hint.innerHTML='点击地图上的「成都市」可下钻查看 20 个区县';
  } else {
    bN.style.display='inline-block'; bS.style.display='inline-block'; s1.style.display='inline'; s2.style.display='inline';
    cur.textContent='成都市 · 20 区县 + 3 功能区';
    hint.innerHTML='数据来源：有墨公考 / 搜狐 / 鸿途 / 知乎 / 四川金标尺（2020–2025）';
  }
}

function setStats(html){ document.getElementById('statsBox').innerHTML = html; }
function setNote(html){ document.getElementById('noteBox').innerHTML = html; }

// ================= 全国 =================
function renderNational(){
  view='national'; setCrumb('national'); setNote(NOTE_NAT);
  setStats('<div class="stat"><b>31</b>个省级单位</div>'
    +'<div class="stat"><b>278</b>条地市/个案明细</div>'
    +'<div class="stat"><b>8</b>个独立来源交叉验证</div>'
    +'<div class="stat"><b>31</b>省达 3 源以上</div>');

  chart.setOption({
    backgroundColor:'transparent',
    title:{text:'年综合收入（万元）', left:16, top:12, textStyle:{color:'#cbd5e1', fontSize:14, fontWeight:600}},
    tooltip:{trigger:'item', backgroundColor:'rgba(15,23,42,.95)', borderColor:'#334155',
      textStyle:{color:'#e2e8f0', fontSize:13},
      formatter:function(p){
        var d=natMap[p.name];
        if(!d||d.value==null) return '<b>'+(d?d.name:p.name)+'</b><br/>暂无数据';
        var tip = d.name==='四川省' ? '<br/><span style="color:#38bdf8">▸ 点击可下钻 21 个市州</span>' : '';
        return '<b>'+d.name+'</b><br/>年综合收入：<b style="color:#f8d477">'+d.value+' 万元</b><br/>'
          +'参考区间：'+d.lo+'–'+d.hi+' 万元<br/>置信度：'+d.conf+'　样本：'+d.n+' 条 / '+d.ns+' 源<br/>'
          +'<span style="color:#94a3b8">'+d.note+'</span>'+tip;
      }},
    visualMap:{type:'continuous', min:6, max:22, left:18, bottom:26, text:['高','低'], calculable:true,
      inRange:{color:['#2b83ba','#7fc6a0','#ffffbf','#fdae61','#d7191c']},
      textStyle:{color:'#94a3b8'}, formatter:function(v){return v+'万';}},
    series:[{type:'map', map:'china', roam:true, zoom:1.18, center:[104,36],
      label:{show:true, fontSize:9, color:'#e5edf7'},
      itemStyle:{borderColor:'#0f172a', borderWidth:1, areaColor:'#334155'},
      emphasis:{label:{color:'#fff', fontSize:11, fontWeight:700}, itemStyle:{areaColor:'#f8d477'}},
      data:NAT.map(function(d){return {name:d.gname, value:d.value};})}]
  }, true);

  var sorted = NAT.filter(function(d){return d.value!=null;}).slice().sort(function(a,b){return a.value-b.value;});
  chart2.setOption({
    backgroundColor:'transparent',
    title:{text:'省份排行（万元）', left:14, top:12, textStyle:{color:'#cbd5e1', fontSize:14, fontWeight:600}},
    grid:{left:78, right:52, top:44, bottom:20},
    tooltip:{trigger:'axis', axisPointer:{type:'shadow'}, backgroundColor:'rgba(15,23,42,.95)',
      borderColor:'#334155', textStyle:{color:'#e2e8f0'},
      formatter:function(ps){var p=ps[0], d=natMap[p.name];
        return '<b>'+d.name+'</b><br/>年综合收入：<b style="color:#f8d477">'+d.value+' 万元</b><br/>'
          +'参考区间：'+d.lo+'–'+d.hi+' 万元<br/>置信度：'+d.conf+'（'+d.n+' 条 / '+d.ns+' 源）';}},
    xAxis:{type:'value', axisLabel:{color:'#64748b'}, splitLine:{lineStyle:{color:'#1e2f4d'}}},
    yAxis:{type:'category', data:sorted.map(function(d){return d.gname;}),
      axisLabel:{color:'#94a3b8', fontSize:11}, axisLine:{lineStyle:{color:'#334155'}}},
    dataZoom:[{type:'inside', yAxisIndex:0}],
    series:[{type:'bar', barWidth:'62%',
      data:sorted.map(function(d){return {value:d.value, itemStyle:{color:CONF_COLOR[d.conf]||'#6366f1'}};}),
      itemStyle:{borderRadius:[0,4,4,0]},
      label:{show:true, position:'right', color:'#cbd5e1', fontSize:10, formatter:'{c}'}}]
  }, true);
}

// ================= 四川 =================
function renderSichuan(){
  view='sichuan'; setCrumb('sichuan'); setNote(NOTE_SC);
  setStats('<div class="stat"><b>21</b>个市州全覆盖</div>'
    +'<div class="stat"><b>74</b>条明细数据点</div>'
    +'<div class="stat"><b>5</b>个独立来源</div>'
    +'<div class="stat">全省区间 <b>6.7 – 24</b> 万</div>');

  chart.setOption({
    backgroundColor:'transparent',
    title:{text:'四川省年综合收入（万元）', left:16, top:12, textStyle:{color:'#cbd5e1', fontSize:14, fontWeight:600}},
    tooltip:{trigger:'item', backgroundColor:'rgba(15,23,42,.95)', borderColor:'#334155',
      textStyle:{color:'#e2e8f0', fontSize:13},
      formatter:function(p){
        var d=cityMap[p.name];
        if(!d) return '<b>'+p.name+'</b><br/>暂无数据';
        var tip = d.name==='成都市' ? '<br/><span style="color:#38bdf8">▸ 点击可下钻 20 个区县</span>' : '';
        return '<b>'+d.label+'</b>　<span style="color:#94a3b8">第'+d.tier+'梯队</span><br/>'
          +'年综合收入：<b style="color:#f8d477">'+d.value+' 万元</b><br/>'
          +'参考区间：'+d.lo+'–'+d.hi+' 万元<br/>置信度：'+d.conf+'　样本：'+d.n+' 条 / '+d.ns+' 源<br/>'
          +'<span style="color:#94a3b8">'+d.note+'</span>'+tip;
      }},
    visualMap:{type:'continuous', min:6, max:16, left:18, bottom:26, text:['高','低'], calculable:true,
      inRange:{color:['#2b83ba','#7fc6a0','#ffffbf','#fdae61','#d7191c']},
      textStyle:{color:'#94a3b8'}, formatter:function(v){return v+'万';}},
    series:[{type:'map', map:'sichuan', roam:true, zoom:1.12,
      label:{show:true, fontSize:9.5, color:'#0f172a', fontWeight:600},
      itemStyle:{borderColor:'#0f172a', borderWidth:1.2, areaColor:'#334155'},
      emphasis:{label:{color:'#fff', fontSize:11.5, fontWeight:700}, itemStyle:{areaColor:'#f8d477'}},
      data:CITY.map(function(d){
        var o=LABEL_OFFSET_SC[d.name], it={name:d.name, value:d.value};
        if(o) it.label={offset:o};
        return it;
      })}]
  }, true);

  var sorted = CITY.slice().sort(function(a,b){return a.value-b.value;});
  var avg = CITY.reduce(function(s,d){return s+d.value;},0)/CITY.length;
  chart2.setOption({
    backgroundColor:'transparent',
    title:{text:'四川 21 市州排行（万元）', left:14, top:12, textStyle:{color:'#cbd5e1', fontSize:14, fontWeight:600}},
    grid:{left:78, right:56, top:44, bottom:20},
    tooltip:{trigger:'axis', axisPointer:{type:'shadow'}, backgroundColor:'rgba(15,23,42,.95)',
      borderColor:'#334155', textStyle:{color:'#e2e8f0'},
      formatter:function(ps){var p=ps[0], d=cityMap[p.name];
        return '<b>'+d.label+'</b>　<span style="color:#94a3b8">第'+d.tier+'梯队</span><br/>'
          +'年综合收入：<b style="color:#f8d477">'+d.value+' 万元</b><br/>'
          +'参考区间：'+d.lo+'–'+d.hi+' 万元<br/>置信度：'+d.conf+'（'+d.n+' 条 / '+d.ns+' 源）';}},
    xAxis:{type:'value', axisLabel:{color:'#64748b'}, splitLine:{lineStyle:{color:'#1e2f4d'}}},
    yAxis:{type:'category', data:sorted.map(function(d){return d.label;}),
      axisLabel:{color:'#94a3b8', fontSize:11}, axisLine:{lineStyle:{color:'#334155'}}},
    dataZoom:[{type:'inside', yAxisIndex:0}],
    series:[{type:'bar', barWidth:'62%',
      data:sorted.map(function(d){return {value:d.value, itemStyle:{color:TIER_COLOR[d.tier]}};}),
      itemStyle:{borderRadius:[0,4,4,0]},
      label:{show:true, position:'right', color:'#cbd5e1', fontSize:10,
        formatter:function(p){var d=cityMap[p.name]; return d ? (p.value+'  ('+d.lo+'–'+d.hi+')') : p.value;}},
      markLine:{silent:true, symbol:'none', lineStyle:{color:'#f8d477', type:'dashed', width:1},
        label:{color:'#f8d477', fontSize:10.5, formatter:'均值 '+avg.toFixed(1)+'万'},
        data:[{xAxis:avg}]}}]
  }, true);
}

// ================= 成都 =================
function renderChengdu(){
  view='chengdu'; setCrumb('chengdu'); setNote(NOTE_CD);
  setStats('<div class="stat"><b>20</b>个区县 + <b>3</b>个功能区</div>'
    +'<div class="stat"><b>' + __NCD__ + '</b>条明细数据点</div>'
    +'<div class="stat"><b>6</b>个独立来源</div>'
    +'<div class="stat">全市区间 <b>12 – 24</b> 万</div>');

  var mapData = CD.filter(function(d){return d.gname;})
    .map(function(d){return {name:d.gname, value:d.value};});

  chart.setOption({
    backgroundColor:'transparent',
    title:{text:'成都市年综合收入（万元）', left:16, top:12, textStyle:{color:'#cbd5e1', fontSize:14, fontWeight:600}},
    tooltip:{trigger:'item', backgroundColor:'rgba(15,23,42,.95)', borderColor:'#334155',
      textStyle:{color:'#e2e8f0', fontSize:13},
      formatter:function(p){
        var d=cdMap[p.name];
        if(!d) return '<b>'+p.name+'</b><br/>暂无数据';
        return '<b>'+d.label+'</b>　<span style="color:#94a3b8">第'+d.ring+'档</span><br/>'
          +'年综合收入：<b style="color:#f8d477">'+d.value+' 万元</b><br/>'
          +'参考区间：'+d.lo+'–'+d.hi+' 万元<br/>置信度：'+d.conf+'　样本：'+d.n+' 条 / '+d.ns+' 源<br/>'
          +'<span style="color:#94a3b8">'+d.note+'</span>';
      }},
    visualMap:{type:'continuous', min:12, max:22, left:18, bottom:26, text:['高','低'], calculable:true,
      inRange:{color:['#2b83ba','#7fc6a0','#ffffbf','#fdae61','#d7191c']},
      textStyle:{color:'#94a3b8'}, formatter:function(v){return v+'万';}},
    graphic:[
      {type:'text', right:20, bottom:18, z:100, silent:true,
       style:{text:'※ 高新区 / 天府新区 / 东部新区\n　 为功能区，无独立行政区划，\n　 不在图中着色，见右侧排行',
              fill:'#94a3b8', fontSize:11, lineHeight:16, textAlign:'right',
              backgroundColor:'rgba(11,20,36,.85)', padding:[5,9], borderRadius:5}}
    ],
    series:[{type:'map', map:'chengdu', roam:true, zoom:1.62, center:[103.93, 30.62],
      label:{show:true, fontSize:9, color:'#0f172a', fontWeight:600,
        formatter:function(p){ return p.name.replace(/(区|县|市)$/,''); }},
      labelLine:{show:true, length:4, length2:8, smooth:true,
        lineStyle:{color:'#94a3b8', width:1, type:'solid'}},
      labelLayout:{hideOverlap:false},
      itemStyle:{borderColor:'#0f172a', borderWidth:1, areaColor:'#334155'},
      emphasis:{label:{color:'#fff', fontSize:11, fontWeight:700}, itemStyle:{areaColor:'#f8d477'}},
      data:mapData.map(function(it){
        var o = LABEL_OFFSET_CD[it.name];
        if(!o) return it;
        return {name:it.name, value:it.value, label:{show:true, offset:o, fontSize:9.5}};
      })}]
  }, true);

  var sorted = CD.slice().sort(function(a,b){return a.value-b.value;});
  chart2.setOption({
    backgroundColor:'transparent',
    title:{text:'成都各区县排行（万元）', left:14, top:12, textStyle:{color:'#cbd5e1', fontSize:14, fontWeight:600}},
    grid:{left:92, right:58, top:44, bottom:20},
    tooltip:{trigger:'axis', axisPointer:{type:'shadow'}, backgroundColor:'rgba(15,23,42,.95)',
      borderColor:'#334155', textStyle:{color:'#e2e8f0'},
      formatter:function(ps){var p=ps[0], d=cdLabel[p.name];
        return '<b>'+d.label+'</b>　<span style="color:#94a3b8">第'+d.ring+'档</span><br/>'
          +'年综合收入：<b style="color:#f8d477">'+d.value+' 万元</b><br/>'
          +'参考区间：'+d.lo+'–'+d.hi+' 万元<br/>置信度：'+d.conf+'（'+d.n+' 条 / '+d.ns+' 源）<br/>'
          +'<span style="color:#94a3b8;font-size:11.5px">'+d.note+'</span>';}},
    xAxis:{type:'value', axisLabel:{color:'#64748b'}, splitLine:{lineStyle:{color:'#1e2f4d'}}},
    yAxis:{type:'category',
      data:sorted.map(function(d){ return d.gname ? d.label : d.label+'（功能区）'; }),
      axisLabel:{color:'#94a3b8', fontSize:10.5}, axisLine:{lineStyle:{color:'#334155'}}},
    dataZoom:[{type:'inside', yAxisIndex:0}],
    series:[{type:'bar', barWidth:'62%',
      data:sorted.map(function(d){return {value:d.value, itemStyle:{color:TIER_COLOR[d.ring]}};}),
      itemStyle:{borderRadius:[0,4,4,0]},
      label:{show:true, position:'right', color:'#cbd5e1', fontSize:10,
        formatter:function(p){var d=cdLabel[p.name]; return d ? (p.value+'  ('+d.lo+'–'+d.hi+')') : p.value;}}}]
  }, true);
}

// ---------- 事件 ----------
chart.on('click', function(p){
  if(view==='national' && p.name==='四川') renderSichuan();
  else if(view==='sichuan' && p.name==='成都市') renderChengdu();
});
document.getElementById('btnNat').addEventListener('click', function(){ renderNational(); });
document.getElementById('btnSC').addEventListener('click', function(){ renderSichuan(); });

renderNational();
window.addEventListener('resize', function(){ chart.resize(); chart2.resize(); });
</script>
</body>
</html>'''

html = (html.replace('__GEO__', geo).replace('__SCGEO__', scgeo).replace('__CDGEO__', cdgeo)
            .replace('__ECHARTS__', echarts_js)
            .replace('__DATA__', json.dumps(nat, ensure_ascii=False))
            .replace('__CITY__', json.dumps(city, ensure_ascii=False))
            .replace('__CDIST__', json.dumps(cdist, ensure_ascii=False))
            .replace('__NOTE_NAT_JS__', json.dumps(NOTE_NAT, ensure_ascii=False))
            .replace('__NOTE_SC_JS__', json.dumps(NOTE_SC, ensure_ascii=False))
            .replace('__NOTE_CD_JS__', json.dumps(NOTE_CD, ensure_ascii=False))
            .replace('__NCD__', str(len(CD_DETAIL))))

out = os.path.join(OUT, '全国公务员收入地图.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML:', out, round(os.path.getsize(out)/1024/1024, 2), 'MB')
print('provinces:', len(DATA), '| sc cities:', len(CITY), '| cd districts:', len(CD), '| cd detail:', len(CD_DETAIL))
