# Features — Alerta Córrego

Disciplina: Testing, Compliance & Quality Assurance — Turma 3ES

Formato: Título · Descrição (história de usuário) · Critérios de aceite (Dado/Quando/Então) · Prioridade (1 = mais alta, 4 = mais baixa, escala do Azure) · Business Value.

| ID | Feature | Prioridade | Business Value | Casos de teste |
|---|---|---|---|---|
| F01 | Monitoramento do nível do córrego | 1 | 100 | CT01, CT02, CT03, CT04, CT05, CT06, CT07 |
| F02 | Classificação automática de risco | 1 | 100 | CT08, CT09, CT10, CT11, CT12, CT13, CT14, CT15, CT16 |
| F03 | Emissão de alertas | 1 | 95 | CT17, CT18, CT19, CT20, CT21, CT22 |
| F04 | Cadastro de morador | 1 | 85 | CT23, CT24, CT25, CT26, CT27, CT28 |
| F05 | Priorização de moradores com mobilidade reduzida | 1 | 90 | CT29, CT30, CT31 |
| F06 | Consulta de status pelo app | 2 | 80 | CT32, CT33, CT34, CT35 |
| F07 | Histórico de leituras e alertas | 3 | 60 | CT36, CT37, CT38 |
| F08 | Gestão de córregos e sensores | 2 | 70 | CT39, CT40, CT41, CT42 |
| F09 | Proteção de dados pessoais (LGPD) | 1 | 85 | CT43, CT44, CT45, CT46, CT47 |

## F01 — Monitoramento do nível do córrego

**Descrição:** Como morador de área de risco de alagamento, quero que o sensor ESP32 instalado no córrego envie automaticamente o nível da água e a chuva para o sistema, para ter uma medição real do córrego da minha rua, e não apenas a previsão de chuva da região inteira.

**Prioridade:** 1  
**Business Value:** 100

**Critérios de aceite:**

- **CA01** — **Dado** um sensor ativo cadastrado, **Quando** o sensor envia POST /api/leituras com sensorId, nivelAguaCm e chuvaMmHora válidos, **Então** a leitura é gravada com data/hora (registradaEm) e a API responde HTTP 201 com a leitura e o nivelRisco calculado.
- **CA02** — **Dado** um sensorId que não existe, **Quando** uma leitura é enviada com esse sensorId, **Então** a API responde HTTP 404 e nenhuma leitura é gravada.
- **CA03** — **Dado** um sensor cadastrado com ativo = false, **Quando** uma leitura é enviada por esse sensor, **Então** a leitura é rejeitada com erro de validação e nenhuma leitura é gravada.
- **CA04** — **Dado** uma leitura com nivelAguaCm ou chuvaMmHora negativos, **Quando** ela é enviada à API, **Então** a API responde erro de validação indicando o campo inválido (0 é o menor valor aceito).
- **CA05** — **Dado** uma leitura sem um dos campos obrigatórios (sensorId, nivelAguaCm, chuvaMmHora), **Quando** ela é enviada à API, **Então** a API responde erro de validação informando o campo ausente.

## F02 — Classificação automática de risco

**Descrição:** Como agente da Defesa Civil / operador do painel, quero que cada leitura seja classificada automaticamente em NORMAL, ATENCAO, ALERTA ou CRITICO, para saber imediatamente a gravidade da situação, sem interpretar números manualmente.

**Prioridade:** 1  
**Business Value:** 100

**Critérios de aceite:**

- **CA01** — **Dado** um córrego com nivelCriticoCm = 180, **Quando** chega uma leitura com nível >= 180 cm (qualquer chuva), **Então** o nivelRisco é CRITICO.
- **CA02** — **Dado** um córrego com nivelAlertaCm = 120 e nivelCriticoCm = 180, **Quando** chega uma leitura com nível entre 120 e 179 cm, **Então** o nivelRisco é ALERTA, mesmo que a chuva seja >= 30 mm/h.
- **CA03** — **Dado** um córrego com nivelAlertaCm = 120, **Quando** chega uma leitura com nível entre 90 cm (0,75 × 120) e 119 cm, **Então** o nivelRisco é ATENCAO.
- **CA04** — **Dado** uma leitura com nível abaixo de 90 cm, **Quando** a chuva informada é >= 30,0 mm/h, **Então** o nivelRisco é ATENCAO.
- **CA05** — **Dado** uma leitura com nível abaixo de 90 cm, **Quando** a chuva informada é menor que 30,0 mm/h, **Então** o nivelRisco é NORMAL.
- **CA06** — **Dado** qualquer leitura classificada, **Quando** o status do córrego é consultado, **Então** o nivelRisco exibido é o mesmo calculado na última leitura.

