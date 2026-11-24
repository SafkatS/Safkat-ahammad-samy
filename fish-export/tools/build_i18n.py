"""Arabic (/ar/) and Bangla (/bn/) pages for GoodBuy Foods Global.

Called from tools/build_site.py with the build_site module as B. Returns [(lang, english_path), ...] for the sitemap.
Arabic pages target Gulf importers; Bangla pages target Bengali grocery buyers worldwide.
"""
import json
from i18n import AR_NAME, BN_NAME, AR_CAT, BN_CAT, AR_CAT_INFO, GULF_MARKETS

WA_NUM_DISPLAY = "+880 1331-352255"

L = {
 "ar": dict(dir="rtl", locale="ar_AR", name="العربية",
            fonts="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Noto+Naskh+Arabic:wght@500;600;700&family=IBM+Plex+Mono:wght@500&display=swap",
            skip="انتقل إلى المحتوى", tag="أفضل الأغذية للشراء في العالم", brand="جودباي فودز جلوبال",
            nav=[("index.html", "home", "الرئيسية"), ("products.html", "products", "المنتجات"), ("dry-food.html", "dryfood", "الأغذية الجافة"),
                 ("vegetables.html", "vegetables", "الخضروات"), ("services.html", "services", "الخدمات والرسوم"), ("contact.html", "contact", "تواصل معنا")],
            menu="القائمة", cta="اطلب عرض سعر", wa="واتساب", home="الرئيسية", faq="أسئلة شائعة", arrow="←",
            focus='<a href="index.html#markets">لمستوردي الأغذية في الخليج</a><span aria-hidden="true">·</span><a href="../bn/index.html" lang="bn">للبقالات البنغالية حول العالم</a><span aria-hidden="true">·</span><a href="dry-food.html#ramadan" class="u-hot">طلبات رمضان 2027 مفتوحة</a>',
            foot_about="نشتري لكم الأغذية والأسماك من المصدّرين المرخّصين في بنغلاديش، ونتولى فحص الجودة والمستندات وسلسلة التبريد لمستوردي الخليج والعالم.",
            foot_explore="تصفّح", foot_work="اعمل معنا", foot_office="المكتب",
            office=f'دكا، بنغلاديش<br>من الأحد إلى الخميس، 09:00–18:00 (بتوقيت دكا، UTC+6)<br>واتساب <a href="#" data-wa="مرحباً GoodBuy Foods Global" data-track="whatsapp_click" dir="ltr">{WA_NUM_DISPLAY}</a>، نرد سبعة أيام في الأسبوع',
            foot_note="معلومات المنتجات استرشادية. يُؤكَّد رمز النظام المنسق وشروط دخول السوق لكل شحنة.",
            cookie="نستخدم تحليلات داخلية لمعرفة المنتجات التي يطّلع عليها المشترون، دون أي متتبّعات إعلانية.", accept="موافق", decline="رفض",
            wa_float="تحدث معنا على واتساب", hello="مرحباً GoodBuy Foods Global، أريد عرض سعر."),
 "bn": dict(dir="ltr", locale="bn_BD", name="বাংলা",
            fonts="https://fonts.googleapis.com/css2?family=Noto+Sans+Bengali:wght@400;500;600&family=Noto+Serif+Bengali:wght@600;700&family=IBM+Plex+Mono:wght@500&display=swap",
            skip="মূল লেখায় যান", tag="বিশ্বের সেরা খাবার কেনার ঠিকানা", brand="গুডবাই ফুডস গ্লোবাল",
            nav=[("index.html", "home", "হোম"), ("../products.html", "products", "পণ্য তালিকা"), ("dry-food.html", "dryfood", "শুকনা খাবার"),
                 ("vegetables.html", "vegetables", "তাজা সবজি"), ("../services.html", "services", "সেবা ও ফি"), ("contact.html", "contact", "যোগাযোগ")],
            menu="মেনু", cta="দাম জানতে চাই", wa="হোয়াটসঅ্যাপ", home="হোম", faq="সাধারণ প্রশ্ন", arrow="→",
            focus='<a href="index.html#who">বিশ্বজুড়ে বাঙালি গ্রোসারি ক্রেতা</a><span aria-hidden="true">·</span><a href="../ar/index.html" lang="ar">উপসাগরীয় আমদানিকারক</a><span aria-hidden="true">·</span><a href="dry-food.html#ramadan" class="u-hot">রমজান ২০২৭-এর অর্ডার চলছে</a>',
            foot_about="বাংলাদেশের লাইসেন্সধারী রপ্তানিকারকদের কাছ থেকে আমরা আপনার জন্য খাবার ও মাছ কিনি, আর মান, কাগজপত্র ও কোল্ড চেইনের দায়িত্ব নিই।",
            foot_explore="দেখুন", foot_work="আমাদের সাথে কাজ", foot_office="অফিস",
            office=f'ঢাকা, বাংলাদেশ<br>রবি–বৃহস্পতিবার, সকাল ৯টা–সন্ধ্যা ৬টা (বাংলাদেশ সময়)<br>হোয়াটসঅ্যাপ <a href="#" data-wa="আসসালামু আলাইকুম GoodBuy Foods Global" data-track="whatsapp_click">{WA_NUM_DISPLAY}</a>, সপ্তাহে সাত দিন উত্তর দিই',
            foot_note="পণ্যের তথ্য নির্দেশক। প্রতিটি চালানের জন্য এইচএস কোড ও বাজারের শর্ত আলাদাভাবে নিশ্চিত করা হয়।",
            cookie="কোন পণ্য ক্রেতারা দেখছেন তা বুঝতে আমরা নিজস্ব বিশ্লেষণ ব্যবহার করি। কোনো বিজ্ঞাপন ট্র্যাকার নেই।", accept="সম্মতি দিন", decline="না",
            wa_float="হোয়াটসঅ্যাপে কথা বলুন", hello="আসসালামু আলাইকুম GoodBuy Foods Global, আমি দাম জানতে চাই।"),
}

MKT_AR = {"UK": "المملكة المتحدة", "Middle East": "الشرق الأوسط", "EU": "الاتحاد الأوروبي", "USA": "الولايات المتحدة", "Japan": "اليابان",
          "China": "الصين", "Malaysia": "ماليزيا", "Singapore": "سنغافورة", "Taiwan": "تايوان", "Hong Kong": "هونغ كونغ", "Asia": "آسيا",
          "Africa": "أفريقيا", "India": "الهند", "Nepal": "نيبال", "Sri Lanka": "سريلانكا", "Pakistan": "باكستان", "UAE": "الإمارات",
          "South Korea": "كوريا الجنوبية", "Korea": "كوريا", "Australia": "أستراليا", "Canada": "كندا", "Europe": "أوروبا", "Thailand": "تايلاند"}


def ar_markets(m):
    return "، ".join(MKT_AR.get(x.strip(), x.strip()) for x in m.split("·"))


