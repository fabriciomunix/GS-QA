# Casos de Teste — Alerta Córrego

Testes funcionais de caixa-preta para aceite/homologação.

## Massa de teste (seed) assumida

- **Córrego 1:** Córrego Ponte Baixa — M'Boi Mirim; nivelAlertaCm = 120; nivelCriticoCm = 180 (limite de ATENÇÃO por nível = 0,75 × 120 = 90 cm)
- **Córrego 2:** Córrego Morro do S — Campo Limpo; nivelAlertaCm = 100; nivelCriticoCm = 150
- **Sensor 1:** codigo ESP32-PB-01, corregoId = 1, ativo = true
- **Sensor 2:** codigo ESP32-MS-01, corregoId = 2, ativo = true
- **Sensor 3:** codigo ESP32-PB-02, corregoId = 1, ativo = false (criado para CT07)
- **Moradores:** 6 fictícios: 3 no córrego 1 (2 prioritários: IDOSO e CADEIRANTE; 1 NENHUMA) e 3 no córrego 2 (1 prioritário: ACAMADO; 2 NENHUMA). Dados simulados, sem CPF.
- **IDs inexistentes:** 999 (usado nos testes negativos de recurso inexistente)

## Convenções

- Erro de validação: HTTP 400 (Web API .NET) ou HTTP 422 (FastAPI). Ambos são aceitos, desde que o corpo da resposta indique o campo inválido.
- Recurso inexistente: HTTP 404 com mensagem de erro, sem stack trace.
- Criação bem-sucedida: HTTP 201 com o recurso criado (JSON em camelCase).
- Regra de risco: nível >= crítico → CRITICO; nível >= alerta → ALERTA; nível >= 0,75 × alerta OU chuva >= 30 mm/h → ATENCAO; senão NORMAL. A primeira condição verdadeira, de cima para baixo, prevalece.

## Resumo

| ID | Título | Feature | Tipo | Técnica |
|---|---|---|---|---|
| CT01 | Registrar leitura válida enviada pelo sensor | F01 | Positivo | Partição de equivalência |
| CT02 | Rejeitar leitura de sensor inexistente (404) | F01 | Negativo | Partição de equivalência |
| CT03 | Rejeitar nível de água negativo (-1 cm) | F01 | Negativo | Análise de valor-limite |
| CT04 | Aceitar nível e chuva iguais a zero (limite inferior válido) | F01 | Positivo | Análise de valor-limite |
| CT05 | Rejeitar leitura com campo obrigatório ausente | F01 | Negativo | Partição de equivalência |
| CT06 | Rejeitar chuva negativa e valor não numérico | F01 | Negativo | Análise de valor-limite / Partição de equivalência |
| CT07 | Rejeitar leitura de sensor inativo | F01 | Negativo | Partição de equivalência |
| CT08 | Classificar leitura nível 89 cm / chuva 0 mm/h como NORMAL | F02 | Positivo | Análise de valor-limite |
| CT09 | Classificar leitura nível 90 cm / chuva 0 mm/h como ATENCAO | F02 | Positivo | Análise de valor-limite |
| CT10 | Classificar leitura nível 119 cm / chuva 0 mm/h como ATENCAO | F02 | Positivo | Análise de valor-limite |
| CT11 | Classificar leitura nível 120 cm / chuva 0 mm/h como ALERTA | F02 | Positivo | Análise de valor-limite |
| CT12 | Classificar leitura nível 179 cm / chuva 0 mm/h como ALERTA | F02 | Positivo | Análise de valor-limite |
| CT13 | Classificar leitura nível 180 cm / chuva 0 mm/h como CRITICO | F02 | Positivo | Análise de valor-limite |
| CT14 | Classificar leitura nível 50 cm / chuva 29,9 mm/h como NORMAL | F02 | Positivo | Análise de valor-limite |
| CT15 | Classificar leitura nível 50 cm / chuva 30,0 mm/h como ATENCAO | F02 | Positivo | Análise de valor-limite |
| CT16 | Combinações de nível e chuva (precedência da regra) | F02 | Positivo | Tabela de decisão |
| CT17 | Gerar alerta ALERTA com lista de prioritários | F03 | Positivo | Partição de equivalência |
| CT18 | Gerar alerta CRITICO | F03 | Positivo | Partição de equivalência |
| CT19 | Não gerar alerta para leitura ATENCAO | F03 | Negativo | Partição de equivalência |
| CT20 | Encerrar alerta ativo | F03 | Positivo | Partição de equivalência |
| CT21 | Encerrar alerta inexistente (404) | F03 | Negativo | Partição de equivalência |
| CT22 | App exibe notificação de alerta em segundo plano | F03 | Positivo | Partição de equivalência |
| CT23 | Cadastrar morador com dados válidos | F04 | Positivo | Partição de equivalência |
| CT24 | Rejeitar cadastro sem nome / com nome em branco | F04 | Negativo | Partição de equivalência |
| CT25 | Validar formato do telefone | F04 | Negativo | Análise de valor-limite / Partição de equivalência |
| CT26 | Rejeitar morador vinculado a córrego inexistente | F04 | Negativo | Partição de equivalência |
| CT27 | Rejeitar tipoNecessidade fora da lista | F04 | Negativo | Partição de equivalência |
| CT28 | Atualizar dados do morador | F04 | Positivo | Partição de equivalência |
| CT29 | Marcar como prioritário morador com necessidade especial | F05 | Positivo | Partição de equivalência |
| CT30 | Listar prioritários somente do córrego informado | F05 | Positivo | Partição de equivalência |
| CT31 | Córrego sem prioritários retorna lista vazia | F05 | Negativo | Partição de equivalência |
| CT32 | Consultar status do córrego no app | F06 | Positivo | Partição de equivalência |
| CT33 | Consultar status de córrego inexistente (404) | F06 | Negativo | Partição de equivalência |
| CT34 | Status de córrego sem leituras | F06 | Negativo | Partição de equivalência |
| CT35 | App sem conexão exibe último status em cache | F06 | Negativo | Partição de equivalência |
| CT36 | Consultar histórico de leituras com limite | F07 | Positivo | Análise de valor-limite |
| CT37 | Rejeitar limite inválido no histórico | F07 | Negativo | Análise de valor-limite |
| CT38 | Listar somente alertas ativos do córrego | F07 | Positivo | Partição de equivalência |
| CT39 | Cadastrar córrego com limites válidos | F08 | Positivo | Partição de equivalência |
| CT40 | Rejeitar córrego com nível crítico <= nível de alerta | F08 | Negativo | Análise de valor-limite |
| CT41 | Rejeitar sensor com código duplicado | F08 | Negativo | Partição de equivalência |
| CT42 | Rejeitar sensor vinculado a córrego inexistente | F08 | Negativo | Partição de equivalência |
| CT43 | Logs da API sem dados pessoais/sensíveis | F09 | Negativo | Partição de equivalência |
| CT44 | Status e alertas não expõem dados de moradores | F09 | Negativo | Partição de equivalência |
| CT45 | Cadastro no app exige aceite do termo de privacidade | F09 | Negativo | Tabela de decisão |
| CT46 | Excluir dados do morador a pedido (direito de eliminação) | F09 | Positivo | Partição de equivalência |
| CT47 | Erro interno não expõe stack trace nem dados | F09 | Negativo | Partição de equivalência |

