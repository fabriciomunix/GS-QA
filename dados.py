# -*- coding: utf-8 -*-
"""Fonte única de verdade: Features e Casos de Teste do Alerta Córrego.

Todos os artefatos (features.md, test-cases.md, CSVs do Azure, PDF e DOCX)
são gerados a partir deste arquivo. Para alterar um texto, altere aqui e
rode novamente os scripts (ver README.md).
"""

PROJETO = "Alerta Córrego"
DISCIPLINA = "Testing, Compliance & Quality Assurance"
TURMA = "3ES"
INTEGRANTES = [
    ("Fabricio Carlos Duarte Rossi Junior", "555017"),
    ("Arnaldo Filho", "555780"),
]

# Massa de teste (seed) assumida por todos os casos de teste.
MASSA = [
    ("Córrego 1", "Córrego Ponte Baixa — M'Boi Mirim; nivelAlertaCm = 120; nivelCriticoCm = 180 "
                  "(limite de ATENÇÃO por nível = 0,75 × 120 = 90 cm)"),
    ("Córrego 2", "Córrego Morro do S — Campo Limpo; nivelAlertaCm = 100; nivelCriticoCm = 150"),
    ("Sensor 1", "codigo ESP32-PB-01, corregoId = 1, ativo = true"),
    ("Sensor 2", "codigo ESP32-MS-01, corregoId = 2, ativo = true"),
    ("Sensor 3", "codigo ESP32-PB-02, corregoId = 1, ativo = false (criado para CT07)"),
    ("Moradores", "6 fictícios: 3 no córrego 1 (2 prioritários: IDOSO e CADEIRANTE; 1 NENHUMA) e "
                  "3 no córrego 2 (1 prioritário: ACAMADO; 2 NENHUMA). Dados simulados, sem CPF."),
    ("IDs inexistentes", "999 (usado nos testes negativos de recurso inexistente)"),
]

CONVENCOES = [
    "Erro de validação: HTTP 400 (Web API .NET) ou HTTP 422 (FastAPI). Ambos são aceitos, "
    "desde que o corpo da resposta indique o campo inválido.",
    "Recurso inexistente: HTTP 404 com mensagem de erro, sem stack trace.",
    "Criação bem-sucedida: HTTP 201 com o recurso criado (JSON em camelCase).",
    "Regra de risco: nível >= crítico → CRITICO; nível >= alerta → ALERTA; "
    "nível >= 0,75 × alerta OU chuva >= 30 mm/h → ATENCAO; senão NORMAL. "
    "A primeira condição verdadeira, de cima para baixo, prevalece.",
]