def build(B):
    E, P, CAT, SITE, IMG, V, LOGO, WA = B.E, B.P, B.CAT, B.SITE, B.IMG, B.V, B.LOGO, B.WA
    byid = {p[0]: p for p in P}
    out = []

    # ------------------------------------------------------------------ chrome
    def head(lang, title, desc, path, ld=(), og="iced-snapper.jpg"):
        title, desc = B.fit_title(title.replace("، ", ", ")).replace(", ", "، ") if lang == "ar" else B.fit_title(title), B.fit_desc(desc)
        c = L[lang]
        graph = {"@context": "https://schema.org", "@graph": [B.ORG, *ld]}
        url = B.lang_url(lang, path)
        return f'''<!DOCTYPE html>
<html lang="{lang}" dir="{c['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">{B.hreflang_links(path)}
<meta property="og:locale" content="{c['locale']}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:site_name" content="{B.BRAND}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{V}{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5FBFD">
<link rel="alternate" type="text/plain" title="LLM summary" href="/llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{c['fonts']}">
<link rel="stylesheet" href="../assets/css/site.css">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
</head>'''

    def header(lang, page, path):
        c = L[lang]
        links = "\n      ".join(f'<a href="{h}" data-nav="{k}">{t}</a>' for h, k, t in c["nav"][1:])
        other = "bn" if lang == "ar" else "ar"
        has_other = B.has_bn(path) if other == "bn" else B.has_ar(path)
        en = "../" + ("" if path == "index.html" else path)
        en = en if en != "../" else "../index.html"
        langs = (f'<a href="{en}" lang="en" hreflang="en">English</a>'
                 + "".join(f'<a href="{"#" if l == lang else "../" + l + "/" + (path if (l == lang or has_other) else "index.html")}" lang="{l}"{" aria-current=\"true\"" if l == lang else f" hreflang=\"{l}\""}>{L[l]["name"]}</a>' for l in ("ar", "bn")))
        return f'''<body data-page="{page}">
<a class="skip" href="#main">{c['skip']}</a>
<div class="utility"><div class="wrap">
  <p class="u-focus">{c['focus']}</p>
  <nav class="langs" aria-label="Language">{langs}</nav>
</div></div>
<header class="top">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="{B.BRAND}">{LOGO}<span><span>{c['brand']}</span><small>{c['tag']}</small></span></a>
    <nav class="nav" id="nav" aria-label="Main">
      {links}
    </nav>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="nav">{c['menu']}</button>
    <a class="btn btn-primary cta-top" href="contact.html#rfq" data-track="cta_header">{c['cta']} <span class="flag" data-basket-count hidden style="background:#fff;color:var(--coral-ink)">0</span></a>
  </div>
</header>
<main id="main">'''

    def foot(lang):
        c = L[lang]
        nav = "".join(f'<li><a href="{h}">{t}</a></li>' for h, k, t in c["nav"])
        extra = ('<li><a href="import-from-bangladesh-to-saudi-arabia.html">الاستيراد إلى السعودية</a></li><li><a href="import-from-bangladesh-to-united-arab-emirates.html">الاستيراد إلى الإمارات</a></li>'
                 if lang == "ar" else '<li><a href="../bangladeshi-grocery-importers.html">Bengali grocery importers (English)</a></li>')
        return f'''</main>

<footer>
  <div class="wrap foot-grid">
    <div>
      <a class="logo" href="index.html" style="color:var(--fg)">{LOGO}<span><span>{c['brand']}</span><small>{c['tag']}</small></span></a>
      <p style="margin-top:1rem;max-width:40ch">{c['foot_about']}</p>
    </div>
    <div><h4>{c['foot_explore']}</h4><ul>{nav}{extra}</ul></div>
    <div><h4>{c['foot_work']}</h4><ul><li><a href="contact.html#rfq">{c['cta']}</a></li><li><a href="#" data-wa="{E(c['hello'])}" data-track="whatsapp_click">{c['wa']}</a></li><li><a href="#" data-mail data-track="email_click">Email</a></li><li><a href="../index.html" lang="en">English</a> · <a href="../ar/index.html" lang="ar">العربية</a> · <a href="../bn/index.html" lang="bn">বাংলা</a></li></ul></div>
    <div><h4>{c['foot_office']}</h4><p>{c['office']}</p></div>
  </div>
  <div class="foot-bottom"><div class="wrap" style="padding-block:1.25rem calc(1.25rem + env(safe-area-inset-bottom,0px))">
    <span>© <span data-year>{B.TODAY[:4]}</span> {B.BRAND}</span>
    <span>{c['foot_note']}</span>
  </div></div>
</footer>

<a class="wa-float" href="#" data-wa="{E(c['hello'])}" data-track="whatsapp_click" aria-label="{c['wa_float']}">{WA}</a>
<div class="cookie" id="cookie" hidden>
  <span>{c['cookie']}</span>
  <div><button class="btn btn-primary" id="ckYes" type="button">{c['accept']}</button><button class="btn btn-ghost" id="ckNo" type="button">{c['decline']}</button></div>
</div>
<div class="toast" id="toast" hidden></div>
<script src="../assets/js/catalog.js"></script>
<script src="../assets/js/site.js"></script>
</body>
</html>
'''

    def hero(lang, crumb, title, lede, image, extra=""):
        c = L[lang]
        return f'''  <section class="vid page-hero">
    <img class="bg" src="../{IMG}{image}-lg.jpg" alt="" aria-hidden="true" fetchpriority="high">
    <canvas class="sea" data-level="0.74" aria-hidden="true"></canvas>
    <div class="wrap">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">{c['home']}</a><span aria-hidden="true">/</span><span>{crumb}</span></nav>
      <h1>{title}</h1>
      <p class="lede">{lede}</p>{extra}
    </div>
  </section>'''

    def faq(lang, faqs, heading):
        items = "\n".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs)
        return f'''  <section id="faq">
    <div class="wrap">
      <p class="eyebrow">{L[lang]['faq']}</p>
      <h2 style="margin:.8rem 0 2rem">{heading}</h2>
      <div class="faq">{items}</div>
    </div>
  </section>'''

    def cta(lang, eyebrow, title, lede):
        c = L[lang]
        return f'''  <section class="vid center cta-band">
    <video class="bg" data-auto muted loop playsinline preload="none" poster="../{V}school-underwater.jpg" aria-hidden="true"><source src="../{V}school-underwater.mp4" type="video/mp4"></video>
    <canvas class="sea" data-level="0.8" data-rays="off" aria-hidden="true"></canvas>
    <div class="wrap">
      <p class="eyebrow">{eyebrow}</p>
      <h2>{title}</h2>
      <p class="lede">{lede}</p>
      <div class="actions">
        <a class="btn btn-primary" href="contact.html#rfq" data-track="cta_band">{c['cta']}</a>
        <a class="btn btn-wa" href="#" data-wa="{E(c['hello'])}" data-track="whatsapp_click">{WA} {c['wa']}</a>
      </div>
    </div>
  </section>'''

    def crumbs_ld(lang, name, path):
        return {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": L[lang]["home"], "item": B.lang_url(lang, "index.html")},
            {"@type": "ListItem", "position": 2, "name": name, "item": B.lang_url(lang, path)}]}

    def nm(lang, pid):
        return (AR_NAME if lang == "ar" else BN_NAME).get(pid, byid[pid][2])

    def chip(lang, pid):
        href = B.pslug(byid[pid]) if lang == "ar" else "../" + B.pslug(byid[pid])
        return f'<a class="chip" href="{href}">{E(nm(lang, pid))}</a>'

    def add_btn(lang, pid):
        t = "أضف إلى طلب السعر" if lang == "ar" else "কোটেশনে যোগ করুন"
        return f'<button class="add" type="button" data-add="{pid}" aria-pressed="false">{t}</button>'

    def prod_table(lang, ids, cols):
        head_ = "".join(f"<th>{E(h)}</th>" for h, _ in cols)
        body = "".join(f'<tr><td>{chip(lang, i).replace("class=\"chip\" ", "")}<br><small lang="en" dir="ltr">{E(byid[i][2])}</small></td>'
                       + "".join(f"<td>{E(f(byid[i]))}</td>" for _, f in cols) + f"<td>{add_btn(lang, i)}</td></tr>" for i in ids)
        first = "المنتج" if lang == "ar" else "পণ্য"
        return f'<div class="tbl"><table class="dtable prodtable"><thead><tr><th>{first}</th>{head_}<th><span class="sr">+</span></th></tr></thead><tbody>{body}</tbody></table></div>'

    def write(lang, path, html_):
        B.write(f"{lang}/{path}", html_)
        out.append((lang, path))

    # ------------------------------------------------------------------ shared copy
    PROM = {
     "ar": [("ادفعوا بعد رؤية الدفعة", "توافقون على صور الدفعة والفيديو وتقرير المختبر قبل تحويل الدفعة النهائية."),
            ("سعر واحد واضح", "سعر التصدير والشحن والتأمين ورسومنا، كلٌّ في سطر مستقل. لا عمولة نأخذها من المورّدين."),
            ("استرداد الرسوم إذا أخطأنا", "في خدمة «متكامل»، إذا لم تطابق دفعةٌ أفرجنا عنها المواصفات المتفق عليها، نعيد رسومنا كاملة لتلك الشحنة."),
            ("حاوية واحدة من عدة موردين", "سمك مجفف وأرز وتوابل ووجبات خفيفة وزيت من موردين مختلفين في حاوية واحدة، متى أمكن شحنها معاً."),
            ("بلغتكم، سبعة أيام", "العربية والإنجليزية والبنغالية. نرد على واتساب طوال الأسبوع، وعرض السعر خلال 24 ساعة عمل."),
            ("إعادة الطلب برسالة واحدة", "نحتفظ بمواصفاتكم وبطاقاتكم وآخر أسعاركم، فتصبح الطلبات المتكررة وبرامج رمضان برسالة واحدة.")],
     "bn": [("লট দেখে তারপর বাকি টাকা", "লটের ছবি, ভিডিও আর ল্যাব রিপোর্ট দেখে আপনি অনুমোদন দিলে তবেই বাকি পেমেন্ট ছাড়া হয়।"),
            ("এক দামে সব খোলাখুলি", "এফওবি দাম, জাহাজ ভাড়া, বিমা আর আমাদের ফি আলাদা লাইনে দেখানো থাকে। সরবরাহকারীর কাছ থেকে আমরা কোনো কমিশন নিই না।"),
            ("ভুল হলে ফি ফেরত", "‘কমপ্লিট’ সেবায় আমাদের ছাড়পত্র দেওয়া লট চুক্তির স্পেসিফিকেশনের সাথে না মিললে ওই চালানের পুরো ফি ফেরত দিই।"),
            ("এক কন্টেইনারে অনেক সরবরাহকারী", "শুঁটকি, চাল, মসলা, চানাচুর, তেল—আলাদা সরবরাহকারীর পণ্য এক কন্টেইনারে, যেখানে একসাথে পাঠানো যায়।"),
            ("আপনার ভাষায়, সপ্তাহে সাত দিন", "বাংলা, ইংরেজি ও আরবি। হোয়াটসঅ্যাপে সপ্তাহে সাত দিন উত্তর, কর্মদিবসে ২৪ ঘণ্টার মধ্যে দাম।"),
            ("এক মেসেজে আবার অর্ডার", "আপনার স্পেসিফিকেশন, লেবেল আর শেষ দাম আমাদের কাছে থাকে, তাই আবার অর্ডার বা রমজানের প্রোগ্রাম এক মেসেজেই।")],
    }
    RAM = {
     "ar": [("قبل 15 ديسمبر 2026", "تأكيد المنتجات والعبوات والبطاقات العربية، ثم العقد والدفعة المقدمة."),
            ("أواخر ديسمبر – أوائل يناير", "الإنتاج وفحص الجودة في خمس مراحل ونتائج المختبر، وموافقتكم على ملف الدفعة."),
            ("أوائل يناير 2027", "إبحار الحاوية من شيتاغونغ، 12–25 يوماً إلى موانئ الخليج."),
            ("أواخر يناير 2027", "التخليص والبضاعة على رفوفكم قبل رمضان.")],
     "bn": [("১৫ ডিসেম্বর ২০২৬-এর মধ্যে", "পণ্য, প্যাক ও লেবেল চূড়ান্ত করুন; চুক্তি ও অগ্রিম।"),
            ("ডিসেম্বরের শেষ – জানুয়ারির শুরু", "উৎপাদন, পাঁচ ধাপে মান পরীক্ষা আর ল্যাব রিপোর্ট; আপনার অনুমোদন।"),
            ("জানুয়ারি ২০২৭-এর শুরু", "চট্টগ্রাম থেকে জাহাজ ছাড়ে। উপসাগরীয় বন্দরে ১২–২৫ দিন, ইউরোপ-আমেরিকায় ৩০–৪৫ দিন।"),
            ("জানুয়ারি ২০২৭-এর শেষে", "উপসাগরে খালাস হয়ে রমজানের আগেই দোকানে। দূরের বাজারের জন্য নভেম্বরেই অর্ডার দিন।")],
    }

    def promises(lang, eyebrow, h2):
        cards = "".join(f'<article class="promise-card tilt3d"><span class="pc-n">{i + 1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></article>' for i, (t, d) in enumerate(PROM[lang]))
        return f'''  <section id="promise" style="padding-top:1rem">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2></div></div>
      <div class="promises">{cards}</div>
    </div>
  </section>'''

    def ramadan(lang, anchor, eyebrow, h2, lede):
        steps = "".join(f'<li class="tilt3d"><b>{E(a)}</b><span>{E(b)}</span></li>' for a, b in RAM[lang])
        return f'''  <section id="{anchor}" class="ramadan">
    <div class="wrap">
      <div class="ram-head"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2><p class="lede">{lede}</p></div>
      <ol class="ram-steps">{steps}</ol>
    </div>
  </section>'''

    DRY_IDS = ["dm", "dl", "dr", "ds", "dpf", "dan", "dcr", "nh", "ar", "rr", "mu", "ch", "kh", "se", "rf", "tu", "rc", "co", "nc", "bay", "msd", "pp", "sm", "te", "gt2", "ses",
               "bi", "rus", "sn", "nd", "len", "rm", "mo2", "jg", "hn"]
    VEG_IDS = [p[0] for p in P if p[1] == "veg"]
    SEA_VEG = {"po", "pk2", "ag", "ta", "cb"}

    # ================================================================== ARABIC
    lang = "ar"
    cube_ar = B.cube_html("../", [("dry-goods-sacks", "أغذية جافة"), ("aromatic-rice-spoon", "أرز عطري"), ("green-red-chillies", "توابل"),
                                  ("pointed-gourd-brinjal-beans", "خضروات طازجة"), ("hilsa-on-ice", "أسماك ومأكولات بحرية"), ("packed-cartons-warehouse", "معبّأ للتصدير")],
                          "اسحب للتدوير", f"جميع المنتجات ({len(P)})", "products.html")
    gulf = {m[0]: m for m in B.MARKETS}
    AR_MKT = {
     "saudi-arabia": ("المملكة العربية السعودية", "السعودية",
        ["يجب أن تكون مصانع الأسماك مدرجة في قائمة الهيئة العامة للغذاء والدواء للمنشآت البنغلاديشية المعتمدة.",
         "يسجّل المستورد المنشأة والمنتجات الغذائية لدى الهيئة (منصة غد) قبل الفسح.",
         "شهادات الحلال من جهة معتمدة لدى الهيئة مطلوبة للمنتجات ذات المكوّنات الحيوانية أو التي تحمل ادعاء الحلال.",
         "البطاقة الغذائية باللغة العربية، مع تاريخَي الإنتاج والانتهاء."],
        "14–20 يوماً إلى جدة أو الدمام", ["لم يعد المصنع مدرجاً في قائمة الهيئة", "البطاقة غير عربية أو ينقصها التاريخ", "سوء التحكم بالحرارة أثناء النقل"]),
     "united-arab-emirates": ("الإمارات العربية المتحدة", "الإمارات",
        ["تُسجَّل المنتجات وبطاقاتها لدى جهة الرقابة الغذائية في الإمارة قبل الاستيراد.",
         "شهادة الحلال مطلوبة لكثير من المنتجات.",
         "البطاقة الغذائية باللغة العربية، مع تاريخَي الإنتاج والانتهاء."],
        "14–18 يوماً إلى جبل علي، ويوم واحد جواً إلى دبي", ["عدم إكمال تسجيل البطاقة قبل الشحن", "قواعد مدة الصلاحية للمنتجات المبرّدة والمجمّدة", "غياب شهادة الحلال"]),
     "kuwait": ("الكويت", "الكويت",
        ["تسجّل الهيئة العامة للغذاء والتغذية الأغذية المستوردة وتفسحها.",
         "تُطبَّق المواصفات الخليجية، ومنها البطاقة العربية مع تاريخَي الإنتاج والانتهاء.",
         "شهادة الحلال مطلوبة للمنتجات ذات المنشأ الحيواني ويطلبها معظم المشترين للأغذية المصنّعة."],
        "18–25 يوماً إلى الشويخ أو الشعيبة عبر جبل علي أو كولومبو، ويوم واحد جواً", ["بطاقة عربية ناقصة", "مدة صلاحية متبقية قصيرة عند الوصول", "غياب شهادة الحلال"]),
     "qatar": ("قطر", "قطر",
        ["تفحص وزارة الصحة العامة الأغذية المستوردة قبل الإفراج عنها.",
         "تُطبَّق المواصفات الخليجية، ومنها البطاقة العربية مع تاريخَي الإنتاج والانتهاء.",
         "شهادة الحلال مطلوبة للمنتجات ذات المنشأ الحيواني ويطلبها معظم المشترين للأغذية المصنّعة."],
        "16–22 يوماً إلى ميناء حمد عبر جبل علي أو كولومبو، ويوم واحد جواً إلى الدوحة", ["بطاقة عربية ناقصة", "سوء التحكم بحرارة الخضروات المبرّدة", "غياب شهادة الحلال"]),
     "oman": ("سلطنة عُمان", "عُمان",
        ["يتولى مركز سلامة وجودة الغذاء الرقابة على الأغذية المستوردة.",
         "تُطبَّق المواصفات الخليجية، ومنها البطاقة العربية مع تاريخَي الإنتاج والانتهاء.",
         "شهادة الحلال مطلوبة للمنتجات ذات المنشأ الحيواني ويطلبها معظم المشترين للأغذية المصنّعة."],
        "12–18 يوماً إلى صحار أو مسقط، غالباً عبر جبل علي، ويوم واحد جواً", ["بطاقة عربية ناقصة", "بقايا المبيدات في الخضروات الطازجة", "غياب شهادة الحلال"]),
    }
    AR_DOCS = ["الشهادة الصحية أو شهادة الصحة النباتية", "شهادة الحلال عند الطلب", "شهادة المنشأ", "الفاتورة التجارية وقائمة التعبئة وبوليصة الشحن"]

    # ---------- AR home
    faqs = [("ما الأغذية البنغلاديشية الأكثر طلباً في الخليج؟", "التوابل والأسماك المجففة والأسماك المجمّدة والأرز العطري والأرز المنفوخ والمبسوط والشعيرية والبسكويت والوجبات الخفيفة والخضروات الطازجة. الإمارات أكبر مشترٍ للتوابل البنغلاديشية، تليها ماليزيا والكويت وعُمان، والشرق الأوسط هو السوق الرئيسية للسمك المجفف."),
            ("هل تتعاملون باللغة العربية؟", "نعم. نستقبل الطلبات ونرسل العروض ونراجع البطاقات العربية باللغة العربية، وكذلك عبر واتساب."),
            ("ما الحد الأدنى للطلب؟", "من 500 كغ للأغذية الجافة والخضروات بالشحن الجوي، أو حاوية مختلطة تجمع عدة منتجات وموردين. الأسماك المجمّدة عادة حاوية مبرّدة 20 قدماً."),
            ("متى أدفع؟", "عادةً دفعة مقدمة عند العقد، والدفعة النهائية بعد موافقتكم على صور الدفعة والفيديو وتقرير المختبر، أو باعتماد مستندي (L/C) عند الاطلاع."),
            ("من يسجّل المنتجات لدى الهيئة العامة للغذاء والدواء؟", "في السعودية يسجّل المستورد المنشأة والمنتجات على منصة غد قبل الفسح. نحن نجهّز لكم المواصفات ونص البطاقة والشهادات اللازمة للتسجيل.")]
    mk_cards = "".join(f'<a class="segment tilt3d" href="import-from-bangladesh-to-{s}.html"><span class="seg-flag" aria-hidden="true">{gulf[s][2]}</span><b>{AR_MKT[s][0]}</b><span>{AR_MKT[s][3]}</span><em>دليل الاستيراد {L[lang]["arrow"]}</em></a>' for s in GULF_MARKETS)
    groups = [("أغذية جافة", ["dm", "dl", "dpf", "ar", "mu", "ch", "se", "tu", "rc", "nc", "bi", "sn"], "dry-food.html"),
              ("خضروات طازجة", ["jl", "ok", "bj", "bg", "pt", "gc", "lg", "po", "cu2", "lm"], "vegetables.html"),
              ("أسماك ومأكولات بحرية", ["sp", "hl", "rb", "pc", "km", "gr", "rh", "pg", "tl", "bt", "gp", "mc"], "products.html#cat-marine")]
    gl = "".join(f'<article class="drygroup tilt3d"><h3>{t}</h3><p class="related">{"".join(chip(lang, i) for i in ids)} <a class="chip" href="{h}">الكل {L[lang]["arrow"]}</a></p></article>' for t, ids, h in groups)
    page = head(lang, "جودباي فودز جلوبال | توريد الأغذية من بنغلاديش لمستوردي الخليج",
                "شريككم في بنغلاديش لتوريد الأسماك المجففة والأرز والتوابل والوجبات الخفيفة والخضروات الطازجة والأسماك المجمدة إلى السعودية والإمارات والكويت وقطر وعُمان، مع فحص كل دفعة وبطاقة عربية وشهادة حلال. عرض السعر خلال 24 ساعة.",
                "index.html", [{"@type": "WebSite", "@id": SITE + "/ar/#web", "url": SITE + "/ar/", "name": "جودباي فودز جلوبال", "inLanguage": "ar", "publisher": {"@id": SITE + "/#org"}}, B.faq_ld(faqs)]) + header(lang, "home", "index.html") + f'''
  <section class="hero vid" style="padding:0">
    <video class="bg" data-auto autoplay muted loop playsinline preload="auto" poster="../{V}iced-snapper.jpg" aria-hidden="true"><source src="../{V}iced-snapper.mp4" type="video/mp4"></video>
    <canvas class="sea" data-level="0.7" aria-hidden="true"></canvas>
    <div class="wrap">
      <div>
        <p class="eyebrow">شريككم في بنغلاديش لتوريد الأغذية</p>
        <h1>أغذية بنغلاديش لمستوردي الخليج، <em>بجودة مفحوصة وسعر واضح</em>.</h1>
        <p class="lede">نشتري لكم الأسماك المجففة والأرز والتوابل والوجبات الخفيفة والخضروات الطازجة والأسماك المجمّدة من أفضل المصدّرين المؤهّلين في بنغلاديش، ونفحص كل دفعة ونتحقق من البطاقة العربية وشهادة الحلال قبل إغلاق الحاوية.</p>
        <form class="find" action="products.html" method="get" role="search">
          <label for="findQ">ماذا تريدون أن تشتروا؟</label>
          <div><input id="findQ" name="q" type="search" placeholder="مثال: سمك مجفف، كركم، بامية، أرز منفوخ" autocomplete="off"><button class="btn btn-primary" type="submit">بحث</button></div>
        </form>
        <div class="actions">
          <a class="btn btn-primary" href="contact.html#rfq" data-track="cta_hero">اطلب عرض سعر</a>
          <a class="btn btn-wa" href="#" data-wa="{E(L[lang]['hello'])}" data-track="whatsapp_click">{WA} واتساب</a>
        </div>
        <div class="trust-row"><span>الدفعة النهائية بعد موافقتكم على الدفعة</span><span>سعر مفصّل وواضح</span><span>العربية والإنجليزية والبنغالية</span><span>فحص الجودة في خمس مراحل</span></div>
      </div>
      {cube_ar}
    </div>
  </section>

  <section style="padding-block:3rem">
    <div class="wrap">
      <div class="statband">
        <div><b>{len(P)}</b><span>منتجاً بنغلاديشياً للتصدير في دليلنا</span><cite>أسماك وأغذية وخضروات</cite></div>
        <div><b>24 ساعة</b><span>لإرسال عرض السعر</span><cite>أيام العمل</cite></div>
        <div><b>12–25</b><span>يوماً بحراً إلى موانئ الخليج</span><cite>حسب الميناء</cite></div>
        <div><b>5</b><span>مراحل لفحص الجودة لكل دفعة</span><cite>من المادة الخام إلى التحميل</cite></div>
      </div>
    </div>
  </section>

  <section id="markets" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">أسواق الخليج</p><h2>نعرف قواعد سوقكم قبل أن نحمّل الحاوية.</h2></div>
        <p class="lede">البطاقة العربية والحلال وتسجيل المنتجات تختلف من دولة لأخرى. اختاروا سوقكم لمعرفة الموافقات والمستندات ومدة الشحن.</p></div>
      <div class="segments five">{mk_cards}</div>
      <p class="langline">البحرين: تُطبَّق المواصفات الخليجية نفسها، ومنها البطاقة العربية مع تاريخَي الإنتاج والانتهاء.</p>
    </div>
  </section>

{promises(lang, "لماذا يشتري المستوردون عبر goodbuyfoods.com", "مخاطرة أقل من الشراء المباشر، وتكلفة أقل من السفر إلى بنغلاديش.")}

{ramadan(lang, "ramadan-plan", "مخطط رمضان 2027", "يُتوقع أن يبدأ رمضان نحو 8 فبراير 2027. اطلبوا الأغذية الجافة الآن.", "يزداد الطلب على الأرز المنفوخ والمبسوط والشعيرية والوجبات الخفيفة والأرز والتوابل والسمك المجفف في الأسابيع التي تسبق رمضان والعيد. يتحدد الموعد الدقيق برؤية الهلال.")}

  <section style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">الأكثر طلباً</p><h2>ما يطلبه مستوردو الخليج من بنغلاديش.</h2></div>
        <p class="lede">أضيفوا المنتجات إلى طلب السعر من أي صفحة منتج، وننقلها معكم إلى نموذج الطلب.</p></div>
      <div class="drygroups">{gl}</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">كيف نعمل</p><h2>شريك واحد من الاستفسار حتى الوصول.</h2></div></div>
      <ol class="steps">
        <li><h3>المواصفات</h3><p>أخبرونا بالمنتج والدرجة والتعبئة والكمية والميناء. نرد بعرض سعر خلال 24 ساعة.</p></li>
        <li><h3>المطابقة</h3><p>نختار المصدّرين الذين تحمل مصانعهم الموافقات التي يتطلبها سوقكم.</p></li>
        <li><h3>العينة والعقد</h3><p>إرسال العينات، ثم الفاتورة المبدئية والدفع باعتماد مستندي أو تحويل بنكي.</p></li>
        <li><h3>الفحص</h3><p>فحص ما قبل الشحن ونتائج المختبر لكل دفعة، مع الصور والفيديو.</p></li>
        <li><h3>الشحن</h3><p>حجز الحاوية وإغلاقها في المصنع، وإرسال مستندات الشحن إليكم.</p></li>
        <li><h3>المتابعة</h3><p>نتابع الوصول ونعالج أي مطالبة جودة مع المصدّر خلال 48 ساعة.</p></li>
      </ol>
    </div>
  </section>

  <section id="chairman" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap chair">
      <figure class="chair-photo">{B.CHAIR_PHOTO.replace('src="assets/', 'src="../assets/')}</figure>
      <div>
        <p class="eyebrow">رسالة رئيس مجلس الإدارة</p>
        <blockquote>
          <p>لا ينبغي أن يضطر المستورد إلى السفر إلى بنغلاديش ليثق بما يشتريه. في جودباي فودز جلوبال نقف في صف المشتري: نفاوض على السعر من المصدر، ونفحص كل دفعة قبل شحنها، ونتحمّل مسؤولية النتيجة.</p>
          <p>هدفنا بسيط: أن تُباع كل حاوية بربح، وأن يرغب كل مشترٍ في الطلب مرة أخرى.</p>
        </blockquote>
        <p class="chair-name"><b>صفكات أحمد سامي</b><span>رئيس مجلس الإدارة، جودباي فودز جلوبال</span><span>خبير في الأعمال الدولية · ماجستير التجارة والأعمال الدولية (MITB)، جامعة دكا</span></p>
      </div>
    </div>
  </section>

{faq(lang, faqs, "أسئلة المستوردين الأولى")}

{cta(lang, "الإبحار القادم من شيتاغونغ", "جاهزون لتوريد حاويتكم القادمة؟", "أرسلوا المنتجات والتعبئة والميناء. يصلكم عرض سعر خلال 24 ساعة.")}
''' + foot(lang)
    write(lang, "index.html", page)

    # ---------- AR dry food
    def life_ar(p):
        return {"dried": "6–12 شهراً بتغليف مفرغ", "rice": "الأرز 12–18 شهراً؛ الأرز المنفوخ 4–6 أشهر", "spice": "التوابل الكاملة 12–24 شهراً؛ المطحونة 12 شهراً",
                "processed": "6–12 شهراً حسب المنتج", "sweet": "6–24 شهراً حسب المنتج"}.get(p[1], "")
    faqs = [("ما الحد الأدنى لطلب الأغذية الجافة؟", "من 500 كغ لكل منتج، أو حاوية مختلطة تجمع عدة منتجات وموردين. يمكن شحن السمك المجفف والتوابل جواً بعبوات مفرغة للطلبات التجريبية."),
            ("هل تأتي العبوات ببطاقة عربية؟", "يمكن ذلك. تشترط أسواق الخليج بطاقة عربية مع تاريخَي الإنتاج والانتهاء. نراجع نص البطاقة وفق القواعد الخليجية قبل الطباعة، وكثير من الموردين يطبعون عبوات ثنائية اللغة."),
            ("متى أطلب لرمضان 2027؟", "يُتوقع أن يبدأ رمضان نحو 8 فبراير 2027 حسب رؤية الهلال. لتكون البضاعة على الرفوف في أواخر يناير، أكّدوا الطلب قبل 15 ديسمبر 2026."),
            ("كيف تفحصون جودة السمك المجفف؟", "نفحص الرطوبة والملح وبقايا المبيدات لكل دفعة، لأن إساءة استخدام المبيدات أثناء التجفيف خطر معروف. لا تُشحن إلا الدفعات المطابقة.")]
    page = head(lang, "الأغذية الجافة من بنغلاديش بالجملة: سمك مجفف، أرز، توابل، شعيرية | GFG",
                "توريد الأغذية الجافة من بنغلاديش لمستوردي الخليج: السمك المجفف (شوتكي)، الأرز العطري، الأرز المنفوخ والمبسوط، الشعيرية، التوابل، الشاي، البسكويت والبقوليات. بطاقة عربية وفحص مخبري لكل دفعة.",
                "dry-food.html", [crumbs_ld(lang, "الأغذية الجافة", "dry-food.html"), B.faq_ld(faqs)], "../img/dry-goods-sacks-lg.jpg") + header(lang, "dryfood", "dry-food.html") + "\n" + hero(
        lang, "الأغذية الجافة", "الأغذية الجافة من بنغلاديش، لمستوردي الخليج",
        "السمك المجفف والأرز العطري والأرز المنفوخ والمبسوط والشعيرية والتوابل والشاي والبسكويت والبقوليات: ما يشتريه زبائنكم كل أسبوع، مفحوص دفعةً بدفعة ومعبّأ بالبطاقة التي يتطلبها سوقكم.", "dry-goods-sacks") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>باختصار:</b> معظم الأغذية الجافة البنغلاديشية يشتريها مستوردو الخليج والبقالات البنغالية في الخارج. الإمارات أكبر مشترٍ للتوابل البنغلاديشية، تليها ماليزيا والكويت وعُمان (<a href="https://oec.world/profile/bilateral-product/spices/reporter/bgd" rel="noopener" target="_blank">OEC</a>)، والشرق الأوسط، ولا سيما السعودية والإمارات والكويت، هو السوق الرئيسية للسمك المجفف (<a href="https://thefinancialexpress.com.bd/economy/bangladesh/how-shutki-can-be-a-mainstay-of-bangladeshs-robust-fisheries-export-sector" rel="noopener" target="_blank">The Financial Express</a>). تُشحن الأغذية الجافة في حاويات عادية، فيمكن جمع عدة منتجات وموردين في حاوية واحدة.</p>
    </div>
  </section>