## CT01 — Registrar leitura válida enviada pelo sensor

| Campo | Valor |
|---|---|
| Feature relacionada | F01 — Monitoramento do nível do córrego |
| Objetivo do teste | Garantir que uma leitura válida de sensor ativo é gravada e classificada. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 50, "chuvaMmHora": 5}` |
| Resultado esperado | Leitura persistida, com data/hora e nivelRisco NORMAL. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com o corpo informado. | HTTP 201. |
| 2 | Conferir o corpo da resposta. | Contém id, sensorId 1, nivelAguaCm 50, chuvaMmHora 5, registradaEm preenchido e nivelRisco NORMAL. |
| 3 | Consultar GET /api/leituras?corregoId=1&limite=1. | A leitura criada é a primeira da lista. |

## CT02 — Rejeitar leitura de sensor inexistente (404)

| Campo | Valor |
|---|---|
| Feature relacionada | F01 — Monitoramento do nível do córrego |
| Objetivo do teste | Garantir que a API não aceita leitura de sensor não cadastrado. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Sensor 999 não existe. |
| Dados de entrada | `POST /api/leituras {"sensorId": 999, "nivelAguaCm": 50, "chuvaMmHora": 5}` |
| Resultado esperado | HTTP 404; nenhuma leitura gravada. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 999. | HTTP 404 com mensagem "Sensor não encontrado". |
| 2 | Consultar GET /api/leituras?corregoId=1&limite=1. | Nenhuma leitura nova foi gravada. |

## CT03 — Rejeitar nível de água negativo (-1 cm)

| Campo | Valor |
|---|---|
| Feature relacionada | F01 — Monitoramento do nível do córrego |
| Objetivo do teste | Validar o limite inferior inválido do nível de água. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": -1, "chuvaMmHora": 0}` |
| Resultado esperado | Leitura rejeitada por erro de validação; nada gravado. |
| Tipo | Negativo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com nivelAguaCm -1. | Erro de validação (400/422) indicando o campo nivelAguaCm. |
| 2 | Consultar o histórico do córrego 1. | Nenhuma leitura com nível -1 foi gravada. |

## CT04 — Aceitar nível e chuva iguais a zero (limite inferior válido)

