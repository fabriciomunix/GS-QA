# -*- coding: utf-8 -*-
"""Gera GS_QA_Alerta_Corrego.pdf (A4) a partir de dados.py usando reportlab."""
import os
import sys
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import dados as d  # noqa: E402

# ---------------------------------------------------------------- fontes
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DV-I", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DV-BI", FD + "DejaVuSans-BoldOblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")

AZUL = colors.HexColor("#0B4F8A")
AZUL_CLARO = colors.HexColor("#E8F0F8")
CINZA = colors.HexColor("#F3F4F6")
BORDA = colors.HexColor("#B8C2CC")
VERDE = colors.HexColor("#E6F4EA")
VERMELHO = colors.HexColor("#FDECEA")

S = {
    "body": ParagraphStyle("body", fontName="DV", fontSize=9.5, leading=13),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.3, leading=10.6),
    "cellb": ParagraphStyle("cellb", fontName="DV-B", fontSize=8.3, leading=10.6),
    "cellh": ParagraphStyle("cellh", fontName="DV-B", fontSize=8.3, leading=10.6, textColor=colors.white),
    "mono": ParagraphStyle("mono", fontName="DV", fontSize=7.8, leading=10, textColor=colors.HexColor("#1F2937")),
    "h1": ParagraphStyle("h1", fontName="DV-B", fontSize=16, leading=20, textColor=AZUL, spaceBefore=4, spaceAfter=10),
    "h2": ParagraphStyle("h2", fontName="DV-B", fontSize=11.5, leading=15, textColor=AZUL, spaceBefore=10, spaceAfter=5),
    "capa_t": ParagraphStyle("ct", fontName="DV-B", fontSize=28, leading=34, alignment=TA_CENTER, textColor=AZUL),
    "capa_s": ParagraphStyle("cs", fontName="DV", fontSize=13, leading=18, alignment=TA_CENTER),
    "capa_m": ParagraphStyle("cm", fontName="DV", fontSize=11, leading=16, alignment=TA_CENTER),
}

LARG = A4[0] - 4 * cm  # largura útil


def P(txt, st="cell"):
    return Paragraph(txt, S[st])


def E(txt, st="cell"):
    return Paragraph(escape(txt), S[st])


def tabela(dados, col_w, header=True, zebra=False, extra=None):
    t = Table(dados, colWidths=col_w, repeatRows=1 if header else 0)
    st = [
        ("GRID", (0, 0), (-1, -1), 0.5, BORDA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), AZUL))
    if zebra:
        for r in range(1 if header else 0, len(dados)):
            if r % 2 == 0:
                st.append(("BACKGROUND", (0, r), (-1, r), CINZA))
    if extra:
        st += extra
    t.setStyle(TableStyle(st))
    return t


def kv(rows, w0=4.2 * cm):
    """Tabela chave/valor (coluna 1 em negrito com fundo claro)."""
    data = [[P(k, "cellb"), v if not isinstance(v, str) else E(v)] for k, v in rows]
    return tabela(data, [w0, LARG - w0], header=False,
                  extra=[("BACKGROUND", (0, 0), (0, -1), AZUL_CLARO)])


# ---------------------------------------------------------------- página
def rodape(c, doc):
    if doc.page == 1:
        return
    c.saveState()
    c.setFont("DV", 7.5)
    c.setFillColor(colors.HexColor("#6B7280"))
    c.drawString(2 * cm, 1.2 * cm, f"GS 2026 — {d.PROJETO} — {d.DISCIPLINA}")
    c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    c.setStrokeColor(BORDA)
    c.line(2 * cm, A4[1] - 1.4 * cm, A4[0] - 2 * cm, A4[1] - 1.4 * cm)
    c.drawString(2 * cm, A4[1] - 1.25 * cm, "CitizenTech Alerta Córrego — Features e Casos de Teste (Azure Boards)")
    c.restoreState()