{ramadan(lang, "ramadan", "رمضان 2027", "البضاعة على رفوفكم قبل رمضان.", "يُتوقع أن يبدأ رمضان نحو 8 فبراير 2027 وعيد الفطر بعده بشهر تقريباً، والموعد الدقيق برؤية الهلال. احسبوا الموعد بالرجوع من تاريخ العرض على الرفوف:")}

  <section id="mixed" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">حاوية مختلطة</p><h2>اختاروا الأصناف، ونحن نجمع الموردين.</h2></div>
        <p class="lede">أضيفوا المنتجات إلى طلب السعر. نختار أفضل مورد مؤهل لكل صنف، ونفحص كل دفعة، ونحمّلها معاً في حاوية 20 أو 40 قدماً. مدة الصلاحية المذكورة قيم نموذجية نتحقق منها لدى كل مورد.</p></div>
      {prod_table(lang, DRY_IDS, [("رمز HS", lambda p: p[5]), ("مدة الصلاحية النموذجية", life_ar)])}
      <div class="more"><a class="btn btn-primary" href="contact.html#rfq">أرسل طلب الحاوية المختلطة</a></div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <p class="eyebrow">الامتثال في الخليج</p>
      <h2 style="margin:.7rem 0 1.2rem">فسح من المرة الأولى.</h2>
      <ul class="ticks">
        <li><b>البطاقة العربية:</b> اسم المنتج والمكونات والوزن الصافي وبلد المنشأ وتاريخا الإنتاج والانتهاء، نراجعها قبل الطباعة.</li>
        <li><b>تسجيل المستورد:</b> في السعودية يسجّل المستورد المنشأة والمنتجات لدى الهيئة العامة للغذاء والدواء (منصة غد) قبل الفسح، ونجهّز لكم بيانات المنتجات المطلوبة.</li>
        <li><b>شهادات الحلال</b> للمنتجات ذات المكوّنات الحيوانية أو التي تحمل ادعاء الحلال، من جهة يقبلها سوقكم.</li>
        <li><b>فحوص مخبرية لكل دفعة:</b> بقايا المبيدات والرطوبة في السمك المجفف؛ الأفلاتوكسين وأصباغ سودان وكرومات الرصاص في التوابل؛ الرطوبة والشوائب في الأرز.</li>
      </ul>
    </div>
  </section>