| Campo | Valor |
|---|---|
| Feature relacionada | F01 — Monitoramento do nível do córrego |
| Objetivo do teste | Validar que 0 é o menor valor aceito para nível e chuva. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 0, "chuvaMmHora": 0}` |
| Resultado esperado | Leitura aceita e classificada como NORMAL. |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com nível 0 e chuva 0. | HTTP 201. |
| 2 | Verificar nivelRisco. | nivelRisco = NORMAL. |

## CT05 — Rejeitar leitura com campo obrigatório ausente

| Campo | Valor |
|---|---|
| Feature relacionada | F01 — Monitoramento do nível do córrego |
| Objetivo do teste | Garantir validação de campos obrigatórios da leitura. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `a) {"nivelAguaCm": 50, "chuvaMmHora": 5} (sem sensorId); b) {"sensorId": 1, "chuvaMmHora": 5} (sem nivelAguaCm); c) {"sensorId": 1, "nivelAguaCm": 50} (sem chuvaMmHora)` |
| Resultado esperado | Todas as requisições rejeitadas; nada gravado. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com o corpo (a). | Erro de validação citando sensorId. |
| 2 | Enviar POST /api/leituras com o corpo (b). | Erro de validação citando nivelAguaCm. |
| 3 | Enviar POST /api/leituras com o corpo (c). | Erro de validação citando chuvaMmHora. |
| 4 | Consultar o histórico do córrego 1. | Nenhuma das 3 leituras foi gravada. |

## CT06 — Rejeitar chuva negativa e valor não numérico

| Campo | Valor |
|---|---|
| Feature relacionada | F01 — Monitoramento do nível do córrego |
| Objetivo do teste | Validar partições inválidas do campo chuvaMmHora. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `a) {"sensorId": 1, "nivelAguaCm": 50, "chuvaMmHora": -0.1}; b) {"sensorId": 1, "nivelAguaCm": 50, "chuvaMmHora": "muita"}` |
| Resultado esperado | Ambas rejeitadas; nenhuma leitura gravada. |
| Tipo | Negativo |
| Técnica | Análise de valor-limite / Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com o corpo (a). | Erro de validação citando chuvaMmHora. |
| 2 | Enviar POST /api/leituras com o corpo (b). | Erro de validação citando chuvaMmHora. |

## CT07 — Rejeitar leitura de sensor inativo

| Campo | Valor |
|---|---|
| Feature relacionada | F01 — Monitoramento do nível do córrego |
| Objetivo do teste | Garantir que sensores desativados não alimentam a classificação. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Sensor 3 (ESP32-PB-02) cadastrado com ativo = false. |
| Dados de entrada | `POST /api/leituras {"sensorId": 3, "nivelAguaCm": 200, "chuvaMmHora": 40}` |
| Resultado esperado | Leitura rejeitada; nenhum alerta falso gerado. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 3. | Erro de validação informando sensor inativo. |
| 2 | Consultar GET /api/alertas?ativos=true&corregoId=1. | Nenhum alerta CRITICO novo foi criado. |

## CT08 — Classificar leitura nível 89 cm / chuva 0 mm/h como NORMAL

| Campo | Valor |
|---|---|
| Feature relacionada | F02 — Classificação automática de risco |
| Objetivo do teste | Validar a regra de risco no ponto logo abaixo de 0,75 × alerta (89 cm). |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com alerta = 120 cm e crítico = 180 cm. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 89, "chuvaMmHora": 0}` |
| Resultado esperado | Leitura registrada e classificada como NORMAL. Nenhum alerta é criado (campo de alerta nulo/ausente). |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 1, nivelAguaCm 89 e chuvaMmHora 0. | HTTP 201 com a leitura gravada. |
| 2 | Verificar o campo nivelRisco da resposta. | nivelRisco = NORMAL. |
| 3 | Verificar o alerta retornado na resposta. | Nenhum alerta é criado (campo de alerta nulo/ausente). |
| 4 | Consultar GET /api/corregos/1/status. | Último nível = 89 cm e nivelRisco = NORMAL. |

## CT09 — Classificar leitura nível 90 cm / chuva 0 mm/h como ATENCAO

| Campo | Valor |
|---|---|
| Feature relacionada | F02 — Classificação automática de risco |
| Objetivo do teste | Validar a regra de risco no ponto exatamente 0,75 × alerta (90 cm). |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com alerta = 120 cm e crítico = 180 cm. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 90, "chuvaMmHora": 0}` |
| Resultado esperado | Leitura registrada e classificada como ATENCAO. Nenhum alerta é criado (campo de alerta nulo/ausente). |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 1, nivelAguaCm 90 e chuvaMmHora 0. | HTTP 201 com a leitura gravada. |
| 2 | Verificar o campo nivelRisco da resposta. | nivelRisco = ATENCAO. |
| 3 | Verificar o alerta retornado na resposta. | Nenhum alerta é criado (campo de alerta nulo/ausente). |
| 4 | Consultar GET /api/corregos/1/status. | Último nível = 90 cm e nivelRisco = ATENCAO. |

## CT10 — Classificar leitura nível 119 cm / chuva 0 mm/h como ATENCAO

| Campo | Valor |
|---|---|
| Feature relacionada | F02 — Classificação automática de risco |
| Objetivo do teste | Validar a regra de risco no ponto logo abaixo do nível de alerta (119 cm). |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com alerta = 120 cm e crítico = 180 cm. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 119, "chuvaMmHora": 0}` |
| Resultado esperado | Leitura registrada e classificada como ATENCAO. Nenhum alerta é criado (campo de alerta nulo/ausente). |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 1, nivelAguaCm 119 e chuvaMmHora 0. | HTTP 201 com a leitura gravada. |
| 2 | Verificar o campo nivelRisco da resposta. | nivelRisco = ATENCAO. |
| 3 | Verificar o alerta retornado na resposta. | Nenhum alerta é criado (campo de alerta nulo/ausente). |
| 4 | Consultar GET /api/corregos/1/status. | Último nível = 119 cm e nivelRisco = ATENCAO. |

## CT11 — Classificar leitura nível 120 cm / chuva 0 mm/h como ALERTA

| Campo | Valor |
|---|---|
| Feature relacionada | F02 — Classificação automática de risco |
| Objetivo do teste | Validar a regra de risco no ponto exatamente igual ao nível de alerta (120 cm). |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com alerta = 120 cm e crítico = 180 cm. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 120, "chuvaMmHora": 0}` |
| Resultado esperado | Leitura registrada e classificada como ALERTA. Alerta ALERTA criado para o córrego 1. |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 1, nivelAguaCm 120 e chuvaMmHora 0. | HTTP 201 com a leitura gravada. |
| 2 | Verificar o campo nivelRisco da resposta. | nivelRisco = ALERTA. |
| 3 | Verificar o alerta retornado na resposta. | Alerta ALERTA criado para o córrego 1. |
| 4 | Consultar GET /api/corregos/1/status. | Último nível = 120 cm e nivelRisco = ALERTA. |

## CT12 — Classificar leitura nível 179 cm / chuva 0 mm/h como ALERTA

| Campo | Valor |
|---|---|
| Feature relacionada | F02 — Classificação automática de risco |
| Objetivo do teste | Validar a regra de risco no ponto logo abaixo do nível crítico (179 cm). |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com alerta = 120 cm e crítico = 180 cm. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 179, "chuvaMmHora": 0}` |
| Resultado esperado | Leitura registrada e classificada como ALERTA. Alerta ALERTA criado para o córrego 1. |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 1, nivelAguaCm 179 e chuvaMmHora 0. | HTTP 201 com a leitura gravada. |
| 2 | Verificar o campo nivelRisco da resposta. | nivelRisco = ALERTA. |
| 3 | Verificar o alerta retornado na resposta. | Alerta ALERTA criado para o córrego 1. |
| 4 | Consultar GET /api/corregos/1/status. | Último nível = 179 cm e nivelRisco = ALERTA. |

