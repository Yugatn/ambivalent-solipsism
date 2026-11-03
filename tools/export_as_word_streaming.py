#!/usr/bin/env python3
"""Streaming OOXML DOCX backup; preserves every Markdown text source without building an enormous DOM."""
from __future__ import annotations
import hashlib, json, re, shutil, tempfile, zipfile
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape
from docx import Document
from docx.shared import Cm, Pt
from lxml import etree

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"exports";OUT.mkdir(exist_ok=True)
DOCX=OUT/"AMBIVALENTNY_SOLIPSIZM_POLNOE_SOBRANIE_2026_11_04.docx"
MAN=OUT/"AMBIVALENTNY_SOLIPSIZM_REESTR_2026_11_04.json"
IGNORE={".git",".github","exports","__pycache__",".venv"}
sources=sorted((p for p in ROOT.rglob("*.md") if not set(p.relative_to(ROOT).parts)&IGNORE),key=lambda p:p.relative_to(ROOT).as_posix().casefold())
def group(p):
    n=p.relative_to(ROOT).as_posix()
    if n.startswith("BOOK_SNAPSHOT/NOTION_MAIN_AUTHOR_MANUSCRIPT_"):return "main_original"
    if n.startswith("BOOK_SNAPSHOT/NOTION_WORKING_CHAPTERS_"):return "notion_chapters"
    if n.startswith("BOOK_SNAPSHOT/NOTION_EARLIER_MANUSCRIPT_"):return "earlier_original"
    if n.startswith("BOOK/"):
        if re.match(r"BOOK/\d\d[A-Z]?_",n) or n in ("BOOK/AMBIVALENT_SOLIPSISM_FULL.md","BOOK/NEUROCOMMUNISM_AND_SOCIAL_NEURAL_NETWORK.md","BOOK/INDIVIDUALITY_AS_LIMIT_OF_PERSONALITY.md","BOOK/INNATE_VIRTUE_CONDITIONING_AND_RESTORATION.md","BOOK/LAW_OF_DEVELOPMENT_SEED_ENVIRONMENT_SYNTHESIS.md"):
            return "book"
        return "book_archive"
    return "other_archive"
groups=OrderedDict((k,[]) for k in ("main_original","book","notion_chapters","earlier_original","book_archive","other_archive"))
for p in sources:groups[group(p)].append(p)
if len(sources)<668 or [len(groups[k]) for k in ("main_original","notion_chapters","earlier_original")]!=[3,6,3]:
    raise RuntimeError("Incomplete source inventory: "+str({k:len(v) for k,v in groups.items()}))

TITLES={
"main_original":("ЧАСТЬ I. ОСНОВНАЯ АВТОРСКАЯ РУКОПИСЬ","15 архивных частей из Notion в трёх последовательных файлах. Источник: 1 ноября 2026 года."),
"book":("ЧАСТЬ II. КНИГА И ФИЛОСОФСКИЕ ГЛАВЫ GITHUB","Исходные разделы BOOK/ сохранены без сокращения и выбора между параллельными редакциями."),
"notion_chapters":("ЧАСТЬ III. РАБОЧИЕ ЛИТЕРАТУРНЫЕ ГЛАВЫ NOTION","48 отдельных страниц; статусы не приравнены к утверждённому авторскому канону."),
"earlier_original":("ЧАСТЬ IV. БОЛЕЕ РАННЯЯ РУКОПИСЬ","Текстовый архив прежней версии в 11 частях; сохранён отдельно."),
"book_archive":("ЧАСТЬ V. ИССЛЕДОВАНИЯ И ДРУГИЕ ИСХОДНИКИ BOOK/","Исследовательские отчёты, редакционные документы, материалы «Сюжета Икс» и история редакций."),
"other_archive":("ЧАСТЬ VI. ОСТАЛЬНОЙ АРХИВ GITHUB И NOTION","Остальные Markdown-файлы репозитория и материалы резервирования.")}

d=Document();section=d.sections[0];section.page_width=Cm(21);section.page_height=Cm(29.7);section.top_margin=Cm(1.8);section.bottom_margin=Cm(1.8);section.left_margin=Cm(2.1);section.right_margin=Cm(1.8)
normal=d.styles["Normal"];normal.font.name="Times New Roman";normal.font.size=Pt(10);normal.paragraph_format.space_after=Pt(5)
for name,pts in (("Title",24),("Heading 1",16),("Heading 2",12),("Heading 3",11)):
    st=d.styles[name];st.font.name="Times New Roman";st.font.size=Pt(pts);st.font.bold=True;st.paragraph_format.keep_with_next=True
