# -*- coding: utf-8 -*-
"""Gera features.md, test-cases.md e os CSVs de importação do Azure DevOps a partir de dados.py."""
import csv
import html
import os

import dados as d

AQUI = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------- Markdown
def gerar_features_md():
    L = [f"# Features — {d.PROJETO}", "",
         f"Disciplina: {d.DISCIPLINA} — Turma {d.TURMA}", "",
         "Formato: Título · Descrição (história de usuário) · Critérios de aceite (Dado/Quando/Então) · "
         "Prioridade (1 = mais alta, 4 = mais baixa, escala do Azure) · Business Value.", ""]
    L += ["| ID | Feature | Prioridade | Business Value | Casos de teste |", "|---|---|---|---|---|"]
    for f in d.FEATURES:
        cts = ", ".join(c["id"] for c in d.casos_da_feature(f["id"]))
        L.append(f"| {f['id']} | {f['titulo']} | {f['prioridade']} | {f['bv']} | {cts} |")
    L.append("")
    for f in d.FEATURES:
        L += [f"## {f['id']} — {f['titulo']}", "",
              f"**Descrição:** {d.historia(f)}", "",
              f"**Prioridade:** {f['prioridade']}  ", f"**Business Value:** {f['bv']}", "",
              "**Critérios de aceite:**", ""]
        for i, (dado, quando, entao) in enumerate(f["ca"], 1):
            L.append(f"- **CA{i:02d}** — **Dado** {dado}, **Quando** {quando}, **Então** {entao}.")
        L.append("")
    return "\n".join(L)


def gerar_tc_md():
    L = [f"# Casos de Teste — {d.PROJETO}", "",
         "Testes funcionais de caixa-preta para aceite/homologação.", "",
         "## Massa de teste (seed) assumida", ""]
    for k, v in d.MASSA:
        L.append(f"- **{k}:** {v}")
    L += ["", "## Convenções", ""] + [f"- {c}" for c in d.CONVENCOES] + [""]
    L += ["## Resumo", "", "| ID | Título | Feature | Tipo | Técnica |", "|---|---|---|---|---|"]
    for c in d.TEST_CASES:
        L.append(f"| {c['id']} | {c['titulo']} | {c['feature']} | {c['tipo']} | {c['tecnica']} |")
    L.append("")
    for c in d.TEST_CASES:
        f = d.feature_por_id(c["feature"])
        L += [f"## {c['id']} — {c['titulo']}", "",
              "| Campo | Valor |", "|---|---|",
              f"| Feature relacionada | {f['id']} — {f['titulo']} |",
              f"| Objetivo do teste | {c['objetivo']} |",
              f"| Pré-condições / Preparação | {c['pre']} |",
              f"| Dados de entrada | `{c['entrada']}` |",
              f"| Resultado esperado | {c['esperado']} |",
              f"| Tipo | {c['tipo']} |",
              f"| Técnica | {c['tecnica']} |", "",
              "| # | Ação | Resultado esperado do passo |", "|---|---|---|"]
        for i, (a, e) in enumerate(c["passos"], 1):
            L.append(f"| {i} | {a} | {e} |")
        L.append("")
    return "\n".join(L)


def gerar_matriz_md():
    cts = [c["id"] for c in d.TEST_CASES]
    L = ["## Matriz de rastreabilidade (Feature × Caso de Teste)", "",
         "| Feature | Casos de teste | Positivos | Negativos |", "|---|---|---|---|"]
    for f in d.FEATURES:
        cs = d.casos_da_feature(f["id"])
        L.append(f"| {f['id']} — {f['titulo']} | {', '.join(c['id'] for c in cs)} | "
                 f"{sum(c['tipo'] == 'Positivo' for c in cs)} | {sum(c['tipo'] == 'Negativo' for c in cs)} |")
    return "\n".join(L + [""])


# ---------------------------------------------------------------- CSV Azure
def gerar_features_csv(path):
    with open(path, "w", newline="", encoding="utf-8") as fp:
        w = csv.writer(fp, quoting=csv.QUOTE_ALL)
        w.writerow(["ID", "Work Item Type", "Title", "Description", "Acceptance Criteria",
                    "Priority", "Business Value", "Tags"])
        for f in d.FEATURES:
            desc = f"<p>{esc(d.historia(f))}</p>"
            ac = "".join(
                f"<p><b>CA{i:02d}</b> — <b>Dado</b> {esc(a)}, <b>Quando</b> {esc(b)}, <b>Então</b> {esc(c)}.</p>"
                for i, (a, b, c) in enumerate(f["ca"], 1))
            w.writerow(["", "Feature", f"{f['id']} - {f['titulo']}", desc, ac,
                        f["prioridade"], f["bv"], f"{f['id']}; Alerta Córrego"])


def gerar_tc_csv(path):
    with open(path, "w", newline="", encoding="utf-8") as fp:
        w = csv.writer(fp, quoting=csv.QUOTE_ALL)
        w.writerow(["ID", "Work Item Type", "Title", "Test Step", "Step Action", "Step Expected",
                    "Priority", "Description", "Tags"])
        for c in d.TEST_CASES:
            f = d.feature_por_id(c["feature"])
            desc = (f"<p><b>Feature relacionada:</b> {esc(f['id'] + ' - ' + f['titulo'])}</p>"
                    f"<p><b>Objetivo do teste:</b> {esc(c['objetivo'])}</p>"
                    f"<p><b>Pré-condições / Preparação:</b> {esc(c['pre'])}</p>"
                    f"<p><b>Dados de entrada:</b> {esc(c['entrada'])}</p>"
                    f"<p><b>Resultado esperado:</b> {esc(c['esperado'])}</p>"
                    f"<p><b>Tipo:</b> {c['tipo']} &nbsp; <b>Técnica:</b> {esc(c['tecnica'])}</p>")
            tags = f"{c['feature']}; {c['tipo']}; {c['tecnica'].replace(' / ', '; ')}"
            w.writerow(["", "Test Case", f"{c['id']} - {c['titulo']}", "", "", "",
                        f["prioridade"], desc, tags])
            for i, (a, e) in enumerate(c["passos"], 1):
                w.writerow(["", "", "", i, a, e, "", "", ""])


def main():
    os.makedirs(os.path.join(AQUI, "azure-import"), exist_ok=True)
    with open(os.path.join(AQUI, "features.md"), "w", encoding="utf-8") as fp:
        fp.write(gerar_features_md())
    with open(os.path.join(AQUI, "test-cases.md"), "w", encoding="utf-8") as fp:
        fp.write(gerar_tc_md() + "\n" + gerar_matriz_md())
    gerar_features_csv(os.path.join(AQUI, "azure-import", "features.csv"))
    gerar_tc_csv(os.path.join(AQUI, "azure-import", "test-cases.csv"))
    print(f"OK: {len(d.FEATURES)} features, {len(d.TEST_CASES)} casos de teste")


if __name__ == "__main__":
    main()