## CT13 — Classificar leitura nível 180 cm / chuva 0 mm/h como CRITICO

| Campo | Valor |
|---|---|
| Feature relacionada | F02 — Classificação automática de risco |
| Objetivo do teste | Validar a regra de risco no ponto exatamente igual ao nível crítico (180 cm). |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com alerta = 120 cm e crítico = 180 cm. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 180, "chuvaMmHora": 0}` |
| Resultado esperado | Leitura registrada e classificada como CRITICO. Alerta CRITICO criado para o córrego 1. |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 1, nivelAguaCm 180 e chuvaMmHora 0. | HTTP 201 com a leitura gravada. |
| 2 | Verificar o campo nivelRisco da resposta. | nivelRisco = CRITICO. |
| 3 | Verificar o alerta retornado na resposta. | Alerta CRITICO criado para o córrego 1. |
| 4 | Consultar GET /api/corregos/1/status. | Último nível = 180 cm e nivelRisco = CRITICO. |

## CT14 — Classificar leitura nível 50 cm / chuva 29,9 mm/h como NORMAL

| Campo | Valor |
|---|---|
| Feature relacionada | F02 — Classificação automática de risco |
| Objetivo do teste | Validar a regra de risco no ponto de chuva logo abaixo de 30 mm/h (29,9). |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com alerta = 120 cm e crítico = 180 cm. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 50, "chuvaMmHora": 29.9}` |
| Resultado esperado | Leitura registrada e classificada como NORMAL. Nenhum alerta é criado (campo de alerta nulo/ausente). |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 1, nivelAguaCm 50 e chuvaMmHora 29.9. | HTTP 201 com a leitura gravada. |
| 2 | Verificar o campo nivelRisco da resposta. | nivelRisco = NORMAL. |
| 3 | Verificar o alerta retornado na resposta. | Nenhum alerta é criado (campo de alerta nulo/ausente). |
| 4 | Consultar GET /api/corregos/1/status. | Último nível = 50 cm e nivelRisco = NORMAL. |

## CT15 — Classificar leitura nível 50 cm / chuva 30,0 mm/h como ATENCAO

| Campo | Valor |
|---|---|
| Feature relacionada | F02 — Classificação automática de risco |
| Objetivo do teste | Validar a regra de risco no ponto de chuva exatamente igual a 30 mm/h. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com alerta = 120 cm e crítico = 180 cm. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 50, "chuvaMmHora": 30.0}` |
| Resultado esperado | Leitura registrada e classificada como ATENCAO. Nenhum alerta é criado (campo de alerta nulo/ausente). |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/leituras com sensorId 1, nivelAguaCm 50 e chuvaMmHora 30.0. | HTTP 201 com a leitura gravada. |
| 2 | Verificar o campo nivelRisco da resposta. | nivelRisco = ATENCAO. |
| 3 | Verificar o alerta retornado na resposta. | Nenhum alerta é criado (campo de alerta nulo/ausente). |
| 4 | Consultar GET /api/corregos/1/status. | Último nível = 50 cm e nivelRisco = ATENCAO. |

## CT16 — Combinações de nível e chuva (precedência da regra)

| Campo | Valor |
|---|---|
| Feature relacionada | F02 — Classificação automática de risco |
| Objetivo do teste | Validar que a condição mais grave prevalece quando nível e chuva disparam regras diferentes. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com alerta = 120 cm e crítico = 180 cm. |
| Dados de entrada | `Tabela de decisão — (nível cm; chuva mm/h → risco): R1 (200; 0 → CRITICO); R2 (200; 50 → CRITICO); R3 (130; 50 → ALERTA); R4 (100; 50 → ATENCAO); R5 (40; 50 → ATENCAO); R6 (40; 10 → NORMAL)` |
| Resultado esperado | Cada combinação recebe exatamente o risco da tabela de decisão. |
| Tipo | Positivo |
| Técnica | Tabela de decisão |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar leitura R1 (200; 0). | nivelRisco = CRITICO. |
| 2 | Enviar leitura R2 (200; 50). | nivelRisco = CRITICO (chuva não rebaixa nem eleva). |
| 3 | Enviar leitura R3 (130; 50). | nivelRisco = ALERTA (não fica em ATENCAO por causa da chuva). |
| 4 | Enviar leitura R4 (100; 50). | nivelRisco = ATENCAO. |
| 5 | Enviar leitura R5 (40; 50). | nivelRisco = ATENCAO (apenas pela chuva). |
| 6 | Enviar leitura R6 (40; 10). | nivelRisco = NORMAL. |

## CT17 — Gerar alerta ALERTA com lista de prioritários

| Campo | Valor |
|---|---|
| Feature relacionada | F03 — Emissão de alertas |
| Objetivo do teste | Garantir criação de alerta e identificação de prioritários ao atingir ALERTA. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Nenhum alerta ativo para o córrego 1. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 140, "chuvaMmHora": 20}` |
| Resultado esperado | Alerta ativo criado e prioritários do córrego 1 identificados. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar a leitura. | HTTP 201 com nivelRisco = ALERTA. |
| 2 | Verificar o alerta na resposta. | Alerta com corregoId 1, nivelRisco ALERTA, nivelAguaCm 140, mensagem com o nome do córrego, ativo = true. |
| 3 | Verificar a lista de prioritários na resposta. | Contém os 2 moradores prioritários do córrego 1 e nenhum do córrego 2. |
| 4 | Consultar GET /api/alertas?ativos=true&corregoId=1. | O alerta criado aparece na lista. |