{faq(lang, faqs, "الأغذية الجافة: أسئلة شائعة")}

{cta(lang, "الأغذية الجافة من بنغلاديش", "أخبرونا بالأصناف والميناء.", "أرسلوا أسماء المنتجات والعبوات والكميات. يصلكم عرض سعر واحد خلال 24 ساعة.")}
''' + foot(lang)
    write(lang, "dry-food.html", page)

    # ---------- AR vegetables
    def season_ar(p):
        return AR_CAT_INFO["veg"]["season"]
    faqs = [("كيف تحافظون على أسعار منخفضة للخضروات؟", "نشتري من مراكز التعبئة المخصّصة للتصدير دون وسطاء، ونجمع عدة خضروات في شحنة جوية واحدة، ونحجز الشحن بأفضل سعر متاح لمطاركم، ونشحن الخضروات المتينة مثل البطاطس والقرع والقلقاس والملفوف بحراً بتكلفة أقل بكثير للكيلوغرام."),
            ("كيف تقلّلون الخسائر عند الوصول؟", "تُفرز الخضروات وتُفحص في مركز التعبئة يوم التعبئة، وتُبرَّد مسبقاً عند الحاجة، وتُنقل إلى مستودع الشحن في مطار دكا مع صور لكل مرحلة. نعالج مطالبات النقص أو الجودة مع مركز التعبئة."),
            ("ما الحد الأدنى للطلب؟", "من 500 كغ للشحنة الجوية، مختلطة من عدة خضروات. الشحن البحري للخضروات المتينة يبدأ من حاوية مبرّدة 20 أو 40 قدماً."),
            ("كم تكلفة خدمة «طازج»؟", "120 دولاراً أمريكياً لكل شحنة جوية حتى 3 أطنان، أو 400 دولار شهرياً لبرنامج أسبوعي من أربع شحنات. فحوص المبيدات بتكلفة المختبر.")]
    page = head(lang, "خضروات طازجة من بنغلاديش بالشحن الجوي أسبوعياً إلى الخليج | GFG",
                "خضروات بنغلاديشية طازجة أسبوعياً بالشحن الجوي إلى السعودية والإمارات والكويت وقطر وعُمان: الملوخية، البامية، الباذنجان، القرعيات، الفاصوليا، الفلفل الأخضر والمزيد. فحص يوم التعبئة وتكلفة واضحة.",
                "vegetables.html", [crumbs_ld(lang, "الخضروات الطازجة", "vegetables.html"), B.faq_ld(faqs)], "../img/pointed-gourd-brinjal-beans-lg.jpg") + header(lang, "vegetables", "vegetables.html") + "\n" + hero(
        lang, "الخضروات الطازجة", "خضروات بنغلاديشية طازجة كل أسبوع، بأفضل سعر واصل",
        "الملوخية والبامية والباذنجان والقرعيات والفاصوليا والفلفل الأخضر والخضروات الورقية وغيرها، تُفحص في مركز التعبئة يوم التعبئة وتُشحن جواً من دكا إلى مطاركم.", "pointed-gourd-brinjal-beans") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>باختصار:</b> ننظّم شحنات جوية أسبوعية من دكا لمستوردي الخليج، وشحنات بحرية للخضروات المتينة. تدفعون سعر مركز التعبئة والشحن ورسوم فحص ثابتة، كلٌّ في سطر مستقل، فتعرفون التكلفة الواصلة للكيلوغرام قبل الطلب.</p>
      <div class="levers">
        <article class="lever tilt3d"><b>مباشرة من مراكز التعبئة</b><span>لا وسطاء بين مجموعات المزارعين ومركز التعبئة وبينكم.</span></article>
        <article class="lever tilt3d"><b>شحنات مختلطة</b><span>عدة خضروات في شحنة جوية واحدة، فتُشحن الكميات الصغيرة بأسعار المنصات الكاملة.</span></article>
        <article class="lever tilt3d"><b>البحر للأصناف المتينة</b><span>البطاطس والقرع والقلقاس والملفوف في حاويات مبرّدة، بجزء من تكلفة الشحن الجوي.</span></article>
        <article class="lever tilt3d"><b>الشراء في الموسم</b><span>خضروات الشتاء من نوفمبر إلى مارس والقرعيات من أبريل إلى أكتوبر أرخص في ذروتها.</span></article>
        <article class="lever tilt3d"><b>فحص يوم التعبئة</b><span>الفرز والطزاجة وبقايا المبيدات قبل خروج الشاحنة، فلا تدفعون ثمن شحن الهدر.</span></article>
        <article class="lever tilt3d"><b>رسوم ثابتة تغطي التكلفة</b><span>120 دولاراً للشحنة، دون نسبة مضافة على سعر الخضروات.</span></article>
      </div>
    </div>
  </section>

  <section id="calc-veg" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap cols2">
      <div>
        <p class="eyebrow">التكلفة الواصلة للكيلوغرام</p>
        <h2 style="margin:.7rem 0 1.2rem">اعرفوا هامش الربح قبل الطلب.</h2>
        <p class="lede">أدخلوا سعر مركز التعبئة والشحن الجوي وسعر البيع لديكم. تضيف الحاسبة التعبئة ورسومنا والتخليص ونسبة الفاقد، ليغطي سعر البيع كل التكاليف.</p>
        <p class="hint" style="margin-top:1rem">الأرقام أمثلة للتخطيط وليست عرض سعر. يبيّن عرضكم كل رقم لمطاركم وأسبوع الشحن.</p>
      </div>
      <form class="calc" id="vegCalc" onsubmit="return false" aria-labelledby="vegCalcTitle">
        <h3 id="vegCalcTitle">لكل شحنة جوية</h3>
        <div class="row">
          <div class="f"><label for="vKg">وزن الشحنة (كغ)</label><input id="vKg" type="number" min="100" step="100" value="1500" inputmode="numeric" dir="ltr"></div>
          <div class="f"><label for="vFob">سعر مركز التعبئة (دولار/كغ)</label><input id="vFob" type="number" min="0" step="0.05" value="0.90" inputmode="decimal" dir="ltr"></div>
          <div class="f"><label for="vAir">الشحن الجوي (دولار/كغ)</label><input id="vAir" type="number" min="0" step="0.05" value="1.40" inputmode="decimal" dir="ltr"></div>
          <div class="f"><label for="vPack">التعبئة والمناولة (دولار/كغ)</label><input id="vPack" type="number" min="0" step="0.01" value="0.15" inputmode="decimal" dir="ltr"></div>
          <div class="f"><label for="vLocal">التخليص والتوصيل (دولار)</label><input id="vLocal" type="number" min="0" step="10" value="250" inputmode="numeric" dir="ltr"></div>
          <div class="f"><label for="vShrink">نسبة الفاقد (%)</label><input id="vShrink" type="number" min="0" max="50" step="0.5" value="5" inputmode="decimal" dir="ltr"></div>
          <div class="f"><label for="vSell">سعر البيع لديكم (دولار/كغ)</label><input id="vSell" type="number" min="0" step="0.05" value="3.60" inputmode="decimal" dir="ltr"></div>
        </div>
        <div class="out" aria-live="polite">
          <div><b id="vLanded" dir="ltr">—</b><span>دولار/كغ واصل</span></div>
          <div><b id="vMargin" dir="ltr">—</b><span>هامش الربح الإجمالي</span></div>
          <div><b id="vProfit" dir="ltr">—</b><span>الربح الإجمالي للشحنة</span></div>
        </div>
        <p class="hint" style="margin-top:.8rem">تشمل رسوم خدمة «طازج» البالغة 120 دولاراً للشحنة.</p>
        <button class="btn btn-ghost" style="margin-top:.8rem" id="vegToRfq" type="button">أرسل هذه الأرقام مع طلبي</button>
      </form>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">{len(VEG_IDS)} صنفاً</p><h2>ما نشحنه ومتى.</h2></div>
        <p class="lede">أضيفوا الخضروات إلى طلب السعر. نؤكد التوفر والسعر كل خميس للأسبوع التالي.</p></div>
      {prod_table(lang, VEG_IDS, [("الشحن", lambda p: "جواً أو بحراً" if p[0] in SEA_VEG else "جواً"), ("رمز HS", lambda p: p[5])])}
      <div class="more"><a class="btn btn-primary" href="contact.html#rfq">اطلب عرضاً أسبوعياً للخضروات</a></div>
    </div>
  </section>

{faq(lang, faqs, "الخضروات الطازجة: أسئلة شائعة")}

{cta(lang, "أسبوعياً من دكا", "ابدأوا برنامج خضروات أسبوعياً.", "أخبرونا بمطاركم والأصناف والكمية الأسبوعية. نرد بسعر واصل للكيلوغرام خلال 24 ساعة.")}
''' + foot(lang)
    write(lang, "vegetables.html", page)

    # ---------- AR products
    sections = []
    for cid, title, group, intro in B.CATEGORIES:
        ids = [p[0] for p in P if p[1] == cid]
        sections.append(f'''      <section class="cat" id="cat-{cid}" data-group="{group}">
        <div class="cat-head"><h2>{AR_CAT[cid]} <span class="count">{len(ids)}</span></h2></div>
        {prod_table(lang, ids, [("رمز HS", lambda p: p[5]), ("الأسواق الرئيسية", lambda p: ar_markets(p[7]))])}
      </section>''')
    page = head(lang, f"دليل المنتجات: {len(P)} منتجاً غذائياً من بنغلاديش للتصدير | GFG",
                f"دليل {len(P)} منتجاً بنغلاديشياً للتصدير بالعربية: الأسماك المجففة والمجمدة، الأرز، التوابل، الخضروات، الفواكه والأغذية المعبأة، مع رمز النظام المنسق والأسواق الرئيسية.",
                "products.html", [crumbs_ld(lang, "المنتجات", "products.html")]) + header(lang, "products", "products.html") + "\n" + hero(
        lang, "المنتجات", f"{len(P)} منتجاً من بنغلاديش في دليل واحد",
        "ابحثوا بالاسم العربي أو الإنجليزي، وأضيفوا ما تحتاجونه إلى طلب السعر.", "dry-goods-sacks") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <div class="dir-tools"><label class="sr" for="arSearch">بحث</label><input id="arSearch" type="search" placeholder="ابحثوا: سمك مجفف، كركم، بامية…" data-table-filter></div>
      <div class="directory-ar">
{chr(10).join(sections)}
      </div>
    </div>
  </section>

