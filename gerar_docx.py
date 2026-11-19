# -*- coding: utf-8 -*-
"""Gera GS_QA_Alerta_Corrego.docx (mesmo conteúdo do PDF) para colar os prints e exportar para PDF."""
import os
import sys

from docx import Document
from docx.enum.section import WD_ORIENT  # noqa: F401
from docx.enum.table import WD_ROW_HEIGHT_RULE, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import dados as d  # noqa: E402

AZUL = RGBColor(0x0B, 0x4F, 0x8A)


def larguras_fixas(t, larguras):
    t.autofit = False
    grid = t._tbl.tblGrid
    for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(Cm(larguras[i]).twips)))
    for row in t.rows:
        for i, w in enumerate(larguras):
            row.cells[i].width = Cm(w)


def sombrear(cell, hexcor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcor)
    tcPr.append(shd)


def escrever(cell, texto, bold=False, cor=None, size=8.5):
    cell.text = ""
    p = cell.paragraphs[0]
    r = p.add_run(texto)
    r.bold = bold
    r.font.size = Pt(size)
    if cor:
        r.font.color.rgb = cor
    p.paragraph_format.space_after = Pt(0)


def tabela(doc, cab, linhas, larguras):
    t = doc.add_table(rows=1, cols=len(cab))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(cab):
        escrever(t.rows[0].cells[i], h, bold=True, cor=RGBColor(0xFF, 0xFF, 0xFF))
        sombrear(t.rows[0].cells[i], "0B4F8A")
    for ln in linhas:
        cells = t.add_row().cells
        for i, v in enumerate(ln):
            escrever(cells[i], str(v))
    larguras_fixas(t, larguras)
    doc.add_paragraph()
    return t


def kv(doc, linhas, w0=4.0, w1=13.0):
    t = doc.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    for k, v in linhas:
        c = t.add_row().cells
        escrever(c[0], k, bold=True)
        sombrear(c[0], "E8F0F8")
        escrever(c[1], v)
    larguras_fixas(t, [w0, w1])
    doc.add_paragraph()
    return t


def h(doc, txt, nivel):
    p = doc.add_heading(txt, level=nivel)
    for r in p.runs:
        r.font.color.rgb = AZUL
    return p