with tempfile.TemporaryDirectory() as tempdir:
    temp=Path(tempdir)
    template=temp/"template.docx";d.add_paragraph("placeholder");d.save(template)
    ns="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    nsq="{"+ns+"}"
    def clean(s):
        return "".join(c for c in s if c in "\t\n\r" or 32<=ord(c)<=0xD7FF or 0xE000<=ord(c)<=0xFFFD or 0x10000<=ord(c)<=0x10FFFF)
    def par(w,s,style=None,pagebreak=False):
        global paragraph_count
        paragraph_count+=1
        w.write("<w:p>")
        if style or pagebreak:
            w.write("<w:pPr>")
            if style:w.write('<w:pStyle w:val="'+style+'"/>')
            if pagebreak:w.write('<w:pageBreakBefore/>')
            w.write("</w:pPr>")
        text=clean(s)
        if text:
            w.write("<w:r><w:t xml:space=\"preserve\">")
            for i in range(0,len(text),16000):w.write(escape(text[i:i+16000]))
            w.write("</w:t></w:r>")
        w.write("</w:p>\n")
    manifest=[];paragraph_count=0;source_chars=0
    xml=temp/"document.xml"
    with xml.open("w",encoding="utf-8") as w:
        w.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
        w.write('<w:document xmlns:w="'+ns+'"><w:body>\n')
        par(w,"АМБИВАЛЕНТНЫЙ СОЛИПСИЗМ",style="Title")
        par(w,"Полное рабочее текстовое собрание · Югатн · 4 ноября 2026 года")
        par(w,"Резервная копия авторской рукописи, отдельных рабочих редакций, материалов Notion и всего доступного Markdown-корпуса GitHub. Это архивный снимок, а не утверждённое издание для печати.")
        par(w,"Сохраняются различные редакции и повторы; научные гипотезы, проекты, технические заметки и роман «Сюжет Икс» в специальном архивном разделе. Отдельная книга автором ещё не сведена в единый подтверждённый канон.")
        par(w,"Оригинальные бинарные файлы Word (таблицы, фотографии, стили) не воспроизводятся точно: у текстов Notion использованы архивные текстовые извлечения. Точная копия каждого Markdown-источника остается в GitHub, здесь содержатся все его непустые строки.")
        par(w,"Полный реестр исходников и SHA-256 включён в отдельный JSON. Все материалы сборки сохранены в выделенной резервной ветке.")
        for key,paths in groups.items():
            title,desc=TITLES[key]
            par(w,title,style="Heading1",pagebreak=True)
            par(w,desc)
            for p in paths:
                rel=p.relative_to(ROOT).as_posix()
                raw=p.read_text(encoding="utf-8-sig",errors="replace")
                source_chars+=len(raw)
                first=next((re.sub(r"^#+\s*","",line).strip() for line in raw.splitlines() if re.match(r"^#{1,2}\s+",line)),p.stem.replace("_"," "))
                par(w,first[:150],style="Heading2")
                par(w,"Источник: "+rel)
                for line in raw.splitlines():
                    line=line.rstrip("\r")
                    if not line.strip():continue
                    mat=re.match(r"^(#{1,6})\s+(.+)$",line)
                    par(w,mat.group(2) if mat else line,style="Heading3" if mat else None)
                manifest.append({"path":rel,"section":key,"size_bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"text_characters":len(raw),"lines":len(raw.splitlines())})
                if len(manifest)%50==0:print("Processed",len(manifest),"/",len(sources),flush=True)
        w.write('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1021" w:right="1021" w:bottom="1021" w:left="1191" w:header="453" w:footer="453" w:gutter="0"/></w:sectPr>')
        w.write("</w:body></w:document>\n")
    with zipfile.ZipFile(template,"r") as zsrc,zipfile.ZipFile(DOCX,"w") as zout:
        for entry in zsrc.infolist():
            if entry.filename=="word/document.xml":
                zout.write(xml,arcname=entry.filename,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
            else:zout.writestr(entry,zsrc.read(entry.filename))
    with zipfile.ZipFile(DOCX) as z:
        if z.testzip() is not None:raise RuntimeError("Zip file corruption")
        with z.open("word/document.xml") as stream:
            count=0
            for _,elem in etree.iterparse(stream,events=("end",),tag=nsq+"p"):
                count+=1
                elem.clear()
            if count!=paragraph_count:raise RuntimeError("OOXML paragraph count mismatch")
    manifest_data={"generated_at":datetime.now(timezone.utc).isoformat(),"docx":DOCX.name,"sources":len(sources),"source_characters":source_chars,"word_paragraphs":paragraph_count,"docx_bytes":DOCX.stat().st_size,"group_counts":{k:len(v) for k,v in groups.items()},"files":manifest}
    MAN.write_text(json.dumps(manifest_data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"docx":str(DOCX),"bytes":DOCX.stat().st_size,"sources":len(sources),"characters":source_chars,"paragraphs":paragraph_count,"groups":{k:len(v) for k,v in groups.items()}},ensure_ascii=False),flush=True)
