# GS 2026 — Alerta Córrego — Testing, Compliance & Quality Assurance

Entrega de QA da CitizenTech **Alerta Córrego**: Features com critérios de aceite e casos de teste funcionais
(caixa-preta, positivos e negativos) para montar no Azure DevOps (Boards + Test Plans).

## Ficha da CitizenTech — Alerta Córrego

| Campo | Preenchimento |
|---|---|
| **Nome da CitizenTech** | Alerta Córrego |
| **Cidade e bairro** | São Paulo — M'Boi Mirim (Zona Sul) |
| **Cidadão beneficiado** | Morador de rua às margens de córrego com risco de alagamento, com prioridade para idosos e pessoas com mobilidade reduzida |
| **Problema, em uma frase** | Moradores de ruas às margens de córregos pequenos recebem o alerta de chuva da Defesa Civil para a região inteira, mas não sabem quando o córrego da rua deles vai transbordar, e quem tem mobilidade reduzida depende de vizinhos para sair a tempo. |
| **Como funciona** | Um ESP32 no córrego mede o nível da água e a chuva e publica via MQTT. Um servidor Linux recebe as leituras, classifica o risco (Normal / Atenção / Evacuar) e mostra um painel web com a rede de apoio aos moradores prioritários. Um modelo de ML antecipa temporais, e os dados sensíveis dos moradores são auditados e protegidos. |
| **Diferencial** | Complementa a Defesa Civil: o alerta oficial avisa que vai chover na região; o Alerta Córrego avisa que a água está subindo naquela rua e quem precisa de ajuda primeiro. |
| **O que cada parte faz** | **Physical Computing:** estação ESP32 no Wokwi (nível do córrego, chuva, LEDs, sirene, LCD, MQTT) · **Operating Systems:** servidor Linux provisionado por Shell Script, monitorado e tolerante a falhas, que hospeda o painel · **IA & ML:** XGBoost que prevê chuva forte nas próximas 3 h para antecipar o alerta · **Cybersecurity:** CitizenGuard, que detecta dados pessoais e sensíveis, rastreia vazamentos (taint analysis), traduz falhas em alertas por IA e mede o Risco Cidadão |
| **Link do repositório** | **QA (este repositório): https://github.com/fabriciomunix/GS-QA** · Mobile: https://github.com/fabriciomunix/GS-Mobile · SOA: https://github.com/fabriciomunix/Gs-soa · C#: https://github.com/fabriciomunix/Gs-c- |
| **Indicador de impacto** | Minutos de antecedência entre o alerta e o transbordamento; nº de moradores prioritários alertados; Risco Cidadão dos dados cadastrados |
| **ODS conectados** | ODS 11 (cidades resilientes, meta 11.5) · ODS 13 (adaptação ao clima, meta 13.1) · ODS 10 (inclusão de idosos e PcD) |

Integrantes: Fabricio Carlos Duarte Rossi Junior (RM 555017) · Arnaldo Filho (RM 555780) — Turma 3ES

Repositórios: [Mobile](https://github.com/fabriciomunix/GS-Mobile) ·
[SOA](https://github.com/fabriciomunix/Gs-soa) · [C#](https://github.com/fabriciomunix/Gs-c-) ·
[QA](https://github.com/fabriciomunix/GS-QA)

## Conteúdo

| Arquivo | O que é |
|---|---|
| `features.md` | 9 Features (F01–F09): história de usuário, critérios de aceite CA01… (Dado/Quando/Então), Prioridade, Business Value |
| `test-cases.md` | 47 casos de teste (24 positivos, 23 negativos), com massa de teste, convenções e matriz de rastreabilidade |
| `azure-import/features.csv` | Features no formato de importação CSV do Azure Boards |
| `azure-import/test-cases.csv` | Test Cases no formato CSV do Azure (uma linha por passo: Test Step / Step Action / Step Expected) |
| `azure-import/COMO_IMPORTAR.md` | Passo a passo: criar o projeto, importar, vincular (Tested By), Test Plan, professor como admin, prints |
| `GS_QA_Alerta_Corrego.pdf` | Documento de entrega (capa, ficha, features, casos de teste, matriz, anexo para os prints) |
| `GS_QA_Alerta_Corrego.docx` | Mesmo documento em Word, para colar os prints e o link e exportar o PDF final |
| `dados.py` | **Fonte única** de todas as Features e Casos de Teste |
| `gerar_artefatos.py` | Gera os `.md` e os `.csv` |
| `gerar_pdf.py` | Gera o PDF (reportlab) |
| `gerar_docx.py` | Gera o DOCX (python-docx) |

## Regerar tudo após editar `dados.py`

```bash
cd qa
python3 gerar_artefatos.py && python3 gerar_pdf.py && python3 gerar_docx.py
```

## Cobertura

| Feature | Casos de teste |
|---|---|
| F01 Monitoramento do nível do córrego | CT01–CT07 |
| F02 Classificação automática de risco | CT08–CT16 (valores-limite 89/90, 119/120, 179/180 cm; chuva 29,9/30,0 mm/h; tabela de decisão) |
| F03 Emissão de alertas | CT17–CT22 |
| F04 Cadastro de morador | CT23–CT28 |
| F05 Priorização de moradores com mobilidade reduzida | CT29–CT31 |
| F06 Consulta de status pelo app (inclui offline) | CT32–CT35 |
| F07 Histórico de leituras e alertas | CT36–CT38 |
| F08 Gestão de córregos e sensores | CT39–CT42 |
| F09 Proteção de dados pessoais (LGPD) | CT43–CT47 |

Técnicas: partição de equivalência, análise de valor-limite e tabela de decisão.

## Premissas adotadas (alinhar com Mobile/SOA/C# se necessário)

- Massa de teste: córrego 1 (Ponte Baixa) com alerta 120 cm e crítico 180 cm; córrego 2 com 100/150; sensor 3 inativo.
- Erro de validação aceito como HTTP 400 (.NET) ou 422 (FastAPI).
- `prioritario` é marcado automaticamente quando `tipoNecessidade` ≠ NENHUMA (CT29).
- Telefone válido = 10 ou 11 dígitos numéricos (DDD + número).
- O app exige aceite do termo de privacidade antes de enviar o cadastro (CT45) e mantém o último status em cache offline (CT35).
- Leitura de sensor inativo é rejeitada (CT07); código de sensor é único (CT41); `nivelCriticoCm > nivelAlertaCm > 0` (CT40).