## CT18 — Gerar alerta CRITICO

| Campo | Valor |
|---|---|
| Feature relacionada | F03 — Emissão de alertas |
| Objetivo do teste | Garantir criação de alerta com nível CRITICO. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 185, "chuvaMmHora": 45}` |
| Resultado esperado | Alerta CRITICO ativo criado para o córrego 1. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar a leitura. | HTTP 201 com nivelRisco = CRITICO. |
| 2 | Verificar o alerta na resposta. | Alerta com nivelRisco CRITICO, nivelAguaCm 185, ativo = true. |

## CT19 — Não gerar alerta para leitura ATENCAO

| Campo | Valor |
|---|---|
| Feature relacionada | F03 — Emissão de alertas |
| Objetivo do teste | Evitar alarmes falsos: ATENCAO não deve criar Alerta. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Nenhum alerta ativo para o córrego 1. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 100, "chuvaMmHora": 10}` |
| Resultado esperado | Nenhum alerta criado. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar a leitura. | HTTP 201 com nivelRisco = ATENCAO e sem alerta na resposta. |
| 2 | Consultar GET /api/alertas?ativos=true&corregoId=1. | Lista vazia. |

## CT20 — Encerrar alerta ativo

| Campo | Valor |
|---|---|
| Feature relacionada | F03 — Emissão de alertas |
| Objetivo do teste | Validar o encerramento de alerta pelo operador. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Alerta ativo existente para o córrego 1 (ex.: gerado no CT17), id anotado. |
| Dados de entrada | `PATCH /api/alertas/{id}/encerrar` |
| Resultado esperado | Alerta encerrado e fora da lista de ativos. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar PATCH /api/alertas/{id}/encerrar. | HTTP 200 com ativo = false. |
| 2 | Consultar GET /api/alertas?ativos=true&corregoId=1. | O alerta encerrado não aparece. |

## CT21 — Encerrar alerta inexistente (404)

| Campo | Valor |
|---|---|
| Feature relacionada | F03 — Emissão de alertas |
| Objetivo do teste | Validar tratamento de id de alerta inexistente. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Alerta 999 não existe. |
| Dados de entrada | `PATCH /api/alertas/999/encerrar` |
| Resultado esperado | HTTP 404. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar PATCH /api/alertas/999/encerrar. | HTTP 404 com mensagem de erro, sem stack trace. |

## CT22 — App exibe notificação de alerta em segundo plano

| Campo | Valor |
|---|---|
| Feature relacionada | F03 — Emissão de alertas |
| Objetivo do teste | Validar que o morador é avisado pelo app quando um alerta é criado. |
| Pré-condições / Preparação | App instalado no celular, morador cadastrado no córrego 1, permissão de notificação concedida, app em segundo plano. |
| Dados de entrada | `POST /api/leituras {"sensorId": 1, "nivelAguaCm": 150, "chuvaMmHora": 35}` |
| Resultado esperado | Morador notificado e levado ao status atualizado. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar a leitura pela API. | Alerta ALERTA criado. |
| 2 | Observar o celular. | Notificação exibida com "ALERTA" e a mensagem do córrego Ponte Baixa. |
| 3 | Tocar na notificação. | O app abre na tela de status do córrego 1 em cor laranja. |

## CT23 — Cadastrar morador com dados válidos

| Campo | Valor |
|---|---|
| Feature relacionada | F04 — Cadastro de morador |
| Objetivo do teste | Validar o cadastro completo de um morador. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `POST /api/moradores {"nome": "Maria Teste", "telefone": "11987654321", "endereco": "Rua Fictícia, 10", "corregoId": 1, "tipoNecessidade": "NENHUMA"}` |
| Resultado esperado | Morador gravado corretamente. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/moradores. | HTTP 201. |
| 2 | Conferir a resposta. | id e criadoEm preenchidos; prioritario = false. |
| 3 | Consultar GET /api/moradores/{id}. | Mesmos dados enviados. |

## CT24 — Rejeitar cadastro sem nome / com nome em branco

| Campo | Valor |
|---|---|
| Feature relacionada | F04 — Cadastro de morador |
| Objetivo do teste | Validar campo obrigatório nome. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `a) corpo do CT23 sem "nome"; b) "nome": "   " (só espaços)` |
| Resultado esperado | Cadastro rejeitado. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar o corpo (a). | Erro de validação citando nome. |
| 2 | Enviar o corpo (b). | Erro de validação citando nome. |
| 3 | Consultar GET /api/moradores. | Nenhum morador novo gravado. |

## CT25 — Validar formato do telefone

| Campo | Valor |
|---|---|
| Feature relacionada | F04 — Cadastro de morador |
| Objetivo do teste | Validar partições e limites do telefone (DDD + 8 ou 9 dígitos = 10 ou 11 dígitos). |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `Corpo do CT23 variando "telefone": a) "119876543" (9 dígitos); b) "1198765432" (10); c) "11987654321" (11); d) "119876543210" (12); e) "11abc654321"` |
| Resultado esperado | Somente telefones com 10 ou 11 dígitos numéricos são aceitos. |
| Tipo | Negativo |
| Técnica | Análise de valor-limite / Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar com telefone (a). | Erro de validação no telefone. |
| 2 | Enviar com telefone (b). | HTTP 201 (fixo com 8 dígitos). |
| 3 | Enviar com telefone (c). | HTTP 201 (celular com 9 dígitos). |
| 4 | Enviar com telefone (d). | Erro de validação no telefone. |
| 5 | Enviar com telefone (e). | Erro de validação no telefone. |

## CT26 — Rejeitar morador vinculado a córrego inexistente