{cta(lang, "دليل المنتجات", "لم تجدوا ما تبحثون عنه؟", "أرسلوا اسم المنتج والمواصفات، ونبحث لكم عن مورد مؤهل.")}
''' + foot(lang)
    write(lang, "products.html", page)

    # ---------- AR services
    AR_SVC = [("verify", "تحقّق", "التحقق من المورد", "150 دولاراً", "لكل مورد، مرة واحدة",
               ["التحقق من سجل التصدير والترخيص", "موافقة المصنع أو مركز التعبئة وإدراجه لسوقكم", "التحقق من الشهادات لدى الجهة المصدرة (الحلال، HACCP…)", "زيارة المنشأة مع تقرير مصوّر وتقييم المخاطر خلال 5 أيام عمل"]),
              ("assure", "ضمان", "فحص الجودة والامتثال لكل شحنة", "290 دولاراً", "لكل حاوية · الفحوص المخبرية وسفر المفتش خارج دكا وشيتاغونغ وخولنا بالتكلفة",
               ["مراحل الفحص الخمس من المادة الخام إلى التحميل", "فحص مخبري للدفعة لدى مختبر معتمد بالتكلفة دون زيادة", "فحص AQL وفق مواصفاتكم مع صور وفيديو", "مراجعة المستندات والإشراف على التحميل", "توافقون قبل الدفعة النهائية"]),
              ("fresh", "طازج", "الخضروات والفواكه بالشحن الجوي", "120 دولاراً", "لكل شحنة جوية حتى 3 أطنان · برنامج أسبوعي 400 دولار شهرياً (4 شحنات)",
               ["زيارة مركز التعبئة يوم التعبئة: الفرز والحجم والطزاجة", "خطة فحص بقايا المبيدات لسوقكم بتكلفة المختبر", "مراجعة شهادة الصحة النباتية والفاتورة", "فحص سلسلة التبريد حتى مطار دكا مع صور", "حجز الشحن بأفضل سعر متاح"]),
              ("complete", "متكامل", "وكيل المشتري من البداية للنهاية", "1.5% من قيمة فوب", "لكل شحنة · بحد أدنى 450 دولاراً للحاوية",
               ["كل ما في «تحقّق» و«ضمان»", "عروض متنافسة من مصانع مؤهلة والتفاوض نيابة عنكم", "إدارة العقد والمواصفات والبطاقات", "حجز الشحن وتتبعه حتى ميناءكم", "معالجة المطالبات خلال 48 ساعة", "ضمان الجودة: نعيد رسومنا كاملة إذا لم تطابق الدفعة المواصفات المتفق عليها"]),
              ("programme", "برنامج", "برنامج توريد متكرر", "من 750 دولاراً", "شهرياً · يشمل حتى 3 حاويات من خدمة «ضمان»",
               ["مسؤول جودة مخصص لحسابكم", "أولوية في الإنتاج ومصنع بديل لكل منتج", "خطة شراء موسمية ونوافذ تثبيت الأسعار", "تقرير شهري عن الجودة وأداء الموردين"])]
    cards = "".join(f'''<article class="pkg{' feat' if sid == 'complete' else ''} tilt3d" id="pkg-{sid}"><p class="eyebrow">{E(tag)}</p><h3>{E(n)}</h3><p class="fee"><b dir="ltr">{E(fee)}</b><span>{E(basis)}</span></p><ul class="ticks">{"".join(f"<li>{E(x)}</li>" for x in inc)}</ul><a class="btn btn-primary" href="contact.html?package={sid}#rfq">اختر «{E(n)}»</a></article>'''
                    for sid, n, tag, fee, basis, inc in AR_SVC)
    page = head(lang, "الخدمات والرسوم: فحص الجودة والتحقق من الموردين في بنغلاديش | GFG",
                "رسوم منشورة وواضحة: التحقق من المورد 150 دولاراً، فحص الجودة لكل حاوية 290 دولاراً، الخضروات بالشحن الجوي 120 دولاراً للشحنة، والخدمة المتكاملة 1.5% من قيمة فوب. يدفعها المشتري فقط.",
                "services.html", [crumbs_ld(lang, "الخدمات والرسوم", "services.html")]) + header(lang, "services", "services.html") + "\n" + hero(
        lang, "الخدمات والرسوم", "رسوم واضحة يدفعها المشتري فقط",
        "لا نأخذ عمولة من الموردين، لذا نعمل لمصلحتكم وحدكم. الفحوص المخبرية بتكلفتها، وسفر المفتش خارج مناطق الإنتاج الرئيسية بتكلفته.", "packed-cartons-warehouse") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <div class="pkgs">{cards}</div>
      <p class="src" style="margin-top:1.5rem">الأسعار بالدولار الأمريكي. التفاصيل الكاملة في <a href="../services.html" lang="en">الصفحة الإنجليزية</a>.</p>
    </div>
  </section>

{cta(lang, "الخدمات والرسوم", "لستم متأكدين من الباقة المناسبة؟", "أخبرونا بالمنتج والكمية، ونقترح الخدمة الأنسب لكم.")}
''' + foot(lang)
    write(lang, "services.html", page)

    # ---------- AR / BN contact
    def contact(lang):
        A = lang == "ar"
        t = (dict(title="اطلب عرض سعر | جودباي فودز جلوبال", desc="أرسلوا طلب عرض السعر للأغذية البنغلاديشية: المنتجات والتعبئة والكمية والميناء. نرد خلال 24 ساعة عمل بالعربية أو الإنجليزية.",
                  crumb="اطلب عرض سعر", h1="أخبرونا بما تحتاجون، ونرد خلال 24 ساعة", lede="بالعربية أو الإنجليزية أو البنغالية. أسرع طريقة: واتساب.",
                  products="المنتجات", addhint='<a href="products.html">أضيفوا منتجات من الدليل</a>، أو اكتبوها أدناه.', company="اسم الشركة", name="الاسم", email="البريد الإلكتروني للعمل",
                  wa="رقم واتساب", wahint="اختياري، مع رمز الدولة.", country="الدولة", port="ميناء أو مطار الوصول", porteg="مثال: جدة",
                  inc="شروط التسليم", vol="الكمية", btype="نشاطكم", pkg="الخدمة", month="موعد الشحن المطلوب", details="تفاصيل الطلب",
                  detph="المنتج والدرجة والتعبئة والبطاقة العربية والشهادات المطلوبة…", consent="أوافق على أن تحفظ جودباي فودز جلوبال هذه البيانات لإعداد عرض السعر والتواصل معي بشأنه. لا نشارك بياناتكم مع أي طرف ثالث.",
                  send="أرسل طلب السعر", quick="يستغرق أقل من دقيقة.",
                  vols=[("sample", "عينات فقط"), ("lcl", "أقل من حاوية"), ("1", "حاوية 40 قدماً واحدة"), ("2-4", "2–4 حاويات شهرياً"), ("air", "شحن جوي أسبوعي")],
                  types=["مستورد / موزع", "سلسلة متاجر", "مطاعم وتموين", "مصنّع / إعادة تعبئة", "وكيل تجاري"],
                  pkgs=[("complete", "متكامل: من البداية للنهاية"), ("assure", "ضمان: فحص لكل حاوية"), ("fresh", "طازج: خضروات بالشحن الجوي"), ("verify", "تحقّق: فحص المورد فقط"), ("programme", "برنامج: توريد متكرر"), ("advise", "لست متأكداً، انصحوني")])
             if A else
             dict(title="দাম জানতে চাই | গুডবাই ফুডস গ্লোবাল", desc="বাংলাদেশি খাবারের কোটেশনের জন্য লিখুন: পণ্য, প্যাক, পরিমাণ আর বন্দর। কর্মদিবসে ২৪ ঘণ্টার মধ্যে বাংলায় বা ইংরেজিতে উত্তর।",
                  crumb="দাম জানতে চাই", h1="কী লাগবে জানান, ২৪ ঘণ্টার মধ্যে দাম পাঠাব", lede="বাংলা, ইংরেজি বা আরবিতে লিখুন। সবচেয়ে দ্রুত: হোয়াটসঅ্যাপ।",
                  products="পণ্য", addhint='<a href="../products.html">পণ্য তালিকা থেকে যোগ করুন</a>, অথবা নিচে লিখুন।', company="প্রতিষ্ঠানের নাম", name="আপনার নাম", email="ইমেইল",
                  wa="হোয়াটসঅ্যাপ নম্বর", wahint="ঐচ্ছিক, দেশের কোডসহ।", country="দেশ", port="গন্তব্য বন্দর বা বিমানবন্দর", porteg="যেমন: লন্ডন",
                  inc="ডেলিভারি শর্ত", vol="পরিমাণ", btype="আপনি", pkg="সেবা", month="কবে চালান চান", details="বিস্তারিত",
                  detph="পণ্য, গ্রেড, প্যাক, লেবেল, প্রয়োজনীয় সার্টিফিকেট…", consent="কোটেশন তৈরি ও যোগাযোগের জন্য গুডবাই ফুডস গ্লোবাল এই তথ্য সংরক্ষণ করতে পারে—আমি সম্মত। আপনার তথ্য তৃতীয় কারও সাথে শেয়ার করা হয় না।",
                  send="কোটেশন পাঠান", quick="এক মিনিটও লাগবে না।",
                  vols=[("sample", "শুধু নমুনা"), ("lcl", "এক কন্টেইনারের কম"), ("1", "একটি ৪০ ফুট কন্টেইনার"), ("2-4", "মাসে ২–৪ কন্টেইনার"), ("air", "সাপ্তাহিক বিমানে")],
                  types=["আমদানিকারক / পাইকার", "সুপারমার্কেট / দোকান", "রেস্তোরাঁ ও ক্যাটারিং", "প্রক্রিয়াকারী / রিপ্যাকার", "ট্রেডিং এজেন্ট"],
                  pkgs=[("complete", "কমপ্লিট: শুরু থেকে শেষ"), ("assure", "অ্যাশিওর: প্রতি কন্টেইনারে মান পরীক্ষা"), ("fresh", "ফ্রেশ: বিমানে তাজা সবজি"), ("verify", "ভেরিফাই: শুধু সরবরাহকারী যাচাই"), ("programme", "প্রোগ্রাম: নিয়মিত সরবরাহ"), ("advise", "নিশ্চিত নই, পরামর্শ দিন")]))
        opts = lambda xs: "".join(f'<option value="{v}">{E(x)}</option>' for v, x in xs)
        page = head(lang, t["title"], t["desc"], "contact.html", [crumbs_ld(lang, t["crumb"], "contact.html")]) + header(lang, "contact", "contact.html") + "\n" + hero(
            lang, t["crumb"], t["h1"], t["lede"], "packed-cartons-warehouse",
            f'<div class="actions" style="margin-top:1.2rem"><a class="btn btn-wa" href="#" data-wa="{E(L[lang]["hello"])}" data-track="whatsapp_click">{WA} {L[lang]["wa"]} <span dir="ltr">{WA_NUM_DISPLAY}</span></a></div>') + f'''

  <section id="rfq" style="padding-top:1.5rem">
    <div class="wrap">
      <form class="rfq-form" id="rfqForm" novalidate>
        <div class="f full"><label>{t['products']}</label><div class="basket" id="basket" aria-live="polite"></div><span class="hint">{t['addhint']}</span></div>
        <div class="f"><label for="company">{t['company']}</label><input id="company" name="company" required autocomplete="organization"></div>
        <div class="f"><label for="name">{t['name']}</label><input id="name" name="name" required autocomplete="name"></div>
        <div class="f"><label for="email">{t['email']}</label><input id="email" name="email" type="email" required autocomplete="email" dir="ltr"></div>
        <div class="f"><label for="whatsapp">{t['wa']}</label><input id="whatsapp" name="whatsapp" type="tel" placeholder="+966 5x xxx xxxx" autocomplete="tel" dir="ltr"><span class="hint">{t['wahint']}</span></div>
        <div class="f"><label for="country">{t['country']}</label><input id="country" name="country" required autocomplete="country-name"></div>
        <div class="f"><label for="port">{t['port']}</label><input id="port" name="port" placeholder="{t['porteg']}"></div>
        <div class="f"><label for="incoterm">{t['inc']}</label><select id="incoterm" name="incoterm"><option>CFR</option><option>CIF</option><option>FOB Chattogram</option><option>CPT / CIP (air)</option><option>Not sure yet</option></select></div>
        <div class="f"><label for="volume">{t['vol']}</label><select id="volume" name="volume">{opts(t['vols'])}</select></div>
        <div class="f"><label for="buyerType">{t['btype']}</label><select id="buyerType" name="buyerType">{"".join(f"<option>{E(x)}</option>" for x in t['types'])}</select></div>
        <div class="f"><label for="servicePackage">{t['pkg']}</label><select id="servicePackage" name="servicePackage">{opts(t['pkgs'])}</select></div>
        <div class="f"><label for="shipMonth">{t['month']}</label><input id="shipMonth" name="shipMonth" type="month" dir="ltr"></div>
        <div class="f full"><label for="details">{t['details']}</label><textarea id="details" name="details" placeholder="{t['detph']}"></textarea></div>
        <label class="consent full" for="consent"><input type="checkbox" id="consent" name="consent" required> {t['consent']}</label>
        <input type="text" name="website" id="website" tabindex="-1" autocomplete="off" class="sr" aria-hidden="true">
        <div class="full" style="display:flex;gap:.75rem;flex-wrap:wrap;align-items:center"><button class="btn btn-primary" type="submit" id="rfqSubmit">{t['send']}</button><span class="hint" style="margin:0">{t['quick']}</span></div>
        <div class="status" id="rfqStatus" role="status" hidden></div>
      </form>
    </div>
  </section>
''' + foot(lang)
        write(lang, "contact.html", page)
    contact("ar")

    # ---------- AR Gulf market guides
    for s in GULF_MARKETS:
        mname, short, rules, transit, risks = AR_MKT[s]
        fn = f"import-from-bangladesh-to-{s}.html"
        ids = gulf[s][7]
        faqs = [(f"ما الموافقات المطلوبة لاستيراد الأغذية من بنغلاديش إلى {short}؟", rules[0]),
                (f"كم تستغرق الشحنة من بنغلاديش إلى {short}؟", f"عادةً {transit}."),
                (f"ما المستندات المطلوبة لاستيراد الأغذية من بنغلاديش إلى {short}؟", "، ".join(AR_DOCS) + ".")]
        page = head(lang, f"استيراد الأغذية من بنغلاديش إلى {short}: المتطلبات والمستندات | GFG",
                    f"دليل استيراد الأغذية والأسماك من بنغلاديش إلى {mname}: الموافقات، البطاقة العربية، الحلال، المستندات ومدة الشحن وأسباب رفض الشحنات، مع موردين موثّقين.",
                    fn, [crumbs_ld(lang, f"الاستيراد إلى {short}", fn), B.faq_ld(faqs)]) + header(lang, "markets", fn) + "\n" + hero(
            lang, f"دليل الاستيراد · {short}", f"استيراد الأغذية من بنغلاديش إلى {mname}",
            "الموافقات والمستندات والفحوص التي تحتاجها شحنتكم، وكيف نتأكد من استيفائها قبل التحميل.", "grain-sacks-market") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap cols2">
      <div>
        <p class="answer"><b>باختصار:</b> {E(rules[0])} مدة الشحن: {E(transit)}.</p>
        <h2 style="font-size:1.6rem;margin:2rem 0 1rem">الموافقات والقواعد</h2>
        <ul class="ticks">{"".join(f"<li>{E(r)}</li>" for r in rules)}</ul>
        <h2 style="font-size:1.6rem;margin:2rem 0 1rem">الرسوم الجمركية</h2>
        <p>تعتمد الرسوم على رمز النظام المنسق وفق التعرفة الجمركية الخليجية الموحدة. أكّدوها مع مخلّصكم الجمركي.</p>
        <p class="src">القواعد والتعرفة تتغير. هذا الدليل نقطة بداية وليس استشارة قانونية أو جمركية. آخر تحديث <time datetime="{B.TODAY}">{B.TODAY}</time>.</p>
      </div>
      <div>
        <h2 style="font-size:1.6rem;margin:0 0 1rem">المستندات</h2>
        <ul class="ticks">{"".join(f"<li>{E(d)}</li>" for d in AR_DOCS)}</ul>
        <h2 style="font-size:1.6rem;margin:2rem 0 1rem">أسباب شائعة لاحتجاز الشحنات أو رفضها</h2>
        <ul class="ticks warn">{"".join(f"<li>{E(w)}</li>" for w in risks)}</ul>
      </div>
    </div>
  </section>

  <section style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <h2 style="font-size:1.6rem;margin-bottom:1rem">منتجات بنغلاديشية رائجة في {short}</h2>
      <p class="related">{"".join(chip(lang, i) for i in ids if i in byid)} <a class="chip" href="dry-food.html">الأغذية الجافة</a> <a class="chip" href="vegetables.html">الخضروات</a></p>
      <p class="src" style="margin-top:1.5rem">أسواق أخرى: {" · ".join(f'<a href="import-from-bangladesh-to-{m}.html">{AR_MKT[m][1]}</a>' for m in GULF_MARKETS if m != s)}</p>
    </div>
  </section>