# ---------------------------------------------------------------- seções
def capa():
    s = [Spacer(1, 2.2 * cm),
         P("FIAP — Global Solution 2026", "capa_s"), Spacer(1, 0.4 * cm),
         P(d.DISCIPLINA, "capa_s"), Spacer(1, 1.8 * cm),
         P("CitizenTech", "capa_m"),
         P(d.PROJETO, "capa_t"), Spacer(1, 0.3 * cm),
         P("Features, critérios de aceite e casos de teste funcionais (caixa-preta) no Azure DevOps", "capa_m"),
         Spacer(1, 1.6 * cm)]
    integ = [[P("Integrante", "cellh"), P("RM", "cellh")]] + \
            [[E(n), E(rm)] for n, rm in d.INTEGRANTES]
    s.append(tabela(integ, [11 * cm, 4 * cm]))
    s += [Spacer(1, 0.4 * cm), P(f"Turma: <b>{d.TURMA}</b>", "capa_m"), Spacer(1, 1.2 * cm)]
    link = Table([[P("<b>Link do projeto no Azure DevOps:</b>", "body")],
                  [P("https://dev.azure.com/______________________/______________________", "body")]],
                 colWidths=[LARG])
    link.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1.2, AZUL), ("BACKGROUND", (0, 0), (-1, -1), AZUL_CLARO),
                              ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    s.append(link)
    s.append(Spacer(1, 0.4 * cm))
    s.append(P("Professor adicionado como <i>Project Administrator</i>: ( &nbsp; ) sim", "capa_m"))
    s.append(PageBreak())
    return s


def sumario():
    itens = ["1. Ficha da solução e repositórios", "2. Features e critérios de aceite",
             "3. Massa de teste e convenções", "4. Resumo dos casos de teste",
             "5. Casos de teste detalhados", "6. Matriz de rastreabilidade (Feature × Casos de Teste)",
             "Anexo A — Prints do Azure Boards / Test Plans"]
    s = [P("Sumário", "h1")] + [P(i, "body") for i in itens]
    s += [Spacer(1, 0.6 * cm), P("Números do material", "h2")]
    pos = sum(c["tipo"] == "Positivo" for c in d.TEST_CASES)
    s.append(kv([("Features", str(len(d.FEATURES))),
                 ("Critérios de aceite", str(sum(len(f["ca"]) for f in d.FEATURES))),
                 ("Casos de teste", f"{len(d.TEST_CASES)} ({pos} positivos, {len(d.TEST_CASES) - pos} negativos)"),
                 ("Técnicas", "Partição de equivalência, análise de valor-limite e tabela de decisão")]))
    return s


def ficha():
    s = [PageBreak(), P("1. Ficha da solução", "h1"), kv(d.FICHA_RESUMO, 3.6 * cm),
         P("Repositórios", "h2")]
    s.append(kv([(k, v) for k, v in d.REPOS], 4.6 * cm))
    s += [P("Escopo dos testes", "h2"),
          P("Os casos de teste são funcionais, de caixa-preta, voltados ao aceite/homologação. Validam a API REST "
            "(contrato comum às versões FastAPI e .NET), o app mobile (Expo) e requisitos de proteção de dados (LGPD). "
            "A rastreabilidade é feita no Azure DevOps vinculando cada Test Case à sua Feature (link "
            "<i>Tested By / Tests</i>).", "body")]
    return s


