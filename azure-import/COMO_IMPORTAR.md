# Como montar o projeto no Azure DevOps e tirar os prints

Tempo estimado: 40–60 min. Faça na ordem. Ao final, preencha o link do projeto na capa do
`GS_QA_Alerta_Corrego.docx`, cole os prints no Anexo A e exporte para PDF.

Arquivos desta pasta:

- `features.csv`: 9 Features (F01–F09) com Description (história de usuário), Acceptance Criteria (CA01…, Dado/Quando/Então), Priority e Business Value.
- `test-cases.csv`: 47 Test Cases (CT01–CT47) com passos (Test Step / Step Action / Step Expected), Priority, Description (feature, objetivo, pré-condições, entradas, resultado esperado, tipo, técnica) e Tags.

---

## 1. Criar a organização e o projeto

1. Acesse https://dev.azure.com e entre com a conta da FIAP/Microsoft.
2. Se ainda não tiver uma organização, crie uma (ex.: `gs-alerta-corrego`).
3. Clique em **+ New project**:
   - Project name: `Alerta Corrego`
   - Visibility: **Private**
   - **Advanced > Work item process: Agile.** No Agile, a Feature tem os campos *Acceptance Criteria*, *Priority* e *Business Value* usados no CSV. O Scrum também funciona; o Basic **não** tem Feature.
4. Clique em **Create**.
5. **Print A1**: página *Overview* do projeto, com a URL visível na barra do navegador.

## 2. Importar as Features

1. Menu lateral **Boards > Work items**.
2. Clique em **Import Work Items** (no topo da lista; se não aparecer, use o menu `...`).
3. **Choose file** → `features.csv` → **Import**.
4. Confira a pré-visualização: 9 itens do tipo *Feature*. Clique em **Save items** (ou **Save all**).
   - Anote os IDs gerados pelo Azure (ex.: F01 = 1, F02 = 2…). Você vai usar esses números no passo 4.
5. **Print A2**: *Boards > Work items* (ou *Boards > Backlogs* com o nível **Features** selecionado) listando F01–F09.
6. Abra a **F02** e tire o **Print A3** (Description, Acceptance Criteria, Priority e Business Value visíveis).
7. Abra a **F09** e tire o **Print A4**.

## 3. Importar os Test Cases

1. **Boards > Work items > Import Work Items** → `test-cases.csv` → **Import**.
2. Na pré-visualização devem aparecer 47 itens do tipo *Test Case*. Ao abrir um deles, os passos aparecem na aba *Steps*.
   As linhas sem Title no CSV são os passos do Test Case acima delas (formato documentado pela Microsoft).
3. Clique em **Save items**.
4. **Print A5**: lista dos Test Cases (em *Work items*, filtre por *Type = Test Case*).
5. Abra o **CT09** (valor-limite) e tire o **Print A6** mostrando os passos (Action / Expected Result).
6. Abra o **CT02** ou o **CT43** (negativo) e tire o **Print A7**.

> Se a importação recusar alguma coluna (por exemplo, *Description* em Test Case num processo personalizado),
> abra o CSV no Excel/LibreOffice, apague só essa coluna, salve como CSV UTF-8 e importe de novo.
> Mesmo sem ela, o objetivo e a técnica de cada teste continuam no PDF e nas Tags.

## 4. Vincular Test Cases às Features (rastreabilidade "Tested By")

A matriz de rastreabilidade do PDF diz qual CT pertence a qual Feature:

| Feature | Test Cases |
|---|---|
| F01 | CT01–CT07 |
| F02 | CT08–CT16 |
| F03 | CT17–CT22 |
| F04 | CT23–CT28 |
| F05 | CT29–CT31 |
| F06 | CT32–CT35 |
| F07 | CT36–CT38 |
| F08 | CT39–CT42 |
| F09 | CT43–CT47 |

Para cada Feature:

1. Abra a Feature e clique em **Add link > Existing item** (aba *Related Work*, ou ícone de link).
2. Em **Link type** escolha **Tested By**.
3. Em **Work items to link** digite os IDs dos Test Cases dessa Feature, separados por vírgula
   (use os IDs que o Azure gerou; o título de cada Test Case começa com o código CTxx).
4. **OK** e **Save**.
5. Depois de vincular a F02, tire o **Print A8** com a seção de links mostrando os Test Cases como *Tested By*.

Dica: cada Test Case também tem a tag da sua Feature (ex.: `F02`). Em *Work items*, filtre por tag para achar os IDs rapidamente.

## 5. Criar o Test Plan e as suítes

1. Menu lateral **Test Plans > + New Test Plan**. Nome: `Homologação Alerta Córrego`. Clique em **Create**.
2. No plano, clique em `...` ao lado do nome > **New Suite > Static suite**. Crie uma suíte por Feature
   (ex.: `F01 - Monitoramento do nível do córrego`).
   - (Requirement-based suite só aceita User Story/PBI. Como os requisitos aqui são Features, use **Static suite**.)
3. Em cada suíte: **Add existing test cases** → filtre por *Tags Contains F01* (ou pelo título `CT0`) → selecione → **Add test cases**.
4. **Print A9**: o plano com as suítes e os Test Cases.
5. (Opcional, mas fica bom) Na aba **Execute**, marque alguns testes como *Passed* / *Failed* depois de rodar contra a API.

## 6. Dar acesso ao professor

1. **Project settings** (canto inferior esquerdo) **> Permissions**.
2. Abra o grupo **Project Administrators** > aba **Members** > **Add**.
3. Digite o e-mail do professor > **Save**.
   - Se o e-mail não for encontrado, primeiro convide-o para a organização em
     **Organization settings > Users > Add users** (Access level: *Basic*; Add to project: `Alerta Corrego`; grupo: *Project Administrators*).
4. **Print A10**: lista de membros de *Project Administrators* com o professor.

## 7. Montar o PDF final

1. Copie a URL do projeto (ex.: `https://dev.azure.com/<organizacao>/Alerta%20Corrego`).
2. Abra `GS_QA_Alerta_Corrego.docx`:
   - Capa: cole a URL no campo **Link do projeto no Azure DevOps** e marque o "(X) sim" do professor.
   - Anexo A: em cada quadro, apague `[ colar o print aqui ]` e cole a imagem correspondente (A1…A10).
3. **Arquivo > Salvar como > PDF** (ou *Exportar > PDF*). Este é o arquivo de entrega.

Checklist dos prints: A1 Overview · A2 lista de Features · A3 F02 aberta · A4 F09 aberta · A5 lista de Test Cases ·
A6 CT09 com passos · A7 CT negativo com passos · A8 Feature com links *Tested By* · A9 Test Plan/suítes ·
A10 professor em Project Administrators.