| Campo | Valor |
|---|---|
| Feature relacionada | F04 — Cadastro de morador |
| Objetivo do teste | Garantir integridade do vínculo morador–córrego. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 999 não existe. |
| Dados de entrada | `Corpo do CT23 com "corregoId": 999` |
| Resultado esperado | Cadastro rejeitado. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/moradores. | HTTP 404 ou erro de validação citando corregoId. |
| 2 | Consultar GET /api/moradores. | Morador não gravado. |

## CT27 — Rejeitar tipoNecessidade fora da lista

| Campo | Valor |
|---|---|
| Feature relacionada | F04 — Cadastro de morador |
| Objetivo do teste | Validar o domínio (enum) de tipoNecessidade. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `Corpo do CT23 com "tipoNecessidade": "GESTANTE" e depois "idoso" (minúsculo)` |
| Resultado esperado | Valores fora do enum não são gravados. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar com "GESTANTE". | Erro de validação listando os valores permitidos. |
| 2 | Enviar com "idoso". | Erro de validação (ou aceito como IDOSO, se a API normaliza — registrar o comportamento). |

## CT28 — Atualizar dados do morador

| Campo | Valor |
|---|---|
| Feature relacionada | F04 — Cadastro de morador |
| Objetivo do teste | Validar alteração cadastral via PUT. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Morador criado no CT23 (id anotado). |
| Dados de entrada | `PUT /api/moradores/{id} com "telefone": "11912345678" e "endereco": "Rua Nova, 20"` |
| Resultado esperado | Dados atualizados; id inexistente retorna 404. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar o PUT. | HTTP 200. |
| 2 | Consultar GET /api/moradores/{id}. | Telefone e endereço atualizados; demais campos inalterados. |
| 3 | Executar PUT /api/moradores/999. | HTTP 404. |

## CT29 — Marcar como prioritário morador com necessidade especial

| Campo | Valor |
|---|---|
| Feature relacionada | F05 — Priorização de moradores com mobilidade reduzida |
| Objetivo do teste | Validar a derivação de prioritario a partir de tipoNecessidade. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `Corpo do CT23 com "nome": "José Teste" e "tipoNecessidade": "CADEIRANTE"` |
| Resultado esperado | Morador cadeirante cadastrado como prioritário. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/moradores. | HTTP 201 com prioritario = true. |
| 2 | Consultar GET /api/moradores/prioritarios?corregoId=1. | José Teste aparece na lista. |

## CT30 — Listar prioritários somente do córrego informado

| Campo | Valor |
|---|---|
| Feature relacionada | F05 — Priorização de moradores com mobilidade reduzida |
| Objetivo do teste | Garantir o filtro por córrego e a exclusão de não prioritários. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `GET /api/moradores/prioritarios?corregoId=1 e ?corregoId=2` |
| Resultado esperado | Listas filtradas corretamente. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Consultar com corregoId=1. | Somente os 2 prioritários do córrego 1 (IDOSO e CADEIRANTE). |
| 2 | Verificar se há moradores com tipoNecessidade NENHUMA. | Nenhum morador NENHUMA na lista. |
| 3 | Consultar com corregoId=2. | Somente o prioritário ACAMADO do córrego 2. |

## CT31 — Córrego sem prioritários retorna lista vazia

| Campo | Valor |
|---|---|
| Feature relacionada | F05 — Priorização de moradores com mobilidade reduzida |
| Objetivo do teste | Validar resposta para córrego sem moradores prioritários. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 3 criado (CT39) sem moradores. |
| Dados de entrada | `GET /api/moradores/prioritarios?corregoId=3` |
| Resultado esperado | Lista vazia, sem erro. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Consultar a lista. | HTTP 200 com lista vazia []. |

## CT32 — Consultar status do córrego no app

| Campo | Valor |
|---|---|
| Feature relacionada | F06 — Consulta de status pelo app |
| Objetivo do teste | Validar a tela de status com nível, chuva, risco e cor. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Última leitura do córrego 1: nível 100 cm, chuva 10 mm/h (ATENCAO). App com conexão. |
| Dados de entrada | `Abrir o app logado como morador do córrego 1 (GET /api/corregos/1/status)` |
| Resultado esperado | Status correto e legível. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Abrir o app na tela inicial. | Tela de status do córrego Ponte Baixa é exibida. |
| 2 | Conferir os valores. | Nível 100 cm, chuva 10 mm/h, data/hora da leitura. |
| 3 | Conferir o indicador de risco. | Texto ATENCAO em cor amarela. |

## CT33 — Consultar status de córrego inexistente (404)

| Campo | Valor |
|---|---|
| Feature relacionada | F06 — Consulta de status pelo app |
| Objetivo do teste | Validar tratamento de córrego inexistente. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `GET /api/corregos/999/status` |
| Resultado esperado | HTTP 404. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar a requisição. | HTTP 404 com mensagem "Córrego não encontrado". |

## CT34 — Status de córrego sem leituras

| Campo | Valor |
|---|---|
| Feature relacionada | F06 — Consulta de status pelo app |
| Objetivo do teste | Validar o comportamento quando ainda não há leituras. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 3 criado (CT39) sem sensor/leituras. |
| Dados de entrada | `GET /api/corregos/3/status; app aberto no córrego 3` |
| Resultado esperado | Ausência de dados tratada sem erro. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar a requisição. | HTTP 200 com nível/chuva nulos (sem inventar valores). |
| 2 | Abrir o status no app. | Mensagem "Sem leituras registradas"; app não trava. |

## CT35 — App sem conexão exibe último status em cache