{faq(lang, faqs, f"الاستيراد إلى {short}: أسئلة شائعة")}

{cta(lang, f"الشحن إلى {short}", "أخبرونا بما تحتاجون.", "نطابق طلبكم مع موردين معتمدين لسوقكم ونرسل عرض السعر خلال 24 ساعة.")}
''' + foot(lang)
        write(lang, fn, page)

    # ---------- AR product pages
    for pr in P:
        pid, cat, name, local, sci, hs, forms, markets, note, _f = pr
        fn = B.pslug(pr); an = nm("ar", pid); info = AR_CAT_INFO[cat]
        img = B.PROD_IMG.get(pid)
        faqs = [(f"ما رمز النظام المنسق لـ{an}؟", f"يُصنَّف {an} من بنغلاديش تحت البند {hs}. يُؤكَّد الرمز الكامل المكوّن من 8 أرقام حسب شكل المنتج لكل شحنة."),
                (f"ما الحد الأدنى لطلب {an} من بنغلاديش؟", info["moq"] + "."),
                (f"متى يتوفر {an}؟", info["season"] + "."),
                (f"ما المستندات المرافقة لشحنات {an}؟", info["docs"] + ".")]
        ld = [{"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": B.lang_url("ar", "index.html")},
                {"@type": "ListItem", "position": 2, "name": "المنتجات", "item": B.lang_url("ar", "products.html")},
                {"@type": "ListItem", "position": 3, "name": an, "item": B.lang_url("ar", fn)}]},
              {"@type": "Product", "name": f"{an} من بنغلاديش", "alternateName": f"{name} from Bangladesh", "category": AR_CAT[cat],
               "description": f"{an} ({sci}) من بنغلاديش. رمز HS {hs}. الأسواق الرئيسية: {ar_markets(markets)}.", "inLanguage": "ar",
               "countryOfOrigin": {"@type": "Country", "name": "Bangladesh"}, "brand": {"@id": SITE + "/#org"}, **({"image": f"{SITE}/{IMG}{img}-lg.jpg"} if img else {})},
              B.faq_ld(faqs)]
        related = [q[0] for q in P if q[1] == cat and q[0] != pid][:8]
        bn = BN_NAME.get(pid)
        page = head("ar", f"{an} من بنغلاديش: المواصفات ورمز HS والتوريد | GFG",
                    f"توريد {an} من بنغلاديش: رمز HS {hs}، الأشكال، الموسم، الحد الأدنى للطلب، المستندات وفحوص الجودة. موردون موثّقون وعرض سعر خلال 24 ساعة.",
                    fn, ld, (f"../img/{img}-lg.jpg" if img else "iced-snapper.jpg")) + header("ar", "products", fn) + f'''
  <section class="vid page-hero novideo">
    <div class="bg-field" aria-hidden="true"></div>
    <canvas class="sea" data-level="0.78" aria-hidden="true"></canvas>
    <div class="wrap">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">الرئيسية</a><span aria-hidden="true">/</span><a href="products.html">المنتجات</a><span aria-hidden="true">/</span><a href="products.html#cat-{cat}">{AR_CAT[cat]}</a></nav>
      <h1>{E(an)} من بنغلاديش</h1>
      <p class="lede"><span lang="en" dir="ltr">{E(name)}</span> · <i lang="la" dir="ltr">{E(sci)}</i>{f' · <span lang="bn">{E(bn)}</span>' if bn else ''}. من موردين موثّقين في بنغلاديش، يُفحص في خمس مراحل ويُشحن بالمستندات التي يتطلبها سوقكم.</p>
      <div class="actions" style="display:flex;gap:.75rem;flex-wrap:wrap;margin-top:.6rem">{add_btn("ar", pid).replace('class="add"', 'class="btn btn-primary add-hero"')}<a class="btn btn-wa" href="#" data-wa="مرحباً، أريد عرض سعر لـ{E(an)} ({E(name)})." data-track="whatsapp_click">{WA} واتساب</a></div>
    </div>
  </section>

  <section style="padding-top:1.5rem">
    <div class="wrap cols2">
      <div>
        <p class="answer"><b>باختصار:</b> يُصدَّر {E(an)} من بنغلاديش إلى {E(ar_markets(markets))}، ضمن البند الجمركي {E(hs)}. {E(info["ship"])}.</p>
        <div class="tbl" style="margin-top:1.5rem"><table class="dtable">
          <tbody>
            <tr><td><b>الاسم بالإنجليزية</b></td><td lang="en" dir="ltr">{E(name)}</td></tr>
            <tr><td><b>الاسم العلمي</b></td><td dir="ltr"><i>{E(sci)}</i></td></tr>
            {f'<tr><td><b>الاسم البنغالي</b></td><td><span lang="bn">{E(bn)}</span>{f" ({E(local)})" if local else ""}</td></tr>' if bn else ''}
            <tr><td><b>الفئة</b></td><td>{AR_CAT[cat]}</td></tr>
            <tr><td><b>رمز النظام المنسق</b></td><td class="mono" dir="ltr">{E(hs)}</td></tr>
            <tr><td><b>الأشكال</b></td><td lang="en" dir="ltr">{E(forms)}</td></tr>
            <tr><td><b>الأسواق الرئيسية</b></td><td>{E(ar_markets(markets))}</td></tr>
            <tr><td><b>الموسم</b></td><td>{E(info["season"])}</td></tr>
            <tr><td><b>الشحن</b></td><td>{E(info["ship"])}</td></tr>
            <tr><td><b>الحد الأدنى للطلب</b></td><td>{E(info["moq"])}</td></tr>
            <tr><td><b>المستندات</b></td><td>{E(info["docs"])}</td></tr>
          </tbody></table></div>
        {f'<p class="src" lang="en" dir="ltr">{E(note)}</p>' if note else ''}
      </div>
      <div>
        {B.figure(img, B.PHOTO[img]).replace('src="assets/', 'src="../assets/').replace('srcset="assets/', 'srcset="../assets/').replace(', assets/', ', ../assets/') if img else ''}
        <h2 style="font-size:1.6rem;margin:{'1.5rem' if img else '0'} 0 1rem">ما نفحصه قبل الشحن</h2>
        <ul class="ticks">
          <li><b>الفحوص:</b> {E(info["tests"])}.</li>
          <li><b>المورد:</b> الترخيص وموافقة المنشأة وإدراجها لسوقكم، بالتحقق مع الجهة المصدرة.</li>
          <li><b>التفتيش:</b> عينات AQL وفق مواصفاتكم، مع صور وفيديو.</li>
          <li><b>الأدلة:</b> توافقون على ملف الدفعة الرقمي قبل الدفعة النهائية.</li>
        </ul>
        <p style="margin-top:1rem"><a href="../{fn}" lang="en" hreflang="en">English version</a></p>
      </div>
    </div>
  </section>

