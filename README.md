# Tech Challenge — Fase 2 | POSTECH Data Analytics

## 1. Objetivo

Construir um modelo de **classificação supervisionada** que, a partir das informações pessoais e
financeiras informadas no pedido, indique se um solicitante de cartão de crédito tende a ser um
**bom** ou um **mau pagador**. Os resultados também precisam ser traduzidos para a alta direção,
sem termos técnicos.

## 2. Identificação

- 

## 3. Como reproduzir

### 3.1. Pré-requisitos

No seu ambiente, computador:

- Git instalado: 
  - Site oficial: https://git-scm.com
  - Orientações instalar: https://git-scm.com/install/windows

- Python instalado
  - Acesso ao download : https://www.python.org/downloads/

- (opcional) Ambiente IDE  
  - https://code.visualstudio.com/docs/python/python-tutorial
  

### 3.2. Acesso ao código e instalação

Adaptar na indicação abaixo: em alguns ambintes o Python roda com o comando "python3" em vez de "python".

```bash
git clone https://github.com/MelsarDalRiFilho/postech-challenge-fase2.git
cd postech-challenge-fase2

python -m venv .venv
source .venv/bin/activate        # Windows => source .venv\Scripts\activate

pip install -r requirements.txt
jupyter notebook
```

### 3.3. Acesso aos dados de análise

- Baixe o arquivo compactado em: https://drive.google.com/file/d/1UGLHJc6nqCQ-_oW24up37rVnxe4dInWQ/view?usp=sharing
- Extrair os dois arquivos csv do zip no diretório: `data/raw/`  

### 3.4. Execução do notebook

Execute os Notebooks na ordem indicada abaixo:

| # | Notebook | O que faz |
|---|---|---|
| 1 | `notebooks/01_eda.ipynb` | Análise exploratória |
| 2 | `notebooks/02_preprocessamento.ipynb` | Limpeza, escala e feature engineering |
| 3 | `notebooks/03_modelagem.ipynb` | Treino e comparação dos modelos |
| 4 | `notebooks/04_avaliacao.ipynb` | Métricas, importância de variáveis e conclusões |


---

## 4. Relatório executivo

### 4.1 Sequência utilizada

| Parte | Entrega | Onde está |
|---|---|---|
| 0 — Infraestrutura | Código compartilhado em `src/` (caminhos, carga, alvo, features, modelos, métricas, estilo dos gráficos) | `src/*.py` |
| 1 — Análise exploratória | Perfil dos dados, distribuições, correlações, outliers, balanceamento, perfis repetidos | `notebooks/01_eda.ipynb` |
| 2 — Pré-processamento e seleção de atributos | Nulos, definição do alvo, limpeza, novas variáveis, normalização, seleção, grupos de perfil | `notebooks/02_preprocessamento.ipynb` |
| 3 — Modelagem | Split e validação cruzada agrupados, 3 modelos, ajuste de hiperparâmetros, escolha do modelo | `notebooks/03_modelagem.ipynb` |
| 4 — Avaliação | Métricas no teste com intervalos de confiança, curvas, ponto de corte, importância das variáveis, conclusões | `notebooks/04_avaliacao.ipynb` |
| 5 — Apresentação executiva | PDF de 8 slides e página HTML com gráficos Apache ECharts, gerados juntos a partir dos mesmos números | `src/apresentacao.py` + `src/apresentacao_html.py` → `docs/apresentacao_executiva.pdf` e `.html` |
| 6 — Documentação e entrega | README, `data/README.md`, `requirements.txt` | *pendente (aguarda dados do grupo)* |

**Decisões tomadas nos checkpoints:**