def features():
    s = [PageBreak(), P("2. Features e critérios de aceite", "h1"),
         P("Formato: <b>Título</b>; <b>Descrição</b> como história de usuário (Como &lt;persona&gt;, quero &lt;ação&gt;, "
           "para &lt;benefício&gt;); <b>Critérios de aceite</b> no padrão Dado / Quando / Então; <b>Prioridade</b> "
           "(1 = mais alta … 4 = mais baixa, escala do Azure) e <b>Business Value</b>.", "body"),
         Spacer(1, 0.3 * cm)]
    resumo = [[P(h, "cellh") for h in ("ID", "Feature", "Prior.", "Business Value", "Casos de teste")]]
    for f in d.FEATURES:
        resumo.append([E(f["id"]), E(f["titulo"]), E(str(f["prioridade"])), E(str(f["bv"])),
                       E(", ".join(c["id"] for c in d.casos_da_feature(f["id"])))])
    s.append(tabela(resumo, [1.2 * cm, 5.6 * cm, 1.3 * cm, 2.2 * cm, LARG - 10.3 * cm], zebra=True))
    for f in d.FEATURES:
        bloco = [P(f"{f['id']} — {escape(f['titulo'])}", "h2")]
        rows = [("Descrição", E(d.historia(f))),
                ("Prioridade", E(str(f["prioridade"]))),
                ("Business Value", E(str(f["bv"])))]
        bloco.append(kv(rows, 3.2 * cm))
        ca = [[P("CA", "cellh"), P("Dado", "cellh"), P("Quando", "cellh"), P("Então", "cellh")]]
        for i, (a, b, c) in enumerate(f["ca"], 1):
            ca.append([P(f"<b>CA{i:02d}</b>"), E(a), E(b), E(c)])
        bloco.append(Spacer(1, 3))
        bloco.append(tabela(ca, [1.3 * cm, 4.3 * cm, 4.6 * cm, LARG - 10.2 * cm]))
        s.append(KeepTogether(bloco))
    return s


def massa():
    s = [PageBreak(), P("3. Massa de teste e convenções", "h1"), kv(d.MASSA, 3.4 * cm),
         P("Convenções de resultado", "h2")]
    s += [P("• " + escape(c), "body") for c in d.CONVENCOES]
    return s


def resumo_ct():
    s = [P("4. Resumo dos casos de teste", "h1")]
    rows = [[P(h, "cellh") for h in ("ID", "Título", "Feature", "Tipo", "Técnica")]]
    for c in d.TEST_CASES:
        rows.append([E(c["id"]), E(c["titulo"]), E(c["feature"]), E(c["tipo"]), E(c["tecnica"])])
    extra = []
    for r, c in enumerate(d.TEST_CASES, 1):
        extra.append(("BACKGROUND", (3, r), (3, r), VERDE if c["tipo"] == "Positivo" else VERMELHO))
    s.append(tabela(rows, [1.3 * cm, 7.8 * cm, 1.9 * cm, 1.9 * cm, LARG - 12.9 * cm], extra=extra))
    return s


def detalhes_ct():
    s = [PageBreak(), P("5. Casos de teste detalhados", "h1")]
    for c in d.TEST_CASES:
        f = d.feature_por_id(c["feature"])
        cab = [P(f"{c['id']} — {escape(c['titulo'])}", "h2")]
        info = kv([
            ("ID", E(c["id"])),
            ("Título", E(c["titulo"])),
            ("Feature relacionada", E(f"{f['id']} — {f['titulo']}")),
            ("Objetivo do teste", E(c["objetivo"])),
            ("Pré-condições / Preparação", E(c["pre"])),
            ("Dados de entrada", E(c["entrada"], "mono")),
            ("Resultado esperado", E(c["esperado"])),
            ("Tipo", P(f"<b>{c['tipo']}</b>")),
            ("Técnica", E(c["tecnica"])),
        ], 3.8 * cm)
        passos = [[P("#", "cellh"), P("Passo (ação)", "cellh"), P("Resultado esperado do passo", "cellh")]]
        for i, (a, e) in enumerate(c["passos"], 1):
            passos.append([E(str(i)), E(a), E(e)])
        tp = tabela(passos, [0.8 * cm, 8.0 * cm, LARG - 8.8 * cm], zebra=True)
        s.append(KeepTogether(cab + [info, Spacer(1, 3), tp]))
        s.append(Spacer(1, 6))
    return s


