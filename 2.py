import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import random
import os
import re

# --- الإعدادات ---
# نفس الرابط والمجلد المستخدم في 1.py لضمان الوصول
BASE_URL = "https://ar-no.com/novel/%d8%ac%d9%8a%d9%86%d8%a7%d8%aa-%d8%a7%d9%84%d8%a5%d9%84%d9%87-%d8%a7%d9%84%d8%ae%d8%a7%d8%b1%d9%82%d8%a9/01-1-1000/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
TXT_OUTPUT = "Super_Gene_V2.txt"
HTML_OUTPUT = "Super_Gene_V2.html"

# قائمة الفصول الجديدة (161 - 320)
raw_chapters_text = """
320 - السلحفاة
319 - لقد خرج الرمح
318 - الخدمة هي ان أترككم تعيشون
317 - ليس هناك حاجة لتعرفوني
316 - أطعم حيواني الأليف
315 - ذئب الإعصار
314 - موشو
313 - عودة الإمبراطور
312 - طلقة بلا قوة
311 - يدور
310 - كما تريد
309 - تهديد
308 - من هو؟
307 - جندي في أرض الخصم
306 - التحويل
305 - روح وحش إضافة
304 - سيف الشيطان
303 - مجزرة
302 - مخلوقات عند الباب
301 - عُش أخر
300 - أيمكنك فعل ذلك
299 - عميل صعب
298 - سلاسة
297 - ثلاثة عشر قطع
296 - قتل الجميع بشفرات مزدوجة
295 - بِلا ند
294 - ليس لدي ما يكفي من الوقت
293 - بانوراما
292 - وحش غيمة مختلف
291 - جوع
290 - وتعويذة الهرقطة
289 - فنون جين مفرطة أقوى
288 - خريطة
287 - العودة
286 - الدب شبحي العيون ذو الدم المقدس
285 - ملازم اللهب
284 - البيضة
283 - المبادلة بأرواح الوحوش
282 - نفس السعر
281 - إضطراب
280 - هيكل اليشم الأبيض العظمي
279 - عش
278 - الهدف الحقيقي
277 - سعر السوق
276 - مصدومين
275 - الصيد وحيدا
274 - الدب شبحي العيون
273 - رفاق
272 - جوهر حياة
271 - الفصل 271
270 - الكريستالة الذهبية
269 - السفر مع وحش
268 - فورة اكل
267 - الأسد الذهبي
266 - بحر
265 - ليعِش الإمبراطور
264 - تُوِج
263 - عبر الجحيم
262 - الأن أو أبدا
261 - نزال
260 - يسقط الدماغ
259 - تكتيكات مدهشة
258 - الفرصة الوحيدة
257 - إرادة القتال
256 - خمس أسهم
255 - أقواس
254 - خبير رماية
253 - دعوة من الوحش
252 - جولة فاخرة لزوجين لمدة أربعة أيام
251 - إنهاء حقبة
250 - ضد الوحش
249 - إنتقام
248 - إمتيازات
247 - سهل نوعا ما
246 - روح وحش الشبيه
245 - فارس الخنفساء
244 - أخر خطة
243 - كلاهما مصاب
242 - الرمح الغازل
241 - مخلوقي دم مقدس
240 - فارس الدم المقدس
239 - مخلوق دم مقدس غريب
238 - غير عادية
237 - مطعم الملكة
236 - عمليا
235 - وحش
234 - غير قابل للإيقاف
233 - طبيعي
232 - ساغيتاريوس
231 - أي شيئ ما عدا إنجاب طفل
230 - قطع رأس في وادي الرمل
229 - واحد صعب
228 - أرجوك واصل
227 - طلب صغير
226 - تذوق الكعك
225 - تدريب
224 - خروف أسود
223 - شيطان طماع
222 - كنز متحرك
221 - بروفيسور
220 - التباهي
219 - يد شيطان
218 - أضعف مني
217 - صغير جدا
216 - إختفت
215 - مبادلة
214 - عرض هوانغ فو
213 - الملاك المقدس
212 - قتال ملاك
211 - لتبدء اللعبة
210 - المخلوق البشري
209 - دولار المستبد
208 - جزيرة الغموض
207 - فريد
206 - المعركة بين الملاك والشر
205 - إنفجار يين يانغ
204 - غضب الإمبراطور
203 - إمبراطور القبضة السوداء
202 - إحترافية
201 - عواقب وخيمة
200 - كل ما يأخذه الأمر
199 - غريب
198 - رجل لإبقائه
197 - سحر مرأة بالغة
196 - عشر سنوات من حياتي
195 - كبير
194 - أبيض وأسود ثلاثة
193 - حكم
192 - أويانغ شياوسان
191 - عرض
190 - دعوة من مجتمع الفنون القتالية
189 - الفراشة الشبح ذات الدم المقدس
188 - الفراشة الشبح
187 - كهف
186 - محمول بسهم
185 - وحش الدم المقدس ذو الريش الأسود
184 - إختبار
183 - هوانغ فو بينغ تشينغ
182 - الوحوش ذات الريش الأسود
181 - عصر جديد للبزات الحربية
180 - حبيبين
179 - نسخة محدودة
178 - مصدومين
177 - تصوير الإعلان
176 - بائسة
175 - المبارزة مع جميلة
174 - من هو النجم
173 - ستين لأربعين
172 - إنه أنت
171 - أنا حبيب جي يانران
170 - إفقاد مختار الوعي
169 - رائع فحسب
168 - لا يمكن لله إنقاذك
167 - البحث عن المشاكل
166 - رجل محظوظ
165 - الدعوة من ديغانغ
164 - حيوان دم مقدس أليف
163 - مطرقة الدم المقدس الثقيلة
162 - في الوادي
161 - تطور حيوان أليف
"""

def clean_slug(text, alt=False):
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
    <title>جينات الإله الخارقة - المجلد الثاني</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, sans-serif; padding: 20px; line-height: 1.8; background-color: #f4f7f6; color: #333; max-width: 850px; margin: auto; }}
        .chapter-card {{ background: #fff; padding: 35px; margin-bottom: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); white-space: pre-wrap; }}
        h1 {{ color: #2c3e50; border-bottom: 4px solid #3498db; padding-bottom: 10px; font-size: 24px; }}
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
    # استخراج قائمة الفصول ومعالجتها (نفس منطق 1.py)
    lines = [l.strip() for l in raw_chapters_text.strip().split("\n") if " - " in l]
    lines.reverse() 
    
    print(f"[*] جاري سحب {len(lines)} فصلاً (المجلد الثاني)...")
    
    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        for line in lines:
            num, title = line.split(" - ", 1)
            print(f"[*] سحب: {line}")
            
            slug = f"{num.strip()}-{clean_slug(title)}"
            content = get_content(f"{BASE_URL}{urllib.parse.quote(slug)}/")
            
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
            
            time.sleep(random.uniform(1, 2))

    convert_to_html()

if __name__ == "__main__":
    start()