| Ponto | Decisão |
|---|---|
| Definição de mau pagador | Atraso de **60 dias ou mais** em qualquer mês do histórico |
| Algoritmos | Somente scikit-learn: Regressão Logística, Random Forest, Gradient Boosting |
| Desbalanceamento | `class_weight="balanced"` (sem geração de dados sintéticos) |
| Perfis repetidos | Split e validação **agrupados por perfil** |
| Sexo como variável | **Excluído do modelo** por critério ético e regulatório |
| Cadastro contraditório | Virou a variável explícita `cadastro_inconsistente` |
| Resultado fraco no teste | Mantido como está, **sem reajustar o modelo olhando o teste** |
| Apresentação | Gerar o PDF a partir dos resultados |

---

### 4.2 Dados fonte

#### 4.2.1 `application_record.csv` — cadastro do solicitante

**438.557 linhas × 18 colunas**, uma linha por pedido.

| Grupo | Colunas |
|---|---|
| Identificação | `ID` |
| Pessoais | `CODE_GENDER`, `DAYS_BIRTH` (idade em dias, negativa), `NAME_FAMILY_STATUS`, `CNT_CHILDREN`, `CNT_FAM_MEMBERS` |
| Educação e trabalho | `NAME_EDUCATION_TYPE`, `NAME_INCOME_TYPE`, `OCCUPATION_TYPE`, `DAYS_EMPLOYED` (tempo de emprego em dias, negativo) |
| Financeiras e patrimônio | `AMT_INCOME_TOTAL` (renda anual), `FLAG_OWN_CAR`, `FLAG_OWN_REALTY`, `NAME_HOUSING_TYPE` |
| Contato | `FLAG_MOBIL`, `FLAG_WORK_PHONE`, `FLAG_PHONE`, `FLAG_EMAIL` |

#### 4.2.2 `credit_record.csv` — histórico mensal de pagamento

**1.048.575 linhas × 3 colunas** (`ID`, `MONTHS_BALANCE`, `STATUS`), com 45.985 clientes e mediana
de 19 meses de histórico por cliente.

| STATUS | Significado | % dos meses |
|---|---|---|
| C | quitado no mês | 42,2% |
| X | sem uso no mês | 20,0% |
| 0 | 1–29 dias de atraso | 36,5% |
| 1 | 30–59 dias | 1,06% |
| 2 | 60–89 dias | 0,08% |
| 3 | 90–119 dias | 0,03% |
| 4 | 120–149 dias | 0,02% |
| 5 | 150+ dias ou baixa como perda | 0,16% |

#### 4.2.3 Problemas de qualidade encontrados

| Problema | Tamanho | Tratamento |
|---|---|---|
| `OCCUPATION_TYPE` nulo | 134.203 linhas (30,6%) | Categoria própria `Nao informado` |
| IDs repetidos com cadastros diferentes | 47 IDs (94 linhas) | Todas as linhas descartadas |
| `DAYS_EMPLOYED = 365243` (≈ 1.000 anos) | 75.329 linhas no cadastro; 6.135 na base de trabalho, todas de pensionistas | Código do sistema → flag `aposentado_ou_sem_vinculo` e tempo de emprego 0 |
| `FLAG_MOBIL` constante (sempre 1) | todas | Removida |
| Pedidos sem histórico de pagamento | ~402 mil | Sem rótulo, ficam fora do treino |
| **Perfis idênticos com IDs diferentes** | 73% das linhas da base de trabalho | Validação agrupada por perfil (ver seção 6.3) |

---

### 4.3. Dados tratados

**Base de trabalho:** junção (`inner join` por `ID`) do cadastro limpo com o alvo. São
**36.457 clientes**, dos quais **616 (1,69%) são maus pagadores**. O arquivo é
`data/processed/dataset_tratado.csv` (não versionado), gerado pelo notebook 02.

### 4.4 Variável alvo

`mau_pagador = 1` se o cliente teve **ao menos um mês com STATUS 2 a 5** (atraso ≥ 60 dias).

**Por que 60 dias:** a distribuição do pior atraso de cada cliente cai abruptamente entre 30–59
dias (4.683 clientes) e 60–89 dias (336). Esse é o ponto em que o atraso deixa de ser esporádico e
vira inadimplência, alinhado à prática de mercado.