# ---------------------------------------------------------------------------
# FEATURES
# ---------------------------------------------------------------------------
# Prioridade no Azure: 1 (mais alta) a 4. Business Value: inteiro (maior = mais valor).
FEATURES = [
    {
        "id": "F01",
        "titulo": "Monitoramento do nível do córrego",
        "persona": "morador de área de risco de alagamento",
        "acao": "que o sensor ESP32 instalado no córrego envie automaticamente o nível da água e a chuva para o sistema",
        "beneficio": "ter uma medição real do córrego da minha rua, e não apenas a previsão de chuva da região inteira",
        "prioridade": 1,
        "bv": 100,
        "ca": [
            ("um sensor ativo cadastrado",
             "o sensor envia POST /api/leituras com sensorId, nivelAguaCm e chuvaMmHora válidos",
             "a leitura é gravada com data/hora (registradaEm) e a API responde HTTP 201 com a leitura e o nivelRisco calculado"),
            ("um sensorId que não existe",
             "uma leitura é enviada com esse sensorId",
             "a API responde HTTP 404 e nenhuma leitura é gravada"),
            ("um sensor cadastrado com ativo = false",
             "uma leitura é enviada por esse sensor",
             "a leitura é rejeitada com erro de validação e nenhuma leitura é gravada"),
            ("uma leitura com nivelAguaCm ou chuvaMmHora negativos",
             "ela é enviada à API",
             "a API responde erro de validação indicando o campo inválido (0 é o menor valor aceito)"),
            ("uma leitura sem um dos campos obrigatórios (sensorId, nivelAguaCm, chuvaMmHora)",
             "ela é enviada à API",
             "a API responde erro de validação informando o campo ausente"),
        ],
    },
    {
        "id": "F02",
        "titulo": "Classificação automática de risco",
        "persona": "agente da Defesa Civil / operador do painel",
        "acao": "que cada leitura seja classificada automaticamente em NORMAL, ATENCAO, ALERTA ou CRITICO",
        "beneficio": "saber imediatamente a gravidade da situação, sem interpretar números manualmente",
        "prioridade": 1,
        "bv": 100,
        "ca": [
            ("um córrego com nivelCriticoCm = 180",
             "chega uma leitura com nível >= 180 cm (qualquer chuva)",
             "o nivelRisco é CRITICO"),
            ("um córrego com nivelAlertaCm = 120 e nivelCriticoCm = 180",
             "chega uma leitura com nível entre 120 e 179 cm",
             "o nivelRisco é ALERTA, mesmo que a chuva seja >= 30 mm/h"),
            ("um córrego com nivelAlertaCm = 120",
             "chega uma leitura com nível entre 90 cm (0,75 × 120) e 119 cm",
             "o nivelRisco é ATENCAO"),
            ("uma leitura com nível abaixo de 90 cm",
             "a chuva informada é >= 30,0 mm/h",
             "o nivelRisco é ATENCAO"),
            ("uma leitura com nível abaixo de 90 cm",
             "a chuva informada é menor que 30,0 mm/h",
             "o nivelRisco é NORMAL"),
            ("qualquer leitura classificada",
             "o status do córrego é consultado",
             "o nivelRisco exibido é o mesmo calculado na última leitura"),
        ],
    },
    {
        "id": "F03",
        "titulo": "Emissão de alertas",
        "persona": "morador cadastrado em um córrego",
        "acao": "receber um alerta quando o risco do meu córrego chegar a ALERTA ou CRITICO",
        "beneficio": "ter minutos de antecedência para sair de casa antes da água chegar à rua",
        "prioridade": 1,
        "bv": 95,
        "ca": [
            ("uma leitura classificada como ALERTA ou CRITICO",
             "a leitura é registrada",
             "a API cria um Alerta ativo para o córrego com nivelRisco, mensagem e nivelAguaCm, e o retorna na resposta da leitura"),
            ("uma leitura classificada como NORMAL ou ATENCAO",
             "a leitura é registrada",
             "nenhum Alerta é criado"),
            ("um alerta ativo",
             "o operador executa PATCH /api/alertas/{id}/encerrar",
             "o alerta passa a ativo = false e deixa de aparecer em GET /api/alertas?ativos=true"),
            ("um id de alerta inexistente",
             "o operador tenta encerrá-lo",
             "a API responde HTTP 404"),
            ("um morador com o app instalado e cadastrado no córrego",
             "um alerta é criado para esse córrego",
             "o app exibe notificação com o nível de risco e a mensagem, mesmo com o app em segundo plano"),
        ],
    },
    {
        "id": "F04",
        "titulo": "Cadastro de morador",
        "persona": "morador de área de risco",
        "acao": "cadastrar meu nome, telefone, endereço e o córrego próximo da minha casa",
        "beneficio": "receber os alertas do meu córrego e ser localizado caso precise de ajuda",
        "prioridade": 1,
        "bv": 85,
        "ca": [
            ("os campos nome, telefone, endereco, corregoId e tipoNecessidade válidos",
             "o morador é enviado em POST /api/moradores",
             "a API responde HTTP 201 com id e criadoEm preenchidos"),
            ("o campo nome ou telefone ou endereco vazio/ausente",
             "o cadastro é enviado",
             "a API responde erro de validação e o morador não é gravado"),
            ("um telefone fora do formato brasileiro (DDD + 8 ou 9 dígitos, apenas números)",
             "o cadastro é enviado",
             "a API responde erro de validação no campo telefone"),
            ("um corregoId que não existe",
             "o cadastro é enviado",
             "a API responde erro (HTTP 404 ou de validação) e o morador não é gravado"),
            ("um tipoNecessidade fora da lista NENHUMA, IDOSO, CADEIRANTE, ACAMADO, OUTRA",
             "o cadastro é enviado",
             "a API responde erro de validação"),
            ("um morador cadastrado",
             "seus dados são alterados via PUT /api/moradores/{id}",
             "a API responde HTTP 200 e a consulta seguinte retorna os novos dados"),
        ],
    },
    {
        "id": "F05",
        "titulo": "Priorização de moradores com mobilidade reduzida",
        "persona": "agente da Defesa Civil",
        "acao": "ver a lista dos moradores prioritários (idosos, cadeirantes, acamados) do córrego em risco",
        "beneficio": "organizar a retirada de quem não consegue sair sozinho antes dos demais",
        "prioridade": 1,
        "bv": 90,
        "ca": [
            ("um morador cadastrado com tipoNecessidade IDOSO, CADEIRANTE, ACAMADO ou OUTRA",
             "o cadastro é gravado",
             "o morador fica com prioritario = true"),
            ("moradores prioritários e não prioritários em vários córregos",
             "é chamado GET /api/moradores/prioritarios?corregoId=1",
             "a resposta contém somente os prioritários do córrego 1"),
            ("uma leitura que gera Alerta (ALERTA ou CRITICO)",
             "a resposta da leitura é retornada",
             "ela traz a lista de moradores prioritários do córrego para o atendimento"),
            ("um córrego sem moradores prioritários",
             "a lista de prioritários é consultada",
             "a API responde HTTP 200 com lista vazia"),
        ],
    },
    {
        "id": "F06",
        "titulo": "Consulta de status pelo app",
        "persona": "morador",
        "acao": "abrir o app e ver o nível atual, a chuva e o risco do meu córrego",
        "beneficio": "decidir se preciso me preparar para sair de casa",
        "prioridade": 2,
        "bv": 80,
        "ca": [
            ("um córrego com leituras registradas",
             "o morador abre a tela de status (GET /api/corregos/{id}/status)",
             "o app mostra último nível, chuva, nivelRisco com cor (verde NORMAL, amarelo ATENCAO, laranja ALERTA, vermelho CRITICO) e data/hora da leitura"),
            ("um id de córrego inexistente",
             "o status é consultado",
             "a API responde HTTP 404"),
            ("um córrego cadastrado sem nenhuma leitura",
             "o status é consultado",
             "o app exibe \"Sem leituras registradas\" sem travar ou exibir valores falsos"),
            ("o celular sem conexão com a internet",
             "o morador abre o app",
             "o app exibe o último status salvo com o aviso \"Sem conexão — dados de <data/hora>\" e não fecha inesperadamente"),
        ],
    },
    {
        "id": "F07",
        "titulo": "Histórico de leituras e alertas",
        "persona": "agente da Defesa Civil / operador do painel web",
        "acao": "consultar o histórico de leituras e de alertas de um córrego",
        "beneficio": "analisar como o córrego reage à chuva e medir a antecedência dos alertas",
        "prioridade": 3,
        "bv": 60,
        "ca": [
            ("um córrego com várias leituras",
             "é chamado GET /api/leituras?corregoId=1&limite=5",
             "retornam no máximo 5 leituras do córrego 1, da mais recente para a mais antiga"),
            ("um valor de limite menor que 1 ou não numérico",
             "o histórico é consultado",
             "a API responde erro de validação"),
            ("alertas ativos e encerrados",
             "é chamado GET /api/alertas?ativos=true&corregoId=1",
             "retornam apenas alertas ativos do córrego 1"),
        ],
    },
    {
        "id": "F08",
        "titulo": "Gestão de córregos e sensores",
        "persona": "administrador do sistema",
        "acao": "cadastrar córregos com seus limites de alerta/crítico e vincular sensores a eles",
        "beneficio": "expandir o monitoramento para novos córregos com regras corretas",
        "prioridade": 2,
        "bv": 70,
        "ca": [
            ("nome, bairro, coordenadas e limites válidos (nivelCriticoCm > nivelAlertaCm > 0)",
             "o córrego é enviado em POST /api/corregos",
             "a API responde HTTP 201 com o córrego criado"),
            ("nivelCriticoCm menor ou igual a nivelAlertaCm",
             "o córrego é enviado",
             "a API responde erro de validação"),
            ("um sensor com codigo já existente",
             "outro sensor é cadastrado com o mesmo codigo",
             "a API responde HTTP 409 (conflito) ou erro de validação, sem duplicar"),
            ("um sensor com corregoId inexistente",
             "o sensor é cadastrado",
             "a API responde erro e o sensor não é gravado"),
            ("um córrego existente",
             "ele é consultado por id inexistente (999)",
             "a API responde HTTP 404"),
        ],
    },
    {
        "id": "F09",
        "titulo": "Proteção de dados pessoais (LGPD)",
        "persona": "morador que informa telefone, endereço e condição de saúde/mobilidade",
        "acao": "que meus dados pessoais e sensíveis sejam usados apenas para o alerta e o resgate",
        "beneficio": "não ter minha condição de saúde e meu endereço expostos (LGPD, art. 11 — dado sensível)",
        "prioridade": 1,
        "bv": 85,
        "ca": [
            ("um cadastro ou alteração de morador",
             "a API grava os logs da operação",
             "os logs não contêm telefone, endereço nem tipoNecessidade (no máximo o id do morador)"),
            ("as rotas públicas de status e alertas",
             "elas são consultadas",
             "a resposta não contém nenhum dado pessoal de moradores"),
            ("a tela de cadastro no app",
             "o morador tenta enviar sem marcar o aceite do termo de uso e privacidade",
             "o botão de envio fica desabilitado e nada é enviado à API"),
            ("um morador que pede a exclusão dos seus dados",
             "é executado DELETE /api/moradores/{id}",
             "a API responde HTTP 204/200 e uma consulta posterior ao mesmo id retorna HTTP 404"),
            ("um erro interno qualquer na API",
             "a resposta de erro é devolvida",
             "ela não exibe stack trace, SQL ou dados de outros moradores"),
        ],
    },
]