{faq("ar", faqs, f"{E(an)}: أسئلة شائعة")}

  <section style="padding-top:0">
    <div class="wrap">
      <h2 style="font-size:1.6rem;margin-bottom:1rem">منتجات أخرى من فئة {AR_CAT[cat]}</h2>
      <p class="related">{"".join(chip("ar", q) for q in related)} <a class="chip" href="products.html#cat-{cat}">الكل ←</a></p>
    </div>
  </section>

{cta("ar", "عرض سعر خلال 24 ساعة", f"تريدون {E(an)}؟", "أرسلوا الشكل والدرجة والتعبئة والكمية والميناء.")}
''' + foot("ar")
        write("ar", fn, page)

    # ================================================================== BANGLA
    lang = "bn"
    cube_bn = B.cube_html("../", [("dry-goods-sacks", "শুকনা খাবার"), ("aromatic-rice-spoon", "সুগন্ধি চাল"), ("green-red-chillies", "মসলা"),
                                  ("pointed-gourd-brinjal-beans", "তাজা সবজি"), ("hilsa-on-ice", "মাছ"), ("packed-cartons-warehouse", "রপ্তানির প্যাক")],
                          "ঘুরিয়ে দেখুন", f"সব পণ্য ({len(P)})", "../products.html")
    faqs = [("এক কন্টেইনারে বিভিন্ন বাংলাদেশি পণ্য নেওয়া যায়?", "হ্যাঁ। শুকনা খাবার, মসলা, চানাচুর, তেল আর মিষ্টি—বিভিন্ন সরবরাহকারীর পণ্য এক ড্রাই কন্টেইনারে; ফ্রোজেন মাছ, পরোটা আর স্ন্যাকস এক রিফার কন্টেইনারে। লোড করার আগে প্রতিটি লট পরীক্ষা করা হয়।"),
            ("কোন কোন দেশে পাঠান?", "যুক্তরাজ্য, যুক্তরাষ্ট্র, কানাডা, ইতালি ও ইউরোপ, মালয়েশিয়া, অস্ট্রেলিয়া আর উপসাগরীয় দেশের বাঙালি গ্রোসারি আমদানিকারকদের কাছে। প্রতিটি দেশের নিয়ম—লেবেল, এফডিএ প্রায়র নোটিস, কানাডার এসএফসিআর লাইসেন্স, অস্ট্রেলিয়ার বায়োসিকিউরিটি—আমরা আগে মিলিয়ে নিই।"),
            ("নিজের ব্র্যান্ডে প্যাক করা যায়?", "হ্যাঁ। অনেক বাংলাদেশি প্রক্রিয়াকারী প্রাইভেট লেবেলে প্যাক করে। আর্টওয়ার্ক, আপনার দেশের লেবেলের নিয়ম আর প্রিন্টের অনুমোদন আমরা দেখি।"),
            ("সর্বনিম্ন অর্ডার কত?", "শুকনা খাবার ও বিমানে সবজির জন্য প্রতি পণ্যে ৫০০ কেজি থেকে, অথবা একটি মিশ্র কন্টেইনার। ফ্রোজেন মাছ সাধারণত একটি ২০ ফুট রিফার।"),
            ("বাকি টাকা কখন দিতে হয়?", "সাধারণত চুক্তিতে অগ্রিম, আর লটের ছবি, ভিডিও ও ল্যাব রিপোর্ট দেখে অনুমোদন দেওয়ার পর বাকি টাকা—অথবা এলসি।")]
    groups = [("শুকনা খাবার", ["ar", "mu", "ch", "se", "dl", "dm", "dpf", "len"], "dry-food.html"), ("মসলা ও চা", ["tu", "rc", "nc", "pp", "bay", "sm", "te"], "dry-food.html"),
              ("চানাচুর, বিস্কুট ও মিষ্টি", ["sn", "bi", "rus", "pk", "sw", "rm"], "dry-food.html"), ("তেল, গুড় ও মধু", ["mo2", "jg", "hn"], "dry-food.html"),
              ("ফ্রোজেন মাছ ও খাবার", ["rh", "hl", "pb", "ko", "fp", "fk", "fr"], "../products.html"), ("তাজা সবজি", ["pt", "tg2", "bg", "lg", "kl2", "sk", "ds2", "bfl"], "vegetables.html")]
    gl = "".join(f'<article class="drygroup tilt3d"><h3>{t}</h3><p class="related">{"".join(chip(lang, i) for i in ids)} <a class="chip" href="{h}">সব দেখুন →</a></p></article>' for t, ids, h in groups)
    cities = [("যুক্তরাজ্য", "লন্ডন, বার্মিংহাম, ম্যানচেস্টার, সিলেটি কমিউনিটির দোকান"), ("যুক্তরাষ্ট্র", "নিউ ইয়র্ক, নিউ জার্সি, মিশিগান, টেক্সাস"),
              ("কানাডা", "টরন্টো, মন্ট্রিয়ল"), ("ইতালি ও ইউরোপ", "রোম, মিলান, ভেনিস, লিসবন, প্যারিস"), ("মালয়েশিয়া", "কুয়ালালামপুর"),
              ("অস্ট্রেলিয়া", "সিডনি, মেলবোর্ন"), ("উপসাগরীয় দেশ", "রিয়াদ, জেদ্দা, দুবাই, কুয়েত, দোহা, মাস্কাট")]
    page = head(lang, "গুডবাই ফুডস গ্লোবাল | বিশ্বজুড়ে বাঙালি গ্রোসারি আমদানিকারকদের জন্য বাংলাদেশি খাবার",
                "বিশ্বজুড়ে বাঙালি গ্রোসারি ক্রেতাদের জন্য বাংলাদেশ থেকে শুঁটকি, চিনিগুঁড়া চাল, মুড়ি, চিড়া, সেমাই, মসলা, সরিষার তেল, ফ্রোজেন মাছ ও তাজা সবজি—মিশ্র কন্টেইনারে, প্রতিটি লট যাচাই করে। ২৪ ঘণ্টায় দাম।",
                "index.html", [{"@type": "WebSite", "@id": SITE + "/bn/#web", "url": SITE + "/bn/", "name": "গুডবাই ফুডস গ্লোবাল", "inLanguage": "bn", "publisher": {"@id": SITE + "/#org"}}, B.faq_ld(faqs)]) + header(lang, "home", "index.html") + f'''
  <section class="hero vid" style="padding:0">
    <video class="bg" data-auto autoplay muted loop playsinline preload="auto" poster="../{V}iced-snapper.jpg" aria-hidden="true"><source src="../{V}iced-snapper.mp4" type="video/mp4"></video>
    <canvas class="sea" data-level="0.7" aria-hidden="true"></canvas>
    <div class="wrap">
      <div>
        <p class="eyebrow">বিশ্বজুড়ে বাঙালি ক্রেতাদের বিশ্বস্ত সোর্সিং পার্টনার</p>
        <h1>দেশের স্বাদ, বিশ্বের যেকোনো বন্দরে—<em>যাচাই করা মানে, স্বচ্ছ দামে</em>।</h1>
        <p class="lede">লন্ডন, নিউ ইয়র্ক, টরন্টো, রোম, কুয়ালালামপুর, সিডনি বা উপসাগরীয় দেশ—আপনার দোকানের জন্য শুঁটকি, চিনিগুঁড়া চাল, মুড়ি, চিড়া, সেমাই, মসলা, সরিষার তেল, ফ্রোজেন মাছ আর তাজা সবজি আমরা বাংলাদেশের সেরা রপ্তানিকারকদের কাছ থেকে কিনে দিই, প্রতিটি লট পরীক্ষা করে।</p>
        <div class="actions">
          <a class="btn btn-primary" href="contact.html#rfq" data-track="cta_hero">দাম জানতে চাই</a>
          <a class="btn btn-wa" href="#" data-wa="{E(L[lang]['hello'])}" data-track="whatsapp_click">{WA} হোয়াটসঅ্যাপ</a>
        </div>
        <div class="trust-row"><span>লট দেখে বাকি পেমেন্ট</span><span>এক কন্টেইনারে সব পণ্য</span><span>বাংলায় কথা বলুন</span><span>পাঁচ ধাপে মান পরীক্ষা</span></div>
      </div>
      {cube_bn}
    </div>
  </section>

  <section id="who" style="padding-block:3rem">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">যাদের জন্য কাজ করি</p><h2>প্রবাসের বাঙালি দোকান, পাইকার আর রেস্তোরাঁ।</h2></div>
        <p class="lede">প্রতিটি আমদানিকারক সাধারণত অনেক রপ্তানিকারকের সাথে আলাদা আলাদা কাজ করেন, প্রত্যেকের আলাদা ন্যূনতম অর্ডার। আমরা আপনার দরকারি সব পণ্য সেরা সরবরাহকারীদের কাছ থেকে এক কন্টেইনারে মিলিয়ে দিই।</p></div>
      <div class="tbl"><table class="dtable"><tbody>{"".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in cities)}</tbody></table></div>
    </div>
  </section>

{promises(lang, "কেন goodbuyfoods.com দিয়ে কিনবেন", "সরাসরি কেনার চেয়ে কম ঝুঁকি, বাংলাদেশে উড়ে আসার চেয়ে কম খরচ।")}

  <section style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">সবচেয়ে বেশি চাওয়া পণ্য</p><h2>আপনার ক্রেতারা যা খোঁজেন।</h2></div></div>
      <div class="drygroups">{gl}</div>
    </div>
  </section>