- Com 30 dias, 11,6% seriam "maus", misturando atrasos leves.
- Com 90 dias, só 0,7%, poucos exemplos para aprender.

**Nenhuma informação do histórico entra como variável de entrada.** Ela só existe depois da
aprovação, então usá-la seria vazamento.

### 4.5 Variáveis criadas (`src/preprocessing.build_features`)

| Variável | Regra | Motivo |
|---|---|---|
| `idade_anos` | `-DAYS_BIRTH / 365,25` | legibilidade |
| `anos_empregado` | `-DAYS_EMPLOYED / 365,25`; 0 para o código 365243 | remove o valor artificial |
| `aposentado_ou_sem_vinculo` | `DAYS_EMPLOYED == 365243` | preserva a informação do código |
| `renda_per_capita` | renda ÷ pessoas na família | a mesma renda pesa diferente para 1 ou 5 pessoas |
| `cadastro_inconsistente` | pensionista **com** tempo de emprego preenchido | dados contraditórios (achado da seção 5) |
| `FLAG_FEMININO`, `FLAG_OWN_CAR`, `FLAG_OWN_REALTY` | texto → 0/1 | formato numérico |

### 4.6 Seleção de atributos

Critérios aplicados em ordem:

1. **Variância nula:** sai `FLAG_MOBIL`.
2. **Redundância:** sai `CNT_CHILDREN`, que tem correlação de 0,89 com `CNT_FAM_MEMBERS`.
3. **Relevância:** informação mútua com o alvo comparada a uma **linha de base de ruído**, isto é,
   a mesma medida calculada 20 vezes com o alvo embaralhado. Fica quem supera o percentil 95 do
   ruído.
4. **Critério ético:** sexo excluído do modelo (discriminação; LGPD, art. 20). A variável continua
   na base para análises de equidade.

**9 atributos finais:**

| Tipo | Atributos |
|---|---|
| Numéricos (6) | `cadastro_inconsistente`, `idade_anos`, `FLAG_OWN_REALTY`, `anos_empregado`, `AMT_INCOME_TOTAL`, `renda_per_capita` |
| Categóricos (3) | `NAME_FAMILY_STATUS`, `OCCUPATION_TYPE`, `NAME_HOUSING_TYPE` |

A decisão para cada coluna está em `results/metrics/selecao_atributos.csv`. Na validação cruzada,
os 9 atributos tiveram desempenho equivalente ao de todos os 17 candidatos.

### 4.7 Normalização

`StandardScaler` aplicado **somente na Regressão Logística** e **dentro do `Pipeline`**: ele é
reajustado em cada fold só com dados de treino, o que evita vazamento. Os modelos de árvore não
dependem de escala. O `StandardScaler` foi preferido ao `MinMaxScaler` porque a renda tem cauda
longa. As categóricas passam por `OneHotEncoder`, também dentro do `Pipeline`.

---

## 5. Principais achados dos dados

1. **Inadimplência séria é rara: 1,7%, ou 1 em 59 clientes.** Acurácia é inútil: aprovar todo mundo
   já dá 98,3% de acerto.
2. **Nenhuma variável isolada explica o risco.** Todas as correlações com o alvo ficam entre −0,02
   e +0,01.
3. **Sinais fracos que se somam.** A taxa de maus sobe de 1 a 3 pontos percentuais com:
   - pouco tempo no emprego (≈ 2% até 3 anos, contra 1,3% acima de 10 anos);
   - não ter imóvel (2,1% contra 1,5%);
   - viuvez (2,9%);
   - ocupação de baixa qualificação (4,6%);
   - apartamento funcional ou municipal (3,4% e 2,7%);
   - baixa escolaridade (2,7%).
4. **Renda declarada não protege.** A taxa não cai de forma consistente com a renda. A faixa de
   180–247 mil tem a maior taxa (2,1%). Os valores são "redondos", o que sugere renda declarada e
   não comprovada.