# ---------------------------------------------------------------------------
# CASOS DE TESTE
# ---------------------------------------------------------------------------
PV = "Partição de equivalência"
VL = "Análise de valor-limite"
TD = "Tabela de decisão"
SEED = "Massa de teste (seed) carregada; API em execução; ferramenta de requisições (Postman/Swagger) aberta."


def _leitura_risco(n, ct, nivel, chuva, esperado, tecnica, obs, alerta=None):
    """Gera caso de teste de classificação de risco para o córrego 1."""
    alerta = alerta or ("Nenhum alerta é criado (campo de alerta nulo/ausente)."
                        if esperado in ("NORMAL", "ATENCAO") else
                        "Alerta " + esperado + " criado para o córrego 1.")
    return {
        "id": ct,
        "titulo": f"Classificar leitura nível {nivel} cm / chuva {str(chuva).replace('.', ',')} mm/h como {esperado}",
        "feature": "F02",
        "objetivo": f"Validar a regra de risco no ponto {obs}.",
        "pre": SEED + " Córrego 1 com alerta = 120 cm e crítico = 180 cm.",
        "entrada": f'POST /api/leituras {{"sensorId": 1, "nivelAguaCm": {nivel}, "chuvaMmHora": {chuva}}}',
        "passos": [
            (f"Enviar POST /api/leituras com sensorId 1, nivelAguaCm {nivel} e chuvaMmHora {chuva}.",
             "HTTP 201 com a leitura gravada."),
            ("Verificar o campo nivelRisco da resposta.", f"nivelRisco = {esperado}."),
            ("Verificar o alerta retornado na resposta.", alerta),
            ("Consultar GET /api/corregos/1/status.",
             f"Último nível = {nivel} cm e nivelRisco = {esperado}."),
        ],
        "esperado": f"Leitura registrada e classificada como {esperado}. {alerta}",
        "tipo": "Positivo",
        "tecnica": tecnica,
    }


