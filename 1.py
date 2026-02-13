import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import random
import os
import re

# --- الإعدادات ---
# الرابط المحدث للمجلد الأول
BASE_URL = "https://ar-no.com/novel/%d8%ac%d9%8a%d9%86%d8%a7%d8%aa-%d8%a7%d9%84%d8%a5%d9%84%d9%87-%d8%a7%d9%84%d8%ae%d8%a7%d8%b1%d9%82%d8%a9/01-1-1000/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
TXT_OUTPUT = "Super_Gene_V1.txt"
HTML_OUTPUT = "Super_Gene_V1.html"

# قائمة الفصول (سيتم عكسها للسحب من 1 إلى 160)
raw_chapters_text = """
160 - تقول امي أن الحبيبات للأشخاص المتلاعبين
159 - حقيقة
158 - نصر عظيم
157 - أقتلهم جميعا
156 - بداية اللعبة
155 - تغيير القوانين
154 - القوة الغاشمة
153 - المدمر المثير للضحك
152 - نجم
151 - إكتشاف فانغ مينغ تشيوان
150 - قبلة
149 - خصوم ضعفاء
148 - بزة حربية بيولوجية خارقة
147 - المواجهة على حافة السكين
146 - روح وحش النملة الطيفية
145 - شهية ذات حجم أولمبي
144 - هل تريدين أن تعرفي
143 - ليست تحت هذا الكأس
142 - الدعوة من لوه شيانغ يانغ
141 - موعد
140 - مقابلة جي يانران مجددا
139 - المبارزة مع مدرب
138 - خطة جي يانران
137 - البزات الحربية الثقيلة
136 - جميلة
135 - نزال غير مثير
134 - من السهل جدا هزيمتك
133 - الليلة العاشرة ونصف
132 - روح دم مقدس أخرى
131 - ملك الدود الصخري
130 - جولة قتل
129 - الثعلب الملك ذو الدم المقدس
128 - مجموعة ثعالب
127 - الفتاة التي تساوي ترخيص فئة S
126 - صحراء الشيطان
125 - من هو حبيبك
124 - مشتعل
123 - نزال يد الإله
122 - المساء الأكثر غموضا
121 - مسح
120 - حبيبتي هي جي يانران
119 - جي يانران
118 - روح وحش الملكة الجنية
117 - روح وحش قوقعة اليشم
116 - القبول
115 - جهاز غش
114 - الجائزة هي موعد غرامي
113 - غزوتي في بحر النجوم
112 - رامي
111 - ملاذ المجد
110 - الهرب
109 - المدرع ذو الحراشف
108 - صيد مخلوق دم مقدس
107 - أرينا ما لديك
106 - شخص جيد
105 - من الوحيد للملك
104 - ليس سيئا
103 - القتال بين الملك والمدعي
102 - أراك في النهائي
101 - خزي
100 - مركز المسابقة
99 - مختار مذبوح بضربة واحدة
98 - شخص مثير للإهتمام
97 - نفس الأسلوب
96 - موهبة رائعة
95 - متطور 3
94 - الرابح يأخذ كل شيئ
93 - تحمل أفضل
92 - الإنشطار الذري
91 - بطولة ملاذ الدرع الحديدي
90 - يد الإله
89 - أنا الأقوى
88 - التحمل يهم
87 - غش
86 - تدريب خاص
85 - قتل ثانية
84 - روح وحش القرد
83 - قتال دقيقة واحدة
82 - مقاتلة ليو تيان يانغ
81 - جندية منضبطة
80 - إختبار
79 - فوز واحد
78 - حجر ورقة مقص
77 - تانغ تشن ليو
76 - الملاك المقدس
75 - واحد في مائة
74 - ترخيص فئة S لقاعة القديس
73 - الحلبة القتالية
72 - الصيد بجنون
71 - تدمير العش
70 - أدنى من قط
69 - علم ملابس داخلية بيضاء
68 - رمح سمكة المنشار المتحولة
67 - سمكة منشار متحوله
66 - ملك الثعابين ذو أسنان الشبح
65 - أكاديمية الصقر الأسود
64 - فن شورى قتالي
63 - الملاك دولار
62 - نيزك ذهبي
61 - لماذا لم يتفادى
60 - شورى ذو قرن ذهبي
59 - شخص محظوظ
58 - هدية عظيمة لشخص عظيم
57 - المستنقع المظلم
56 - اللعنة علي
55 - عشر ألاف للصفعة
54 - هدية صغيرة
53 - الوحش ذو الأسنان النحاسية ذو الدم المقدس
52 - التنين ذو الأجنحة الأرجوانية
51 - روح الوحش خاصتي
50 - هجوم
49 - أسهم ضوء النجوم
48 - جهد جماعي
47 - سهم فولاذ Z
46 - تحمل
45 - ألف سهم
44 - ليس رجل بما يكفي
43 - إختلاف العمر
42 - دولار
41 - كامل الممر
40 - مركز الإختبار البدني
39 - القديس باول
38 - تابعي
37 - من مالك السيف العريض
36 - سيد رماية
35 - من يجب أن يذهب
34 - بقوس في يدي
33 - منتدى الليل القطبي
32 - طقس بين الرجال
31 - شريك تدريب مجاني
30 - بيضة فارغة
29 - طائر العاصفة
28 - طعام غالي
27 - طلب نجدة
26 - القط المتحول ثلاثي العيون
25 - تملك الشبح
24 - مهارات الهجوم المفاجئ
23 - تنين السبج
22 - بيضة مكسورة
21 - النهر تحت الأرض
20 - هي
19 - المتميزون والأرستقراطيون فقط
18 - مخلوق متحول
17 - لقاء غير متوقع
16 - عقارب الكوارتز
15 - بيع اللحم
14 - المختار
13 - بشرة اليشم
12 - من هو الحثالة؟
11 - من هو دولار؟
10 - القاتل الدموي
9 - مخلوق دم مقدس
8 - روح وحش بدائية
7 - دولار
6 - الدرع هو كل شيئ
5 - السرعوف الرشيق
4 - المنزل القديم
3 - درع الدم المقدس
2 - مسخ المؤخرات
1 - الجينات الخارقة
"""