5. **73% das linhas repetem o perfil de outra.** Só 9.691 perfis são distintos, com média de 3,8
   cópias por perfil, e 271 perfis aparecem com rótulos conflitantes. É provavelmente o mesmo
   cliente com várias contas.
6. **Cadastro contraditório = risco extremo.** Os 17 clientes declarados pensionistas, mas com tempo
   de emprego ativo, foram **todos** maus pagadores (100%, contra 1,7%). O padrão foi encontrado na
   validação cruzada, só com dados de treino, investigando por que um modelo com todas as
   variáveis tinha o dobro da PR-AUC.

---

## 6. Método adotado e por quê

### 6.1 Tecnologias

| Tecnologia | Versão | Uso | Por que esta |
|---|---|---|---|
| Python | 3.10 (CI em 3.11) | linguagem do projeto | padrão de mercado para análise de dados |
| pandas | 2.2.3 | leitura, junção e transformação | manipulação tabular eficiente e legível |
| NumPy | 2.1.3 | cálculos numéricos, bootstrap | base do ecossistema científico |
| scikit-learn | 1.5.2 | modelos, `Pipeline`, validação, métricas, importância | cobre todo o fluxo com API única; `Pipeline` e `StratifiedGroupKFold` resolvem vazamento e duplicatas sem bibliotecas extras |
| matplotlib | 3.9.2 | gráficos dos notebooks e PDF da apresentação | controle total do layout; gera o PDF sem ferramenta externa |
| seaborn | 0.13.2 | heatmap de correlação e boxplots | atalhos estatísticos sobre o matplotlib |
| Jupyter / nbconvert | 1.1.1 / 7.17.1 | notebooks executados de ponta a ponta | exigência da entrega; `nbconvert --execute` garante a reprodutibilidade |
| joblib | 1.4.2 | salvar os modelos treinados entre os notebooks 03 e 04 | formato padrão do scikit-learn |

**Escolhas deliberadas de não usar:**

- **XGBoost/LightGBM:** o `HistGradientBoostingClassifier` do scikit-learn é da mesma família e
  evita dependências.
- **SMOTE:** `class_weight="balanced"` dá o mesmo efeito de reponderação sem criar clientes
  sintéticos e sem risco de vazamento.
- **Parquet:** CSV evita depender do `pyarrow`.

### 6.2 Por que estes três modelos

| Modelo | Papel |
|---|---|
| **Regressão Logística** | Referência linear, simples, com pesos interpretáveis (razão de chances). Facilita explicar uma recusa ao cliente. |
| **Random Forest** | Média de muitas árvores. Captura interações e relações não lineares, como as vistas na EDA (idade e renda sem tendência linear). |
| **Gradient Boosting** (`HistGradientBoostingClassifier`) | Árvores em sequência, cada uma corrigindo a anterior. Costuma ser o mais forte em dados tabulares. |

Os três usam `class_weight="balanced"` para compensar a classe rara.

### 6.3 Por que validação agrupada por perfil

Com 73% de perfis repetidos, um split aleatório coloca cópias do mesmo cliente no treino e no
teste. O modelo "lembra" o rótulo em vez de aprender um padrão. Para evitar isso:

- **Split treino/teste:** `StratifiedGroupKFold` (5 partes, uma vira teste). São 29.103 clientes de
  treino e 7.354 de teste, com 1,68% e 1,71% de maus e **zero perfis em comum**.
- **Validação cruzada:** `StratifiedGroupKFold` com 5 folds sobre o treino.
- **Grupo = valores idênticos nos 9 atributos que o modelo enxerga.** Agrupar por todas as colunas
  deixava escapar a mesma pessoa com um campo descartado diferente (ex.: telefone), o que mantinha
  um vazamento residual.

**Prova do vazamento:** o mesmo Random Forest teve **AUC de 0,77 com CV comum** e **0,57 com CV
agrupada**. A diferença é ilusória e seria vendida ao negócio como desempenho real.

