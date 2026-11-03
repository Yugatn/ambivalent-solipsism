#!/usr/bin/env python3
"""Build a verifiable, non-destructive Word backup of the complete Ambivalent Solipsism text corpus."""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"exports"
OUT.mkdir(exist_ok=True)
DOCX=OUT/"AMBIVALENTNY_SOLIPSIZM_POLNOE_RABOCHEE_SOBRANIE_2026_11_04.docx"
MANIFEST=OUT/"AMBIVALENTNY_SOLIPSIZM_REESTR_ISKHODNIKOV_2026_11_04.json"
IGNORED={".git",".github","exports","__pycache__",".venv"}
sources=sorted([p for p in ROOT.rglob("*.md") if not set(p.relative_to(ROOT).parts)&IGNORED],key=lambda p:p.relative_to(ROOT).as_posix().casefold())

def group(p):
    name=p.relative_to(ROOT).as_posix()
    if name.startswith("BOOK_SNAPSHOT/NOTION_MAIN_AUTHOR_MANUSCRIPT_"):return "original"
    if name.startswith("BOOK_SNAPSHOT/NOTION_WORKING_CHAPTERS_"):return "notion_working"
    if name.startswith("BOOK_SNAPSHOT/NOTION_EARLIER_MANUSCRIPT_"):return "earlier"
    if name.startswith("BOOK/"):
        if re.match(r"BOOK/\d\d[A-Z]?_",name) or name in (
                "BOOK/AMBIVALENT_SOLIPSISM_FULL.md",
                "BOOK/NEUROCOMMUNISM_AND_SOCIAL_NEURAL_NETWORK.md",
                "BOOK/INDIVIDUALITY_AS_LIMIT_OF_PERSONALITY.md",
                "BOOK/INNATE_VIRTUE_CONDITIONING_AND_RESTORATION.md",
                "BOOK/LAW_OF_DEVELOPMENT_SEED_ENVIRONMENT_SYNTHESIS.md"):
            return "book"
        return "book_support"
    return "other"

groups={k:[] for k in ("original","book","notion_working","earlier","book_support","other")}
for p in sources:groups[group(p)].append(p)
try:gitsha=subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"],text=True).strip()
except Exception:gitsha="unknown"
if len(sources)<650 or len(groups["original"])!=3 or len(groups["notion_working"])!=6 or len(groups["earlier"])!=3:
    raise RuntimeError("Incorrect set of sources: "+str({k:len(v) for k,v in groups.items()}))

d=Document()
section=d.sections[0];section.page_width=Cm(21);section.page_height=Cm(29.7)
section.top_margin=Cm(1.8);section.bottom_margin=Cm(1.9);section.left_margin=Cm(2.2);section.right_margin=Cm(1.9)
section.header_distance=Cm(0.8);section.footer_distance=Cm(0.8)
normal=d.styles["Normal"];normal.font.name="Times New Roman";normal.font.size=Pt(10)
normal.paragraph_format.space_after=Pt(4);normal.paragraph_format.line_spacing=1.08
for name,size in (("Title",25),("Heading 1",16),("Heading 2",12),("Heading 3",11)):
    st=d.styles[name];st.font.name="Times New Roman";st.font.size=Pt(size);st.font.bold=True
    st.font.color.rgb=RGBColor(28,39,48);st.paragraph_format.space_before=Pt(12);st.paragraph_format.space_after=Pt(8)
    st.paragraph_format.keep_with_next=True
section.header.paragraphs[0].text="АМБИВАЛЕНТНЫЙ СОЛИПСИЗМ  ·  РЕЗЕРВНЫЙ ТЕКСТОВЫЙ СНИМОК"
foot=section.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT;foot.add_run("Югатн  ·  ")
field=OxmlElement("w:fldSimple");field.set(qn("w:instr"),"PAGE");foot._p.append(field)

p=d.add_paragraph(style="Title");p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run("АМБИВАЛЕНТНЫЙ СОЛИПСИЗМ")
p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Полное рабочее текстовое собрание\n").bold=True
p.add_run("Югатн\n\nРезервный снимок · 4 ноября 2026 года")
d.add_paragraph("В этом Word-документе сохранён полный доступный на момент сборки Markdown-корпус репозитория Yugatn/ambivalent-solipsism и дополнительно импортированные текстовые материалы Notion. Основная авторская рукопись (1 ноября 2026 года), более ранний архив и рабочие редакции представлены отдельно, чтобы версии не подменяли друг друга.")
d.add_paragraph("Документ предназначен для резервного хранения и последующей сверки. Он не является утверждённой литературной версией или готовым макетом для печати. Исторические исходники, философские гипотезы, исследования, проекты и служебные материалы оставлены в собственных разделах. Наличие материала в архиве не означает, что содержащиеся в нём утверждения доказаны или утверждены автором.")
d.add_paragraph("Часть основных исходников в Notion представляет собой текстовые извлечения из Word; исходное форматирование, таблицы, изображения и побайтовая идентичность оригинальному DOCX не гарантируются. Последняя авторская рукопись, редактируемая офлайн после этого снимка, могла измениться.")
d.add_paragraph("Git-снимок: "+gitsha+". Всего Markdown-файлов: "+str(len(sources))+".")
d.add_paragraph("Точное происхождение каждого источника, контрольные суммы SHA-256, размер и число символов приведены в отдельном JSON-реестре.")
d.add_paragraph("Оглавление",style="Heading 1")
d.add_paragraph("После открытия в Microsoft Word: щёлкните по оглавлению правой кнопкой мыши и выберите «Обновить поле». Разделы можно также просматривать в панели навигации.")
fieldp=d.add_paragraph();toc=OxmlElement("w:fldSimple");toc.set(qn("w:instr"),'TOC \\o "1-2" \\h \\z \\u');fieldp._p.append(toc)
d.add_page_break()