TEST_CASES = [
    # ---------------- F01 ----------------
    {
        "id": "CT01", "titulo": "Registrar leitura válida enviada pelo sensor", "feature": "F01",
        "objetivo": "Garantir que uma leitura válida de sensor ativo é gravada e classificada.",
        "pre": SEED,
        "entrada": 'POST /api/leituras {"sensorId": 1, "nivelAguaCm": 50, "chuvaMmHora": 5}',
        "passos": [
            ("Enviar POST /api/leituras com o corpo informado.", "HTTP 201."),
            ("Conferir o corpo da resposta.",
             "Contém id, sensorId 1, nivelAguaCm 50, chuvaMmHora 5, registradaEm preenchido e nivelRisco NORMAL."),
            ("Consultar GET /api/leituras?corregoId=1&limite=1.", "A leitura criada é a primeira da lista."),
        ],
        "esperado": "Leitura persistida, com data/hora e nivelRisco NORMAL.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT02", "titulo": "Rejeitar leitura de sensor inexistente (404)", "feature": "F01",
        "objetivo": "Garantir que a API não aceita leitura de sensor não cadastrado.",
        "pre": SEED + " Sensor 999 não existe.",
        "entrada": 'POST /api/leituras {"sensorId": 999, "nivelAguaCm": 50, "chuvaMmHora": 5}',
        "passos": [
            ("Enviar POST /api/leituras com sensorId 999.", "HTTP 404 com mensagem \"Sensor não encontrado\"."),
            ("Consultar GET /api/leituras?corregoId=1&limite=1.", "Nenhuma leitura nova foi gravada."),
        ],
        "esperado": "HTTP 404; nenhuma leitura gravada.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT03", "titulo": "Rejeitar nível de água negativo (-1 cm)", "feature": "F01",
        "objetivo": "Validar o limite inferior inválido do nível de água.",
        "pre": SEED,
        "entrada": 'POST /api/leituras {"sensorId": 1, "nivelAguaCm": -1, "chuvaMmHora": 0}',
        "passos": [
            ("Enviar POST /api/leituras com nivelAguaCm -1.",
             "Erro de validação (400/422) indicando o campo nivelAguaCm."),
            ("Consultar o histórico do córrego 1.", "Nenhuma leitura com nível -1 foi gravada."),
        ],
        "esperado": "Leitura rejeitada por erro de validação; nada gravado.",
        "tipo": "Negativo", "tecnica": VL,
    },
    {
        "id": "CT04", "titulo": "Aceitar nível e chuva iguais a zero (limite inferior válido)", "feature": "F01",
        "objetivo": "Validar que 0 é o menor valor aceito para nível e chuva.",
        "pre": SEED,
        "entrada": 'POST /api/leituras {"sensorId": 1, "nivelAguaCm": 0, "chuvaMmHora": 0}',
        "passos": [
            ("Enviar POST /api/leituras com nível 0 e chuva 0.", "HTTP 201."),
            ("Verificar nivelRisco.", "nivelRisco = NORMAL."),
        ],
        "esperado": "Leitura aceita e classificada como NORMAL.",
        "tipo": "Positivo", "tecnica": VL,
    },
    {
        "id": "CT05", "titulo": "Rejeitar leitura com campo obrigatório ausente", "feature": "F01",
        "objetivo": "Garantir validação de campos obrigatórios da leitura.",
        "pre": SEED,
        "entrada": 'a) {"nivelAguaCm": 50, "chuvaMmHora": 5} (sem sensorId); '
                   'b) {"sensorId": 1, "chuvaMmHora": 5} (sem nivelAguaCm); '
                   'c) {"sensorId": 1, "nivelAguaCm": 50} (sem chuvaMmHora)',
        "passos": [
            ("Enviar POST /api/leituras com o corpo (a).", "Erro de validação citando sensorId."),
            ("Enviar POST /api/leituras com o corpo (b).", "Erro de validação citando nivelAguaCm."),
            ("Enviar POST /api/leituras com o corpo (c).", "Erro de validação citando chuvaMmHora."),
            ("Consultar o histórico do córrego 1.", "Nenhuma das 3 leituras foi gravada."),
        ],
        "esperado": "Todas as requisições rejeitadas; nada gravado.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT06", "titulo": "Rejeitar chuva negativa e valor não numérico", "feature": "F01",
        "objetivo": "Validar partições inválidas do campo chuvaMmHora.",
        "pre": SEED,
        "entrada": 'a) {"sensorId": 1, "nivelAguaCm": 50, "chuvaMmHora": -0.1}; '
                   'b) {"sensorId": 1, "nivelAguaCm": 50, "chuvaMmHora": "muita"}',
        "passos": [
            ("Enviar POST /api/leituras com o corpo (a).", "Erro de validação citando chuvaMmHora."),
            ("Enviar POST /api/leituras com o corpo (b).", "Erro de validação citando chuvaMmHora."),
        ],
        "esperado": "Ambas rejeitadas; nenhuma leitura gravada.",
        "tipo": "Negativo", "tecnica": VL + " / " + PV,
    },
    {
        "id": "CT07", "titulo": "Rejeitar leitura de sensor inativo", "feature": "F01",
        "objetivo": "Garantir que sensores desativados não alimentam a classificação.",
        "pre": SEED + " Sensor 3 (ESP32-PB-02) cadastrado com ativo = false.",
        "entrada": 'POST /api/leituras {"sensorId": 3, "nivelAguaCm": 200, "chuvaMmHora": 40}',
        "passos": [
            ("Enviar POST /api/leituras com sensorId 3.", "Erro de validação informando sensor inativo."),
            ("Consultar GET /api/alertas?ativos=true&corregoId=1.", "Nenhum alerta CRITICO novo foi criado."),
        ],
        "esperado": "Leitura rejeitada; nenhum alerta falso gerado.",
        "tipo": "Negativo", "tecnica": PV,
    },
    # ---------------- F02 (valores-limite da regra) ----------------
    _leitura_risco(8, "CT08", 89, 0, "NORMAL", VL, "logo abaixo de 0,75 × alerta (89 cm)"),
    _leitura_risco(9, "CT09", 90, 0, "ATENCAO", VL, "exatamente 0,75 × alerta (90 cm)"),
    _leitura_risco(10, "CT10", 119, 0, "ATENCAO", VL, "logo abaixo do nível de alerta (119 cm)"),
    _leitura_risco(11, "CT11", 120, 0, "ALERTA", VL, "exatamente igual ao nível de alerta (120 cm)"),
    _leitura_risco(12, "CT12", 179, 0, "ALERTA", VL, "logo abaixo do nível crítico (179 cm)"),
    _leitura_risco(13, "CT13", 180, 0, "CRITICO", VL, "exatamente igual ao nível crítico (180 cm)"),
    _leitura_risco(14, "CT14", 50, 29.9, "NORMAL", VL, "de chuva logo abaixo de 30 mm/h (29,9)"),
    _leitura_risco(15, "CT15", 50, 30.0, "ATENCAO", VL, "de chuva exatamente igual a 30 mm/h"),
    {
        "id": "CT16", "titulo": "Combinações de nível e chuva (precedência da regra)", "feature": "F02",
        "objetivo": "Validar que a condição mais grave prevalece quando nível e chuva disparam regras diferentes.",
        "pre": SEED + " Córrego 1 com alerta = 120 cm e crítico = 180 cm.",
        "entrada": "Tabela de decisão — (nível cm; chuva mm/h → risco): "
                   "R1 (200; 0 → CRITICO); R2 (200; 50 → CRITICO); R3 (130; 50 → ALERTA); "
                   "R4 (100; 50 → ATENCAO); R5 (40; 50 → ATENCAO); R6 (40; 10 → NORMAL)",
        "passos": [
            ("Enviar leitura R1 (200; 0).", "nivelRisco = CRITICO."),
            ("Enviar leitura R2 (200; 50).", "nivelRisco = CRITICO (chuva não rebaixa nem eleva)."),
            ("Enviar leitura R3 (130; 50).", "nivelRisco = ALERTA (não fica em ATENCAO por causa da chuva)."),
            ("Enviar leitura R4 (100; 50).", "nivelRisco = ATENCAO."),
            ("Enviar leitura R5 (40; 50).", "nivelRisco = ATENCAO (apenas pela chuva)."),
            ("Enviar leitura R6 (40; 10).", "nivelRisco = NORMAL."),
        ],
        "esperado": "Cada combinação recebe exatamente o risco da tabela de decisão.",
        "tipo": "Positivo", "tecnica": TD,
    },
    # ---------------- F03 ----------------
    {
        "id": "CT17", "titulo": "Gerar alerta ALERTA com lista de prioritários", "feature": "F03",
        "objetivo": "Garantir criação de alerta e identificação de prioritários ao atingir ALERTA.",
        "pre": SEED + " Nenhum alerta ativo para o córrego 1.",
        "entrada": 'POST /api/leituras {"sensorId": 1, "nivelAguaCm": 140, "chuvaMmHora": 20}',
        "passos": [
            ("Enviar a leitura.", "HTTP 201 com nivelRisco = ALERTA."),
            ("Verificar o alerta na resposta.",
             "Alerta com corregoId 1, nivelRisco ALERTA, nivelAguaCm 140, mensagem com o nome do córrego, ativo = true."),
            ("Verificar a lista de prioritários na resposta.", "Contém os 2 moradores prioritários do córrego 1 e nenhum do córrego 2."),
            ("Consultar GET /api/alertas?ativos=true&corregoId=1.", "O alerta criado aparece na lista."),
        ],
        "esperado": "Alerta ativo criado e prioritários do córrego 1 identificados.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT18", "titulo": "Gerar alerta CRITICO", "feature": "F03",
        "objetivo": "Garantir criação de alerta com nível CRITICO.",
        "pre": SEED,
        "entrada": 'POST /api/leituras {"sensorId": 1, "nivelAguaCm": 185, "chuvaMmHora": 45}',
        "passos": [
            ("Enviar a leitura.", "HTTP 201 com nivelRisco = CRITICO."),
            ("Verificar o alerta na resposta.", "Alerta com nivelRisco CRITICO, nivelAguaCm 185, ativo = true."),
        ],
        "esperado": "Alerta CRITICO ativo criado para o córrego 1.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT19", "titulo": "Não gerar alerta para leitura ATENCAO", "feature": "F03",
        "objetivo": "Evitar alarmes falsos: ATENCAO não deve criar Alerta.",
        "pre": SEED + " Nenhum alerta ativo para o córrego 1.",
        "entrada": 'POST /api/leituras {"sensorId": 1, "nivelAguaCm": 100, "chuvaMmHora": 10}',
        "passos": [
            ("Enviar a leitura.", "HTTP 201 com nivelRisco = ATENCAO e sem alerta na resposta."),
            ("Consultar GET /api/alertas?ativos=true&corregoId=1.", "Lista vazia."),
        ],
        "esperado": "Nenhum alerta criado.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT20", "titulo": "Encerrar alerta ativo", "feature": "F03",
        "objetivo": "Validar o encerramento de alerta pelo operador.",
        "pre": SEED + " Alerta ativo existente para o córrego 1 (ex.: gerado no CT17), id anotado.",
        "entrada": "PATCH /api/alertas/{id}/encerrar",
        "passos": [
            ("Executar PATCH /api/alertas/{id}/encerrar.", "HTTP 200 com ativo = false."),
            ("Consultar GET /api/alertas?ativos=true&corregoId=1.", "O alerta encerrado não aparece."),
        ],
        "esperado": "Alerta encerrado e fora da lista de ativos.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT21", "titulo": "Encerrar alerta inexistente (404)", "feature": "F03",
        "objetivo": "Validar tratamento de id de alerta inexistente.",
        "pre": SEED + " Alerta 999 não existe.",
        "entrada": "PATCH /api/alertas/999/encerrar",
        "passos": [
            ("Executar PATCH /api/alertas/999/encerrar.", "HTTP 404 com mensagem de erro, sem stack trace."),
        ],
        "esperado": "HTTP 404.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT22", "titulo": "App exibe notificação de alerta em segundo plano", "feature": "F03",
        "objetivo": "Validar que o morador é avisado pelo app quando um alerta é criado.",
        "pre": "App instalado no celular, morador cadastrado no córrego 1, permissão de notificação concedida, app em segundo plano.",
        "entrada": 'POST /api/leituras {"sensorId": 1, "nivelAguaCm": 150, "chuvaMmHora": 35}',
        "passos": [
            ("Enviar a leitura pela API.", "Alerta ALERTA criado."),
            ("Observar o celular.", "Notificação exibida com \"ALERTA\" e a mensagem do córrego Ponte Baixa."),
            ("Tocar na notificação.", "O app abre na tela de status do córrego 1 em cor laranja."),
        ],
        "esperado": "Morador notificado e levado ao status atualizado.",
        "tipo": "Positivo", "tecnica": PV,
    },
    # ---------------- F04 ----------------
    {
        "id": "CT23", "titulo": "Cadastrar morador com dados válidos", "feature": "F04",
        "objetivo": "Validar o cadastro completo de um morador.",
        "pre": SEED,
        "entrada": 'POST /api/moradores {"nome": "Maria Teste", "telefone": "11987654321", '
                   '"endereco": "Rua Fictícia, 10", "corregoId": 1, "tipoNecessidade": "NENHUMA"}',
        "passos": [
            ("Enviar POST /api/moradores.", "HTTP 201."),
            ("Conferir a resposta.", "id e criadoEm preenchidos; prioritario = false."),
            ("Consultar GET /api/moradores/{id}.", "Mesmos dados enviados."),
        ],
        "esperado": "Morador gravado corretamente.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT24", "titulo": "Rejeitar cadastro sem nome / com nome em branco", "feature": "F04",
        "objetivo": "Validar campo obrigatório nome.",
        "pre": SEED,
        "entrada": 'a) corpo do CT23 sem "nome"; b) "nome": "   " (só espaços)',
        "passos": [
            ("Enviar o corpo (a).", "Erro de validação citando nome."),
            ("Enviar o corpo (b).", "Erro de validação citando nome."),
            ("Consultar GET /api/moradores.", "Nenhum morador novo gravado."),
        ],
        "esperado": "Cadastro rejeitado.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT25", "titulo": "Validar formato do telefone", "feature": "F04",
        "objetivo": "Validar partições e limites do telefone (DDD + 8 ou 9 dígitos = 10 ou 11 dígitos).",
        "pre": SEED,
        "entrada": 'Corpo do CT23 variando "telefone": a) "119876543" (9 dígitos); b) "1198765432" (10); '
                   'c) "11987654321" (11); d) "119876543210" (12); e) "11abc654321"',
        "passos": [
            ("Enviar com telefone (a).", "Erro de validação no telefone."),
            ("Enviar com telefone (b).", "HTTP 201 (fixo com 8 dígitos)."),
            ("Enviar com telefone (c).", "HTTP 201 (celular com 9 dígitos)."),
            ("Enviar com telefone (d).", "Erro de validação no telefone."),
            ("Enviar com telefone (e).", "Erro de validação no telefone."),
        ],
        "esperado": "Somente telefones com 10 ou 11 dígitos numéricos são aceitos.",
        "tipo": "Negativo", "tecnica": VL + " / " + PV,
    },
    {
        "id": "CT26", "titulo": "Rejeitar morador vinculado a córrego inexistente", "feature": "F04",
        "objetivo": "Garantir integridade do vínculo morador–córrego.",
        "pre": SEED + " Córrego 999 não existe.",
        "entrada": 'Corpo do CT23 com "corregoId": 999',
        "passos": [
            ("Enviar POST /api/moradores.", "HTTP 404 ou erro de validação citando corregoId."),
            ("Consultar GET /api/moradores.", "Morador não gravado."),
        ],
        "esperado": "Cadastro rejeitado.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT27", "titulo": "Rejeitar tipoNecessidade fora da lista", "feature": "F04",
        "objetivo": "Validar o domínio (enum) de tipoNecessidade.",
        "pre": SEED,
        "entrada": 'Corpo do CT23 com "tipoNecessidade": "GESTANTE" e depois "idoso" (minúsculo)',
        "passos": [
            ("Enviar com \"GESTANTE\".", "Erro de validação listando os valores permitidos."),
            ("Enviar com \"idoso\".", "Erro de validação (ou aceito como IDOSO, se a API normaliza — registrar o comportamento)."),
        ],
        "esperado": "Valores fora do enum não são gravados.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT28", "titulo": "Atualizar dados do morador", "feature": "F04",
        "objetivo": "Validar alteração cadastral via PUT.",
        "pre": SEED + " Morador criado no CT23 (id anotado).",
        "entrada": 'PUT /api/moradores/{id} com "telefone": "11912345678" e "endereco": "Rua Nova, 20"',
        "passos": [
            ("Executar o PUT.", "HTTP 200."),
            ("Consultar GET /api/moradores/{id}.", "Telefone e endereço atualizados; demais campos inalterados."),
            ("Executar PUT /api/moradores/999.", "HTTP 404."),
        ],
        "esperado": "Dados atualizados; id inexistente retorna 404.",
        "tipo": "Positivo", "tecnica": PV,
    },
    # ---------------- F05 ----------------
    {
        "id": "CT29", "titulo": "Marcar como prioritário morador com necessidade especial", "feature": "F05",
        "objetivo": "Validar a derivação de prioritario a partir de tipoNecessidade.",
        "pre": SEED,
        "entrada": 'Corpo do CT23 com "nome": "José Teste" e "tipoNecessidade": "CADEIRANTE"',
        "passos": [
            ("Enviar POST /api/moradores.", "HTTP 201 com prioritario = true."),
            ("Consultar GET /api/moradores/prioritarios?corregoId=1.", "José Teste aparece na lista."),
        ],
        "esperado": "Morador cadeirante cadastrado como prioritário.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT30", "titulo": "Listar prioritários somente do córrego informado", "feature": "F05",
        "objetivo": "Garantir o filtro por córrego e a exclusão de não prioritários.",
        "pre": SEED,
        "entrada": "GET /api/moradores/prioritarios?corregoId=1 e ?corregoId=2",
        "passos": [
            ("Consultar com corregoId=1.", "Somente os 2 prioritários do córrego 1 (IDOSO e CADEIRANTE)."),
            ("Verificar se há moradores com tipoNecessidade NENHUMA.", "Nenhum morador NENHUMA na lista."),
            ("Consultar com corregoId=2.", "Somente o prioritário ACAMADO do córrego 2."),
        ],
        "esperado": "Listas filtradas corretamente.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT31", "titulo": "Córrego sem prioritários retorna lista vazia", "feature": "F05",
        "objetivo": "Validar resposta para córrego sem moradores prioritários.",
        "pre": SEED + " Córrego 3 criado (CT39) sem moradores.",
        "entrada": "GET /api/moradores/prioritarios?corregoId=3",
        "passos": [
            ("Consultar a lista.", "HTTP 200 com lista vazia []."),
        ],
        "esperado": "Lista vazia, sem erro.",
        "tipo": "Negativo", "tecnica": PV,
    },
    # ---------------- F06 ----------------
    {
        "id": "CT32", "titulo": "Consultar status do córrego no app", "feature": "F06",
        "objetivo": "Validar a tela de status com nível, chuva, risco e cor.",
        "pre": SEED + " Última leitura do córrego 1: nível 100 cm, chuva 10 mm/h (ATENCAO). App com conexão.",
        "entrada": "Abrir o app logado como morador do córrego 1 (GET /api/corregos/1/status)",
        "passos": [
            ("Abrir o app na tela inicial.", "Tela de status do córrego Ponte Baixa é exibida."),
            ("Conferir os valores.", "Nível 100 cm, chuva 10 mm/h, data/hora da leitura."),
            ("Conferir o indicador de risco.", "Texto ATENCAO em cor amarela."),
        ],
        "esperado": "Status correto e legível.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT33", "titulo": "Consultar status de córrego inexistente (404)", "feature": "F06",
        "objetivo": "Validar tratamento de córrego inexistente.",
        "pre": SEED,
        "entrada": "GET /api/corregos/999/status",
        "passos": [
            ("Executar a requisição.", "HTTP 404 com mensagem \"Córrego não encontrado\"."),
        ],
        "esperado": "HTTP 404.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT34", "titulo": "Status de córrego sem leituras", "feature": "F06",
        "objetivo": "Validar o comportamento quando ainda não há leituras.",
        "pre": SEED + " Córrego 3 criado (CT39) sem sensor/leituras.",
        "entrada": "GET /api/corregos/3/status; app aberto no córrego 3",
        "passos": [
            ("Executar a requisição.", "HTTP 200 com nível/chuva nulos (sem inventar valores)."),
            ("Abrir o status no app.", "Mensagem \"Sem leituras registradas\"; app não trava."),
        ],
        "esperado": "Ausência de dados tratada sem erro.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT35", "titulo": "App sem conexão exibe último status em cache", "feature": "F06",
        "objetivo": "Validar o comportamento offline do app.",
        "pre": "App aberto ao menos uma vez com conexão (status do córrego 1 salvo). Em seguida, ativar modo avião.",
        "entrada": "Modo avião ativado",
        "passos": [
            ("Fechar e reabrir o app em modo avião.", "App abre sem fechar inesperadamente."),
            ("Conferir a tela de status.", "Último status salvo + aviso \"Sem conexão — dados de <data/hora>\"."),
            ("Puxar para atualizar.", "Mensagem de falta de conexão; dados antigos permanecem."),
            ("Desativar o modo avião e atualizar.", "Status atualizado e aviso removido."),
        ],
        "esperado": "App utilizável offline, indicando claramente que os dados podem estar desatualizados.",
        "tipo": "Negativo", "tecnica": PV,
    },
    # ---------------- F07 ----------------
    {
        "id": "CT36", "titulo": "Consultar histórico de leituras com limite", "feature": "F07",
        "objetivo": "Validar filtro por córrego, limite e ordenação do histórico.",
        "pre": SEED + " Córrego 1 com pelo menos 6 leituras.",
        "entrada": "GET /api/leituras?corregoId=1&limite=5",
        "passos": [
            ("Executar a requisição.", "HTTP 200 com exatamente 5 leituras."),
            ("Conferir o sensor de cada leitura.", "Todas pertencem a sensores do córrego 1."),
            ("Conferir a ordem.", "Ordenadas por registradaEm, da mais recente para a mais antiga."),
        ],
        "esperado": "Histórico filtrado, limitado e ordenado.",
        "tipo": "Positivo", "tecnica": VL,
    },
    {
        "id": "CT37", "titulo": "Rejeitar limite inválido no histórico", "feature": "F07",
        "objetivo": "Validar valores-limite e partições inválidas do parâmetro limite.",
        "pre": SEED,
        "entrada": "limite = 0; limite = -1; limite = abc; limite = 1",
        "passos": [
            ("GET /api/leituras?corregoId=1&limite=0.", "Erro de validação."),
            ("GET /api/leituras?corregoId=1&limite=-1.", "Erro de validação."),
            ("GET /api/leituras?corregoId=1&limite=abc.", "Erro de validação."),
            ("GET /api/leituras?corregoId=1&limite=1.", "HTTP 200 com 1 leitura (limite mínimo válido)."),
        ],
        "esperado": "Somente limite >= 1 é aceito.",
        "tipo": "Negativo", "tecnica": VL,
    },
    {
        "id": "CT38", "titulo": "Listar somente alertas ativos do córrego", "feature": "F07",
        "objetivo": "Validar os filtros ativos e corregoId da lista de alertas.",
        "pre": SEED + " Córrego 1 com 1 alerta ativo e 1 encerrado; córrego 2 com 1 alerta ativo.",
        "entrada": "GET /api/alertas?ativos=true&corregoId=1",
        "passos": [
            ("Executar a requisição.", "HTTP 200 com 1 alerta."),
            ("Conferir o alerta.", "ativo = true e corregoId = 1; o encerrado e o do córrego 2 não aparecem."),
        ],
        "esperado": "Apenas alertas ativos do córrego 1.",
        "tipo": "Positivo", "tecnica": PV,
    },
    # ---------------- F08 ----------------
    {
        "id": "CT39", "titulo": "Cadastrar córrego com limites válidos", "feature": "F08",
        "objetivo": "Validar o cadastro de um novo córrego (gera o córrego 3 usado em outros CTs).",
        "pre": SEED,
        "entrada": 'POST /api/corregos {"nome": "Córrego Teste", "bairro": "Jardim Ângela", '
                   '"latitude": -23.70, "longitude": -46.77, "nivelAlertaCm": 100, "nivelCriticoCm": 160}',
        "passos": [
            ("Enviar POST /api/corregos.", "HTTP 201 com id gerado (anotar como córrego 3)."),
            ("Consultar GET /api/corregos/{id}.", "Mesmos dados enviados."),
        ],
        "esperado": "Córrego criado.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT40", "titulo": "Rejeitar córrego com nível crítico <= nível de alerta", "feature": "F08",
        "objetivo": "Validar a coerência entre os limites do córrego.",
        "pre": SEED,
        "entrada": "Corpo do CT39 com: a) alerta 120 / crítico 120; b) alerta 120 / crítico 100; "
                   "c) alerta 120 / crítico 121; d) alerta 0 / crítico 50",
        "passos": [
            ("Enviar (a) — crítico igual ao alerta.", "Erro de validação."),
            ("Enviar (b) — crítico menor que alerta.", "Erro de validação."),
            ("Enviar (c) — crítico 1 cm acima.", "HTTP 201 (menor valor válido)."),
            ("Enviar (d) — alerta zero.", "Erro de validação."),
        ],
        "esperado": "Somente nivelCriticoCm > nivelAlertaCm > 0 é aceito.",
        "tipo": "Negativo", "tecnica": VL,
    },
    {
        "id": "CT41", "titulo": "Rejeitar sensor com código duplicado", "feature": "F08",
        "objetivo": "Garantir unicidade do código do sensor.",
        "pre": SEED + " Sensor ESP32-PB-01 já existe.",
        "entrada": 'POST /api/sensores {"codigo": "ESP32-PB-01", "corregoId": 1, "ativo": true}',
        "passos": [
            ("Enviar POST /api/sensores.", "HTTP 409 (ou erro de validação) informando código duplicado."),
            ("Consultar GET /api/sensores.", "Existe apenas um sensor ESP32-PB-01."),
        ],
        "esperado": "Sensor duplicado não é gravado.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT42", "titulo": "Rejeitar sensor vinculado a córrego inexistente", "feature": "F08",
        "objetivo": "Garantir integridade do vínculo sensor–córrego.",
        "pre": SEED,
        "entrada": 'POST /api/sensores {"codigo": "ESP32-XX-99", "corregoId": 999, "ativo": true}; GET /api/corregos/999',
        "passos": [
            ("Enviar POST /api/sensores.", "HTTP 404 ou erro de validação citando corregoId."),
            ("Executar GET /api/corregos/999.", "HTTP 404."),
        ],
        "esperado": "Sensor não gravado; córrego inexistente retorna 404.",
        "tipo": "Negativo", "tecnica": PV,
    },
    # ---------------- F09 ----------------
    {
        "id": "CT43", "titulo": "Logs da API sem dados pessoais/sensíveis", "feature": "F09",
        "objetivo": "Verificar conformidade com a LGPD nos logs da aplicação.",
        "pre": SEED + " Acesso ao console/arquivo de log da API.",
        "entrada": 'Cadastro do CT29 (telefone 11987654321, endereço "Rua Fictícia, 10", CADEIRANTE) e um PUT no mesmo morador',
        "passos": [
            ("Executar o cadastro e a alteração.", "HTTP 201 e HTTP 200."),
            ("Pesquisar no log por \"11987654321\".", "Nenhuma ocorrência."),
            ("Pesquisar no log por \"Rua Fictícia\" e \"CADEIRANTE\".", "Nenhuma ocorrência."),
            ("Verificar o registro da operação.", "Log contém apenas operação, id do morador e data/hora."),
        ],
        "esperado": "Nenhum dado pessoal ou sensível nos logs.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT44", "titulo": "Status e alertas não expõem dados de moradores", "feature": "F09",
        "objetivo": "Garantir minimização de dados nas rotas consultadas pelo app.",
        "pre": SEED + " Alerta ativo no córrego 1.",
        "entrada": "GET /api/corregos/1/status; GET /api/alertas?ativos=true&corregoId=1",
        "passos": [
            ("Executar GET /status e inspecionar o JSON.", "Sem campos nome, telefone, endereco ou tipoNecessidade."),
            ("Executar GET /alertas e inspecionar o JSON.", "Sem campos nome, telefone, endereco ou tipoNecessidade."),
        ],
        "esperado": "Nenhum dado pessoal nas respostas públicas.",
        "tipo": "Negativo", "tecnica": PV,
    },
    {
        "id": "CT45", "titulo": "Cadastro no app exige aceite do termo de privacidade", "feature": "F09",
        "objetivo": "Validar consentimento antes do envio de dado sensível (condição de saúde/mobilidade).",
        "pre": "App instalado, tela de cadastro aberta.",
        "entrada": "Nome, telefone, endereço, córrego e necessidade IDOSO preenchidos; termo NÃO marcado",
        "passos": [
            ("Preencher os campos sem marcar o aceite.", "Botão \"Cadastrar\" desabilitado."),
            ("Marcar o aceite do termo.", "Botão \"Cadastrar\" habilitado."),
            ("Tocar em \"Cadastrar\".", "Cadastro enviado; mensagem de sucesso."),
        ],
        "esperado": "Nada é enviado sem consentimento.",
        "tipo": "Negativo", "tecnica": TD,
    },
    {
        "id": "CT46", "titulo": "Excluir dados do morador a pedido (direito de eliminação)", "feature": "F09",
        "objetivo": "Validar a eliminação dos dados pessoais do titular.",
        "pre": SEED + " Morador criado no CT23 (id anotado).",
        "entrada": "DELETE /api/moradores/{id}; DELETE /api/moradores/999",
        "passos": [
            ("Executar DELETE /api/moradores/{id}.", "HTTP 204 (ou 200)."),
            ("Executar GET /api/moradores/{id}.", "HTTP 404."),
            ("Consultar a lista de prioritários do córrego 1.", "O morador excluído não aparece."),
            ("Executar DELETE /api/moradores/999.", "HTTP 404."),
        ],
        "esperado": "Dados eliminados; id inexistente retorna 404.",
        "tipo": "Positivo", "tecnica": PV,
    },
    {
        "id": "CT47", "titulo": "Erro interno não expõe stack trace nem dados", "feature": "F09",
        "objetivo": "Garantir que mensagens de erro não vazam informação técnica ou pessoal.",
        "pre": SEED,
        "entrada": 'POST /api/moradores com JSON malformado: {"nome": "Ana", "telefone": }',
        "passos": [
            ("Enviar a requisição.", "HTTP 400/422 com mensagem genérica de corpo inválido."),
            ("Inspecionar o corpo da resposta.", "Sem stack trace, SQL, caminhos de arquivo ou dados de outros moradores."),
        ],
        "esperado": "Erro tratado sem vazamento de informação.",
        "tipo": "Negativo", "tecnica": PV,
    },
]