### 6.4 Por que estas métricas

| Métrica | Pergunta que responde |
|---|---|
| **PR-AUC** (principal) | Quão bem o modelo ordena o risco quando a classe de interesse é rara? O acaso vale 0,017. |
| **AUC-ROC** | Qual a chance de um mau pagador receber nota maior que um bom? O acaso vale 0,5. |
| **Recall** | De cada 100 maus pagadores, quantos o modelo segura? |
| **Precisão** | De cada 100 pedidos sinalizados, quantos são maus pagadores de fato? |
| F1 | Referência; pesa os dois erros igualmente, o que não reflete o negócio. |
| ~~Acurácia~~ | Descartada: 98,3% sem identificar ninguém. |

**Custo dos erros:** aprovar um mau pagador (falso negativo) gera perda de crédito e cobrança.
Recusar um bom (falso positivo) gera perda de receita. O primeiro costuma ser mais caro, mas não a
ponto de justificar recusar dezenas de bons para cada mau.

### 6.5 Ajuste de hiperparâmetros

Busca em grade pequena por modelo (`GridSearchCV`), com a mesma CV agrupada e PR-AUC como critério:

| Modelo | Melhor configuração |
|---|---|
| Regressão Logística | `C = 0,01` (penalização forte) |
| Random Forest | `max_features = 0,5`, `min_samples_leaf = 5`, 300 árvores |
| Gradient Boosting | `learning_rate = 0,1`, `max_leaf_nodes = 31`, `min_samples_leaf = 100` |

---

## 7. Modelo escolhido

**Regressão Logística** (`C = 0,01`, `class_weight="balanced"`, atributos padronizados).

**Validação cruzada agrupada** (5 folds, treino):

| Modelo | PR-AUC | AUC-ROC |
|---|---|---|
| **Regressão Logística** | **0,055 ± 0,032** | **0,578 ± 0,021** |
| Random Forest | 0,040 ± 0,019 | 0,566 ± 0,043 |
| Gradient Boosting | 0,033 ± 0,026 | 0,552 ± 0,044 |
| *sem informação* | *0,017* | *0,500* |

**Motivos da escolha:**

- maior média nas duas métricas;
- menor variação entre folds;
- empate técnico com os demais (os desvios se sobrepõem), desempatado por **simplicidade e
  explicabilidade**: cada atributo tem um peso direto, fácil de auditar.

---

## 8. Resultado obtido

### 8.1 Conjunto de teste (usado uma única vez)

| Modelo | AUC-ROC (IC 95%) | PR-AUC (IC 95%) | Recall* | Precisão* |
|---|---|---|---|---|
| Regressão Logística | 0,511 (0,456 – 0,565) | 0,053 (0,027 – 0,093) | 0,365 | 0,017 |
| Random Forest | 0,598 (0,545 – 0,657) | 0,060 (0,029 – 0,101) | 0,040 | 0,185 |
| Gradient Boosting | 0,559 (0,504 – 0,614) | 0,027 (0,019 – 0,042) | 0,310 | 0,028 |

\* no corte padrão de 0,5. Intervalos por bootstrap com 1.000 reamostragens.

**Leitura honesta:**

- **Ordenação completa:** a Regressão Logística escolhida **não superou o acaso** (o intervalo
  inclui 0,5). O Random Forest foi melhor no teste, mas **não houve troca de modelo**: escolher
  olhando o teste invalidaria a avaliação.
- **Incerteza:** os intervalos dos três modelos se sobrepõem. Com só 126 maus pagadores no teste, a
  diferença entre eles é menor que a incerteza da medição.
- **Onde há sinal:** no **topo da lista de risco**, com PR-AUC cerca de 3 vezes acima do acaso.

### 8.2 Política de uso (ponto de corte definido no treino, sem olhar o teste)

**Política:** sinalizar os **10% de pedidos com maior nota de risco** (corte ≥ 0,593).