{ramadan(lang, "ramadan-plan", "রমজান ২০২৭ পরিকল্পনা", "রমজান শুরু হতে পারে ৮ ফেব্রুয়ারি ২০২৭-এর কাছাকাছি। শুকনা খাবারের অর্ডার এখনই দিন।", "মুড়ি, চিড়া, সেমাই, চানাচুর, চাল, মসলা আর শুঁটকি রমজান ও ঈদের আগের সপ্তাহগুলোতে সবচেয়ে বেশি বিক্রি হয়। চাঁদ দেখার ওপর নির্ভর করে সঠিক তারিখ বদলাতে পারে।")}

  <section id="chairman" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap chair">
      <figure class="chair-photo">{B.CHAIR_PHOTO.replace('src="assets/', 'src="../assets/')}</figure>
      <div>
        <p class="eyebrow">চেয়ারম্যানের বার্তা</p>
        <blockquote>
          <p>যা কিনছেন তার ওপর ভরসা করতে আমদানিকারককে বাংলাদেশে উড়ে আসতে হবে কেন? গুডবাই ফুডস গ্লোবাল ক্রেতার পক্ষে কাজ করে: উৎসেই দাম নিয়ে দর-কষাকষি করি, পাঠানোর আগে প্রতিটি লট পরীক্ষা করি, আর ফলাফলের দায় নিই।</p>
          <p>আমাদের লক্ষ্য সহজ: প্রতিটি কন্টেইনার যেন লাভে বিক্রি হয়, আর প্রতিটি ক্রেতা যেন আবার অর্ডার দিতে চান।</p>
        </blockquote>
        <p class="chair-name"><b>সাফকাত আহাম্মদ সামি</b><span>চেয়ারম্যান, গুডবাই ফুডস গ্লোবাল</span><span>আন্তর্জাতিক ব্যবসা বিশেষজ্ঞ · মাস্টার অব ইন্টারন্যাশনাল ট্রেড অ্যান্ড বিজনেস (এমআইটিবি), ঢাকা বিশ্ববিদ্যালয়</span></p>
      </div>
    </div>
  </section>

{faq(lang, faqs, "ক্রেতারা প্রথমে যা জানতে চান")}

{cta(lang, "চট্টগ্রাম থেকে পরের জাহাজ", "আপনার পরের কন্টেইনার কি প্রস্তুত করব?", "পণ্যের নাম বাংলায় বা ইংরেজিতে লিখলেই চলবে। ২৪ ঘণ্টার মধ্যে দাম পাঠাব।")}
''' + foot(lang)
    write(lang, "index.html", page)

    # ---------- BN dry food
    faqs = [("শুকনা খাবারের সর্বনিম্ন অর্ডার কত?", "প্রতি পণ্যে ৫০০ কেজি থেকে, অথবা অনেক পণ্য আর সরবরাহকারী মিলিয়ে একটি মিশ্র কন্টেইনার। ট্রায়াল অর্ডারের জন্য শুঁটকি ও মসলা ভ্যাকুয়াম প্যাকে বিমানেও যায়।"),
            ("শুঁটকির মান কীভাবে পরীক্ষা করেন?", "প্রতিটি লটে আর্দ্রতা, লবণ আর কীটনাশকের অবশিষ্টাংশ পরীক্ষা করি, কারণ শুকানোর সময় কীটনাশকের অপব্যবহার একটি জানা ঝুঁকি। পাস করা লটই শুধু পাঠানো হয়।"),
            ("রমজান ২০২৭-এর জন্য কবে অর্ডার দেব?", "রমজান শুরু হতে পারে ৮ ফেব্রুয়ারি ২০২৭-এর কাছাকাছি। উপসাগরীয় দেশে জানুয়ারির শেষে দোকানে মাল পেতে ১৫ ডিসেম্বর ২০২৬-এর মধ্যে অর্ডার নিশ্চিত করুন; ইউরোপ-আমেরিকার জন্য আরও আগে।")]
    page = head(lang, "বাংলাদেশ থেকে শুকনা খাবার পাইকারি: শুঁটকি, চাল, মুড়ি, চিড়া, সেমাই, মসলা | GFG",
                "প্রবাসের বাঙালি গ্রোসারির জন্য বাংলাদেশ থেকে শুঁটকি, সুগন্ধি চাল, মুড়ি, চিড়া, খই, সেমাই, মসলা, চা, বিস্কুট ও ডাল পাইকারি—ল্যাবে পরীক্ষিত লট, মিশ্র কন্টেইনার।",
                "dry-food.html", [crumbs_ld(lang, "শুকনা খাবার", "dry-food.html"), B.faq_ld(faqs)], "../img/dry-goods-sacks-lg.jpg") + header(lang, "dryfood", "dry-food.html") + "\n" + hero(
        lang, "শুকনা খাবার", "বাংলাদেশের শুকনা খাবার, প্রবাসের দোকানের জন্য",
        "শুঁটকি, সুগন্ধি চাল, মুড়ি, চিড়া, খই, সেমাই, মসলা, চা, বিস্কুট আর ডাল—আপনার ক্রেতারা প্রতি সপ্তাহে যা কেনেন, প্রতিটি লট পরীক্ষা করে আপনার দেশের লেবেলসহ।", "dry-goods-sacks") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>সংক্ষেপে:</b> বাংলাদেশের শুকনা খাবারের বড় ক্রেতা উপসাগরীয় আমদানিকারক আর প্রবাসের বাঙালি গ্রোসারি। শুকনা খাবার সাধারণ ড্রাই কন্টেইনারে যায়, তাই অনেক পণ্য আর সরবরাহকারী এক কন্টেইনারে মেলানো যায়।</p>
    </div>
  </section>

{ramadan(lang, "ramadan", "রমজান ২০২৭", "রমজানের আগেই দোকানে মাল।", "রমজান শুরু হতে পারে ৮ ফেব্রুয়ারি ২০২৭-এর কাছাকাছি, ঈদুল ফিতর প্রায় এক মাস পরে। দোকানে তোলার তারিখ থেকে পিছিয়ে হিসাব করুন:")}

  <section id="mixed" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">মিশ্র কন্টেইনার</p><h2>পণ্য বেছে নিন, সরবরাহকারী মেলানোর দায়িত্ব আমাদের।</h2></div>
        <p class="lede">কোটেশনে পণ্য যোগ করুন। প্রতিটি পণ্যের জন্য সেরা সরবরাহকারী খুঁজি, প্রতিটি লট পরীক্ষা করি আর এক ২০ বা ৪০ ফুট কন্টেইনারে লোড করি।</p></div>
      {prod_table(lang, DRY_IDS, [("এইচএস", lambda p: p[5])])}
      <div class="more"><a class="btn btn-primary" href="contact.html#rfq">মিশ্র কন্টেইনারের দাম জানতে চাই</a></div>
    </div>
  </section>

{faq(lang, faqs, "শুকনা খাবার: সাধারণ প্রশ্ন")}

{cta(lang, "বাংলাদেশের শুকনা খাবার", "পণ্যের তালিকা আর বন্দর জানান।", "পণ্যের নাম, প্যাক আর পরিমাণ পাঠান। ২৪ ঘণ্টার মধ্যে একটি দাম পাবেন।")}
''' + foot(lang)
    write(lang, "dry-food.html", page)

    # ---------- BN vegetables
    faqs = [("সবজির দাম কীভাবে কম রাখেন?", "মধ্যস্বত্বভোগী ছাড়া রপ্তানির প্যাকহাউস থেকে কিনি, অনেক সবজি এক বিমান চালানে মেলাই, আপনার বিমানবন্দরের জন্য সেরা ভাড়ায় বুকিং দিই, আর আলু, মিষ্টি কুমড়া, চালকুমড়া, কচু ও বাঁধাকপির মতো টেকসই সবজি জাহাজে পাঠাই—কেজিপ্রতি খরচ অনেক কম।"),
            ("পৌঁছানোর পর ক্ষতি কীভাবে কমান?", "প্যাক করার দিনই প্যাকহাউসে গ্রেডিং ও মান পরীক্ষা হয়, দরকার হলে প্রি-কুলিং, আর প্রতিটি ধাপের ছবিসহ ঢাকা বিমানবন্দরের কার্গোতে পাঠানো হয়। ঘাটতি বা মানের দাবি আমরা প্যাকহাউসের সাথে মেটাই।"),
            ("‘ফ্রেশ’ সেবার খরচ কত?", "প্রতি বিমান চালানে (৩ টন পর্যন্ত) ১২০ মার্কিন ডলার, অথবা সাপ্তাহিক চারটি চালানের প্রোগ্রামে মাসে ৪০০ ডলার। কীটনাশক পরীক্ষা ল্যাবের খরচে।")]
    page = head(lang, "বাংলাদেশ থেকে বিমানে তাজা সবজি: প্রতি সপ্তাহে যুক্তরাজ্য ও উপসাগরে | GFG",
                "প্রবাসের বাঙালি দোকানের জন্য প্রতি সপ্তাহে বিমানে পটল, কাঁকরোল, করলা, লাউ, ঢেঁড়স, বেগুন, শাক, কচুর লতি, সজনে, মোচা ও আরও তাজা সবজি। প্যাকিংয়ের দিনেই মান পরীক্ষা, স্বচ্ছ খরচ।",
                "vegetables.html", [crumbs_ld(lang, "তাজা সবজি", "vegetables.html"), B.faq_ld(faqs)], "../img/pointed-gourd-brinjal-beans-lg.jpg") + header(lang, "vegetables", "vegetables.html") + "\n" + hero(
        lang, "তাজা সবজি", "প্রতি সপ্তাহে দেশের তাজা সবজি, সবচেয়ে ভালো দামে",
        "পটল, কাঁকরোল, করলা, লাউ, ঢেঁড়স, বেগুন, বরবটি, শাক, কচুর লতি, সজনে, মোচা আর আরও অনেক—প্যাক করার দিনেই পরীক্ষা করে ঢাকা থেকে বিমানে আপনার শহরে।", "pointed-gourd-brinjal-beans") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>সংক্ষেপে:</b> ঢাকা থেকে প্রতি সপ্তাহে বিমানে সবজি পাঠাই, আর টেকসই সবজি জাহাজে। প্যাকহাউসের দাম, ভাড়া আর নির্দিষ্ট মান-পরীক্ষার ফি আলাদা লাইনে দেখাই, তাই অর্ডারের আগেই কেজিপ্রতি খরচ জানেন।</p>
      <div class="levers">
        <article class="lever tilt3d"><b>সরাসরি প্যাকহাউস থেকে</b><span>কৃষক দল, প্যাকহাউস আর আপনার মাঝে কোনো মধ্যস্বত্বভোগী নেই।</span></article>
        <article class="lever tilt3d"><b>মিশ্র চালান</b><span>অনেক সবজি এক বিমান চালানে, তাই অল্প পরিমাণও পুরো প্যালেটের ভাড়ায়।</span></article>
        <article class="lever tilt3d"><b>টেকসই সবজি জাহাজে</b><span>আলু, মিষ্টি কুমড়া, চালকুমড়া, কচু, বাঁধাকপি রিফারে—বিমানের তুলনায় অনেক কম খরচে।</span></article>
        <article class="lever tilt3d"><b>মৌসুমে কেনা</b><span>শীতের সবজি নভেম্বর–মার্চ, লাউ-কুমড়া জাতীয় এপ্রিল–অক্টোবর সবচেয়ে সস্তা।</span></article>
        <article class="lever tilt3d"><b>প্যাকিংয়ের দিনেই পরীক্ষা</b><span>গ্রেড, সতেজতা আর কীটনাশক ট্রাক ছাড়ার আগেই দেখা—নষ্ট মাল উড়িয়ে নেওয়ার খরচ নেই।</span></article>
        <article class="lever tilt3d"><b>নির্দিষ্ট ফি</b><span>প্রতি চালানে ১২০ ডলার, সবজির দামের ওপর কোনো শতাংশ নয়।</span></article>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">{len(VEG_IDS)}টি সবজি</p><h2>কী পাঠাই।</h2></div>
        <p class="lede">কোটেশনে সবজি যোগ করুন। প্রতি বৃহস্পতিবার পরের সপ্তাহের প্রাপ্যতা আর দাম নিশ্চিত করি।</p></div>
      {prod_table(lang, VEG_IDS, [("পাঠানো হয়", lambda p: "বিমান বা জাহাজ" if p[0] in SEA_VEG else "বিমান")])}
      <div class="more"><a class="btn btn-primary" href="contact.html#rfq">সাপ্তাহিক সবজির দাম চাই</a><a class="btn btn-navy" href="../vegetables.html#calc-veg" lang="en">Landed-cost calculator (English)</a></div>
    </div>
  </section>

{faq(lang, faqs, "তাজা সবজি: সাধারণ প্রশ্ন")}

{cta(lang, "প্রতি সপ্তাহে ঢাকা থেকে", "সাপ্তাহিক সবজির প্রোগ্রাম শুরু করুন।", "আপনার বিমানবন্দর, সবজি আর সাপ্তাহিক পরিমাণ জানান। ২৪ ঘণ্টার মধ্যে কেজিপ্রতি দাম পাঠাব।")}
''' + foot(lang)
    write(lang, "vegetables.html", page)
    contact("bn")
    return out