## F03 — Emissão de alertas

**Descrição:** Como morador cadastrado em um córrego, quero receber um alerta quando o risco do meu córrego chegar a ALERTA ou CRITICO, para ter minutos de antecedência para sair de casa antes da água chegar à rua.

**Prioridade:** 1  
**Business Value:** 95

**Critérios de aceite:**

- **CA01** — **Dado** uma leitura classificada como ALERTA ou CRITICO, **Quando** a leitura é registrada, **Então** a API cria um Alerta ativo para o córrego com nivelRisco, mensagem e nivelAguaCm, e o retorna na resposta da leitura.
- **CA02** — **Dado** uma leitura classificada como NORMAL ou ATENCAO, **Quando** a leitura é registrada, **Então** nenhum Alerta é criado.
- **CA03** — **Dado** um alerta ativo, **Quando** o operador executa PATCH /api/alertas/{id}/encerrar, **Então** o alerta passa a ativo = false e deixa de aparecer em GET /api/alertas?ativos=true.
- **CA04** — **Dado** um id de alerta inexistente, **Quando** o operador tenta encerrá-lo, **Então** a API responde HTTP 404.
- **CA05** — **Dado** um morador com o app instalado e cadastrado no córrego, **Quando** um alerta é criado para esse córrego, **Então** o app exibe notificação com o nível de risco e a mensagem, mesmo com o app em segundo plano.

## F04 — Cadastro de morador

**Descrição:** Como morador de área de risco, quero cadastrar meu nome, telefone, endereço e o córrego próximo da minha casa, para receber os alertas do meu córrego e ser localizado caso precise de ajuda.

**Prioridade:** 1  
**Business Value:** 85

**Critérios de aceite:**

- **CA01** — **Dado** os campos nome, telefone, endereco, corregoId e tipoNecessidade válidos, **Quando** o morador é enviado em POST /api/moradores, **Então** a API responde HTTP 201 com id e criadoEm preenchidos.
- **CA02** — **Dado** o campo nome ou telefone ou endereco vazio/ausente, **Quando** o cadastro é enviado, **Então** a API responde erro de validação e o morador não é gravado.
- **CA03** — **Dado** um telefone fora do formato brasileiro (DDD + 8 ou 9 dígitos, apenas números), **Quando** o cadastro é enviado, **Então** a API responde erro de validação no campo telefone.
- **CA04** — **Dado** um corregoId que não existe, **Quando** o cadastro é enviado, **Então** a API responde erro (HTTP 404 ou de validação) e o morador não é gravado.
- **CA05** — **Dado** um tipoNecessidade fora da lista NENHUMA, IDOSO, CADEIRANTE, ACAMADO, OUTRA, **Quando** o cadastro é enviado, **Então** a API responde erro de validação.
- **CA06** — **Dado** um morador cadastrado, **Quando** seus dados são alterados via PUT /api/moradores/{id}, **Então** a API responde HTTP 200 e a consulta seguinte retorna os novos dados.

## F05 — Priorização de moradores com mobilidade reduzida

**Descrição:** Como agente da Defesa Civil, quero ver a lista dos moradores prioritários (idosos, cadeirantes, acamados) do córrego em risco, para organizar a retirada de quem não consegue sair sozinho antes dos demais.

**Prioridade:** 1  
**Business Value:** 90

**Critérios de aceite:**

- **CA01** — **Dado** um morador cadastrado com tipoNecessidade IDOSO, CADEIRANTE, ACAMADO ou OUTRA, **Quando** o cadastro é gravado, **Então** o morador fica com prioritario = true.
- **CA02** — **Dado** moradores prioritários e não prioritários em vários córregos, **Quando** é chamado GET /api/moradores/prioritarios?corregoId=1, **Então** a resposta contém somente os prioritários do córrego 1.
- **CA03** — **Dado** uma leitura que gera Alerta (ALERTA ou CRITICO), **Quando** a resposta da leitura é retornada, **Então** ela traz a lista de moradores prioritários do córrego para o atendimento.
- **CA04** — **Dado** um córrego sem moradores prioritários, **Quando** a lista de prioritários é consultada, **Então** a API responde HTTP 200 com lista vazia.

## F06 — Consulta de status pelo app

**Descrição:** Como morador, quero abrir o app e ver o nível atual, a chuva e o risco do meu córrego, para decidir se preciso me preparar para sair de casa.

**Prioridade:** 2  
**Business Value:** 80