| | Treino (*out-of-fold*) | Teste |
|---|---|---|
| % dos maus pagadores capturados | 18,4% | **18,3%** |
| Pedidos sinalizados | 10,0% | 8,0% (591) |
| Precisão entre os sinalizados | — | 3,9% (2,3× a média) |
| Bons sinalizados por mau barrado | 31 | 25 |
| Cadastros inconsistentes sinalizados | — | **3 de 3** |

**Leitura:**

- O topo da lista se reproduz em clientes nunca vistos.
- O modelo encontra cerca do **dobro** de maus pagadores que a escolha ao acaso.
- Para cada mau pagador barrado, ~25 bons clientes são sinalizados. Por isso a recomendação é
  **análise manual, não recusa automática**.

### 8.3 Importância das variáveis

- **Reduzem o risco** (razão de chances < 1):
  - tempo no emprego atual (0,81);
  - imóvel próprio (0,83);
  - ser casado (0,73);
  - morar com os pais (0,79);
  - ocupações como limpeza, vendas, área médica e serviços privados.
- **Aumentam o risco** (> 1):
  - viuvez (1,48);
  - apartamento funcional (1,41);
  - ocupações como técnicos especializados (1,62), baixa qualificação (1,42) e motoristas;
  - cadastro inconsistente.
- **Ajudam a prever clientes novos** (permutação no teste): estado civil, tempo de emprego e
  cadastro inconsistente, este com o efeito mais estável.
- **Prejudica:** `renda_per_capita`. Embaralhá-la melhora a AUC em 0,05, porque o contraste de renda
  aprendido no treino não se repetiu. Esse é o principal motivo da queda da Logística no teste.

### 8.4 Conclusões de negócio

1. **Não automatizar a recusa** com base só no cadastro.
2. **Triagem:** os ~10% de pedidos de maior risco vão para análise manual, com documentação extra
   ou limite menor.
3. **Regra de alerta para cadastros contraditórios.** É o achado mais forte, simples e barato.
4. **Valorizar sinais de estabilidade** (emprego, imóvel, situação familiar). A renda declarada não
   deve pesar sozinha.
5. **Investir em dados melhores:** birô de crédito e comprovação de renda são o caminho para
   prever melhor.

### 8.5 Limitações

- Poder de previsão baixo e instável. Só o topo da lista de risco é confiável.
- Apenas 616 maus pagadores. As métricas variam muito com poucos casos.
- A regra do cadastro inconsistente se apoia em 17 casos e precisa ser validada com dados novos.
- Sem data do pedido, não foi possível fazer validação temporal.
- Viés de seleção: só há rótulo para quem foi aprovado.
- **Próximo passo registrado:** testar o modelo sem as variáveis de renda, decidindo apenas com
  validação cruzada.

---

## 9. Artefatos gerados

| Tipo | Arquivo | Versionado |
|---|---|---|
| Notebooks executados | `notebooks/01_eda.ipynb` … `04_avaliacao.ipynb` | sim |
| Figuras | `results/figures/01_*` … `04_*` (16 PNGs) | sim |
| Métricas | `results/metrics/selecao_atributos.csv`, `validacao_cruzada.csv`, `comparacao_modelos.csv`, `teste_intervalos.csv`, `importancia_permutacao.csv`, `curva_captura.csv`, `resumo_negocio.json` | sim |
| Apresentação | `docs/apresentacao_executiva.pdf` (8 slides) e `docs/apresentacao_executiva.html` (página única, Apache ECharts) — ambos gerados por `python -m src.apresentacao` | sim |
| Dados tratados e split | `data/processed/dataset_tratado.csv`, `split.csv` | não |
| Modelos treinados | `results/models/modelos.joblib` | não |
| Código compartilhado | `src/config.py`, `data.py`, `preprocessing.py`, `models.py`, `evaluation.py`, `viz.py`, `apresentacao.py`, `apresentacao_html.py` | sim |