def feature_por_id(fid):
    return next(f for f in FEATURES if f["id"] == fid)


def historia(f):
    return f"Como {f['persona']}, quero {f['acao']}, para {f['beneficio']}."


def ca_texto(i, ca):
    dado, quando, entao = ca
    return f"CA{i:02d} — Dado {dado}, Quando {quando}, Então {entao}."


def casos_da_feature(fid):
    return [c for c in TEST_CASES if c["feature"] == fid]

REPOS = [
    ("Mobile (app Expo)", "https://github.com/fabriciomunix/GS-Mobile"),
    ("SOA (API Python/FastAPI)", "https://github.com/fabriciomunix/Gs-soa"),
    ("C# (Web API .NET)", "https://github.com/fabriciomunix/Gs-c-"),
    ("QA (este material)", "https://github.com/fabriciomunix/GS-QA"),
]

FICHA_RESUMO = [
    ("Nome", "Alerta Córrego"),
    ("Local", "São Paulo — região do Córrego Ponte Baixa / M'Boi Mirim (Zona Sul)"),
    ("Cidadão beneficiado", "Morador de área de risco de alagamento, com prioridade para idosos e pessoas com mobilidade reduzida."),
    ("Problema", "Moradores às margens de córregos pequenos, não monitorados pelas estações da Prefeitura, recebem "
                 "alertas de chuva para a região inteira, mas não sabem quando o córrego da rua deles vai transbordar; "
                 "quem tem mobilidade reduzida depende de vizinhos para sair a tempo."),
    ("Como funciona", "Um sensor ESP32 no córrego mede o nível da água e a chuva e envia para uma API REST; a API "
                      "classifica o risco e gera alertas; o app (Expo) e o painel web mostram os alertas aos moradores "
                      "cadastrados, com prioridade para quem precisa de ajuda para sair."),
    ("Regra de risco", "nível >= nivelCriticoCm → CRITICO; nível >= nivelAlertaCm → ALERTA; nível >= 0,75 × nivelAlertaCm "
                       "ou chuva >= 30 mm/h → ATENCAO; caso contrário → NORMAL. Leituras ALERTA/CRITICO geram um Alerta e "
                       "a lista de moradores prioritários do córrego."),
    ("Indicador de impacto", "Minutos de antecedência do alerta antes de a água atingir a rua; nº de moradores prioritários alertados."),
    ("ODS", "ODS 11 (meta 11.5), ODS 13 (meta 13.1), ODS 10 (inclusão de idosos e PcD)."),
]

PRINTS = [
    ("A1", "Visão geral do projeto no Azure DevOps (Overview), com a URL do projeto visível na barra do navegador."),
    ("A2", "Boards > Work items (ou Backlogs nível Features) listando as 9 Features F01–F09."),
    ("A3", "Feature F02 aberta, mostrando Descrição (história de usuário), Critérios de aceite, Priority e Business Value."),
    ("A4", "Outra Feature aberta (ex.: F09 — LGPD) com os critérios de aceite."),
    ("A5", "Lista de Test Cases (Boards > Work items filtrado por tipo Test Case, ou Test Plans > suite)."),
    ("A6", "Test Case de valor-limite aberto (ex.: CT09) mostrando os passos (Action / Expected Result)."),
    ("A7", "Test Case negativo aberto (ex.: CT02 ou CT43) mostrando os passos."),
    ("A8", "Feature com a aba Links/Related Work mostrando os Test Cases vinculados como \"Tested By\"."),
    ("A9", "Test Plans > plano \"Homologação Alerta Córrego\" com as suítes por Feature."),
    ("A10", "Project settings > Permissions > Project Administrators com o professor adicionado."),
]