**Critérios de aceite:**

- **CA01** — **Dado** um córrego com leituras registradas, **Quando** o morador abre a tela de status (GET /api/corregos/{id}/status), **Então** o app mostra último nível, chuva, nivelRisco com cor (verde NORMAL, amarelo ATENCAO, laranja ALERTA, vermelho CRITICO) e data/hora da leitura.
- **CA02** — **Dado** um id de córrego inexistente, **Quando** o status é consultado, **Então** a API responde HTTP 404.
- **CA03** — **Dado** um córrego cadastrado sem nenhuma leitura, **Quando** o status é consultado, **Então** o app exibe "Sem leituras registradas" sem travar ou exibir valores falsos.
- **CA04** — **Dado** o celular sem conexão com a internet, **Quando** o morador abre o app, **Então** o app exibe o último status salvo com o aviso "Sem conexão — dados de <data/hora>" e não fecha inesperadamente.

## F07 — Histórico de leituras e alertas

**Descrição:** Como agente da Defesa Civil / operador do painel web, quero consultar o histórico de leituras e de alertas de um córrego, para analisar como o córrego reage à chuva e medir a antecedência dos alertas.

**Prioridade:** 3  
**Business Value:** 60

**Critérios de aceite:**

- **CA01** — **Dado** um córrego com várias leituras, **Quando** é chamado GET /api/leituras?corregoId=1&limite=5, **Então** retornam no máximo 5 leituras do córrego 1, da mais recente para a mais antiga.
- **CA02** — **Dado** um valor de limite menor que 1 ou não numérico, **Quando** o histórico é consultado, **Então** a API responde erro de validação.
- **CA03** — **Dado** alertas ativos e encerrados, **Quando** é chamado GET /api/alertas?ativos=true&corregoId=1, **Então** retornam apenas alertas ativos do córrego 1.

## F08 — Gestão de córregos e sensores

**Descrição:** Como administrador do sistema, quero cadastrar córregos com seus limites de alerta/crítico e vincular sensores a eles, para expandir o monitoramento para novos córregos com regras corretas.

**Prioridade:** 2  
**Business Value:** 70

**Critérios de aceite:**

- **CA01** — **Dado** nome, bairro, coordenadas e limites válidos (nivelCriticoCm > nivelAlertaCm > 0), **Quando** o córrego é enviado em POST /api/corregos, **Então** a API responde HTTP 201 com o córrego criado.
- **CA02** — **Dado** nivelCriticoCm menor ou igual a nivelAlertaCm, **Quando** o córrego é enviado, **Então** a API responde erro de validação.
- **CA03** — **Dado** um sensor com codigo já existente, **Quando** outro sensor é cadastrado com o mesmo codigo, **Então** a API responde HTTP 409 (conflito) ou erro de validação, sem duplicar.
- **CA04** — **Dado** um sensor com corregoId inexistente, **Quando** o sensor é cadastrado, **Então** a API responde erro e o sensor não é gravado.
- **CA05** — **Dado** um córrego existente, **Quando** ele é consultado por id inexistente (999), **Então** a API responde HTTP 404.

## F09 — Proteção de dados pessoais (LGPD)

**Descrição:** Como morador que informa telefone, endereço e condição de saúde/mobilidade, quero que meus dados pessoais e sensíveis sejam usados apenas para o alerta e o resgate, para não ter minha condição de saúde e meu endereço expostos (LGPD, art. 11 — dado sensível).

**Prioridade:** 1  
**Business Value:** 85

**Critérios de aceite:**

- **CA01** — **Dado** um cadastro ou alteração de morador, **Quando** a API grava os logs da operação, **Então** os logs não contêm telefone, endereço nem tipoNecessidade (no máximo o id do morador).
- **CA02** — **Dado** as rotas públicas de status e alertas, **Quando** elas são consultadas, **Então** a resposta não contém nenhum dado pessoal de moradores.
- **CA03** — **Dado** a tela de cadastro no app, **Quando** o morador tenta enviar sem marcar o aceite do termo de uso e privacidade, **Então** o botão de envio fica desabilitado e nada é enviado à API.
- **CA04** — **Dado** um morador que pede a exclusão dos seus dados, **Quando** é executado DELETE /api/moradores/{id}, **Então** a API responde HTTP 204/200 e uma consulta posterior ao mesmo id retorna HTTP 404.
- **CA05** — **Dado** um erro interno qualquer na API, **Quando** a resposta de erro é devolvida, **Então** ela não exibe stack trace, SQL ou dados de outros moradores.