def clean_slug(text, alt=False):
    # تنظيف العنوان ليتناسب مع رابط الموقع
    text = re.sub(r"[؟?()!.'،,]", "", text)
    if alt:
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ة', 'ه')
    text = text.strip().replace(" ", "-")
    return re.sub(r'-+', '-', text)

def get_content(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            # الموقع يستخدم "text-left" لمحتوى الرواية
            div = soup.find("div", class_="text-left")
            if div: return div.get_text(separator="\n").strip()
    except: pass
    return None

def convert_to_html():
    if not os.path.exists(TXT_OUTPUT): return
    
    print(f"\n[*] جاري تحويل {TXT_OUTPUT} إلى HTML...")
    with open(TXT_OUTPUT, "r", encoding="utf-8") as f:
        content = f.read()

    chapters = content.split("====================")
    
    html_header = f"""<!DOCTYPE html>
<html dir='rtl' lang='ar'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>جينات الإله الخارقة - المجلد الأول</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, sans-serif; 
            padding: 20px; 
            line-height: 1.8; 
            background-color: #f4f7f6; 
            color: #333; 
            max-width: 850px; 
            margin: auto; 
        }}
        .chapter-card {{ 
            background: #fff; 
            padding: 35px; 
            margin-bottom: 30px; 
            border-radius: 12px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
            white-space: pre-wrap; 
        }}
        h1 {{ 
            color: #2c3e50; 
            border-bottom: 4px solid #3498db; 
            padding-bottom: 10px; 
            font-size: 24px; 
        }}
    </style>
</head>
<body>
    <div id="main_content">
"""
    html_body = ""
    for i in range(1, len(chapters), 2):
        title = chapters[i].strip()
        body = chapters[i+1].strip() if (i+1) < len(chapters) else ""
        if title:
            html_body += f"<div class='chapter-card'><h1>{title}</h1>\n{body}</div>\n"

    with open(HTML_OUTPUT, "w", encoding="utf-8") as hf:
        hf.write(html_header + html_body + "    </div>\n</body>\n</html>")
    print(f"[V] تم إنشاء ملف الـ HTML بنجاح: {HTML_OUTPUT}")

def start():
    # استخراج قائمة الفصول ومعالجتها
    lines = [l.strip() for l in raw_chapters_text.strip().split("\n") if " - " in l]
    lines.reverse() # البدء من الفصل الأول
    
    print(f"[*] جاري سحب {len(lines)} فصلاً من جينات الإله الخارقة...")
    
    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        for line in lines:
            num, title = line.split(" - ", 1)
            print(f"[*] سحب: {line}")
            
            # محاولة الرابط الأول (الرابط الجديد)
            slug = f"{num.strip()}-{clean_slug(title)}"
            content = get_content(f"{BASE_URL}{urllib.parse.quote(slug)}/")
            
            # محاولة الرابط البديل (بدون همزات)
            if not content:
                print(f"    [!] تجربة الرابط البديل...")
                slug_alt = f"{num.strip()}-{clean_slug(title, alt=True)}"
                content = get_content(f"{BASE_URL}{urllib.parse.quote(slug_alt)}/")
            
            if content:
                f.write(f"\n\n{'='*20}\n{line}\n{'='*20}\n\n{content}")
                f.flush()
                print(f"    [V] تم السحب بنجاح")
            else:
                print(f"    [X] فشل العثور على محتوى الفصل")
            
            # تأخير بسيط لتجنب الحظر
            time.sleep(random.uniform(1, 2))

    # التحويل التلقائي
    convert_to_html()

if __name__ == "__main__":
    start()