| Campo | Valor |
|---|---|
| Feature relacionada | F06 — Consulta de status pelo app |
| Objetivo do teste | Validar o comportamento offline do app. |
| Pré-condições / Preparação | App aberto ao menos uma vez com conexão (status do córrego 1 salvo). Em seguida, ativar modo avião. |
| Dados de entrada | `Modo avião ativado` |
| Resultado esperado | App utilizável offline, indicando claramente que os dados podem estar desatualizados. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Fechar e reabrir o app em modo avião. | App abre sem fechar inesperadamente. |
| 2 | Conferir a tela de status. | Último status salvo + aviso "Sem conexão — dados de <data/hora>". |
| 3 | Puxar para atualizar. | Mensagem de falta de conexão; dados antigos permanecem. |
| 4 | Desativar o modo avião e atualizar. | Status atualizado e aviso removido. |

## CT36 — Consultar histórico de leituras com limite

| Campo | Valor |
|---|---|
| Feature relacionada | F07 — Histórico de leituras e alertas |
| Objetivo do teste | Validar filtro por córrego, limite e ordenação do histórico. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com pelo menos 6 leituras. |
| Dados de entrada | `GET /api/leituras?corregoId=1&limite=5` |
| Resultado esperado | Histórico filtrado, limitado e ordenado. |
| Tipo | Positivo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar a requisição. | HTTP 200 com exatamente 5 leituras. |
| 2 | Conferir o sensor de cada leitura. | Todas pertencem a sensores do córrego 1. |
| 3 | Conferir a ordem. | Ordenadas por registradaEm, da mais recente para a mais antiga. |

## CT37 — Rejeitar limite inválido no histórico

| Campo | Valor |
|---|---|
| Feature relacionada | F07 — Histórico de leituras e alertas |
| Objetivo do teste | Validar valores-limite e partições inválidas do parâmetro limite. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `limite = 0; limite = -1; limite = abc; limite = 1` |
| Resultado esperado | Somente limite >= 1 é aceito. |
| Tipo | Negativo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | GET /api/leituras?corregoId=1&limite=0. | Erro de validação. |
| 2 | GET /api/leituras?corregoId=1&limite=-1. | Erro de validação. |
| 3 | GET /api/leituras?corregoId=1&limite=abc. | Erro de validação. |
| 4 | GET /api/leituras?corregoId=1&limite=1. | HTTP 200 com 1 leitura (limite mínimo válido). |

## CT38 — Listar somente alertas ativos do córrego

| Campo | Valor |
|---|---|
| Feature relacionada | F07 — Histórico de leituras e alertas |
| Objetivo do teste | Validar os filtros ativos e corregoId da lista de alertas. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Córrego 1 com 1 alerta ativo e 1 encerrado; córrego 2 com 1 alerta ativo. |
| Dados de entrada | `GET /api/alertas?ativos=true&corregoId=1` |
| Resultado esperado | Apenas alertas ativos do córrego 1. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar a requisição. | HTTP 200 com 1 alerta. |
| 2 | Conferir o alerta. | ativo = true e corregoId = 1; o encerrado e o do córrego 2 não aparecem. |

## CT39 — Cadastrar córrego com limites válidos

| Campo | Valor |
|---|---|
| Feature relacionada | F08 — Gestão de córregos e sensores |
| Objetivo do teste | Validar o cadastro de um novo córrego (gera o córrego 3 usado em outros CTs). |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `POST /api/corregos {"nome": "Córrego Teste", "bairro": "Jardim Ângela", "latitude": -23.70, "longitude": -46.77, "nivelAlertaCm": 100, "nivelCriticoCm": 160}` |
| Resultado esperado | Córrego criado. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/corregos. | HTTP 201 com id gerado (anotar como córrego 3). |
| 2 | Consultar GET /api/corregos/{id}. | Mesmos dados enviados. |

## CT40 — Rejeitar córrego com nível crítico <= nível de alerta

| Campo | Valor |
|---|---|
| Feature relacionada | F08 — Gestão de córregos e sensores |
| Objetivo do teste | Validar a coerência entre os limites do córrego. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `Corpo do CT39 com: a) alerta 120 / crítico 120; b) alerta 120 / crítico 100; c) alerta 120 / crítico 121; d) alerta 0 / crítico 50` |
| Resultado esperado | Somente nivelCriticoCm > nivelAlertaCm > 0 é aceito. |
| Tipo | Negativo |
| Técnica | Análise de valor-limite |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar (a) — crítico igual ao alerta. | Erro de validação. |
| 2 | Enviar (b) — crítico menor que alerta. | Erro de validação. |
| 3 | Enviar (c) — crítico 1 cm acima. | HTTP 201 (menor valor válido). |
| 4 | Enviar (d) — alerta zero. | Erro de validação. |

## CT41 — Rejeitar sensor com código duplicado

| Campo | Valor |
|---|---|
| Feature relacionada | F08 — Gestão de córregos e sensores |
| Objetivo do teste | Garantir unicidade do código do sensor. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Sensor ESP32-PB-01 já existe. |
| Dados de entrada | `POST /api/sensores {"codigo": "ESP32-PB-01", "corregoId": 1, "ativo": true}` |
| Resultado esperado | Sensor duplicado não é gravado. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/sensores. | HTTP 409 (ou erro de validação) informando código duplicado. |
| 2 | Consultar GET /api/sensores. | Existe apenas um sensor ESP32-PB-01. |

## CT42 — Rejeitar sensor vinculado a córrego inexistente

| Campo | Valor |
|---|---|
| Feature relacionada | F08 — Gestão de córregos e sensores |
| Objetivo do teste | Garantir integridade do vínculo sensor–córrego. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `POST /api/sensores {"codigo": "ESP32-XX-99", "corregoId": 999, "ativo": true}; GET /api/corregos/999` |
| Resultado esperado | Sensor não gravado; córrego inexistente retorna 404. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar POST /api/sensores. | HTTP 404 ou erro de validação citando corregoId. |
| 2 | Executar GET /api/corregos/999. | HTTP 404. |