def matriz():
    s = [PageBreak(), P("6. Matriz de rastreabilidade (Feature × Casos de Teste)", "h1")]
    rows = [[P(h, "cellh") for h in ("Feature", "Casos de teste", "Pos.", "Neg.", "Total")]]
    for f in d.FEATURES:
        cs = d.casos_da_feature(f["id"])
        pos = sum(c["tipo"] == "Positivo" for c in cs)
        rows.append([E(f"{f['id']} — {f['titulo']}"), E(", ".join(c["id"] for c in cs)),
                     E(str(pos)), E(str(len(cs) - pos)), E(str(len(cs)))])
    tp = sum(c["tipo"] == "Positivo" for c in d.TEST_CASES)
    rows.append([P("<b>Total</b>"), E(""), P(f"<b>{tp}</b>"), P(f"<b>{len(d.TEST_CASES) - tp}</b>"),
                 P(f"<b>{len(d.TEST_CASES)}</b>")])
    s.append(tabela(rows, [5.6 * cm, LARG - 9.2 * cm, 1.2 * cm, 1.2 * cm, 1.2 * cm], zebra=True))

    s += [Spacer(1, 0.4 * cm), P("Matriz detalhada (X = caso de teste cobre a Feature)", "h2")]
    fids = [f["id"] for f in d.FEATURES]
    w0, w1 = 1.3 * cm, 7.0 * cm
    wf = (LARG - w0 - w1) / len(fids)
    head = [P("CT", "cellh"), P("Título", "cellh")] + [P(x, "cellh") for x in fids]
    rows = [head]
    extra = [("ALIGN", (2, 0), (-1, -1), "CENTER")]
    for r, c in enumerate(d.TEST_CASES, 1):
        linha = [E(c["id"]), E(c["titulo"])]
        for j, x in enumerate(fids):
            if c["feature"] == x:
                linha.append(P("<b>X</b>"))
                extra.append(("BACKGROUND", (j + 2, r), (j + 2, r), AZUL_CLARO))
            else:
                linha.append(E(""))
        rows.append(linha)
    s.append(tabela(rows, [w0, w1] + [wf] * len(fids), extra=extra))
    return s


def anexo():
    s = [PageBreak(), P("Anexo A — Prints do Azure Boards / Test Plans", "h1"),
         P("Substituir cada quadro pelo print correspondente (use a versão .docx para colar as imagens e exportar "
           "novamente para PDF). Os prints devem mostrar a URL do projeto e o nome da organização.", "body"),
         Spacer(1, 0.3 * cm)]
    for cod, desc in d.PRINTS:
        box = Table([[P(f"<b>Print {cod}</b> — {escape(desc)}", "cell")],
                     [P("<font color='#9CA3AF'>[ colar o print aqui ]</font>", "capa_m")]],
                    colWidths=[LARG], rowHeights=[None, 8.2 * cm])
        box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.8, AZUL),
            ("LINEBELOW", (0, 0), (-1, 0), 0.5, BORDA),
            ("BACKGROUND", (0, 0), (-1, 0), AZUL_CLARO),
            ("VALIGN", (0, 1), (-1, 1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        s += [KeepTogether([box]), Spacer(1, 0.4 * cm)]
    return s


def main():
    saida = os.path.join(AQUI, "GS_QA_Alerta_Corrego.pdf")
    doc = SimpleDocTemplate(saida, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm,
                            title=f"GS — {d.PROJETO} — QA", author="; ".join(n for n, _ in d.INTEGRANTES),
                            subject=d.DISCIPLINA)
    story = capa() + sumario() + ficha() + features() + massa() + resumo_ct() + detalhes_ct() + matriz() + anexo()
    doc.build(story, onFirstPage=rodape, onLaterPages=rodape)
    print("PDF gerado:", saida)


if __name__ == "__main__":
    main()