sections=[
("original","I. ОСНОВНАЯ АВТОРСКАЯ РУКОПИСЬ · 1 НОЯБРЯ 2026","Текстовая копия 5224 строк из 15 частей Notion. Сохраняется самостоятельным первичным источником, без замены другими версиями."),
("book","II. ГЛАВЫ И КНИЖНЫЕ МАТЕРИАЛЫ GITHUB","Философские разделы BOOK/ и цельная книга из GitHub, без удаления параллельных редакций."),
("notion_working","III. НОВЫЕ ЛИТЕРАТУРНЫЕ РАБОЧИЕ ГЛАВЫ NOTION","48 рабочих страниц Notion, перенесённых в шесть текстовых сборников в исходной последовательности реестра."),
("earlier","IV. РАННЯЯ АВТОРСКАЯ РУКОПИСЬ · ОТДЕЛЬНАЯ ВЕРСИЯ","Сохранённая ранее авторская рукопись из 11 частей Notion; отличается, в частности, вступлением."),
("book_support","V. РЕДАКЦИОННЫЕ МАТЕРИАЛЫ, ИССЛЕДОВАНИЯ И ИСТОЧНИКИ BOOK/","Архив BOOK/, содержащий служебные правила, источники и также материалы «Сюжета Икс»; не считать его единым текстом философской книги."),
("other","VI. ОСТАЛЬНОЙ ТЕКСТОВЫЙ АРХИВ РЕПОЗИТОРИЯ","Исследования, связанные проекты, канон, дорожные карты, документы, программные инструкции и прочие Markdown-источники, разделённые от основной книги.")]

manifest=[]
raw_characters=0
def safe_xml(s):
    return "".join(c for c in s if c in "\t\n\r" or 32<=ord(c)<=0xD7FF or 0xE000<=ord(c)<=0xFFFD or 0x10000<=ord(c)<=0x10FFFF)

def insert_file(path):
    global raw_characters
    rel=path.relative_to(ROOT).as_posix()
    raw=path.read_text(encoding="utf-8-sig",errors="replace")
    raw_characters+=len(raw)
    firsthead=next((re.sub(r"^#+\s*","",line).strip() for line in raw.splitlines() if re.match(r"^#{1,2}\s+",line)),None)
    title=firsthead or path.stem.replace("_"," ")
    title=title[:160] if len(title)>160 else title
    heading=d.add_paragraph(style="Heading 2");heading.add_run(safe_xml(title))
    meta=d.add_paragraph(style="Caption");meta.add_run(rel)
    for line in raw.splitlines():
        line=safe_xml(line.rstrip("\r"))
        if not line.strip():continue
        m=re.match(r"^(#{1,6})\s+(.+)$",line)
        if m:
            p=d.add_paragraph(style="Heading 3");p.add_run(safe_xml(m.group(2)));continue
        if line.strip() in ("---","***","___"):
            sep=d.add_paragraph("•  •  •");sep.alignment=WD_ALIGN_PARAGRAPH.CENTER;continue
        if line.startswith("> "):
            p=d.add_paragraph(style="Quote");p.add_run(line[2:]);continue
        p=d.add_paragraph()
        if line.startswith(("- ","* ","+ ")):
            p.paragraph_format.left_indent=Cm(.5)
        p.add_run(line)
    manifest.append({"path":rel,"group":group(path),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size,"text_characters":len(raw),"lines":len(raw.splitlines()),"title":title})

count=0
for key,label,description in sections:
    d.add_page_break()
    d.add_paragraph(label,style="Heading 1")
    d.add_paragraph(description)
    for path in groups[key]:
        insert_file(path)
        count+=1
        if count%40==0:print(f"Completed {count}/{len(sources)}",flush=True)

d.core_properties.title="Амбивалентный Солипсизм — полное рабочее собрание и резервный архив"
d.core_properties.author="Югатн"
d.core_properties.subject="Полная текстовая резервная копия GitHub и выбранных источников Notion"
d.save(DOCX)
check=Document(DOCX)
outchars=sum(len(p.text) for p in check.paragraphs)
if len(manifest)!=len(sources) or outchars<raw_characters*.58:
    raise RuntimeError(f"Failed completeness check: {len(manifest)}/{len(sources)}; {outchars}/{raw_characters}")
data={"generated_utc":datetime.now(timezone.utc).isoformat(),"repo_commit":gitsha,"word_filename":DOCX.name,
      "source_files":len(sources),"group_counts":{k:len(v) for k,v in groups.items()},
      "characters_in_sources":raw_characters,"characters_in_docx":outchars,
      "docx_bytes":DOCX.stat().st_size,"sources":manifest}
MANIFEST.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"docx":str(DOCX),"bytes":DOCX.stat().st_size,"sources":len(sources),
"groups":{k:len(v) for k,v in groups.items()},"characters":raw_characters,"word_characters":outchars,"paragraphs":len(check.paragraphs)},ensure_ascii=False),flush=True)