## CT43 — Logs da API sem dados pessoais/sensíveis

| Campo | Valor |
|---|---|
| Feature relacionada | F09 — Proteção de dados pessoais (LGPD) |
| Objetivo do teste | Verificar conformidade com a LGPD nos logs da aplicação. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Acesso ao console/arquivo de log da API. |
| Dados de entrada | `Cadastro do CT29 (telefone 11987654321, endereço "Rua Fictícia, 10", CADEIRANTE) e um PUT no mesmo morador` |
| Resultado esperado | Nenhum dado pessoal ou sensível nos logs. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar o cadastro e a alteração. | HTTP 201 e HTTP 200. |
| 2 | Pesquisar no log por "11987654321". | Nenhuma ocorrência. |
| 3 | Pesquisar no log por "Rua Fictícia" e "CADEIRANTE". | Nenhuma ocorrência. |
| 4 | Verificar o registro da operação. | Log contém apenas operação, id do morador e data/hora. |

## CT44 — Status e alertas não expõem dados de moradores

| Campo | Valor |
|---|---|
| Feature relacionada | F09 — Proteção de dados pessoais (LGPD) |
| Objetivo do teste | Garantir minimização de dados nas rotas consultadas pelo app. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Alerta ativo no córrego 1. |
| Dados de entrada | `GET /api/corregos/1/status; GET /api/alertas?ativos=true&corregoId=1` |
| Resultado esperado | Nenhum dado pessoal nas respostas públicas. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar GET /status e inspecionar o JSON. | Sem campos nome, telefone, endereco ou tipoNecessidade. |
| 2 | Executar GET /alertas e inspecionar o JSON. | Sem campos nome, telefone, endereco ou tipoNecessidade. |

## CT45 — Cadastro no app exige aceite do termo de privacidade

| Campo | Valor |
|---|---|
| Feature relacionada | F09 — Proteção de dados pessoais (LGPD) |
| Objetivo do teste | Validar consentimento antes do envio de dado sensível (condição de saúde/mobilidade). |
| Pré-condições / Preparação | App instalado, tela de cadastro aberta. |
| Dados de entrada | `Nome, telefone, endereço, córrego e necessidade IDOSO preenchidos; termo NÃO marcado` |
| Resultado esperado | Nada é enviado sem consentimento. |
| Tipo | Negativo |
| Técnica | Tabela de decisão |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Preencher os campos sem marcar o aceite. | Botão "Cadastrar" desabilitado. |
| 2 | Marcar o aceite do termo. | Botão "Cadastrar" habilitado. |
| 3 | Tocar em "Cadastrar". | Cadastro enviado; mensagem de sucesso. |

## CT46 — Excluir dados do morador a pedido (direito de eliminação)

| Campo | Valor |
|---|---|
| Feature relacionada | F09 — Proteção de dados pessoais (LGPD) |
| Objetivo do teste | Validar a eliminação dos dados pessoais do titular. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. Morador criado no CT23 (id anotado). |
| Dados de entrada | `DELETE /api/moradores/{id}; DELETE /api/moradores/999` |
| Resultado esperado | Dados eliminados; id inexistente retorna 404. |
| Tipo | Positivo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Executar DELETE /api/moradores/{id}. | HTTP 204 (ou 200). |
| 2 | Executar GET /api/moradores/{id}. | HTTP 404. |
| 3 | Consultar a lista de prioritários do córrego 1. | O morador excluído não aparece. |
| 4 | Executar DELETE /api/moradores/999. | HTTP 404. |

## CT47 — Erro interno não expõe stack trace nem dados

| Campo | Valor |
|---|---|
| Feature relacionada | F09 — Proteção de dados pessoais (LGPD) |
| Objetivo do teste | Garantir que mensagens de erro não vazam informação técnica ou pessoal. |
| Pré-condições / Preparação | Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta. |
| Dados de entrada | `POST /api/moradores com JSON malformado: {"nome": "Ana", "telefone": }` |
| Resultado esperado | Erro tratado sem vazamento de informação. |
| Tipo | Negativo |
| Técnica | Partição de equivalência |

| # | Ação | Resultado esperado do passo |
|---|---|---|
| 1 | Enviar a requisição. | HTTP 400/422 com mensagem genérica de corpo inválido. |
| 2 | Inspecionar o corpo da resposta. | Sem stack trace, SQL, caminhos de arquivo ou dados de outros moradores. |

## Matriz de rastreabilidade (Feature × Caso de Teste)

| Feature | Casos de teste | Positivos | Negativos |
|---|---|---|---|
| F01 — Monitoramento do nível do córrego | CT01, CT02, CT03, CT04, CT05, CT06, CT07 | 2 | 5 |
| F02 — Classificação automática de risco | CT08, CT09, CT10, CT11, CT12, CT13, CT14, CT15, CT16 | 9 | 0 |
| F03 — Emissão de alertas | CT17, CT18, CT19, CT20, CT21, CT22 | 4 | 2 |
| F04 — Cadastro de morador | CT23, CT24, CT25, CT26, CT27, CT28 | 2 | 4 |
| F05 — Priorização de moradores com mobilidade reduzida | CT29, CT30, CT31 | 2 | 1 |
| F06 — Consulta de status pelo app | CT32, CT33, CT34, CT35 | 1 | 3 |
| F07 — Histórico de leituras e alertas | CT36, CT37, CT38 | 2 | 1 |
| F08 — Gestão de córregos e sensores | CT39, CT40, CT41, CT42 | 1 | 3 |
| F09 — Proteção de dados pessoais (LGPD) | CT43, CT44, CT45, CT46, CT47 | 1 | 4 |