def quebra(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def main():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Cm(2))
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)

    # Capa
    for _ in range(3):
        doc.add_paragraph()
    for txt, sz, b in [("FIAP — Global Solution 2026", 14, False), (d.DISCIPLINA, 14, False), ("", 10, False),
                       ("CitizenTech", 12, False), (d.PROJETO, 30, True),
                       ("Features, critérios de aceite e casos de teste funcionais (caixa-preta) no Azure DevOps", 11, False)]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        r.font.size = Pt(sz)
        r.bold = b
        if b:
            r.font.color.rgb = AZUL
    doc.add_paragraph()
    tabela(doc, ["Integrante", "RM"], d.INTEGRANTES, [11, 4])
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Turma: ").font.size = Pt(12)
    r = p.add_run(d.TURMA)
    r.bold = True
    r.font.size = Pt(12)
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run("Link do projeto no Azure DevOps: ")
    r.bold = True
    p.add_run("https://dev.azure.com/______________________/______________________")
    doc.add_paragraph("Professor adicionado como Project Administrator: (   ) sim")
    quebra(doc)

    # 1. Ficha
    h(doc, "1. Ficha da solução", 1)
    kv(doc, d.FICHA_RESUMO, 3.6, 13.4)
    h(doc, "Repositórios", 2)
    kv(doc, d.REPOS, 4.6, 12.4)
    h(doc, "Escopo dos testes", 2)
    doc.add_paragraph("Casos de teste funcionais, de caixa-preta, para aceite/homologação da API REST (contrato comum "
                      "FastAPI e .NET), do app mobile (Expo) e dos requisitos de proteção de dados (LGPD). Cada Test Case "
                      "é vinculado à sua Feature no Azure DevOps pelo link Tested By / Tests.")
    quebra(doc)

    # 2. Features
    h(doc, "2. Features e critérios de aceite", 1)
    tabela(doc, ["ID", "Feature", "Prior.", "Business Value", "Casos de teste"],
           [(f["id"], f["titulo"], f["prioridade"], f["bv"],
             ", ".join(c["id"] for c in d.casos_da_feature(f["id"]))) for f in d.FEATURES],
           [1.2, 5.6, 1.3, 2.2, 6.7])
    for f in d.FEATURES:
        h(doc, f"{f['id']} — {f['titulo']}", 2)
        kv(doc, [("Descrição", d.historia(f)), ("Prioridade", str(f["prioridade"])),
                 ("Business Value", str(f["bv"]))], 3.2, 13.8)
        tabela(doc, ["CA", "Dado", "Quando", "Então"],
               [(f"CA{i:02d}", a, b, c) for i, (a, b, c) in enumerate(f["ca"], 1)], [1.3, 4.6, 4.6, 6.5])
    quebra(doc)

    # 3. Massa / 4. Resumo
    h(doc, "3. Massa de teste e convenções", 1)
    kv(doc, d.MASSA, 3.4, 13.6)
    for c in d.CONVENCOES:
        doc.add_paragraph(c, style="List Bullet")
    h(doc, "4. Resumo dos casos de teste", 1)
    tabela(doc, ["ID", "Título", "Feature", "Tipo", "Técnica"],
           [(c["id"], c["titulo"], c["feature"], c["tipo"], c["tecnica"]) for c in d.TEST_CASES],
           [1.3, 7.8, 1.6, 1.9, 4.4])
    quebra(doc)

    # 5. Detalhes
    h(doc, "5. Casos de teste detalhados", 1)
    for c in d.TEST_CASES:
        f = d.feature_por_id(c["feature"])
        h(doc, f"{c['id']} — {c['titulo']}", 2)
        kv(doc, [("ID", c["id"]), ("Título", c["titulo"]), ("Feature relacionada", f"{f['id']} — {f['titulo']}"),
                 ("Objetivo do teste", c["objetivo"]), ("Pré-condições / Preparação", c["pre"]),
                 ("Dados de entrada", c["entrada"]), ("Resultado esperado", c["esperado"]),
                 ("Tipo", c["tipo"]), ("Técnica", c["tecnica"])], 3.8, 13.2)
        tabela(doc, ["#", "Passo (ação)", "Resultado esperado do passo"],
               [(i, a, e) for i, (a, e) in enumerate(c["passos"], 1)], [0.8, 8.0, 8.2])
    quebra(doc)

    # 6. Matriz
    h(doc, "6. Matriz de rastreabilidade (Feature × Casos de Teste)", 1)
    linhas = []
    for f in d.FEATURES:
        cs = d.casos_da_feature(f["id"])
        pos = sum(c["tipo"] == "Positivo" for c in cs)
        linhas.append((f"{f['id']} — {f['titulo']}", ", ".join(c["id"] for c in cs), pos, len(cs) - pos, len(cs)))
    tp = sum(c["tipo"] == "Positivo" for c in d.TEST_CASES)
    linhas.append(("Total", "", tp, len(d.TEST_CASES) - tp, len(d.TEST_CASES)))
    tabela(doc, ["Feature", "Casos de teste", "Pos.", "Neg.", "Total"], linhas, [5.6, 7.8, 1.2, 1.2, 1.2])
    fids = [f["id"] for f in d.FEATURES]
    tabela(doc, ["CT", "Título"] + fids,
           [[c["id"], c["titulo"]] + ["X" if c["feature"] == x else "" for x in fids] for c in d.TEST_CASES],
           [1.3, 6.7] + [1.0] * len(fids))
    quebra(doc)

    # Anexo
    h(doc, "Anexo A — Prints do Azure Boards / Test Plans", 1)
    doc.add_paragraph("Apague o texto \"[ colar o print aqui ]\" e cole a imagem no lugar (Inserir > Imagem). "
                      "Depois exporte: Arquivo > Salvar como > PDF.")
    for n, (cod, desc) in enumerate(d.PRINTS):
        if n and n % 2 == 0:
            quebra(doc)
        t = doc.add_table(rows=2, cols=1)
        t.style = "Table Grid"
        escrever(t.rows[0].cells[0], f"Print {cod} — {desc}", bold=True, size=9)
        sombrear(t.rows[0].cells[0], "E8F0F8")
        escrever(t.rows[1].cells[0], "[ colar o print aqui ]", cor=RGBColor(0x9C, 0xA3, 0xAF), size=10)
        t.rows[1].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        t.rows[1].height = Cm(9)
        t.rows[1].height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        for row in t.rows:
            trPr = row._tr.get_or_add_trPr()
            cs = OxmlElement("w:cantSplit")
            trPr.append(cs)
        t.rows[0].cells[0].paragraphs[0].paragraph_format.keep_with_next = True
        larguras_fixas(t, [17])
        doc.add_paragraph()

    saida = os.path.join(AQUI, "GS_QA_Alerta_Corrego.docx")
    doc.save(saida)
    print("DOCX gerado:", saida)


if __name__ == "__main__":
    main()
