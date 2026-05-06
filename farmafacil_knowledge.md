# Base de Conhecimento FarmaFácil / PrismaFive

> Gerado automaticamente em 17/04/2026 11:19 a partir de 288 artigos da base de conhecimento oficial.
>
> **Legenda de confiabilidade:**
> - 🟢 Artigo recente (menos de 1 ano) — alta confiabilidade
> - 🟡 Artigo médio (1 a 2 anos) — verificar se ainda válido
> - 🔴 Artigo antigo (mais de 2 anos) — **⚠️ INFORMAR AO ANALISTA: pode estar desatualizado**

---

## Índice por confiabilidade

- 🟢 Artigos recentes: 53
- 🟡 Artigos médios: 90
- 🔴 Artigos antigos (verificar): 145

---

## 🟢 🛠️ Notas da Versão 20.01.90.15 — 02/04/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/581878
> Publicado em: 02/04/2026

🛠️ Notas da Versão 20.01.90.15
📅
Data de Liberação: 02/04/2026
A versão 20.01.90.15 do
FarmaFácil Desktop
incorpora avanços importantes em funcionalidades estratégicas, além de revisões que garantem maior consistência nas operações do sistema.
⚙️
Melhorias
ID-801
– Inclusão do campo
“Localização Lab”
no cadastro de produtos, permitindo maior rastreabilidade e organização das informações.
ID-814
– Implementação de opção para ajuste de
Markup
e
Valor de Venda por valor fixo
, além do modelo percentual já existente.
ID-822
– Inclusão da
tag de localização LAB
nos rótulos, possibilitando personalização das impressões.
ID-823
– Ordem de produção impressa com informações mais detalhadas
ID-827
– Geração do registro
H020
no arquivo do
SPED Fiscal
, atendendo às exigências fiscais.
ID-856
– Adequação para emissão de
NFS-e
via provedor
ISSNETONLINE20
para o município de Ribeirão Preto.
ID-865
– Implementação de opção para impressão de
rol’s
em impressoras
Jato de Tinta / Laser
.
ID-862
– Ajuste na definição automática do
Tipo de Receita
, considerando o tipo de registro do profissional (
CRMV
).
ID-869
– Revisão do comportamento na edição do campo
Proximidade
entre endereço principal e endereço de entrega no cadastro de clientes.
ID-874
– Permissão para configuração de
regime tributário distinto
entre
NF-e
e
NFS-e
.
ID-878
– Adequação no envio de
NFS-e
para o provedor
ISSNet
, considerando atualizações da Reforma Tributária.
🧩
Comportamentos Revisados
ID-677
– Revisão na repetição de vendas para manter a descrição alterada via
CTRL + E.
ID-718
– Revisão nos cálculos de associação do
QSP
em formas farmacêuticas de
volume
e
Vol x QTD
.
ID-816
– Revisão na apresentação da descrição informada via
CTRL + E
nas mensagens do
SYNC
e
ORYA
.
ID-817
– Revisão na atualização das informações do rótulo modelo 4 na tela de vendas afim de sempre carregar as informações corretas da venda.
ID-818
– Revisão dos cálculos dos campos
Quantidade Calculada
e
Custo MP
no relatório de Fórmula Padrão para fórmulas do tipo
Volume x QTD
.
ID-819
– Revisão na geração de linhas no arquivo
.txt do SIPROQUIM2
, evitando duplicidade em entradas de insumo.
ID-824
– Revisão na leitura do código de barras da
DANFE simplificada
.
ID-836
– Revisão na exibição das notas de entrada no
balanço controlado de drogaria
.
ID-837
– Revisão na geração do código de barras em etiquetas de estoque via
Ordem de Manipulação
.
ID-839
– Revisão na emissão de
NFS-e
para o município de Cravinhos via padrão
TecnoSpeed
.
ID-857
– Revisão no cálculo de
volume
de fórmulas para o tipo de cálculo
sem cálculo
.
ID-860
– Revisão no processo de
pesagem monitorada
para considerar a margem padrão para produtos desmembrados .
ID-864
– Revisão na exibição da mensagem de
“Excipiente Negativo”
ao repetir vendas de cápsulas mesmo quando o vol x cap estivesse compativel com o tamanho da capsula.
ID-866
– Revisão na emissão de
NFS-e
sem a tag
Código de Tributação do Município
quando configurado
API Própria
.
ID-867
– Revisão de 
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Adequação de Telefones às Regras Fiscais (SEFAZ e Prefeituras) — 30/03/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/581211
> Publicado em: 30/03/2026

Contexto
Foi identificado um comportamento recorrente no sistema Farma Fácil relacionado ao cadastro de telefones de clientes, que pode impactar diretamente a emissão de notas fiscais (NF-e, NFC-e e NFS-e).
Esse cenário ocorre devido à adequação do sistema às exigências atuais de validação fiscal.
Problema
Falha na emissão de nota fiscal devido à inconsistência no campo de
telefone
do cliente. O erro ocorre quando a quantidade de dígitos informada não atende ao padrão regulatório ou do sistema.
Causa
Em versões anteriores do sistema:
Não havia validação rígida dos números
Eram aceitos formatos variados
Atualmente:
Há validações baseadas na quantidade de dígitos
O sistema foi ajustado para atender exigências fiscais
Cadastros antigos podem permanecer fora do padrão
Regras de Validação
Celular
Até 12 dígitos
Pode conter:
DDD com 2 dígitos (com ou sem zero na frente)
Número com 9 dígitos iniciando em 9
Telefone (Fixo)
Até 11 dígitos
Deve conter:
DDD com 2 dígitos
Número com 8 dígitos (sem o 9 inicial)
Importante:
O erro de emissão ocorre quando o campo excede o limite de 11 dígitos (DDD + Número). Para fixos, a estrutura obrigatória é:
DDD: 3 dígitos entre parênteses — Ex:
(
047
)
ou (
479
).
Número: Exatamente 8 dígitos — Ex: 88888888.
Atenção
:
Se o campo "Número" contiver 9 dígitos, o total somará 12 caracteres, o que é incompatível com o padrão de telefonia fixa e causa a rejeição no sistema.
Validação dos Órgãos Fiscais
A validação considera principalmente:
Quantidade de dígitos
Estrutura do número
Limites observados:
Telefone fixo: até 11 dígitos
Celular: até 12 dígitos
Como Corrigir
Opção 1 – Ajustar o DDD
Remover o zero inicial
Exemplo:
049999999999 → 49999999999
Opção 2 – Ajustar o número
Remover o dígito 9 inicial (para telefone fixo)
Exemplo:
049988888888 → 04988888888
Boas Práticas
Utilizar o campo correto para cada tipo de número
Celular → números com 9 dígitos
Telefone → números fixos (8 dígitos)
Evitar padrões antigos
Revisar cadastros antigos
Observações
O sistema ainda permite algumas variações no campo telefone
Isso poderá ser ajustado em versões futuras
A validação final é feita pelos órgãos fiscais
Importante
Cadastros antigos não são corrigidos automaticamente.
É necessário realizar ajuste manual para evitar erros na emissão.

---

## 🟢 NOTA FISCAL PARA O EXTERIOR — 30/03/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/581206
> Publicado em: 30/03/2026

NOTA FISCAL PARA O EXTERIOR
Neste artigo, vamos aprender como realizar a emissão de nota fiscal para o exterior, abordando as principais configurações e o passo a passo necessário para preencher corretamente esse tipo de operação no sistema.
A primeira etapa para realizar a emissão de uma nota para o exterior é verificar se o cadastro do cliente está completo. É necessário que ele esteja preenchido conforme o layout abaixo para que a emissão ocorra corretamente.
Caso a farmácia já possua um cliente fixo que tenha se mudado recentemente para o exterior, basta atualizar o cadastro existente, seguindo o passo a passo conforme demonstrado nos prints abaixo:
Para obter o código do IBGE, você pode realizar a pesquisa diretamente no Google ou em outro navegador de sua preferência. Caso, ao final do processo, ocorra erro relacionado a esse código, é possível utilizar o código genérico
9999999
.
Da mesma forma que foi realizado o cadastro da cidade, deverá ser feito também o cadastro do bairro.
Após inserir todas as informações, será necessário informar o local de saída da mercadoria, ou seja, onde essa mercadoria será embarcada.
Após a conclusão dessa etapa, vamos prosseguir para a criação da nota.
⚠️
Atenção:
A partir deste momento, todas as informações devem ser validadas junto à contabilidade antes da emissão da nota. O preenchimento incorreto, especialmente do NCM do produto, pode gerar multas para a farmácia, assim como inconsistências nos demais campos.
Verifique corretamente os seguintes dados:
CFOP
CST
CSOSN
NCM
Antes de emitir a nota, há mais um ponto importante: caso o cliente possua o número de DI (Declaração de Importação), essa informação deverá ser preenchida.
Caso o cliente não possua esse dado, a nota pode ser salva normalmente e emitida sem esse preenchimento.
Em caso de erros na emissão, verifique e, se necessário, ajuste as seguintes informações no cadastro:
Remover a opção
“ISENTO”
da Inscrição Estadual (IE), devido ao erro relacionado a contribuinte de ICMS
Definir o
estado como “EX”
(Exterior)
Ajustar o
NCM para 61019090
(foi o código que validou na emissão)
Informar o
CSOSN como 300
Não preencher o campo de
local de entrega
Após esses ajustes, tente realizar a emissão novamente.
⚠️
Observação:
Sempre consulte a contabilidade para validar quais dados devem ser informados na nota.

---

## 🟢 Como Unificar Cadastros de Convênio no Sistema — 30/03/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/581203
> Publicado em: 30/03/2026

Em muitos casos, é comum que clientes realizem mais de um cadastro para o mesmo convênio dentro do sistema. Normalmente, quando isso acontece, um dos cadastros acaba sendo apenas inativado, o que pode gerar acúmulo de registros desnecessários e dificultar a organização.
Para resolver esse problema, o sistema disponibiliza a funcionalidade de
unificação de cadastros de convênio
, permitindo consolidar múltiplos registros em apenas um.
Quando utilizar a unificação?
A unificação deve ser utilizada quando:
Existem dois ou mais cadastros para o mesmo convênio;
Um dos cadastros foi criado de forma duplicada;
Deseja-se manter apenas um código ativo no sistema.
Como acessar a funcionalidade
Para realizar a unificação, siga o caminho abaixo:
Arquivo > Utilitário > Manutenção Geral
Localize a opção
“ALTERAÇÃO DO CÓDIGO DO CONVÊNIO”
;
Marque essa opção para habilitar a funcionalidade;
Informe o código do convênio que será unificado (cadastro antigo ou duplicado);
No campo
“NOVO CÓDIGO”
, informe o código que deverá permanecer no sistema. Atenção: O “novo código” será o cadastro final, ou seja, o único que permanecerá ativo após a unificação.
Finalizando o processo
Após preencher corretamente as informações:
Clique em
“Salvar Alteração”
;
Com isso, o sistema irá unificar os cadastros e manter apenas um registro válido.
Resultado
Ao final do processo:
Apenas um cadastro de convênio permanecerá no sistema;
Os registros duplicados serão consolidados;
A base de dados ficará mais organizada e consistente.

---

## 🟢 Unificar Cadastro de Cliente — 24/03/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/580552
> Publicado em: 24/03/2026

Neste artigo será apresentado o passo a passo para unificar o cadastro de clientes no sistema. O objetivo é orientar o usuário na identificação de registros duplicados e na realização do processo de unificação, garantindo que todas as informações fiquem centralizadas em um único cadastro. Com isso, é possível evitar inconsistências, melhorar a organização dos dados e otimizar o uso do sistema no dia a dia.
1-
Arquivo > Utilitário > Manutenção geral.
2- Selecione o campo : Alteração do Código do Cliente

---

## 🟢 DRE & Plano de contas — 18/03/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/579736
> Publicado em: 18/03/2026

Segue em anexo E-book para DRE & Plano de contas.

---

## 🟢 🛠️ Notas da Versão 20.01.90.13 — 27/02/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/577324
> Publicado em: 27/02/2026

🛠️ Notas da Versão 20.01.90.13
📅
Data de Liberação: 27/02/2026
A versão 20.01.90.14 do
FarmaFácil Desktop
incorpora avanços importantes em funcionalidades estratégicas, além de revisões que garantem maior consistência nas operações do sistema.
⚙️
Melhorias
ID-774
– Homolagada a integração com o provedor SigCorp para envio das informações relacionadas à reforma tributária.
ID-783
– Homologada a emissão de NFSe com o provedor FintelISS no Padrão Nacional para o município de Juiz de Fora/MG.
ID-789
–
Homolagada
a integração com o provedor SilTecnologia para envio de PIS e COFINS conforme parametrização do sistema.
ID-802
–
Homolagad
a a integração com o provedor PRONIM utilizando API própria no Padrão Nacional.
ID-825
– Ajustado a composição da base de cálculo do IPI, desconsiderando frete e outras despesas.
ID-720
– Melhoria do provedor no Padrão Nacional para envio de e-mail e visualização da NFSe.
🧩
Comportamentos Revisados
ID-709
– revisados envio de NFSe para aplicação de desconto concedido no caixa.
ID-853
– Inserido novas Natureza de Operação para NFSe com o provedor Pública.
ID-785
– Revisadoo comportamento de edição das NFSe/NFE para evitar duplicidade de itens.
ID-794
– Re-homologação do município de Sinop/MT para emissão de NFSe.
ID-800
– Re-homologação do município de Presidente Prudente/SP para emissão de NFSe.
ID-805
– Re-homologação do provedor Pública para envio das informações da NFSe no município de Itajaí/SC.
ID-806
– Re-homologação do provedor SimpISS para retorno e visualização da NFSe no município de Volta Redonda/RJ.
ID-815
– Re-homologação do provedor SilTecnologia para emissão de NFSe.
ID-820
– Re-homologação do município de São Bernardo do Campo/SP para emissão de NFSe.
ID-826
– Re-homologação do envio de NFSe no Padrão Nacional para regime Normal.
ID-828
– Re-homologação do envio do código NBS para NFSe com integração via TecnoSpeed.
ID-830
– Re-homologação da integração com o IPM 2.0 no Padrão Nacional para o município de Porto Belo/SC.
ID-831
– Re-homologação do município de Canoas/RS provedor SILTECNOLOGIA para atualização da situação da NFSe.
ID-832
– Re-homologação do município de Garibaldi/RS para emissão de NFSe via TecnoSpeed.
ID-834
– Re-homologação do provedor SigISS no município de Rio Grande/RS.
ID-840
– Re-homologação do provedor Betha para retorno e visualização da NFSe no município de Porto União/SC.
ID-841
– Re-homologação do município de Bauru/SP para visualização da NFSe provedor SILTecnologia via API própria.
ID-842
– Re-homologação do provedor GISSOnline para visualização da NFSe no município de São José do Rio Preto/SP.
ID-797
– Comportamento revisado no processo de importação do arquivo AUTTAR conforme layout atualizado.
ID-798
– Comportamento revisado na validação do peso do paciente no cadastro pela tela de fórmula.
ID-803
– Comportamento revisado no recálculo de embalagem e cápsulas ao carregar pré-venda.
ID-811
– Comportamento revisado na vinculação de veículo nas formas farmacêuticas Floral e Pap
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 🛠️ Notas da Versão 20.01.90.13 — 04/02/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/574566
> Publicado em: 04/02/2026

🛠️ Notas da Versão 20.01.90.13
📅
Data de Liberação: 04/02/2026
A versão 20.01.90.13 do
FarmaFácil Desktop
incorpora avanços importantes em funcionalidades estratégicas, além de revisões que garantem maior consistência nas operações do sistema.
⚙️
Melhorias
[ID-761]
A integração de NFS-e de Salvador foi atualizada para atender ao novo layout exigido pela reforma tributária.
[ID-760]
Foram aplicadas atualizações no ACBr e nos códigos fiscais relacionados à NFS-e.
[ID-733]
O cabeçalho da nota de entrada passou a aceitar séries com mais de dois dígitos.
[ID-738]
O relatório de produtos por tributação de grupo passou a contemplar os tributos da reforma tributária.
[ID-741]
O módulo de NFS-e passou a disponibilizar o campo
Código de Serviço Nacional (CSN)
.
[ID-746]
Foi aprimorado o vínculo de orçamentos recebidos via Sync/Orya quando direcionados entre filiais.
[ID-748]
O módulo de Inventário passou a contar com filtro para produtos
Ativos, Inativos ou Ambos
.
[ID-751]
A rotina
Manutenção Geral > Alterar Tributação de Grupos
passou a permitir filtro por tipo de grupo.
[ID-752]
O cadastro de prescritores foi ampliado para suportar novos conselhos aceitos pelo SNGPC.
[ID-753]
A base de cálculo do PIS/COFINS foi ajustada para desconsiderar o ICMS.
[ID-757]
O processo de emissão de NFC-e com local de entrega foi adequado às regras da reforma tributária (IBS/CBS).
[ID-762]
A integração NFS-e ISSNet foi atualizada para envio do código NBS.
[ID-766]
A integração NFS-e com o provedor SILTECNOLOGIA foi adaptada para utilização de API própria no Modelo Padrão Nacional.
[ID-771]
A integração NFS-e com o provedor BETHA foi adaptada para utilização de API própria no Modelo Padrão Nacional.
[ID-777]
A integração NFS-e ISSNatal passou a contemplar as tags exigidas pela reforma tributária.
🧩
Comportamentos Revisados
[ID-661]
O tratamento dos valores de custo em notas de entrada com unidade em KG foi revisado e ajustado.
[ID-691]
O comportamento relacionado à atualização da validade das fórmulas foi revisado.
[ID-697]
A geração de rótulos do tipo Fórmula Padrão (modelo 2) teve seu comportamento revisado quanto à inclusão de tags.
[ID-703]
O processo de geração de fórmulas com ativos associados a fórmulas padrão desmembradas foi revisado para evitar duplicidades.
[ID-719]
Foi revisado o cálculo dos subtotais no relatório de Romaneio de Entrega (modelo sintético).
[ID-728]
O relatório de descontos teve o tratamento dos valores revisado.
[ID-732]
O utilitário de alteração de cabeçalho das notas de entrada passou por revisão no processo de substituição do cabeçalho anterior.
[ID-735]
O comportamento da retenção de ISS em NFS-e foi revisado no Modelo Padrão Nacional.
[ID-739]
A exibição do código do cliente no relatório sintético de notas fiscais foi revisada.
[ID-740]
O limite de caracteres do número da receita nos relatórios A e B2 foi revisado.
[ID-743]
O comportamento de atualização do preço de venda após a inclusão de ativos foi revisado.
[ID-744]
O processo de atuali
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 📖 Guia: Configurando Horários e Mensagens Automáticas (Nexys/Orya) — 29/01/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/573856
> Publicado em: 29/01/2026

Este guia prático ensina como gerenciar a disponibilidade do seu atendimento no WhatsApp e personalizar as mensagens que seus clientes recebem ao entrar em contato.
1. Acessando as Configurações
O primeiro passo é localizar o menu de gerenciamento do sistema:
No menu lateral esquerdo, localize e clique em
Orya
.
Clique na opção
Preferências
para expandir as subcategorias.
Selecione
Horário de Atendimento
.
2. Definindo a Grade de Horários
Nesta tela, você define em quais períodos sua equipe estará disponível para responder.
Ativação:
Certifique-se de que a chave
Horário de Atendimento
esteja marcada como
Ativar
.
Configuração por dia:
Para cada dia da semana (Segunda a Sábado), insira o horário de
Início
e
Fim
(Ex: 08:00 às 18:00).
Dias sem expediente:
Para dias em que a farmácia não abre (como o Domingo no exemplo), marque a opção
Não terá atendimento
.
3. Personalizando Mensagens (Saudação e Ausência)
Abaixo dos horários, você encontrará os campos para automatizar a comunicação:
Mensagem de Saudação
O que é:
O texto enviado automaticamente quando um cliente inicia um contato dentro do horário de expediente.
Dica:
Use este espaço para dar boas-vindas e informar canais oficiais de suporte ou pedidos.
Mensagem de Ausência
O que é:
O texto enviado quando o cliente chama
fora
dos horários definidos no passo anterior.
Dica:
Informe que a equipe está ausente e deixe um número de plantão ou o horário de retorno das atividades.
4. Intervalo e Finalização
Intervalo entre mensagens:
Existe um campo para definir o tempo (em minutos) antes que o sistema envie a mesma mensagem automática para o mesmo cliente novamente. No exemplo, está configurado para um intervalo longo para evitar spam.
Salvar:
Após realizar todas as alterações,
nunca esqueça de clicar no botão azul "Salvar"
no rodapé da página para aplicar as configurações.
5. Conclusão:
Com essas configurações concluídas, o atendimento via WhatsApp ficará alinhado ao horário de funcionamento da farmácia, garantindo uma comunicação mais organizada, profissional e transparente com os clientes.
Manter os horários e mensagens automáticas corretamente configurados ajuda a evitar dúvidas, melhora a experiência do cliente e otimiza o fluxo de atendimento da equipe. Sempre que houver mudanças nos horários ou na estratégia de comunicação, recomendamos revisar essas configurações.

---

## 🟢 Caixa – Recebimento de Vendas — 19/01/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/572615
> Publicado em: 19/01/2026

Para que serve o Recebimento de Vendas
O
Recebimento de Vendas
é a etapa onde a venda criada no sistema é
baixada no caixa
e
registrada fiscalmente
.
É a partir desse processo que o sistema consegue:
Controlar o pagamento da venda
Emitir
NFC-e (Cupom Fiscal)
Gerar
NF-e ou NFS-e
, quando necessário
Onde a venda nasce
A venda
nasce na Tela de Vendas
, separadamente.
Após isso, o cliente deve:
Acessar o
Caixa
Informar o
número da venda
Realizar o
recebimento
para dar baixa nela
📌 Enquanto o recebimento não for feito, a venda permanece
em aberto
.
Onde acessar o recebimento
Menu:
Caixa → Caixa
No campo
Tipo de Lançamento
, selecione:
Recebimento Venda
Como funciona o Recebimento de Vendas
1. Informar o número da venda
Digite ou pesquise o
número da venda
O sistema irá carregar:
Cliente
Vendedor
Itens da venda
Valor total
Valor a receber
2. Formas de pagamento
Pressione
F8 – Selecionar forma de pagamento
.
As formas de pagamento mais utilizadas são:
Pix
Dinheiro
Cartão
É possível utilizar
mais de uma forma de pagamento
na mesma venda.
👉 Caso seja necessário
cadastrar ou configurar novas formas de pagamento
, consulte o artigo:
🔗
Formas de Pagamento – Cadastro e Configuração
https://prismafive.movidesk.com/kb/pt-br/article/431853/formas-de-pagamento?ticketId=&q=
3. Vendas a prazo
Quando a venda for
a prazo
:
O sistema permite receber
parcelas
Enquanto o valor total não for recebido:
Não é gerado documento fiscal
É emitido apenas um
comprovante de recebimento
📌 O documento fiscal (NFC-e, NF-e ou NFS-e) será gerado
somente após a finalização total do pagamento
.
👉 Para entender como configurar e receber vendas a prazo, consulte o artigo:
🔗
Configuração e Recebimento de Vendas a Prazo
https://prismafive.movidesk.com/kb/pt-br/article/287765/vendas-a-prazo?ticketId=&q=
Emissão de documentos fiscais
Impressora – NFC-e (Cupom Fiscal)
A
impressora sempre gera NFC-e, SAT ou ECF
Ao finalizar o recebimento e clicar na impressora:
O sistema emite a
NFC-e, SAT ou ECF
📌 Se o recebimento for
parcial
, será gerado apenas um comprovante.
A NFC-e será emitida
somente após o recebimento total da venda
.
Botão de Nota Fiscal
O botão ao lado da impressora abre a
Tela de Nota Fiscal
Nessa tela, é possível selecionar:
Nota Fiscal de Serviço
Nota Fiscal de Fatura
Esse botão deve ser utilizado quando o cliente solicita
nota fiscal em vez de cupom
.
Fluxo resumido
Venda criada na
Tela de Vendas
No Caixa, informar o
número da venda
Selecionar a
forma de pagamento (F8)
Finalizar o recebimento
Escolher:
Impressora →
NFC-e, SAT ou ECF
Botão Nota Fiscal → Nota Fiscal (Serviço ou Fatura)
Importante
Sem recebimento no Caixa:
A venda não é baixada
O documento fiscal não é gerado
Sempre confira:
Data
Turno
Filial
Forma de pagamento
Erros nesses dados podem causar
diferença de caixa
ou
problemas fiscais
.

---

## 🟢 Relatório de Movimento de Caixa — 19/01/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/572613
> Publicado em: 19/01/2026

Relatório de Movimento de Caixa
Onde encontrar
Você pode acessar o
Movimento de Caixa
pelo caminho:
Caixa → Relatórios → Movimento de Caixa
Esse relatório mostra
tudo o que entrou e saiu do caixa em um dia ou turno específico
.
Para que serve
O Movimento de Caixa é usado para:
Conferir a
abertura e o fechamento do caixa
Ver os
valores recebidos
Conferir
formas de pagamento
Validar o
saldo final do caixa
Como preencher o relatório
Classificação
Escolha como o relatório será exibido:
Analítico
Mostra todas as informações detalhadas (clientes, valores e pagamentos).
Sintético
Mostra apenas os valores totais.
👉 Recomendamos usar
Analítico
para conferência completa.
Seleção
Turno
Informe o número do turno
Data de Referência
Selecione a data que deseja consultar
Filial
Escolha a filial correta onde o caixa foi movimentado
Cópias
Informe quantas cópias do relatório deseja gerar
Como gerar
Após preencher os campos:
Clique em
Imprimir ou visualizar
O relatório será gerado com todas as movimentações do período escolhido
Informações que aparecem no relatório
Abertura
Valor inicial informado na abertura do caixa
Recebimentos
Mostra os valores recebidos, separados por forma de pagamento, como:
Dinheiro
Cartão
Boleto pago
A prazo / Parcelamento
Cada lançamento pode mostrar o cliente e o valor recebido.
Outros Lançamentos
Valores que não são venda direta, como parcelamentos ou ajustes
Totais e Saldo
Total recebido no período
Quantidade de recebimentos
Valor médio por recebimento
Saldo final do caixa

---

## 🟢 Como emitir Nota Fiscal de Devolução no FarmaFácil — 19/01/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/572611
> Publicado em: 19/01/2026

Como emitir Nota Fiscal de Devolução no FarmaFácil
Este artigo explica
como emitir uma Nota Fiscal de Devolução no sistema FarmaFácil
, destacando os pontos fiscais mais importantes e o caminho correto dentro do sistema.
⚠️
Importante:
Sempre recomendamos que a
contabilidade acompanhe o processo de devolução
, para evitar problemas fiscais, divergências de impostos ou rejeições pela SEFAZ.
1. Acessando a tela de emissão da nota
A Nota Fiscal de Devolução é emitida pelo módulo de caixa.
Caminho no sistema:
Caixa → Nota Fiscal
Esse menu abre a tela de
Nota Fiscal Eletrônica
, onde a devolução será configurada.
2. Configurações iniciais da nota
Na tela de emissão da nota:
Tipo
: Nota Fiscal Eletrônica (Fatura)
Data de Emissão
: conforme a data da devolução
Série / Sub-série
: conforme padrão da empresa
No campo
Finalidade
, selecione:
4 – Devolução
3. Dados do cliente ou fornecedor
Informe o
Cliente
(devolução de venda)
ou o
Fornecedor
(devolução de cmpra)
Confira os dados de endereço, cidade e estado
Os dados cadastrais devem estar corretos para evitar rejeições fiscais.
4. Informando a nota fiscal de origem
A referência da nota original é
obrigatória
em uma devolução.
No FarmaFácil, essa informação deve ser preenchida em:
Dados Adicionais → Devolução
Nesse local:
Informe a
chave de acesso da nota fiscal original
Esse vínculo caracteriza fiscalmente a devolução.
5. Inclusão dos produtos devolvidos
Na grade de itens da nota:
Informe os
produtos que estão sendo devolvidos
Utilize as
quantidades corretas
(total ou parcial)
Confira:
CFOP de devolução
CST / CSOSN
Tributos (ICMS, PIS, COFINS)
O CFOP deve ser específico de devolução, conforme orientação contábil.
7. Detalhamento dos itens na devolução (Manutenção Item Nota Fiscal)
Ao incluir ou editar um produto na Nota Fiscal de Devolução, o sistema abre a tela
Manutenção Item Nota Fiscal
. Essa tela é responsável por definir
quantidade, valores e principalmente a tributação do item
.
7.1 Identificação do item
Na parte superior da tela:
Produto
: item que está sendo devolvido
Quantidade
: quantidade devolvida (total ou parcial)
Unidade
: normalmente "UN"
Valor Unitário
: deve refletir o valor da nota original
🔎
Importante:
A Nota Fiscal de Devolução
não realiza baixa de lote/estoque
. Por esse motivo,
é possível alterar o nome/descrição do produto
, caso seja necessário, sem impacto no controle de lotes.
Em devoluções, os valores devem manter coerência com a nota de origem.
7.2 Natureza da Operação (CFOP)
No campo
Nat Op.
:
Informe o
CFOP de devolução
adequado
Exemplo exibido na tela:
5201 – Devolução de compra para industrialização
O CFOP correto deve ser validado com a
contabilidade
, pois impacta diretamente na apuração dos impostos.
7.3 Tributação do ICMS
Campos relacionados ao ICMS:
ICMS (%)
Base de Cálculo do ICMS
Valor do ICMS
ICMS ST / ICMS ST Retido
(quando aplicável)
Redução de Base / Diferimento
(se houver)
Esses dados devem seguir exatamente a orientação fiscal da nota original e da contabili
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Como exportar XMLs no FarmaFácil (passo a passo) — 19/01/2026

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/572609
> Publicado em: 19/01/2026

Este artigo explica
passo a passo
como realizar a
exportação de XMLs de documentos fiscais (NFC-e)
no sistema
FarmaFácil
, utilizando o caminho correto do menu e as opções adequadas, conforme demonstrado nos prints.
1. Acessando o menu correto
No FarmaFácil, siga o caminho abaixo:
Arquivo → Utilitário → Exportação de Arquivo
Esse caminho leva à tela de
Manutenção de Exportação de Arquivo
, onde é possível selecionar quais informações serão exportadas.
2. Selecionando os dados para exportação
Na tela
Manutenção Exportação Arquivo
:
Localize a seção
Selecione os dados para exportar
Marque
somente
a opção:
Documentos Fiscais
Essa opção é responsável pela exportação dos arquivos
XML
dos documentos fiscais.
3. Definindo a pasta de destino
Ainda na mesma tela:
Em
Informe o destino dos dados a serem exportados
, selecione a pasta onde os XMLs serão salvos
Exemplo de pasta:
C:\FarmaFacil
Utilize sempre uma pasta de fácil acesso para facilitar a conferência dos arquivos.
4. Configurando a exportação dos XMLs
Ao abrir a tela
Exportação Documentos Fiscais
, configure conforme abaixo:
4.1 Tipo de documento
No campo
Tipo
, selecione:
NFC-e / NFE/ NFS-e
4.2 Filtro de notas
Nota Inicial / Nota Final
:
Pode deixar em branco para exportar todas as notas dentro do período informado.
4.3 Período
Preencha corretamente os campos:
Data Inicial
Data Final
Exemplo:
Data Inicial:
01/12/2025
Data Final:
31/12/2025
4.4 Situação das notas
Selecione a opção
Ambos
:
Exporta notas
autorizadas
e
canceladas
.
Caso precise exportar apenas um tipo específico:
Somente Ativos
→ apenas notas válidas
Somente Cancelados
→ apenas notas canceladas
5. Executando a exportação
Após revisar todas as informações:
Clique no botão de
Exportar
Aguarde o processamento do sistema
Ao final, será exibida a mensagem:
“Arquivos exportados com sucesso!”
Isso confirma que os XMLs foram gerados corretamente.
6. Conferência dos arquivos
Após a exportação:
Acesse a pasta configurada no Windows
Verifique se os arquivos possuem a extensão
.xml
Se necessário, compacte os arquivos em
.zip
para envio à contabilidade ou fiscalização.

---

## 🟢 Reforma tributária: Como alterar as tributações — 26/12/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/569979
> Publicado em: 26/12/2025

Com a implantação da Reforma Tributária, é fundamental manter as informações fiscais atualizadas em diferentes níveis do sistema. As alterações podem ser realizadas de forma individual ou em massa, conforme a necessidade. Veja abaixo como proceder em cada caso:
Importante:
A
prioridade das informações tributárias é sempre o NCM
.
Ou seja, quando existir tributação configurada no NCM, ela
sempre prevalecerá
sobre a tributação cadastrada diretamente no produto.
1. Alteração das informações tributárias no NCM
Acesse o menu
Arquivo → Estoque → NCM
.
Selecione o NCM desejado, clique em
Editar
e, em seguida, acesse a aba
Reforma Tributária
para realizar as alterações necessárias.
2. Alteração das informações tributárias diretamente no Produto
Acesse
Arquivo → Produto
.
Selecione o produto desejado e acesse a opção
Reforma Tributária
, onde será possível ajustar as tributações específicas daquele item.
⚠️ Observação: essas informações
somente serão consideradas caso o NCM não possua tributação configurada
.
3. Alteração das informações tributárias por Grupo (em massa)
Para alterar a tributação de vários produtos simultaneamente, acesse
Arquivo → Utilitário → Manutenção Geral
.
Em seguida, selecione
Alterar tributação de grupos
, clique em
Reforma Tributária
, escolha as tributações desejadas e os grupos que deverão ser atualizados.
⚠️ Observação: a tributação por grupo é aplicada apenas quando
não há definição no NCM
.
4. Alteração das informações tributárias por Estado
Acesse
Arquivo → Parâmetro → Estado
.
Selecione o estado desejado, clique em
Editar
e acesse a opção
Reforma Tributária
para configurar as regras tributárias correspondentes.
Em resumo, manter as tributações corretamente configuradas é essencial para garantir conformidade com a Reforma Tributária e evitar inconsistências fiscais. Sempre revise as informações com atenção, lembrando que o
NCM é a principal referência tributária do sistema
, assegurando cálculos corretos e maior segurança nas operações.

---

## 🟢 🛠️ Notas da Versão 20.01.90.12 — 15/12/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/568780
> Publicado em: 15/12/2025

🛠️ Notas da Versão 20.01.90.12
📅
Data de Liberação: 15/12/2025
A versão 20.01.90.12 do
FarmaFácil Desktop
incorpora avanços importantes em funcionalidades estratégicas, além de revisões que garantem maior consistência nas operações do sistema.
🆕
Novidades da Versão
🆕
ID-642 – Adequações do sistema para a nova Reforma Tributária (NF-e e NFC-e)
Implementadas as adaptações necessárias para atendimento às novas regras da Reforma Tributária, possibilitando a emissão de NF-e e NFC-e conforme a legislação vigente.
Esta versão é obrigatória para emissão fiscal dentro do novo modelo tributário.
(link artigo)
⚙️
Melhorias
ID-635 – Atenção Farmacêutica (FUNPEX)
Evolução no fluxo de Atenção Farmacêutica, ampliando o controle e o registro das informações exigidas.
ID-639 – Reconhecimento de etapa finalizada no PCP
O sistema passa a identificar corretamente quando a etapa do PCP já se encontra finalizada, evitando bloqueios indevidos.
ID-664 – Padronização da etiqueta “Preço Acabado / Drogaria”
Padronização e documentação dos campos disponíveis para exibição na etiqueta.
ID-668 – Obrigatoriedade do campo Peso para pacientes veterinários
Implementada validação para tornar obrigatório o preenchimento do campo
Peso
na tela de venda para pacientes VET.
ID-724 – Inclusão de campos da Reforma Tributária na Manutenção Geral
Disponibilizados novos campos fiscais para
atualização em massa por grupo
, facilitando a adequação tributária.
ID-725 – Atualização de códigos fiscais de NFS-e
Atualização dos códigos fiscais utilizados na emissão de NFS-e.
ID-731 – Exclusão de ICMS da base de cálculo do PIS e COFINS
Adequação da regra fiscal para cálculo correto das contribuições.
🧩
Comportamentos Revisados
ID-637 – Recalculo de QSP em fórmulas
Revisão do cálculo automático de QSP ao alterar a quantidade de cápsulas em fórmulas já calculadas.
ID-640 – Controle de concorrência no PCP
Ajuste no controle de concorrência durante a inclusão de etapas no PCP.
ID-660 – Anexação de arquivos PDF na venda
Revisado o processo de anexação para evitar a remoção indevida do arquivo da pasta de origem.
ID-666 – Validação do campo Peso no cadastro de paciente
Ajuste para impedir o salvamento de pacientes com o campo Peso em branco quando acessado pela tela de venda.
ID-688 – Gráfico “Vendas por Tipo”
Correção na exibição das informações por período.
ID-692 – Caracteres especiais em vendas e repetições
Tratamento adequado de caracteres especiais durante a geração de vendas.
ID-696 – Assinatura de XML (NFS-e / NFC-e)
Ajustes de compatibilidade entre bibliotecas de assinatura XML.
ID-698 – Fluxo de caixa com ECF
Revisão do comportamento ao abrir caixa e receber vendas com ECF.
ID-700 – Rotina de backup
Ajustes na execução da rotina de backup na versão Delphi 16.4.
ID-701 – XML NFC-e com duplicidade de tags
Correção da duplicação das tags
<nfeProc>
e
<protNFe>
no XML.
ID-714 – Arredondamento do PMC em notas de entrada
Ajuste no cálculo e arredondamento do valor do PMC.
ID-723 – Etiqueta padrão na v
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Reforma Tributária no Sistema — Emissão de Documentos Fiscais — 11/12/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/568408
> Publicado em: 11/12/2025

A partir da versão
20.01.90.12
, o sistema está preparado para atender às exigências da
Reforma Tributária
, desde que:
A funcionalidade esteja devidamente habilitada no parâmetro ou filial
Os cadastros de tributos, produtos, NCMs, estados e naturezas de operação estejam corretamente configurados
O correto preenchimento dessas informações é essencial para evitar rejeições fiscais e garantir a emissão adequada dos documentos.
Este artigo apresenta o
passo a passo para habilitação da funcionalidade
e a
configuração necessária dos cadastros
, garantindo a correta emissão dos novos campos obrigatórios nos documentos fiscais.
1. Habilitação da Reforma Tributária no Sistema
Para habilitar a emissão de documentos fiscais com a Reforma Tributária, é necessário acessar:
Parâmetro Geral ou Filial → Aba NF-e
Nesta tela, deve ser marcado o checkbox:
“Ativar RTC (CBS / IBS / IS)”
Essa configuração libera no sistema as novas opções e abas relacionadas à Reforma Tributária nos módulos fiscais e cadastrais.
Observação: a habilitação pode ser realizada tanto em nível de
Parâmetro Geral
quanto por
Filial
, conforme a política de uso do cliente.
2. Criação dos Novos Tributos
Na tela de
Tributos
, foram disponibilizados
quatro novos tipos de tributos
, necessários para atender à nova legislação:
CST IS
CST CBS
Classificação Tributária IS
Classificação Tributária CBS
Esses tributos serão utilizados nas configurações de produtos, NCMs e itens de nota fiscal.
3. Configuração da Tributação
Após a habilitação da Reforma Tributária no parâmetro, novas abas e campos passam a ser exibidos nos seguintes módulos:
3.1 Produto
No cadastro de
Produto
, foi criada a aba
Reforma Tributária
, contendo os campos necessários para vinculação dos novos tributos ao produto.
Os tributos informados nesta aba serão utilizados na emissão da nota fiscal.
Caso o
NCM
possua os tributos configurados, o sistema
prioriza automaticamente as informações do NCM
, sobrepondo as do produto.
3.2 NCM
No cadastro de
NCM
, também estão disponíveis os campos da Reforma Tributária.
Quando preenchidos, os tributos do NCM terão prioridade sobre os definidos no produto.
Essa regra garante padronização tributária conforme a classificação fiscal.
3.3 Estado
No cadastro de
Estado
, é
obrigatório
o preenchimento da
alíquota estadual
relacionada à Reforma Tributária.
Atenção:
A ausência dessa informação resultará em
rejeição no lançamento ou emissão da nota fiscal
, conforme validações fiscais.
3.4 Natureza de Operação (CFOP)
A
Natureza de Operação (CFOP)
também passa a considerar as informações relacionadas à Reforma Tributária, sendo fundamental revisar e manter os cadastros atualizados para evitar inconsistências na emissão fiscal.
4. Nota Fiscal de Entrada
4.1 Nota Fiscal de Entrada (Cabeçalho)
Os campos da Reforma Tributária estão disponíveis na nota fiscal de entrada, permitindo o correto registro dos novos tributos conforme o documento recebido.
4.2 Item da Nota Fiscal de Entrada
No item da nota fiscal de en
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Passo a passo para testar e configurar balança para pesagem monitorada. — 28/11/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/566788
> Publicado em: 28/11/2025

Este guia detalhado é um passo a passo para testar e configurar corretamente a comunicação da balança com o computador e o sistema
Farma Fácil
para pesagem monitorada.
1.1 Instalar os Softwares Necessários
Você precisará de dois itens principais:
Aplicativo TERMINAL:
Para testar a comunicação de forma direta.
Driver CH34x_Install_Windows_v3_4:
O driver para que o Windows reconheça o conversor serial/USB da balança.
1.2 Instalar o Driver CH34x
Execute a instalação do driver
chamado
“CH34x_Install_Windows_v3_4”
.
Clique com o botão direito no arquivo e escolha a opção
"Executar como administrador"
.
Na janela de instalação, clique em
“INSTALL”
.
Confirme a instalação clicando em
“OK”
quando a mensagem de sucesso aparecer.
1.3 Testar a Comunicação com o Aplicativo TERMINAL
Abra o aplicativo
“TERMINAL”
.
Clique no botão
“ReScan”
. Isso fará com que o programa reconheça a porta de comunicação (a porta
COM
) onde a balança está conectada (Exemplo:
“COM6”
).
Configure o TERMINAL:
Replique as configurações
da sua balança (como
Baud Rate
,
Data bits
,
Parity
e
Handshaking
) no programa TERMINAL.
Verifique se a porta
COM Port
está correta (Ex:
COM6
).
Clique no botão
“Connect”
.
Se a comunicação estiver correta, o peso registrado na balança deve aparecer na área de recebimento do TERMINAL (Exemplo:
"+ 6.291 g"
).
🚨 Observação:
Se o TERMINAL
não reconhecer a balança
ou não registrar o peso após conectar, o
Setor de TI
(Tecnologia da Informação) da farmácia deve ser acionado para verificar a conexão física e as configurações de porta.
Passo 2: Testar a Comunicação com o Sistema Farma Fácil
Após validar a comunicação no TERMINAL, é hora de testar a integração dentro do sistema de gerenciamento.
2.1 Acessar a Configuração da Balança
No sistema
Farma Fácil
, navegue até o menu:
Arquivo > Produção > Balança
.
Localize a balança que será testada na lista (Ex: AD 330S).
Selecione-a e clique no botão
"Editar"
(ícone de um lápis).
2.2 Conferir as Configurações
Na tela de
Manutenção Balança
, confira se todos os campos de configuração da balança estão preenchidos corretamente.
Modelo
(Ex: AD 330S)
Porta COM
(Deve ser a mesma reconhecida no Passo 1, Ex: COM6)
Bits por Segundo
(Baud Rate, Ex: b9600)
Bits de Dados
(Ex: db7)
Paridade
(Ex: paNone)
2.3 Capturar o Peso no Sistema
Na mesma tela, clique no botão
“Capturar Peso”
.
Validação:
Balança Automática:
O peso deve ser registrado no sistema automaticamente.
Balança Semi-Automática:
Você deve registrar o peso primeiro na balança e, em seguida, clicar em "Capturar Peso" no sistema.
Se o peso for exibido (Exemplo:
"+ 6.294 g"
), a comunicação do sistema com a balança está validada.
Passo 3: Ativar a Chave IDBALANÇA (Configuração Final)
Para que a balança seja usada na pesagem monitorada, você deve ativar a configuração no menu de Parâmetros.
No sistema, navegue até o menu:
Arquivo > Parâmetro > Configurações Prismafive
.
Na tela de configurações, pesquise pela
Chave
chamada
“IDBALANÇA”
.
Edite o campo
"Valor"
dessa chave,
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Passo a Passo para Troca de Foto de Perfil na API Oficial do WhatsApp. — 28/11/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/566675
> Publicado em: 28/11/2025

O processo é simples, rápido e totalmente gerenciado dentro do seu
Gerenciador de Negócios (Business Manager)
, garantindo que você mantenha o controle total sobre o branding da sua API Oficial.
Siga as instruções abaixo, utilizando as ferramentas de configuração do WhatsApp no seu portal Meta.
1. Acessar a Conta do WhatsApp
No Gerenciador de Negócios da Meta (
https://business.facebook.com/settings/security/
:), acesse com a sua conta e vá para
"Configurações"
.
Na barra lateral esquerda, na seção
Contas
, clique em
"Contas do WhatsApp"
Você verá a lista das suas Contas do WhatsApp. Clique no
nome da conta
que possui o número que você deseja editar.
2. Acessar a Configuração de Telefones
Após clicar no nome da conta, você verá as informações da empresa. No menu lateral direito, clique em
"Gerenciador de WhasApp"
.
Você verá uma tabela com os números de telefone vinculados a esta conta.
Localize o número de telefone que você quer editar e clique no ícone de
engrenagem (⚙️)
, que representa as configurações, no canto direito da linha desse número.
3. Fazer o Upload da Nova Foto de Perfil
Ao clicar na engrenagem, um painel lateral se abrirá com as informações do número de telefone.
Clique na aba
"Perfil"
.
Procure a seção
"Foto de perfil"
. Abaixo da frase "Isso ficará visível no seu perfil comercial", clique no botão
"Escolher arquivo"
.
Uma janela do seu computador será aberta para que você
selecione o arquivo da imagem
que deseja usar.
Dica:
Certifique-se de que a imagem está em um formato e tamanho aceitos pelo WhatsApp (geralmente JPG ou PNG).
4. Salvar as Alterações
Após selecionar a imagem, você pode ver uma pré-visualização.
Role o painel para baixo e clique no botão
"Salvar"
.
A Meta processará a solicitação. Se a foto for aceita, você receberá uma notificação como "Perfil atualizado com sucesso".
⚠️ Observação Importante:
A foto de perfil deve estar em conformidade com a
Política Comercial e a Política de Mensagens do WhatsApp
. O WhatsApp pode levar um tempo para
revisar e aprovar
a nova foto de perfil antes que ela se torne visível para todos os seus clientes.

---

## 🟢 Como ajustar cadastros de controlados: Um guia prático de como alterar classe  terapêutica e grupo de produtos controlados. — 27/11/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/566458
> Publicado em: 27/11/2025

As vezes, cadastramos produtos controlados no sistema, mas esquecemos de marcar a opção SUJEITO A CONTROLE especial, o que faz com que nosso produto não conste nos relatórios da ANVISA. Para ajustar essa informação no sistema, é necessário seguir um processo que será descrito abaixo.
Antes de fazer qualquer ajuste nos produtos, é importante lembrar que produtos controlados são rastreados pelo ANVISA, através das informações do lote que são disponibilizadas pelo fornecedor. Para ajustar o cadastro dos controlados, é necessário tomar bastante cuidado para não alterar as informações do lote, ou isso pode prejudicar a rastreabilidade. Dito isso, antes de fazer qualquer alteração, tire prints dos lotes que serão alterados, ou anote as quantidades para não haver erros.
Após anotar as quantidades e os dados do lote, nós iremos zerar todos os lotes do produto. Recomendo fazer isso pelo módulo de INVENTÁRIO (Estoque > Movimento > Inventário). Como você pode ver no print abaixo eu selecionei o GRUPO, PRODUTO e marquei a opção MOSTRAR CONTROLADOS. Caso o produto não esteja marcado como controlado, não é necessário marcar essa opção. O sistema irá retornar todos os lotes daquele produto, como consta na imagem.
Para fazer o acerto de estoque, coloque o valor 0 no campo CONTAGEM, conforme mostra na imagem abaixo. Após informar a quantidade, clique no valor da coluna POSIÇÃO ESTOQUE. Isso irá abrir uma janela para você selecionar o motivo do acerto. Caso o produto esteja vencido, selecione vencimento. Do contrário, o padrão é utilizar a justificativa PERDA NO PROCESSO. Basta seguir o exemplo abaixo.
Após salvar as alterações, o sistema irá exibir um relatório com as alterações feitas, conforme mostra abaixo:
Também é possível verificar as movimentações pelo módulo de acerto de estoque, como mostra abaixo:
Agora que você zerou o estoque do produto, conseguimos fazer as alterações necessárias no cadastro do produto. Caso seja um produto controlado, que você deseja trocar de grupo, é necessário LIMPAR a classe terapêutica, e as informações de controle especial, como consta na imagem abaixo:
Sem a classe terapêutica, você consegue alterar o grupo do produto. Para fazer isso, acesse ARQUIVO > UTILITÁRIOS > MANUTENÇÃO GERAL, e selecione a opção ALTERAR CÓDIGO PRODUTO:
Como você pode ver no print, eu informei o produto que eu desejo fazer alteração nos 2 primeiros campos. No campos de baixo, eu informo em qual grupo eu quero incluir aquele produto. Ao invés de digitar o código do produto, selecione a opção CÓDIGO PRODUTO AUTOMÁTICO. Antes de salvar as alterações, verifique se o seu módulo se parece com a imagem acima.
Feito a troca do grupo, precisamos novamente classificar o produto como controlado. Basta voltar no cadastro do produto, e informar novamente a LISTA CONTROLADO, DCB e CLASSE TERAPÊUTICA, conforme consta na imagem abaixo:
Após fazer isso, será necessário incluir novamente as quantidades no estoque. Por questões de segurança, o sistema não autoriza inclus
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 📘Manual de Aplicação de QSP e Seleção de Excipientes — 26/11/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/566218
> Publicado em: 26/11/2025

📘
Manual de Aplicação de QSP e Seleção de Excipientes
A partir da versão
20.01.90.11
, foi adicionado ao cadastro de
Produto
o recurso de vinculação de
QSP por Forma Farmacêutica
.
Este manual descreve detalhadamente o comportamento do sistema na aplicação de
QSP (Quantidade Suficiente Para)
considerando:
Vinculações configuradas no produto
Comportamento na Formula\Venda
Regras de prioridade aplicadas durante o cálculo
O Campo novo e funciona corretamente para
todas as formas Farmaceuticas
, com exceção de:
Homeopatia
Papel
Floral
O objetivo é padronizar a compreensão do mecanismo de escolha do excipiente/QSP e orientar o uso correto do recurso.
1️⃣ Aplicação de QSP Conforme o Vínculo do Produto
1.1 – Produto com QSP sem Forma Farmacêutica
Quando o produto possui QSP vinculado
sem forma farmacêutica
, o sistema aplica automaticamente o QSP
somente
nas seguintes modalidades:
Cápsulas
Comprimidos
Implantes
Motivo:
Para preservar o comportamento já existente no sistema e evitar impacto nas vendas após a atualização, essa regra foi mantida conforme o funcionamento anterior.
Nota:
Esta regra é temporária e será revisada futuramente para ampliar a cobertura de formas Farmaceuticas.
1.2 – Produto com QSP Vinculado à Forma Farmacêutica
Quando o produto possui QSP vinculado
especificamente
a uma forma farmacêutica, o sistema:
identifica automaticamente a forma farmaceutica utilizada na fórmula;
aplica o QSP correspondente sem necessidade de escolha manual.
2️⃣ Produtos com QSP Diferentes para a Mesma Forma Farmacêutica
Quando dois ou mais produtos possuem QSPs distintos vinculados
à mesma forma farmacêutica
, o sistema:
Identifica o conflito de QSPs.
Abre automaticamente um
modal de escolha de excipiente
.
Permite ao usuário selecionar manualmente qual QSP deseja utilizar.
⚙️
3️⃣
Prioridades de Escolha do QSP
A escolha do QSP segue regras diferentes conforme o tipo de forma farmacêutica.
3.1 – Formas do Tipo Volume e Volume x Quantidade (mg / %)
Ordem de prioridade:
Se o usuário digitou manualmente
→ manter o QSP informado.
Se existir QSP vinculado ao produto com a mesma forma farmacêutica
→ aplica o QSP do produto.
Se não existir no produto, mas existir na forma farmacêutica
→ aplica o QSP da forma farmacêutica.
Se não existir em nenhum dos locais acima
→ a fórmula permanecerá
sem QSP
.
3.2 – Formas do Tipo Cápsula
Ordem de prioridade:
Se o usuário digitou manualmente
→ mantém o QSP informado.
Se existir QSP vinculado ao produto para essa forma farmacêutica
→ aplica o QSP do produto.
Se existir Classificação Biofarmacêutica
→ aplica o QSP conforme a regra de prioridade da biofarmacêutica (Classe IV > II > III > I ).
Se não existir no produto, mas existir na forma farmacêutica
→ aplica o QSP da forma farmacêutica.
Se não existir no produto, nem classificação biofarmacêutica, nem forma farmacêutica
→ aplica o QSP definido no
parâmetro geral
.
Se não existir em nenhum local
→ a fórmula permanecerá
sem excipiente/QSP
.

---

## 🟢 Sem título — 17/11/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/565074
> Publicado em: 17/11/2025

NOTA FISCAL
1. INTRODUÇÃO
Para emitir uma DANFE, vamos precisar das seguintes informações:
CFOP (para encontrar o CFOP somente com a contabilidade, pois varia de entre as finalidades das notas, para fora do estado, dentro do estado, etc...
2. NO SISTEMA
Nota Fiscal
Vá em incluir Nova Nota Fiscal
A CFOP, somente quem pode informar para a farmácia qual pode utilizar é a
CONTABILIDADE,
devido a finalidade de cada uma.
A serie da nota, vai depender de como a farmácia faz a emissão de outras notas a mesma coisa para a Sub Serie, sempre irá seguir a Serie da nota
Nota Fiscal nunca devem mexer ou alterar ela, pois pode bagunçar a sequencia no Sefaz
Sempre conferir antes de adicionar os produtos no cadastro do cliente se ele é contribuinte do ICMS, para descobrir só verificar se ele tem a IE (inscrição estadual), caso ele tenha basta adicionar no cadastro do cliente
Inserindo a IE
Após ter realizado todos esses processos podemos estar adicionando os produtos, podemos incluir os produtos manualmente.
Clicando na Lupa, já vai abrir a aba para adicionar os produtos
Na primeira seleção a onde está o nome do produto, podemos editar com o nome da nota, sem problemas
Na 2º parte devemos preencher com o volume que será devolvido
Caso o cliente/fornecedor seja contribuinte, ou seja, possua inscrição estadual, recomenda-se utilizar a CST 90 e CSOSN 900
Pode clicar em SIM caso apareça isso
Temos agora 2 itens incluídos na nota
Após realizado todo esse procedimento é só salvar e emitir a nota

---

## 🟢 Como Realizar o Cadastro de Fornecedores no Sistema Farma Fácil — 14/11/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/564785
> Publicado em: 14/11/2025

Como Realizar o Cadastro de Fornecedores no Sistema Farma Fácil
O processo de cadastro de fornecedores no sistema Farma Fácil é essencial para manter a organização e o controle das informações de compra e estoque. A seguir, apresentamos um guia completo sobre como realizar esse procedimento corretamente, considerando também as regras vigentes nas versões mais recentes do sistema.
Acessando o Cadastro de Fornecedores
Para iniciar o processo, acesse o menu principal do sistema e siga o caminho:
Arquivo > Estoque > Fornecedor
Ao selecionar essa opção, o sistema exibirá a janela dedicada ao gerenciamento de fornecedores.
Incluindo um Novo Fornecedor
Na janela
Fornecedor
, clique no botão
Incluir
para abrir o formulário de cadastro.
Preencha todas as informações solicitadas, como dados cadastrais, endereço, contato e documentação necessária. Após finalizar o preenchimento, clique em
Salvar
para concluir a inclusão.
Restrição de Cadastro de CNPJ Duplicado
Nas versões mais recentes do Farma Fácil, o sistema
não permite mais cadastrar dois fornecedores utilizando o mesmo CNPJ
. Caso o usuário tente registrar novamente um CNPJ já existente, o sistema retornará uma mensagem de erro informando que o número informado já está vinculado a outro fornecedor.
Essa medida foi implementada para garantir maior confiabilidade nas informações e evitar duplicidade de registros, que poderia comprometer relatórios e controles internos.
Como Proceder em Caso de Empresas Secundárias com o Mesmo CNPJ
Algumas organizações utilizam filiais ou unidades secundárias que compartilham o mesmo CNPJ. Nesses casos, não é necessário (e nem possível) criar novos cadastros de fornecedor.
A alternativa correta é utilizar a
aba “Sinônimo”
dentro do cadastro do fornecedor principal. Nessa área, podem ser adicionados os nomes das empresas secundárias, permitindo organização sem violar a regra de unicidade do CNPJ.
Conclusão
O cadastro adequado de fornecedores no Farma Fácil é fundamental para o bom funcionamento do sistema e para a integridade das informações operacionais. Seguir as etapas corretas e observar as regras de CNPJ garantem um processo mais seguro e eficiente.

---

## 🟢 Impressora Padrão para abrir o Relatório — 14/11/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/564783
> Publicado em: 14/11/2025

No
Farma Fácil
, alguns relatórios
realmente não abrem
se o sistema não encontrar
uma impressora padrão configurada
, especialmente uma
impressora A4
(mesmo que seja virtual).
Isso é um comportamento comum em sistemas feitos em Delphi/Crystal Reports, onde o relatório só inicia se houver uma impressora válida definida no Windows.
✅ Como resolver
1. Defina uma impressora padrão no Windows
Mesmo que você
não tenha impressora física
, funciona assim:
Abra
Configurações do Windows
→
Dispositivos
→
Impressoras e scanners
Instale ou ative:
Microsoft Print to PDF
(já vem no Windows)
Ou
Microsoft XPS Document Writer
Clique nela e selecione
“Definir como padrão”
.
2. (Opcional) Instale uma impressora A4 genérica
Se o relatório exigir especificamente A4:
Painel de Controle →
Dispositivos e Impressoras
Adicionar impressora
Adicionar impressora local
Porta:
FILE:
Modelo:
Generic → Generic / Text Only
Defina o papel como
A4
.
3. Reinicie o Farma Fácil
Depois de definir qualquer impressora como padrão, feche e abra o sistema, após isso, abra o relatório de sua escolha dentro do Farma Fácil.
É importante observar se a impressora padrão que você escolheu seja de papel A4
1
2

---

## 🟢 🛠️ Notas da Versão 20.01.90.11 — 13/11/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/564536
> Publicado em: 13/11/2025

🛠️ Notas da Versão 20.01.90.11
📅
Data de Liberação: 25/11/2025
A versão 20.01.90.11 do
FarmaFácil Desktop
incorpora avanços importantes em funcionalidades estratégicas, além de revisões que garantem maior consistência nas operações do sistema.
🆕
Novidades da Versão
A partir desta versão, o sistema passa a contar com integração direta com o
iFood
, permitindo
sincronizar produtos, receber pedidos automaticamente
dentro do próprio FarmaFácil.
Essa novidade amplia o ecossistema de vendas, trazendo mais praticidade e conectividade para o dia a dia da farmácia.
🆕
ID-386 – Integração com o IFOOD (
Link artigo
)
🆕
ID-246 – Adicionada configuração de excipiente por forma farmacêutica no cadastro do produto, facilitando o processo de parametrização e escolhas de QSP (
Link artigo
);
⚙️
Melhorias
ID-7
– Envio da Mensagem Padrão calculada (modelo 2) em formato PDF, ampliando a flexibilidade de compartilhamento.
ID-497
– Disponibilizada visualização da imagem da receita lado a lado com a tela de venda de acabados, otimizando a conferência durante o atendimento.
ID-548
– Implementado indicador de presença NF-e para maior controle das emissões.
ID-594
– Revisada a implementação de NFS-e TecnoSpeed, assegurando estabilidade e tratamento adequado no envio.
ID-605
– Bloqueio e atualização automática do endereço de entrega com título “CADASTRO”, garantindo maior consistência de dados e sincronismo com o Nexys.
ID-612
– Adicionado filtro por período no relatório de atenção farmacêutica, permitindo consultas mais precisas.
ID-613
– Atualização automática do valor de custo no relatório de Posição de Estoque Financeiro ao ocorrer correção de entrada.
ID-614
– Tornado opcional o preenchimento do local de entrega quando se tratar de orçamento via SyncWhats e SyncMail.
ID-615
– Habilitada alteração de embalagem na tela de ordem de produção com ordem no status “pesada”.
ID-616
– Adicionado filtro por etapa no relatório de Produção por Forma Farmacêutica, ampliando a filtragem de informações.
ID-617
– Incluída a justificativa aplicada em descontos no relatório de Justificativas.
ID-623
– Criada tabela de preços específica para florais por forma farmacêutica, garantindo flexibilidade comercial.
ID-667
– Ajustada mensagem exibida ao alterar lote na tela de manipulação, tornando-a mais clara e informativa.
ID-672
– Ajustado comportamento da venda com produtos oriundos de fórmulas padrão desmembradas inativas, mantendo consistência nos itens.
🧩
Comportamentos Revisados
ID-174
– Revisado o comportamento de escolha automática de excipiente conforme a classificação biofarmacêutica.
ID-288
– Revisado o processo de relacionamento de faturas dentro do módulo de Conciliação Bancária, assegurando o correto vínculo dos documentos.
ID-487
– Revisado o comportamento de composição de embalagem em pré-vendas, garantindo a correta replicação das quantidades.
ID-571
– Revisada a geração do relatório de movimento de estoque para apresentar as informações consolidadas corretamente.
ID-574
– Re
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Como Aplicar Desconto em um Produto no Sistema de Vendas — 28/10/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/562193
> Publicado em: 28/10/2025

Como Aplicar Desconto em um Produto no Sistema de Vendas
Aplicar descontos diretamente nos produtos é uma funcionalidade útil para promoções, queima de estoque ou estratégias de fidelização de clientes. Veja abaixo um passo a passo simples de como configurar descontos no sistema, para que eles sejam aplicados automaticamente no momento da venda.
Passo 1: Acesse o Cadastro de Produtos
Vá até o menu:
Arquivo > Estoque > Produto
Isso abrirá a tela de gerenciamento dos produtos cadastrados no sistema.
Passo 2: Acesse a Aba de Promoções
Com a tela de produtos aberta, pressione a tecla
F6
ou acesse diretamente a aba
"Produtos em Promoção"
.
Passo 3: Localize o Produto que Terá o Desconto
Utilize a barra de pesquisa para
localizar o medicamento ou item
ao qual você deseja aplicar o desconto.
Passo 4: Aplique o Desconto
Após localizar o produto, informe a
porcentagem de desconto
que deseja aplicar.
Defina o período
de validade da promoção, caso o desconto seja temporário.
Se deseja que o desconto seja
permanente
, simplesmente
deixe o campo de período em
branco
.
Passo 5: Salve as Alterações
Clique em
“Salvar”
para aplicar as mudanças no sistema.
Passo 6: Finalize a Venda com Desconto
Ao realizar uma nova venda, basta
puxar o produto normalmente
, e o sistema
aplicará automaticamente o desconto configurado
, sem necessidade de ajustes manuais.

---

## 🟢 Manual de Integração FarmaFacil x iFood — 27/10/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/561943
> Publicado em: 27/10/2025

Manual de Integração FarmaFacil x iFood
Versão mínima requerida:
20.01.90.11
1. Visão Geral
A partir da versão
20.01.90.11
, o
FarmaFacil
passa a contar com integração nativa com o
iFood
, permitindo o gerenciamento automatizado de produtos, estoques e pedidos entre as plataformas.
🔄 O que a integração contempla:
Cadastro e atualização de produtos e estoque
diretamente do FarmaFacil para o iFood.
Atualização automática
de preços e promoções.
Importação de pedidos do iFood
para o FarmaFacil em tempo real.
Conversão automática de pedidos do iFood em vendas
dentro do FarmaFacil.
2. Pré-requisitos
Antes de iniciar a integração, verifique:
A
loja já deve estar cadastrada e ativa no iFood
.
Não pode haver
pendências de cadastro
(dados incompletos, loja inativa, etc.).
É necessário ter acesso ao
Portal de Parceiros iFood
com permissão de administrador.
🧩 3. Configuração Inicial
As chaves de integração são configuradas em:
Parâmetro Geral
ou
Configurações da Filial → Aba Integrações → WEB / iFood
Campos obrigatórios:
Campo
Descrição
ClientID
Chave do FarmaFacil com o iFood
Secret
Senha do FarmaFacil gerada para a integração
MerchantID
ID da loja no iFood
Vendedor
Vendedor padrão para vendas no farmafacil.
🔍 Onde encontrar o MerchantID (ID da Loja)
Acesse o
Portal de Parceiros do iFood
.
Vá em
Minha Loja → Loja
.
Copie o campo
ID da Loja
.
Informe o ID no campo correspondente dentro do FarmaFacil.
Após salvar as configurações no FarmaFacil, prossiga com o
login e sincronização de produtos
.
🔑 4. Login iFood
O login autoriza o FarmaFacil a gerenciar
estoque e pedidos
no iFood.
Passo a passo:
Acesse o menu
Arquivo → E-commerce → Produto iFood → Login iFood
.
Clique no botão
Login iFood
.
Será exibido um
link de autorização
— clique para abrir o portal do iFood.
Faça login no
Portal de Parceiros
e clique em
Autorizar o FarmaFacil
.
Copie o
código de autorização
exibido e cole no campo indicado no FarmaFacil.
Confirme para concluir a autorização.
⚠️
Importante:
A sincronização de produtos e pedidos
só é realizada após o login
.
A cada novo login no FarmaFacil, é necessário efetuar o login no iFood novamente.
📦 5. Cadastro de Produtos iFood
A tela
Produtos iFood
é o ponto central da integração.
Nela é possível cadastrar, editar, atualizar e sincronizar produtos com o iFood.
Principais funções:
Cadastro individual de produto
Cadastro em lote (por grupo)
Edição de preços e promoções
Atualização e sincronização de estoque
🔹 Cadastro Individual
Para cadastrar um produto:
O produto deve possuir
código de barras
cadastrado.
Sem código de barras, o produto
não será enviado
ao iFood.
Informe os preços de venda e promocional(opcional) o estoque já puxará de acordo com o estoque da farmacia.
Clique em Salvar  para posteriormente sincronizar com o iFood.
Caso informe produtos sem código de barras.
🔹 Cadastro em Lote
Acesse
Arquivo
→
E-commerce
→
P
rodutos iFood → Cadastro em Lote
.
Escolha um
grupo de produtos
e defina um
estoque mínimo
.
Edite preços e promoções conform
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 ⚠ Instabilidade resolvida: Caso sua instância permaneça inativa, acesse o WhatsApp no seu celular, vá em Configurações e depois — 24/10/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/561723
> Publicado em: 24/10/2025

⚠️ Instabilidade resolvida:
Caso sua instância permaneça inativa, acesse o WhatsApp no seu celular, vá em Configurações e depois em Dispositivos conectados.
Desconecte todos os dispositivos e, em seguida, siga os passos abaixo na página do ORYA:
1️⃣ Acesse Instâncias;
2️⃣ Procure a instância com o seu número — ela estará com o status Desconectado;
3️⃣ Gere um novo QR Code e faça novamente a leitura.
⚠️ Importante: NÃO CLIQUE EM EXCLUIR, pois isso fará com que você perca todo o histórico de mensagens.

---

## 🟢 Guia de Cadastro e Vinculação de Visitadores no FarmaFácil. — 21/10/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/561089
> Publicado em: 21/10/2025

O FarmaFácil permite gerenciar de forma prática o vínculo entre médicos e visitadores, garantindo que cada profissional de vendas esteja corretamente associado aos médicos que atende.
Este guia detalhado apresenta, passo a passo, como
vincular um visitador a um médico
e como
cadastrar um novo visitador
, facilitando o controle e a organização das informações dentro do sistema.
Seguindo estas instruções, você poderá manter os cadastros atualizados, agilizar o atendimento e garantir que todos os registros estejam corretos. ✅
🔹 Como vincular o visitador a um médico no FarmaFácil
1-
Abrir o FarmaFácil
Acesse o sistema com um usuário que tenha permissões de cadastro ou edição de médicos e visitadores.
2 - Localizar o médico
Pressione
Ctrl + F
no teclado para abrir a busca rápida.
Digite
“Médico”
e pressione
Enter
.
Será exibida a lista de médicos cadastrados.
3- Selecionar o médico desejado
Clique sobre o nome do médico que deseja vincular ao visitador.
4- Editar informações do médico
Clique no botão
Editar
(ícone do lápis) para abrir o formulário de edição
5- Acessar a aba Complemento
No formulário, vá até a aba
Complemento
.
6- Vincular o visitador
No campo
Visitador
, selecione o visitador desejado na lista.
⚠️
Importante:
somente visitadores com cadastro
ativo
aparecerão para seleção.
7- Salvar as alterações
Clique em
Salvar
para concluir o processo.
O médico agora estará vinculado ao visitador escolhido.
Como cadastrar um novo visitador
1- Abrir o FarmaFácil
Certifique-se de ter permissão para cadastrar novos visitadores.
2- Acessar a tela de Visitadores
Pressione
Ctrl + F
e digite
“Visitador”
.
Pressione
Enter
para abrir a tela de gerenciamento de visitadores.
3- Iniciar o cadastro
Clique em
Novo
(ícone “+”) para abrir o formulário de cadastro.
4- Preencher os dados obrigatórios
Informe todos os campos solicitados, como:
Nome
Endereço
Comissão
Outros dados relevantes exigidos pelo sistema
5- Salvar o cadastro
Salvar o cadastro
Clique em
Salvar
.
6- Disponibilidade para vinculação
Após salvar, o novo visitador ficará
ativo
e disponível na lista para ser vinculado aos médicos.

---

## 🟢 1. Objetivo — 14/10/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/559995
> Publicado em: 14/10/2025

RELATÓRIO DE COMPRAS — SISTEMA FARMA FÁCIL
Documentação Técnica
Data: Outubro de 2025
1. Objetivo
Este documento tem como objetivo detalhar o funcionamento técnico do relatório de compras do sistema Farma Fácil, incluindo suas bases de cálculo, filtros disponíveis, colunas geradas e menu de navegação.
2. Acessando o Módulo de Compras
Para gerar o relatório, você deve seguir o caminho "
Estoque >> Movimento >> Compras
".
3. Tipos de Relatório
Contendo atualmente seis opções, neste campo, você seleciona quais dados serão utilizados para a geração do relatório. Sendo elas:
Venda
Se baseia na data da emissão da venda para gerar a lista de produtos a serem comprados. (Opção recomendada para farmácias que possuem produtos acabados/drogaria).
Demanda
Considerando o tempo de reposição informado e o estoque mínimo/máximo no cadastro do produto, realiza o cálculo da média de consumo no período selecionado.
Fórmula:
QE = QuantidadeDeEstoque
CM = ConsumoMédio
TR = TempoDeReposição
EM = EstoqueMínimo
EA = EstoqueAtual
Cálculo:
QE = (((CM * TR) + EM) - EA)
Ou seja:
QuantidadeDeEstoque = (((ConsumoMédio * TempoDeReposição) + EstoqueMínimo) - EstoqueAtual)
Estoque Mínimo
Se baseia no campo 'Estoque Mínimo' no cadastro do produto para gerar o relatório.
Estoque Máximo
Assim como na opção anterior, utiliza o campo 'Estoque Máximo' para gerar o relatório. (Tanto o campo 'Estoque Mínimo' quanto o 'Estoque Máximo' podem ser calculados automaticamente via sistema).
Consumo
Utiliza as informações das ordens de manipulação do período informado. (Opção exclusiva para farmácias de manipulação).
Faltas / Encomendas
Gera o relatório com base nas faltas e encomendas informadas pelos vendedores no módulo 'Faltas / Encomendas'.
4. Legenda dos Filtros
Filtro
Descrição
Curva ABC
Selecionar quais listas de produtos aparecerão no relatório.
Tipo do valor
Escolha um parâmetro de valor de custo para que o sistema compare entre os fornecedores.
Grupo(s)
Especificar um ou mais grupos de produtos que aparecerão no relatório.
Laboratório
Filtra apenas por laboratório (utilizado por drogarias).
Venda de / Até
Período das movimentações que o sistema utilizará para o cálculo das compras.
Considera Encomendas/Faltas
Inclui produtos adicionados ao módulo 'Faltas / Encomendas'.
Pedido para
Sugere quantidade para compra com base no consumo do período informado.
A partir de
Utiliza o valor da melhor compra a partir da data inserida.
Fornecedor
Possibilidade de filtrar por fornecedores.
Saldo com Quantidade Comprometida
Considera as quantidades comprometidas dos lotes nos cálculos.
Produto
Permite gerar o relatório para apenas um produto específico.
5. Legenda das Colunas do Relatório
Coluna
​
Descrição
Gr
Código do grupo do produto.
Produto
Código do produto.
Descrição
Nome do produto.
Unid.
Unidade de estoque do produto.
Est. Min
Quantidade informada no campo 'Estoque Mínimo'.
Est. Máx
Quantidade informada no campo 'Estoque Máximo'.
Qtd. Vendida
Quantidade vendida/consumida no período filtrado
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Configuração de Nota Fiscal de Serviço (NFSE) no Padrão Nacional — 01/10/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/558386
> Publicado em: 01/10/2025

1) Checagem do município (aderente/ativo)
Antes de migrar para o Padrão Nacional, confirmem na
planilha oficial do gov.br
que o município do prestador está:
• Ativo Operacional
(Planilha disponível na página “Municípios Aderentes”.)
• Se estiver Nao Conveniado, ou Conveniado - Nao Ativo, manter emissão pelo provedor municipal atual e reavaliar depois.
•
Lista dos Municípios Aderentes:
2) Login (já tem cadastro)
ATENÇÃO: Cada CNPJ (filial) precisa do seu próprio certificado, deixe isso claro para o cliente.
Se o cliente já tem cadastro, oriente a entrar por:
• Login do Emissor Nacional (usuário/senha, certificado ou gov.br):
Emissor Nacional
3) Cadastro / primeiro acesso do contribuinte
Peça para o cliente fazer (ou confirmar) o cadastro no Emissor Nacional:
• Primeiro acesso (criar conta/senha):
NFS-e | Portal Contribuinte
4) Configurar o sistema
Quando o município estiver "Ativo Operacional"
• Descompacte o arquivo dentro da pasta EXE:
https://drive.google.com/file/d/1kd8bBlASrqe5EbIztk2jVYiUVtRFrBft/view?usp=sharing
• Provedor: proPadraoNacional
• IBGE do município do prestador deve estar corretamente preenchido no cadastro
• Certificado A1/A3 configurado
• Regra funcional: um único item por NFS-e;
• CEPs com 8 dígitos (sem máscara).
• Configuração do ACBrNFSeXServicos.ini:
Você deve pesquisar o município do cliente que está sendo configurado e deixar neste padrão (Porto Alegre usado como exemplo).
• Configurações dentro do sistema:
• 1) Alterações efetuadas (foram necessárias para o funcionamento com Porto Alegre) - outras cidades podem ser diferentes para o funcionamento:
- Remoção da insc. Municipal:
- Verifique também se no TELEFONE não há caractere especial, exemplo: 3333-8815. Caso tenha, remova o caractere.
2) No parâmetro NFSe/CFSe, configure da seguinte forma:
3) Configure o provedor "PadraoNacional" caso não possua:

---

## 🟢 Fator UI, Fator UTR, Fator UFC - Lote — 01/10/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/558375
> Publicado em: 01/10/2025

Fator UI, Fator UTR, Fator UFC - Lote
1. Introdução
1.1
O que são os fatores UI, UTR e UFC?:
Os
Fatores UI, UTR e UFC
são comumente utilizados pelas
F
armácias Magistrais
(
F
armácias de Manipulação
), e estão relacionados ao cálculo de doses e conversão de unidades de substâncias ativas.
Obs.
:
Todas estas informações deverão ser verificadas através do
laudo
do produto enviado pelo fornecedor.
1.1.1
O que é o Fator UI?:
O
Fator UI
(
Unidade Internacional
), é uma unidade de medida padronizada utilizada para quantificar a
atividade biológica
de uma substância, como
vitaminas
,
hormônios
e
enzimas
.
Por exemplo:
A
vitamina D
pode ser prescrita como
1000UI
.
Isso não representa uma massa exata em mg ou mcg, mas sim uma quantidade com base em sua
potência biológica
.
Obs.
:
Diferentes substâncias podem ter diferentes equivalências entre
UI
e
mg
, dependendo de sua origem e forma.
1.1.2
O que é o Fator UTR?:
O
Fator UTR
(
Unidade de Titulação Relativa
), é uma unidade usada para expressar a
concentração de ativos titulados
, ou seja, substâncias cuja quantidade de princípio ativo é
padronizada
e
comprovada por análise
.
Por exemplo:
Um extrato vegetal pode conter
95%
de princípio ativo, e isso pode ser expresso em
UTR
.
Um extrato
padronizado
para conter
10mg
de um composto ativo pode equivaler a
100UTR
, dependendo da padronização do fabricante.
1.1.3
O é o Fator UFC?:
O
Fator UFC
(
Unidade Formadora de Colônias
) é usada
para expressar a
quantidade de microrganismos viáveis
presentes em um produto, como
probióticos
ou
cosméticos
. Indicando a
eficácia microbiológica
de produtos que dependem da ação de
microrganismos vivos
.
Por exemplo:
Um
probiótico
pode conter
1.000.000.000UFC
por cápsula, ou seja,
1
x
10
⁹
bactérias capazes de formar colônias.
1.2
Fórmula dos Fatores UI, UTR e UFC:
A
fórmula
para calcularmos a quantidade final utilizando os
Fatores UI
,
UTR
ou
UFC
é a seguinte:
X
=
(
1
/
FatorUI/UTR/UFCdoLote
)
QuantidadeFinal
=
(
X
*
DosagemDaFormula
)
2. Processo
2.1
Caminho para cadastro dos Fatores UI/UTR/UFC:
Os
Fatores UI/UTR/UFC
são cadastrados dentro de cada
Lote
, portanto acesse o caminho "
Estoque
>>
Movimento
>>
Lote
".
2.2 Selecionando o lote:
Encontre o produto que possui o
Lote
no qual serão cadastrados os
Fatores UI/UTR/UFC
e clique no ícone de
edição
.
Após isso, encontre o
Lote
desejado e clique novamente no ícone de
edição
conforme imagens abaixo:
2.3 Cadastrando os Fatores UI/UTR/UFC:
Dentro do
Lote
você encontrará os três campos responsáveis pelos
Fatores UI/UTR/UFC
, que devem ser preenchidos com as informações que estiverem no
laudo
do produto. Após isso, basta salvar as alterações clicando no ícone do disquete.
3. Conclusão:
3.1
Considerações finais:
Após seguir o passo a passo deste artigo, você terá cadastrado os
Fatores UI/UTR/UFC
em seu
Lote
.
Caso ainda restem dúvidas, favor entrar em contato.
Att,
PrismaFive.

---

## 🟢 🛠️ Notas da Versão 20.01.90.10 — 29/09/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/557950
> Publicado em: 29/09/2025

🛠️ Notas da Versão 20.01.90.10
📅
Data de Liberação: 30/09/2025
A versão 20.01.90.10 do
FarmaFácil Desktop
incorpora avanços importantes em funcionalidades estratégicas, além de revisões que garantem maior consistência nas operações do sistema.
🚀 Melhorias
ID-544
– Implementado novo fluxo de descontos de convênio na venda para casos de convênio sem vínculo no cadastro do cliente.
ID-570
– Adicionada funcionalidade para alteração de tributos em massa na Manutenção Geral, otimizando a atualização de informações fiscais em lote.
ID-577
– Adicionado envio automático de movimentações via webservice do SNGPC, garantindo integração direta e simplificada com o sistema da Anvisa.
ID-579
– Ampliada a visualização do orçamento por imagem, facilitando o acompanhamento e análise detalhada das informações apresentadas.
ID-580
– Incluído campo de previsão de entrega na visualização do orçamento por imagem, oferecendo mais transparência no prazo estimado de finalização.
🧩 Comportamentos Revisados
ID-503
– Padronizadas as formatações nos modelos de impressão Cupom NFS-e e NFS-e A4, para integrações com a TecnoSpeed assegurando consistência visual.
ID-506
– Mantida a observação configurada no cadastro do cliente ao repetir uma venda, garantindo continuidade das informações.
ID-527
– Inclusão do fator de correção na impressão da ordem de produção 40 colunas em fórmulas padrão.
ID-538
– Exibição do saldo de resgate do Cashback Nummus conforme o saldo real disponível do cliente.
ID-539
– Operacionalidade da emissão de NFS-e com provedor Elotech para o município de Ponta Grossa/PR.
ID-540
– Organização dos lotes na tela de inventário para evitar duplicidade em produtos do tipo “Acabado”.
ID-541
– Filtro de entregador aprimorado, assegurando a listagem correta de opções.
ID-542
– Relatório de cadastro de médicos disponível para visualização e exportação.
ID-543
– Exibição da descrição da espécie ativada na tela de paciente.
ID-546
– Desempenho da rolagem com mouse otimizado na visualização de relatórios.
ID-550
– Inclusão da leitura de composições de embalagens no relatório de consumo e compras.
ID-551
– Definida a prioridade de uso da “Descrição Rótulo” em mensagens padrão conforme configuração do produto.
ID-554
– Totalização do Relatório Romaneio de Entrega consolidada com remoção de duplicidades nas informações.
ID-556
– Implementada regra que impede dinamização de produtos pertencentes ao grupo “Matéria-prima”.
ID-557
– Recalculo completo de Peso MP e Peso Médio MP na troca de lote com fatores distintos.
ID-559
– Exibição das especialidades médicas ativada no relatório gráfico de vendas por médico conforme filtro aplicado.
ID-560
– Relatório “Cliente > Tipo de contato” disponível para visualização e impressão sem restrições.
ID-565
– Inclusão de produtos acabados sem lote na listagem do inventário.
ID-567
– Ordem de produção gerada corretamente em fórmulas com QSP desmembrado, quando gerado pelo módulo de Produção.
ID-568
– Visualização de prévia da ordem de produç
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 🛠️ Notas da Versão 20.01.90.09 — 25/08/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/552048
> Publicado em: 25/08/2025

🛠️ Notas da Versão 20.01.90.09
📅
Data de Liberação: 25/08/2025
A versão 20.01.90.09 do
FarmaFácil Desktop
incorpora avanços importantes em funcionalidades estratégicas, além de revisões que garantem maior consistência nas operações do sistema.
🚀 Novidades
ID-96
– Criado novo módulo de
Backup Integrado ao FarmaFácil
, oferecendo maior segurança e praticidade na gestão de dados.
ID-403
– Incluída a opção de
QSP/Excipiente automático
para formas farmacêuticas do tipo volume e vol x qtde, otimizando o processo de manipulação.
ID-577
– Envio de movimentações via webservice do
SNGPC
✅ Melhorias
ID-143
– Inclusão de dados adicionais por NCM.
ID-149
– Sincronização de dados cadastrais  para integração com a NUMMUS.
ID-150
– Alteração do responsável técnico da farmácia para assinatura do MAPA permitindo incluir registro CRMV.
ID-156
– Nova Tag de descontos na mensagem padrão de orçamento calculado.
ID-202
– Mensagem padrão de orçamento calculado ajustada para subtrair o valor do local de entrega quando houver cashback resgatado.
ID-212
– Automatização do preenchimento do código cBenef para determinados CFOP.
ID-219
– Integração com Banco Sicredi.
ID-241
– Criação de filtro por forma de pagamento na aba de envio em lote NFS-e.
ID-247
– Validade por produto sem obrigatoriedade de forma farmacêutica.
ID-248
– Filtro por convênio no relatório de vendas por período.
ID-251
– Ajuste da quantidade por fórmula de produto acabado.
ID-252
– Inclusão de todas as opções de atividades no relatório de produtividade por funcionário.
ID-415
– Exibição da validade na impressão de ordem de fórmula padrão 40 colunas.
ID-452
– Automatização na escolha de associação de registros, quando o produto associado estiver inserido na formula.
ID-467
– Parametrização para ordenação personalizada das vendas.
ID-476
– Inclusão de filtro por vendedor, quebra de linha e exportação no relatório de vendas de uso contínuo.
ID-485
– Exibição de orçamentos enviados pelo Sync/Orya com status "Processando" no relatório de orçamentos rejeitados.
ID-498
– Inclusão do código CAS no relatório de produtos.
ID-514
– Transferência de ensaios por lote entre filiais.
ID-522
– Criação de parâmetro para importação de arquivo
.txt
para atualização de preços GRUPO SC.
🔁 Comportamentos Revisados
ID-148
– Revisado o relatório
SNGPC
, que anteriormente apresentava produtos diluídos e puros de forma incorreta.
ID-153
– Revisado o processo de vendas em
formas farmacêuticas do tipo volume
, garantindo a preservação das composições de embalagem.
ID-154
– Revisada a geração de
ordens de produção de fórmula padrão
, assegurando o cálculo correto do fator de equivalência.
ID-155
– Revisada a impressão da
ordem de produção modelo A5
, exibindo corretamente o peso médio.
ID-166
– Revisada a exibição de
excipiente zerado
em cenários com dobra de cápsulas e quarentena habilitada.
ID-172
– Revisado o cálculo do
peso médio
, agora atualizando ao alterar a quantidade de cápsulas na ordem.
ID-186
– Revisado o processo de pré-
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Funcionamento do Novo Módulo de Backup – FarmaFácil — 22/07/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/546937
> Publicado em: 22/07/2025

Funcionamento do Novo Módulo de Backup – FarmaFácil
Introdução
A partir da versão
20.01 (MD-90.09)
do sistema
FarmaFácil
, foi implementada uma nova interface para controle e execução de backups do banco de dados, trazendo mais segurança, rastreabilidade e facilidade no uso por parte dos usuários. Este artigo tem como objetivo apresentar o funcionamento desse novo módulo.
Acesso ao Módulo
O módulo de backup pode ser acessado através do seguinte caminho na interface do sistema:
Menu superior:
Arquivo
Menu lateral:
Utilitário
Opções disponíveis:
Backup Banco de Dados
: executa o aplicativo  do backup imediatamente desde que ele estaja instalado (artigo para instalação).
Relatório Backup Banco de Dados
: exibe o histórico detalhado de todos os backups realizados.
Funcionalidades Disponíveis
🔄
Backup Banco de Dados
Ao clicar nesta opção, o sistema Abre o novo aplicativo do backup(Para abrir necessário que as pastas e aplicativos de backup esteja na mesma "pasta FarmaFacil" onde está sendo executado o programa farmafacil Prisma5_MD).
📊
Relatório Backup Banco de Dados
Este relatório fornece uma visão consolidada de todos os backups realizados, informando:
Data e hora do backup.
Caminho onde foi salvo.
Situação (sucesso ou erro).
Tamanho do arquivo gerado.
📅 Registro de Último Backup
No canto inferior direito da tela principal do sistema, é exibida a
data e hora do último backup realizado
, permitindo um acompanhamento rápido pelo usuário e garantindo maior transparência do processo, também é possível abrir o aplicativo do backup por ele.
Caso Algum Backup dê erro é possível identificar pelo ícone que ficará vermelho
💡 Benefícios da Nova Implementação
Segurança
: permite controle sobre a integridade dos dados.
Auditoria
: com o relatório, é possível rastrear todos os backups anteriores.
Praticidade
: processo mais visível e de fácil execução.
Prevenção de perdas
: reforça a cultura de backup diário com lembrete visível.
Introdução do Aplicativo Backup Farmafacil
O novo aplicativo
Backup FarmaFácil
foi desenvolvido para garantir maior
automação, segurança e controle
sobre os processos de backup do banco de dados utilizado no sistema FarmaFácil. Essa ferramenta é independente do sistema principal e pode ser configurada para realizar backups automáticos em dias e horários específicos, com monitoramento completo através de logs e interface intuitiva.
1. Interface Geral
Na aba
Geral
, o usuário pode configurar:
📁
Pastas de Destino
É possível adicionar múltiplos diretórios onde os backups serão salvos.
O caminho atual configurado:
Pode ser configurado caminho de rede entretanto precisa ser configurado com endereço de IP, pois colocando o nome pode não ser acessível ao Windows.
🗓️
Dias da Semana
O usuário define em quais dias da semana os backups serão realizados (Domingo a Sábado).
Na imagem enviada, Para a esquerda é desabilitado e para a direita é habilitado  — o que significa que a execução ainda depende de ativação manual ou ajuste.
🕒
Horários
O usuário p
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Sem título — 21/07/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/546833
> Publicado em: 21/07/2025

DANFE DE DEVOLUÇÃO
1. INTRODUÇÃO
Para emitir uma Danfe de Devolução, vamos precisar das seguintes informações:
CFOP (para encontrar o CFOP somente com a contabilidade, pois varia de nota de devolução para fora do Estado e dentro do Estado
Informações da nota (nota fiscal física ou pdf) pois terá as informações da chave de devolução que iremos utilizar
2. NO SISTEMA
Nota Fiscal
Vá em incluir Nova Nota Fiscal
Para nota de devolução temos 2 CFOP que somente quem pode informar para a farmácia qual pode utilizar é a
CONTABILIDADE
devido a finalidade de cada um
5202 > devolução dentro do Estado
6202 > devolução fora do estado
A serie da nota, vai depender de como a farmácia faz a emissão de outras notas a mesma coisa para a Sub Serie, sempre irá seguir a Serie da nota
Nota Fiscal nunca devem mexer ou alterar ela, pois pode bagunçar a sequencia dentro da prefeitura ou no Sefaz
Após ajustar essa parte, pode seguir realizado as configurações finais da nota, sempre prestar a ATENÇÃO na Finalidade da nota e o Frete.
Sempre conferir antes de adicionar os produtos no cadastro do cliente se ele é contribuinte do ICMS, para descobrir só verificar se ele tem a IE (inscrição estadual), caso ele tenha basta adicionar no cadastro do cliente
Inserindo a IE
Após ter realizado todos esses processos podemos estar adicionando os produtos, podemos incluir os produtos manualmente.
Clicando na Lupa, já vai abrir a aba para adicionar os produtos
Na primeira seleção a onde está Goma, podemos editar com o nome da nota, sem problemas
Na 2º parte devemos preencher com o volume que será devolvido
Pode clicar em SIM caso apareça isso
Temos agora 2 itens incluídos na nota
Caso a nota tenha um desconto, basta somar os desconto de todos os itens e aplicar fora da nota.
Após ter realizado essa parte agora vem uma das etapas importantes que é a chave de devolução que pode ser encontrada na nota fiscal, precisa ter 44 caracteres sem espaço
Na parte de Dados Adicionais Nota, pode inserir todos os dados que precisar, é o campo de observação
Após realizado todo esse procedimento é só salvar e emitir a nota

---

## 🟢 🛠️ Notas da Versão 20.01.90.08 — 17/07/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/546377
> Publicado em: 17/07/2025

🛠️ Notas da Versão 20.01.90.08
📅
Data de Liberação: 17/07/2025
A versão 20.01.90.08 do
FarmaFácil Desktop
incorpora avanços importantes em funcionalidades estratégicas, além de revisões que garantem maior consistência nas operações do sistema.
✅ Melhorias
ID-319 – Programa de fidelidade adaptado para atender `
Pontuações por venda ao invés de pontuações por valor.
ID-389 – Inclusão de relatório de vendas por médicos sem registro de visitador.
ID-419 – Adição de informações do transportador na DANFE simplificada.
ID-432 – Padronização das datas no relatório de vendas a receber na modalidade a prazo incluído data de recebimento do caixa para melhor legibilidade.
ID-477 – Ajustes de layout na impressão do romaneio de entrega para garantir exibição completa das colunas.
ID-478 – Atualização do link de visualização da NFS-e para integração com a nova URL oficial da prefeitura de São José do Rio Preto (GISS/GINFES).
🔁 Comportamentos Revisados
ID-187 – Ajustes nas informações de recebimento em vendas parceladas no relatório de vendas recebidas.
ID-343 – Reestruturação na geração de pontos do Cartão Fidelidade para incluir pagamentos a prazo parcelado e convenio parcelado.
ID-378 – Adequações no processo de montagem do certificado digital (TecnoSpeed).
ID-416 – Reconfiguração da visualização de PDFs e imagens anexados aos lotes.
ID-420 – Reformulação da impressão do comprovante de venda em modelo 60 colunas para melhor exibição dos valores da fórmula.
ID-427 – Padronização do totalizador de vendas no relatório sintético considerando o filtro de taxa de entrega.
ID-433 – Inclusão automática da descrição da fórmula no romaneio de entrega, mesmo para novas tipos de formas farmacêuticas.
ID-455 – Revisão na seleção automática de embalagens para fórmulas do tipo volume x quantidade mg/%.
ID-457 – Reconfiguração do comportamento ao alterar embalagem, garantindo ajuste coerente na composição.
ID-468 – Atualizações na integração de vendas com o convenio Funcional Card.
ID-475 – Estabilização do vínculo de associações ao transformar orçamentos em vendas.
ID-479 – Reestruturação da aplicação de acréscimos e descontos para harmonização dos valores finais da venda.
ID-483 – Adaptação do envio de NF-e para o modo síncrono conforme novas exigências da SEFAZ.
ID-501 – Ajustes no layout do arquivo Sintegra para garantir conformidade em movimentações do mês selecionado via NFC-e.
ID-504 – Revisão no carregamento de dados no relatório de vendas por receita médica.
ID-507 – Ampliação do campo ‘API KEY’ nos parâmetros da filial, permitindo até 500 caracteres.
ID-512 – Garantia de persistência das imagens inseridas durante a criação da venda.

---

## 🟢 Guia Orya - Mensagem Padrão — 10/07/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/545378
> Publicado em: 10/07/2025

Mensagem Padrão
A mensagem padrão serve para automatizar processos de atendimento e otimizar tempo de atendente, para ativá-la basta seguir os passos abaixo:
1° Entrar no campo Orya e selecionar a aba Cadastros:
2°  Ao selecionar a aba cadastros você pode clicar no ícone de Mensagem Padrão e você entrará no campo de configuração de mensagem padrão:
3° Nessa página você pode visualizar, editar e excluir as mensagens padrão já cadastradas no seu sistema e, para incluir uma nova mensagem padrão basta clicar em incluir:
4° Após clicar em “Incluir” você será direcionado para a página de criação de mensagem padrão, onde pode-se criar o Título de indicação de mensagem e texto da mesma:
5° Em seguida você pode clicar em “Salvar” para salvá-la e para utilizá-la basta você ir na conversa desejada e digitar “//” que aparecerão todas mensagens padrão cadastradas:

---

## 🟢 LEITORES DE CÓDIGO DE BARRAS COMPATÍVEIS COM O FARMA FÁCIL - INFRAESTRUTURA — 10/07/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/545368
> Publicado em: 10/07/2025

LEITORES DE CÓDIGO DE BARRAS COMPATÍVEIS COM O FARMA FÁCIL - INFRAESTRUTURA
1. Introdução
1.1
Informações importantes:
Para a compra de
leitores de código de barras
para utilização com o
Farma Fácil
, é essencial que o leitor seja
compatível
com alguns
padrões
, são eles:
Pedido de Venda (usado no PCP):
O leitor deve ser compatível com o padrão "
Code39
"de sete dígitos.
Obs.
: Os dígitos são a identificação do pedido de venda.
Ordem de Manipulação (usado na pesagem monitorada):
O leitor deve ser compatível com o padrão "
Code39
" de onze dígitos.
Obs.
: Esses dígitos são a junção dos números da ordem de manipulação seguidos do ano de geração da mesma.
Etiqueta de Estoque (usado na pesagem monitorada):
O leitor deve ser compatível com o padrão "
Interleaved 2 of 5 (ITF)
" de oito dígitos.
Obs.
: Esses dígitos são gerados automaticamente pelo sistema com o nome de "lote interno".
2. Conclusão:
2.1
Considerações finais:
Após ler este artigo você estará apto a realizar a compra de leitores de código de barras para utilização com o sistema Farma Fácil.
Caso ainda restem dúvidas, favor entrar em contato.
Att,
PrismaFive.

---

## 🟢 HABILITAR IMPRESSÃO DO RODAPÉ - ORDEM DE MANIPULAÇÃO — 10/07/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/545308
> Publicado em: 10/07/2025

HABILITAR IMPRESSÃO DO RODAPÉ - ORDEM DE MANIPULAÇÃO
1. Introdução
1.1
Informações importantes:
A partir da versão "
90.05
" do
Farma Fácil
, é possível escolher entre habilitar e desabilitar a impressão do
rodapé
nas
ordens de manipulação
conforme preferência do cliente.
Obs.
:
Esta função está disponível apenas para impressoras do modelo "
jato de tinta
" e
"
laser
", limitando-se ao formato de impressão
A4
.
2. Processo
2.1
Acessando os parâmetros:
Para
habilitar
ou
desabilitar
o
rodapé
, primeiramente devemos seguir o caminho "
Arquivo
>>
Parâmetro
>>
Parâmetro
" conforme imagem abaixo.
2.2 Configurações de impressão:
Para ter acesso as configurações de impressão, acesse o caminho "
Manipulação
>>
Impressão
", certifique-se de marcar o tipo de impressora como "
Jato de Tinta/Laser
".
Marque o campo "
Imprimir Rodapé
", e após isso salve as alterações feitas clicando no ícone do disquete conforme imagem abaixo.
2.3 Validando alterações:
Abaixo podemos visualizar a diferença entre as opções de impressão do
rodapé
desabilitada
(
Imagem 1
) e
habilitada
(
Imagem 2
).
Imagem 1
Imagem 2
3. Conclusão:
3.1
Considerações finais:
Após seguir este artigo, você terá habilitado ou desabilitado a impressão do rodapé em suas ordens de manipulação.
Caso ainda restem dúvidas, favor entrar em contato.
Att,
PrismaFive.

---

## 🟢 Introdução ao SNGPC — 30/06/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/543697
> Publicado em: 30/06/2025

INTRODUÇÃO AO SNGPC
O QUE É O SNGPC?
O SNGPC (Sistema Nacional de Gerenciamento de Produtos Controlados) é um sistema eletrônico obrigatório, criado pela ANVISA, que tem como objetivo monitorar as movimentações de entrada (como compras e transferências) e saída (como vendas, transformações, perdas e transferências) de medicamentos em farmácias e drogarias privadas. Ele registra especialmente os medicamentos sujeitos à Portaria 344/1998 — como os entorpecentes e psicotrópicos — além dos antimicrobianos, garantindo o controle e a rastreabilidade dessas substâncias.
PORQUE FOI CRIADO O SNGPC?
O SNGPC (Sistema Nacional de Gerenciamento de Produtos Controlados) foi criado pela Anvisa com o objetivo de monitorar a comercialização de medicamentos e substâncias sujeitas a controle especial, visando garantir a segurança do paciente e combater o uso indevido dessas substâncias. O sistema permite o controle e a escrituração eletrônica das movimentações desses produtos, auxiliando na prevenção de desvios e na tomada de decisões regulatórias.
O SNGPC substituiu de forma gradual, entre 2007 e 2008, a escrituração tradicional, em que as informações ficavam apenas na empresa, pela escrituração obrigatoriamente eletrônica, com transmissão dos dados para a Anvisa. O monitoramento dos hábitos de prescrição e consumo desses medicamentos no país possibilita contribuir com decisões regulatórias e ações educativas a serem promovidas pelos entes que compõem o Sistema Nacional de Vigilância Sanitária.
Aviso de paralisação das transmissões:
Aviso de retorno aos envios:
QUEM DEVE ENVIAR O SNGPC:
Todas as farmácias e drogarias privadas que:
Comercializam medicamentos sujeitos à Portaria 344/1998, como entorpecentes e psicotrópicos por exemplo.
https://www.gov.br/anvisa/pt-br/assuntos/medicamentos/controlados/lista-substancias
Vendam antimicrobianos, conforme exigência da ANVISA (RDC nº 20/2011).
https://portal.cfm.org.br/images/stories/Noticias/novalistadeantibioticos.pdf
Além disso:
A farmácia/drogaria deve ter responsável técnico (farmacêutico) regularmente inscrito no CRF.
Deve possuir autorização de funcionamento da ANVISA (AFE) e licença sanitária local.
Ou seja, qualquer estabelecimento que comercialize medicamentos controlados ou antimicrobianos precisa fazer a escrituração e envio regular das movimentações desses produtos ao SNGPC.
O QUE SÃO PRODUTOS CONTROLADOS OU SUJEITOS A CONTROLE ESPECIAL:
Medicamentos controlados
ou
sujeitos a controle especial
, conforme a
Portaria 344/1998 da ANVISA
, são medicamentos que contêm substâncias com potencial de causar
dependência física ou psíquica
, ou que oferecem
risco à saúde pública
. Por isso, sua fabricação, prescrição, venda e uso são rigorosamente controlados.
Esses medicamentos incluem:
Entorpecentes
(ex: morfina)
Psicotrópicos
(ex: diazepam)
Anabolizantes
(ex: durateston)
Outras substâncias sujeitas a controle especial
(ex: sibutramina, metilfenidato)
Todos os medicamentos controlados estão organizados em
listas de su
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Documentação para instalação do serviço de sincronização da PH24 — 26/06/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/543334
> Publicado em: 26/06/2025

Este documento tem por objetivo auxiliar na instalação do serviço da ph24 em novos clientes. Para iniciar é necessário realizar o contato com o cliente e solicitar a disponibilidade de acesso ao servidor via AnyDesk e alertá-lo que pode ser necessário derrubar algumas conexões com o banco de dados, ocasionando assim a queda do farma fácil desktop.
Antes de acessar a máquina do cliente é importante que você tenha em mãos os arquivos de instalação do projeto. A Pasta com os arquivos do sincronizador se encontra no drive na prisma através do link:
https://drive.google.com/file/d/1P3SlcTfMS6ynK-USk4YjRaYNCTyQ3W_v/view?usp=drive_link
⚓
.
Com os arquivos em mão basta acessar a máquina do cliente e começar a instalação seguindo as seguintes etapas:
Etapa 1 – Verificação de parâmetros do sistema.
Antes de iniciar o sincronizador é importante que você verifique os parâmetros obrigatórios para o sistema funcionar. Para isso é necessário verificar no portal se o cliente possui o ContaId para o PH24, conforme o exemplo abaixo:
Caso o ContaId apareça no registro do cliente podemos seguir com a verificação
do banco do cliente e banco do sync. No banco do sync é necessário acessar o portal e procurar pelo ContaId do cliente no Sync, para conseguir essa informação basta utilizar o filtro abaixo:
Você precisa verificar qual o banco do sync que está alocado o usuário e o ContaId dele, com isso em mão vc deve fazer conexão no banco do cliente e verificar as informações presentes no tabela parâmetro através do select abaixo:
SELECT sistemaid FROM DATA.portalcfg WHERE contaid = ""
Você deve substituir o valor da ContaId para a presente no portal.
Ao executar o select terá o seguinte resultado:
Caso os campos estejam vazios ou a integraçãoPh24 seja falsa será necessário entrar em contato com a Ph24 para gerar as informações necessárias ou verificar a tarefa para ver se as informações necessárias já estão presentes nelas. Desta forma você deve garantir que essas informações estejam presentes nessas colunas.
Já na parte do banco do cliente é necessário verificar se o mesmo já está atualizado com as colunas criadas, para isso será necessário rodar o seguinte comando:
select ph24ultimasincronizacao from parametro p
OBS: Caso as consultas não estejam retornando será necessário derrubar as sessões do farma fácil desktop para liberação do banco.
Caso o comando apresente algum erro, significa que o campo ainda não foi criado, neste caso é necessário entrar em contato com o pessoal do desktop
para que realizem a atualização através dos scripts na base do cliente. Um dos scripts para a adição do campo pesquisado é o abaixo:
select data.create_attribute_if_not_exists('data' , 'parametro' ,
'ph24ultimasincronizacao', 'timestamp without time zone');
Se o comando passar a funcionar o campo
ph24ultimasincronizacao
deve estar null, isso para garantir que todos os dados serão sincronizados do início.
Etapa
2 - Instalar o serviço SyncFFDesktop
Acesse o link, faça o download do sincroni
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Inclusão de Excipiente Padrão por Forma Farmacêutica – Versão 20.01.90.07 — 24/06/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/542670
> Publicado em: 24/06/2025

A partir da versão
20.01.90.07
, foi implementado um novo recurso nas formas farmacêuticas do tipo
CÁPSULA
,
IMPLANTE
e
COMPRIMIDO
, permitindo o
vínculo direto de um excipiente padrão
por forma farmacêutica.
Esse novo campo tem funcionamento
semelhante ao excipiente padrão configurado no parâmetro geral
, com a vantagem de possibilitar maior controle e personalização por tipo de forma farmacêutica.
✅ Comportamento
Ao cadastrar ou editar uma fórmula com uma dessas formas farmacêuticas, caso
nenhum produto tenha sido incluído manualmente no grid como QSP
, o sistema
incluirá automaticamente o excipiente padrão vinculado à forma farmacêutica
, obedecendo à seguinte ordem de prioridade:
🔢 Prioridade na Escolha do Excipiente
Excipiente vinculado diretamente ao produto
(ativo da fórmula);
Excipiente vinculado à classificação biofarmacêutica
(classe do ativo);
Excipiente vinculado à forma farmacêutica
(novo campo);
Excipiente padrão definido em parâmetros global
.
Essa priorização garante que o excipiente mais específico e adequado seja utilizado automaticamente na fórmula, reduzindo a necessidade de intervenção manual e aumentando a padronização das prescrições.

---

## 🟢 🛠️Notas da Versão 20.01.90.07 — 23/06/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/542581
> Publicado em: 23/06/2025

🛠️
Notas da Versão 20.01.90.07
Data de Liberação: 23/06/2025
A versão
20.01.90.07
traz uma série de
comportamentos revisados e melhorados
,
melhorias funcionais
. Confira abaixo os principais destaques:
✅
Melhorias Implementadas
ID-173
– Implementada a funcionalidade de
retenção de receita para pacientes veterinários
, permitindo o controle e armazenamento das receitas conforme exigência para esse segmento.
ID-257
– Corrigida a exibição do campo
"Forma Farmacêutica" no rótulo
, garantindo que o dado apareça corretamente nas impressões.
ID-323
– Adicionada a opção de
vincular QSP e excipientes padrão diretamente na tela de manutenção da forma farmacêutica
, facilitando o cadastro e a padronização de fórmulas.
ID-364
– Realizados
ajustes no layout e estrutura de dados
do relatório de especialidades médicas, garantindo melhor organização e leitura dos dados.
ID-365
– Corrigidos
valores inconsistentes e filtros aplicados
no relatório de
orçamentos rejeitados
, melhorando a fidelidade das informações.
ID-369
– Implementada a opção de
alterar o status de entrega em massa para vários romaneios selecionados simultaneamente
, otimizando o processo logístico.
ID-380
– Refinado o relatório de
visitador sintético
, com
ajustes de campos e ordenação de dados
para melhor análise dos atendimentos realizados.
ID-400
– Incluído
filtro por etapa PCP
no relatório de
produção por forma farmacêutica
, permitindo análise mais segmentada por fase de produção.
ID-401
– Aumentado o limite de caracteres no campo
codigoprodutofornecedor
da tabela
fornecedorproduto
, permitindo cadastro de códigos maiores conforme fornecedores externos.
🔧
Ajustes Realizados em Funcionalidades
ID-146
– Revisado o totalizador do relatório DRE para apresentar corretamente os valores somados por faixa de competência.
ID-228
– Ajustado o cálculo da porcentagem de origem das vendas no relatório por período, garantindo distribuição proporcional correta.
ID-232
– Tratado o comportamento ao gerar venda com o mesmo produto vinculado como item e excipiente, evitando duplicidade quando o QSP automático está ativado.
ID-299
– Incluído o valor dos pagamentos do tipo 'Depósito' no relatório de Receita x Despesas, anteriormente desconsiderados.
ID-308
– Repetição de vendas passou a considerar o mesmo desconto aplicado na venda original, mantendo o preço final correto.
ID-311
– Evitado o reaproveitamento indevido de cápsulas da pré-venda em fórmulas que não utilizam pré-configuração.
ID-327
– Ajustado o inventário para exibir os lotes no grupo de produto de drogaria/acabado, quando se trata de controlados e o grupo não tiver o parametro controle de lote ativo.
ID-334
– Aplicação das incompatibilidades revisada para considerar cenários com mais de um excipiente inserido na fórmula.
ID-336
– Garantido o vínculo de produtos associados ao converter orçamentos em vendas com formas farmacêuticas do tipo Volume/Volume x Quantidade.
ID-339
– Ajustado o cálculo do custo do item ao registrar entrada de nota fiscal co
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 CALCULAR ESTOQUE MÍNIMO E MÁXIMO - PRODUTO — 14/06/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/541526
> Publicado em: 14/06/2025

CALCULAR ESTOQUE MÍNIMO E MÁXIMO - PRODUTO
1. Introdução
1.1
Informações importantes:
Para ter um controle maior do
estoque
e auxiliar nos
pedidos de compra
, o
Farma Fácil
disponibiliza uma calculadora de
estoque mínimo
e
estoque máximo
de cada produto.
Essa calculadora utiliza os dados da sua farmácia (
quantidade utilizada
,
quantidade comprada
,
frequência de compra
,
etc
...) para calcular uma
sugestão
de
estoque mínimo
e
estoque
máximo
para cada produto selecionado.
Caso você aceite a sugestão do sistema, os campos "
Estoque Mín.
" e "
Estoque Máx.
" dentro do cadastro do produto serão atualizados com base nos valores calculados.
1.2
Requisitos:
Para realizar o cálculo do
estoque mínimo
e
estoque máximo
através do
Farma Fácil
, todas as
ordens de manipulação
do período que será utilizado para extração de informações devem estar concluídas, pois produtos com
quantidade comprometida
interferem na precisão do cálculo.
2. Processo
2.1 Acessando a tela de cálculo
:
Para acessar a tela de cálculo, siga o caminho "
Arquivo
>>
Estoque
>>
Produto
" e depois utilize o ícone da caixa conforme imagem abaixo.
Obs.
:
O atalho para acessar esse módulo dentro da tela de produto é a tecla "
F9
".
2.2 Preenchendo os campos:
No campo "
Tipo
" podemos escolher entre as seguintes opções:
-
Demanda
: Para produtos
acabados
e
drogaria
.
-
Consumo
: Para produtos
manipulados
.
No campo "
Período: De
", você deve selecionar o período (no formato "
DD/MM/AAAA
") que o sistema utilizará para extrair os dados e realizar o cálculo para a recomendação de
estoque mínimo
e
estoque
máximo
.
Nos campos relacionados a reposição, temos:
-
Tempo Reposição Mínimo
: Cronograma padrão de compras para reposição do estoque da farmácia.
-
Tempo Reposição Máximo
: Período máximo em que a farmácia pode ficar sem realizar as compras para o estoque sem afetar a produção.
Obs.
:
Estes campos devem ser preenchidos em dias.
Em seguida, marque se deseja que o sistema calcule apenas o
estoque mínimo
recomendado, apenas o
estoque máximo
recomendado, ou calcule ambas em conjunto.
Após preenchidas todas as informações acima, selecione o grupo desejado para as alterações e clique no ícone da calculadora no canto inferior direito conforme mostrado na imagem abaixo.
Obs.
: É possível adicionar mais de um grupo por vez caso seja necessário.
2.3 Analisando o relatório gerado:
Ao gerar o relatório, você poderá observar as seguintes informações respectivamente:
-
Grupo
: Código do grupo no qual o produto está cadastrado.
-
Produto
: Código de identificação do produto dentro do sistema.
-
Descrição
: Nome de identificação do produto dentro do sistema.
-
Est. Mínimo
: Estoque mínimo cadastrado atualmente no produto.
-
Est Máximo
: Estoque máximo cadastrado atualmente no produto.
-
Qtd. Vendida
: Quantidade do produto vendida durante o período selecionado.
-
Pos. Estoque
: Quantidade atual do produto em seu estoque.
-
Mínimo Calc.
: Sugestão do sistema para estoque mínimo baseado nas movimentações durant
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 ENVIO DAS MOVIMENTAÇÕES - SNGPC — 13/06/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/541522
> Publicado em: 13/06/2025

ENVIO DAS MOVIMENTAÇÕES - SNGPC
1. Introdução
1.1
Informações importantes:
Após realizar o envio do
inventário inicial
seguindo os passos do artigo
https://prismafive.movidesk.com/kb/pt-br/article/541456/sngpc_inventario_inicial
, você deve iniciar o envio de suas
movimentações
para o portal do
SNGPC.
O
Responsável Técnico
da farmácia deve enviar todas as
movimentações
de
controlados
entre períodos de no mínimo um dia e no máximo sete dias para o portal do
SNGPC
.
Obs.
: Em visitas da
Anvisa
à sua farmácia para uma fiscalização, ela irá comparar seu
armário de controlados
com seu
inventário
no portal do
SNGPC
, por isso é crucial manter o
inventário
e
movimentações
sempre corretas no portal.
1.2
Requisitos para envio das movimentações:
Para realizar a exportação do arquivo das
movimentações
, é necessário que todas as
ordens de manipulação
contendo
controlados
até a data do período informado estejam concluídas.
Obs.
:
Caso haja
ordens de manipulação
contendo
controlados
pendentes no momento da exportação do arquivo, o sistema exibirá um arquivo
PDF
na tela com as
ordens de manipulação
pendentes de serem finalizadas.
1.3
Bloqueios do sistema:
Após realizar a exportação do arquivo das
movimentações
para seu computador, o
Farma Fácil
bloqueará toda movimentação de
controlados
(
realização de vendas
,
conclusão de ordens de manipulação
,
acertos de estoque
,
dentre outras
...) até o fim do dia (
23h59
).
Isso acontece para que não haja divergências entre as quantidades enviadas no arquivo das
movimentações
e as quantidades reais no estoque do
Farma Fácil
.
Obs.
: Para que o bloqueio não interfira na rotina da farmácia, a
PrismaFive
recomenda que a exportação e envio sejam feitos após o fim do expediente ou em alguma data na qual não haverá manipulação.
2. Processo
2.1
Acessando o módulo do SNGPC:
Para acessar o módulo do
SNGPC
dentro do
Farma Fácil
, você deve seguir o caminho "
Estoque
>>
Movimento
>>
SNGPC
" conforme imagem abaixo.
Obs.
:
Este processo deve ser feito através do usuário do
Responsável Técnico
devido as suas permissões especiais.
2.2 Criando uma nova exportação:
Clicando no botão de inclusão conforme imagem abaixo, a tela de configurações de exportação se abrirá.
Obs.
:
Para clicarmos no botão de nova exportação, é necessário que a exportação anterior esteja concluída. Caso tenha problemas com isso, basta abrir um chamado para o suporte da
PrismaFive
que lhe auxiliaremos.
2.3 Configurando a exportação das movimentações:
Para exportar o arquivo de
movimentação
, primeiro marque o campo "
Tipo
" como "
Movimentação
", depois marque o botão "
Exportação Manual
", após isso preencha os campos "
Período de"
e "
Até
" com a data das
movimentações
desejadas, e por fim clique no ícone para iniciar a exportação.
Obs.
:
Você deve realizar envios constantes, não sendo possível pular alguma data durante as movimentações.
2.4 Validação da exportação:
Caso a exportação tenha ocorrido com sucesso, você receberá a mensagem de êxito mostrada na image
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 ENVIO DO INVENTÁRIO INICIAL - SNGPC — 13/06/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/541456
> Publicado em: 13/06/2025

ENVIO DO INVENTÁRIO INICIAL - SNGPC
1. Introdução
1.1
Informações importantes:
Com todos os passos de preparação para o retorno obrigatório do
SNGPC
presentes no artigo
https://prismafive.movidesk.com/kb/pt-br/article/541398/sngpc_preparativos
⚓
realizados, você poderá enviar o
inventário inicial
para o portal do
SNGPC
.
O
Responsável Técnico
da farmácia tem o direito de enviar quantos
inventários
quiser para o portal do
SNGPC
, porém, recomendamos realizar o envio apenas para pequenas correções ou quando há determinação da
autoridade sanitária
.
Obs.
: Em visitas da
Anvisa
à sua farmácia para uma fiscalização, ela irá comparar seu
armário de controlados
com seu
inventário
no portal do
SNGPC
, por isso é crucial manter o
inventário
no portal sempre correto.
1.2
Requisitos para envio do inventário inicial:
Para realizar a exportação do arquivo do
inventário inicial
, é necessário que todas as
ordens de manipulação
contendo
controlados
até o data referência do
inventário
estejam concluídas.
Obs.
:
Caso haja
ordens de manipulação
contendo
controlados
pendentes no momento da exportação do arquivo, o sistema exibirá um arquivo
PDF
na tela com as
ordens de manipulação
pendentes de serem finalizadas.
1.3
Bloqueios do sistema:
Após realizar a exportação do arquivo do
inventário inicial
para seu computador, o
Farma Fácil
bloqueará toda movimentação de
controlados
(
realização de vendas
,
conclusão de ordens de manipulação
,
acertos de estoque
,
dentre outras
...) até o fim do dia (
23h59
).
Isso acontece para que não haja divergências entre as quantidades enviadas no arquivo do
inventário
e as quantidades reais no estoque do sistema.
Obs.
: Para que o bloqueio não interfira na rotina da farmácia, a
PrismaFive
recomenda que a exportação e envio sejam feitos após o fim do expediente ou em alguma data na qual não haverá manipulação.
2. Processo
2.1
Acessando o módulo do SNGPC:
Para acessar o módulo do
SNGPC
dentro do
Farma Fácil
, você deve seguir o caminho "
Estoque
>>
Movimento
>>
SNGPC
" conforme imagem abaixo.
Obs.
:
Este processo deve ser feito através do usuário do
Responsável Técnico
devido as suas permissões especiais.
2.2 Criando uma nova exportação:
Clicando no botão de inclusão conforme imagem abaixo, a tela de configurações de exportação se abrirá.
Obs.
:
Para clicarmos no botão de nova exportação, é necessário que a exportação anterior esteja concluída. Caso tenha problemas com isso, basta abrir um chamado para o suporte da
PrismaFive
que lhe auxiliaremos.
2.3 Configurando a exportação do inventário inicial:
Para exportar o arquivo do
inventário inicial
, primeiro marque o campo "
Tipo
" como "
Inventário
", depois marque o botão "
Exportação Manual
", após isso preencha o campo "
Data Referência
" com a data atual e por fim clique no ícone para iniciar a exportação.
Obs.
:
Você pode preencher o campo "
Data Referência
" com uma data de até cinco dias anteriores ao dia atual, porém recomendamos sempre enviar o
inventário
com a data atual.
2.4 Va
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 PREPARATIVOS PARA O RETORNO OBRIGATÓRIO - SNGPC — 13/06/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/541398
> Publicado em: 13/06/2025

PREPARATIVOS PARA O RETORNO OBRIGATÓRIO - SNGPC
1. Introdução
1.1
O que é o SNGPC?:
O
Sistema Nacional de Gerenciamento de Produtos Controlados
(
SNGPC
) é uma ferramenta desenvolvida pela
Anvisa
que tem como objetivos principais: monitorar a dispensação e o consumo de
medicamentos controlados
(
entorpecentes
,
psicotrópicos
e
antimicrobianos
), otimizar o processo de escrituração, gerar dados atualizados para subsidiar a
vigilância sanitária
e propor políticas de controle mais eficazes.
Além disso, o sistema integra-se aos processos existentes nas farmácias, estabelecendo um padrão para a transmissão de dados, facilitando o gerenciamento eletrônico das movimentações desses medicamentos.
Implementado entre 2007 e 2008, o
SNGPC
substituiu a escrituração tradicional, que era realizada apenas internamente pelas empresas, por um sistema eletrônico que transmite automaticamente os dados para a
Anvisa
. Essa mudança visa garantir um controle mais eficaz sobre a dispensa e o consumo desses medicamentos, permitindo ações regulatórias e educativas fundamentadas.
O sistema é parte de uma política maior da
Anvisa
, que busca abranger toda a cadeia de produção e distribuição desses produtos, promovendo o uso racional e a prevenção do uso indevido.
Após ser retirado temporariamente do ar em 23 de Dezembro de 2022, a
Anvisa
informou que a inclusão de informações no
Sistema Nacional de Gerenciamento de Produtos Controlados
(
SNGPC
) voltará a ser
obrigatória
em
2025
conforme cronograma que pode ser acessado através deste link:
SNGPC - CRONOGRAMA DE RETORNO OBRIGATÓRIO
Caso necessite de informações adicionais, a
Anvisa
disponibilizou quatro vídeos que explicam um pouco mais sobre o sistema.
Acesse-os através do link:
SNGPC - VIDEOAULAS DA ANVISA
Para dúvidas ou suporte relacionados a
Anvisa
ou ao
SNGPC
, a
vigilância sanitária
possui canais próprios de atendimento, que podem ser acessados através deste link:
ANVISA - CANAIS DE ATENDIMENTO
2. Preparativos para a volta do SNGPC
2.1
Credenciamento na Anvisa:
Primeiramente você deve se certificar que as credenciais da
farmácia
e do
Responsável Técnico
(
RT
) estão ativas e atualizadas no portal da
Anvisa
, pois você irá utilizá-las para acessar o portal e realizar os envios tanto dos inventários quanto das movimentações.
Acesse o portal clicando neste link:
PORTAL DO SNGPC
2.2 Atualização das credenciais no Farma Fácil:
Com as credenciais da
Anvisa
devidamente atualizadas, precisamos registrá-las dentro do
Farma Fácil
.
O que pode ser feito entrando no caminho "
Arquivo
>>
Parâmetro
>>
Parâmetro
" e editando os campos conforme imagem abaixo.
Obs.
:
Caso os campos estiverem bloqueados para edição, você deve abrir um
chamado
para o suporte da
PrismaFive
com o título "
Alteração dos dados do Responsável Técnico
" para lhe auxiliarmos com a alteração.
2.3 Realizar o inventário de produtos controlados pela Anvisa:
Para enviarmos o
inventário inicial
para a
Anvisa
, o ideal é que a farmácia realize o processo de
inventári
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Emissão de NFC-e e Obrigatoriedade de Informar o GTIN (Código Barra) – Legislação do Rio Grande do Sul — 30/05/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/538834
> Publicado em: 30/05/2025

Para atender à legislação vigente no estado do Rio Grande do Sul, é obrigatório informar o GTIN (código de barras) na emissão da NFC-e (Nota Fiscal de Consumidor Eletrônica) para produtos industrializados.
Produtos Industrializados
Para produtos industrializados, é necessário cadastrar o código de barras do item em
dois locais
no sistema:
No campo específico de
código de barras do cadastro do produto
;
2. Na aba
Complemento / Dados Adicionais no cadastro do produto
.
No XML da nota fiscal, essa informação será refletida corretamente com a inclusão do GTIN.
Produtos Acabados Produzidos pela Farmácia (Fórmulas Padrão)
Para os produtos acabados produzidos internamente (como fórmulas padrão), é necessário verificar a viabilidade de
registrar o código de barras
desses produtos.
Recomenda-se
consultar a contabilidade
, pois o registro de código de barras envolve
um custo por produto
.
Para emissão de NFC-e desses produtos, o código de barras deve estar informado tanto no campo próprio do produto quanto na aba de complemento.
Caso o campo de GTIN fique em branco no XML, o sistema indicará “
SEM GTIN
”.
⚠️ A Receita Estadual do RS está emitindo
notificações
para casos em que produtos industrializados ou acabados são informados
sem GTIN
.
Segue exemplo de notificação:
Resumo: Emissão de NFC-e com Código de Barras
Para que a farmácia consiga emitir corretamente o XML da NFC-e, é obrigatório que o
código de barras (GTIN)
esteja cadastrado:
No
campo de código de barras do produto
;
Na
aba Complemento / Dados Adicionais
.
Sem essa informação, o XML será gerado com o status
“SEM GTIN”
, o que pode resultar em
notificações da Receita Estadual do Rio Grande do Sul
.

---

## 🟢 HABILITAR ATUALIZAÇÃO DO PREÇO DE VENDA COM PMC NA NOTA FISCAL DE ENTRADA — 27/05/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/538058
> Publicado em: 27/05/2025

HABILITAR ATUALIZAÇÃO DO PREÇO DE VENDA COM PMC NA NOTA FISCAL DE ENTRADA
1. Introdução
1.1
Informações importantes:
Após a versão 90.05 do Farma Fácil, uma nova função foi adicionada: atualizar o preço de venda conforme o P.M.C. da nota de entrada.
1.2
O que é PMC?:
Para o ramo de Farmácias, o PMC significa Preço Máximo ao Consumidor.
Ele é o valor mais alto que pode ser cobrado do consumidor final por um medicamento nas farmácias e drogarias brasileiras, sendo reajustado anualmente por volta do mês de Março.
Este preço é regulamentado pela Câmara de Regulação do Mercado de Medicamentos (CMED), que é um órgão ligado a Anvisa e está previsto na lei Lei nº 10.742/2003.
2. Processo
2.1
Caminho para verificar tipo do grupo:
Primeiramente, precisamos verificar o tipo do grupo o qual gostaríamos de adicionar a atualização do preço de venda.
Para isso, acesse o caminho "Arquivo >> Estoque >> Grupo", selecione o grupo desejado e clique no botão de editar, conforme imagem abaixo:
Obs.:
Este processo só está disponível para grupos do tipo "Acabado".
2.2 Habilitando o botão:
Após validar que o grupo está cadastrado como tipo "Acabado", basta habilitar o botão "Atualizar Preço de Venda com PMC da Nota fiscal de Entrada" e clicar no botão para salvar as alterações realizadas.
3. Exemplo prático
3.1
Introdução:
Para garantir um melhor entendimento, iremos realizar o processo de entrada de nota do produto.
Preencha o PMC na entrada da nota fiscal do produto.
3.2 Cadastro:
Dentro do cadastro do produto será calculado automaticamente o P.M.C baseado nas notas de entrada.
4. Conclusão:
4.1
Considerações finais:
Após seguir os passos deste artigo corretamente, as novas entradas de nota onde o PMC estiver preenchido terão influência sobre o preço de venda dos produtos.
Caso algo não tenha ficado claro ou necessite de maior auxílio, sinta-se a vontade para abrir um chamado para nossa equipe de suporte.
Att,
PrismaFive.

---

## 🟢 🛠️Notas da Versão 20.01.90.06 — 09/05/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/534272
> Publicado em: 09/05/2025

🛠️
Notas da Versão 20.01.90.06
Data de Liberação: 09/05/2025
A versão
20.01.90.06
traz uma série de
comportamentos revisados e melhorados
,
melhorias funcionais
. Confira abaixo os principais destaques:
✅
Melhorias Implementadas
ID-58
– Revisado o tratamento da tabela de apontamento para garantir que os campos obrigatórios sejam devidamente preenchidos antes do salvamento.
ID-137
– Adicionado parâmetro que permite exibir o texto “FÓRMULA MANIPULADA” na descrição da fórmula da NFC-e, conforme parametrização da filial.
ID-141
– O relatório MAPA Veterinário passa a exibir o número da Nota Fiscal no lugar do número da venda, proporcionando mais precisão nas conferências.
ID-176
– Melhorado o fluxo de atualização de status da NFSe de Cabo Frio-RJ (Provedor ISSINTEL), garantindo retorno adequado após a transmissão.
ID-250
– Adicionado campo de CPF na tela de alteração de receitas, facilitando a conferência e o preenchimento das informações do cliente.
ID-316
– Revisada a rotina de envio de NF-e, com validações adicionais para prevenir eventuais inconsistências.
🐞
Comportamento Revisados
🔧
PCP / Produção
ID-107
– Revisado tratamento de visualização da ordem de produção com fator de equivalência.
ID-147
– Ajustado comportamento para exibir corretamente o número da receita na impressão da ordem de produção.
ID-215
– Revisado controle de status em múltiplas etapas, impedindo que mais de uma máquina mude o status simultaneamente.
ID-217
– Ajustado o tratamento de geração de dinamização com embalagem, evitando inconsistência no processo.
ID-237
– Implementado bloqueio para impedir gravação de venda sem item e evitar a geração indevida de ordem de produção.
ID-261
– Revisado carregamento de dados no apontamento de PCP, garantindo informações consistentes.
ID-306
– Revisado tratamento de concatenação na conclusão de ordens de produção para manter integridade das informações.
💰
Financeiro / Relatórios
ID-139
– Tratamento revisado no relatório Caixa Convênio para apresentar corretamente os totais mesmo sem parcelas, respeitando a opção "exibir parcelas do período".
ID-164
– Ajustado comportamento no relatório Caixa por Grupo/Forma Farmacêutica para exibir a quantidade correta de itens.
ID-165
– Melhorado o tratamento dos valores no relatório de Orçamentos Rejeitados por Visitador, garantindo consistência nas informações.
ID-169/170
– Revisado o preenchimento dos campos de custo médio e venda no relatório de Posição de Estoque Financeiro, além da exportação em CSV.
ID-274
– Ajustado fluxo de envio da NFSe para a cidade de Mafra (Provedor Pública), prevenindo falhas na execução.
ID-335
– Revisado tratamento para geração do Sintegra, incluindo o REGISTRO 70.
📦
Estoque / Produtos
ID-145
– Melhorado o controle de quantidade comprometida no lote ao cancelar fórmulas, garantindo atualização correta.
ID-256
– Revisado o recálculo da quantidade da fórmula após edição, para refletir os ajustes feitos no cadastro.
ID-330
– Tratamento ajustado na Ficha Técnica do produto pa
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Guia do Suporte para Cliente — 25/04/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/532093
> Publicado em: 25/04/2025

SEJA BEM-VINDO!
A PrismaFive oferece o que há de mais moderno em soluções de tecnologia para gestão em farmácias e drogarias. Agora, você descobrirá que também pode contar com um canal aberto de atendimento, auxiliando-o em suas dúvidas e processos ao utilizar nossas soluções, garantindo que estejam sempre alinhadas com o seu negócio. Para nós, proporcionar um atendimento de qualidade é essencial para manter um relacionamento sustentável, duradouro e cada vez mais próximo de você, que é a nossa razão de ser.
Pensando nisso, elaboramos o Guia do Suporte PrismaFive, onde você encontrará todas as informações necessárias para interagir com nossas equipes de atendimento. Através deste guia, você ficará por dentro de todos os nossos serviços, estimativas de prazos e procedimentos, garantindo uma experiência completa e eficiente.
O que faz o Suporte?
O escopo da equipe de suporte abrange as seguintes atividades:
Dúvidas Técnicas:
Esclarecimento de dúvidas pontuais sobre recursos e funcionalidades dos sistemas: PrismaSync, FarmaFácil ,FarmaCommerce, Dashfácil, Alcance.
Problemas Técnicos:
Resolução de incidentes relacionadas ao uso e funcionalidade de nossos produtos e identificando bugs (erro no sistema)  encaminhamos para correção da nossa equipe de desenvolvimento.
Não faz parte deste escopo:
Treinamento Especializado:
Treinamentos detalhados devem ser agendados separadamente com a equipe comercial. No entanto, é importante destacar que durante a implantação do sistema, um usuário-chave no cliente é treinado para posteriormente compartilhar o conhecimento adquirido com os demais membros da farmácia.
Modificações em Cadastros ou Dados no Banco de Dados:
Por questões de segurança e para garantir a integridade dos seus dados, nossa equipe de suporte técnico não tem autorização para realizar alterações diretamente no banco de dados ou nos cadastros dos clientes. A responsabilidade pela alteração dos dados é exclusiva do cliente, cabendo ao suporte apenas a orientação sobre como utilizar a função no sistema para realizar essa tarefa
Solução de Problemas de Rede:
Se houver problemas relacionados à rede, recomendamos entrar em contato com o técnico que presta serviço à sua farmácia, pois ele será capaz de ajudar com questões de infraestrutura de rede.
Problemas com seu Computador:
Questões relacionadas a hardware não estão no escopo do suporte técnico, portanto também devem ser direcionadas ao técnico que presta serviço a farmácia.
Problemas com sua impressora:
Se sua impressora esta com problemas de impressão e não imprime nem a folha teste é necessário acionar seu técnico de informática. A responsabilidade da PrismaFive é apenas configurar a impressora para uso no FarmaFácil.
Clique aqui
saiba mais.
Dúvidas na conduta do seu negócio:
Não faz parte do escopo do suporte repassar informações que afetam o cotidiano da farmácia, como dados tributários e precificação de produtos.
Não realizamos suporte a produtos de terceiros
como exemplo: Siproquim, Farmácia Po
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 FARMÁCIA POPULAR - CANCELAMENTO DE VENDA — 25/04/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/532035
> Publicado em: 25/04/2025

FARMÁCIA POPULAR - CANCELAMENTO DE VENDA
1. Introdução
1.1
Detalhes do erro:
Terminal não habilitado para cancelamento de venda com farmácia popular!
2. Processo
2.1
Acessando as configurações do sistema:
Primeiramente, acesse o módulo "
Configurações PrismaFive
" através do caminho "
Arquivo
>>
Parâmetro
>>
Configurações
PrismaFive
".
2.2 Filtrando chaves locais:
Dentro da aba de Configurações, clique no botão "
Pesquisar
", depois em "
Exibir chaves de configuração deste computador
" e por último em
"
Incluir configuração (Ins)
".
2.2.1 Adicionando chave correta:
Para habilitar a exclusão da venda, precisamos incluir a chave "
FCIAPOP
" no sistema da cliente, então, selecione a chave correta, insira "
1
" no campo "
Valor
" e salve a configuração realizada clicando em "
Gravar (Enter)
".
Obs.: Esta configuração é local, ou seja, deve ser realiza em todos os terminais em que o cliente deseja a possibilidade da exclusão de vendas do Farmácia Popular.
3. Conclusão:
3.1
Considerações finais:
Após seguir o passo a passo dente artigo, o terminal configurado estará apto a excluir vendas do Farmácia Popular.
Caso ainda restem dúvidas, favor entrar em contato.
Att,
PrismaFive.

---

## 🟢 Requisitos para Baixa de Responsabilidade Técnica — 23/04/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/531460
> Publicado em: 23/04/2025

Requisitos para Baixa de Responsabilidade Técnica
1. Introdução
1.1
Informações importantes:
Com a saída da responsável técnica de uma farmácia, a Anvisa exige alguns cuidados para que possa ser validado a baixa/troca de responsável.
Essas solicitações da Anvisa variam conforme a localidade, porém um relatório sempre é pedido, o movimento dos controlados até o último dia de trabalho do Responsável Técnico.
2. Processo
2.1
Gerando o relatório solicitado:
Acesse o relatório "Controlados Manipulação" dentro do módulo "Venda", selecione a classificação "Movimento no Período" e preencha o período desejado para geração do relatório.
2.2 Template do relatório:
O relatório gerado se abrirá em uma nova janela, onde você poderá conferir informações referentes aos controlados de sua farmácia no período filtrado.
Obs.: A partir desta tela, também é possível imprimir ou salvar o relatório para ser enviado para a Anvisa.
2.2.1 Requisitos utilizados pelo relatório
:
Caso algum produto controlado não esteja presente no relatório gerado, você deve acessar o cadastro deste produto faltante através do caminho mostrado abaixo e verificar se os campos "Lista Controlado", "DCB" e "Classe Terapêutica" estão preenchidos corretamente.
3. Conclusão:
3.1
Considerações finais:
Após seguir o passo a passo deste artigo, você terá um levantamento de controlados da data desejada e poderá enviá-lo para a Anvisa.
Caso ainda tenha dúvidas, favor entrar em contato.
Att,
PrismaFive.

---

## 🟡 REMANIPULAÇÃO, FRACIONAMENTO, REENVASE — 08/04/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/529407
> Publicado em: 08/04/2025

REMANIPULAÇÃO, FRACIONAMENTO, REENVASE
O
fracionamento de medicamentos
é o processo de dividir um medicamento industrializado (como comprimidos ou cápsulas) em doses menores, conforme a necessidade do paciente.
Ele é permitido apenas para produtos registrados como “fracionáveis” e deve seguir normas rigorosas de higiene, rotulagem e rastreabilidade. Só farmácias autorizadas pela Anvisa podem realizar esse procedimento.
🚨
IMPORTANTE
🚨
Farmácias e drogarias comuns NÃO podem remanipular
medicamentos industrializados para criar novas dosagens. Elas só podem realizar
fracionamento
, e mesmo assim
seguindo regras muito específicas
.
1. Cadastros e funcionamento do p
rocesso de
r
emanipulação
Quando o paciente solicitar o fracionamento do produto, ele precisará da receita médica com a prescrição personalizada, cuja
forma industrializada não está disponível na dosagem exata recomendada pelo profissional de saúde
.
Durante a manipulação, os comprimidos industrializados são
triturados e homogeneizados
em condições controladas, seguindo as Boas Práticas de Manipulação.
1.1. Passo a passo - FarmaFácil
1.1.1.
Crie um produto referente ao medicamento recebido. No nosso exemplo, supõe-se que o medicamento disponível em drogarias tem a dosagem de 70mg.
1.1.2.Crie o lote deste produto, com referência ao lote original do produto pronto utilizado como matéria-prima (mantendo a rastreabilidade).
Atenção: lembre-se que em medicamentos prontos (de drogaria), além do ativo principal, temos também o excipiente que compõe o volume total do comprimido. Para
corrigir a concentração real do princípio ativo (PA)
,
devemos cadastrar
o fator de correção, que serve para
"compensar" os excipientes presentes
, ajustando a quantidade a ser usada para cada cápsula ou formulação.
1.1.3. Realize um acerto de estoque, com a quantidade total obtida (em gramas) no processo de trituração do medicamento pronto.
1.1.4.
Após estes passos, você já pode realizar a venda no sistema FarmaFácil, com a dosagem prescrita pelo médico. No exemplo elaborado, recebemos o medicamento em 70mg, e iremos reenvasar para 30mg.
Dica:
Caso o farmacêutico tenha dúvidas em relação ao fator de correção, verifique o cálculo exemplo abaixo.
a)
Primeiro, calcula-se quantos comprimidos foram triturados:
4800 mg (total triturado) / 70 mg (por comprimido) = 68,57 comprimidos
b)
Depois, calcula-se a quantidade total de princípio ativo puro (PA) que há nos comprimidos:
68,57 comprimidos × 30 mg (PA por comprimido) = 2057,14 mg de PA
c)
O fator de correção é a razão entre o total triturado (com excipiente) e o total de PA:
FC = 4800 mg (total triturado) / 2057,14 mg (PA) ≈ 2,33

---

## 🟡 Notas de Versão 20.01.90.05 do FarmaFácil Desktop — 01/04/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/528277
> Publicado em: 01/04/2025

Notas da versão 20.01.90.05 do Farma Fácil Desktop
🗓 Data de lançamento: 01/04/2025
📌 Descrição da versão: A versão 20.01.90.05 do Farma Fácil Desktop já está disponível. Esta atualização traz diversas melhorias e correções no sistema que visam aprimorar a experiência de uso e aumentar a eficiência das operações diárias. Aqui estão os principais destaques:
🔧 Correções de Defeitos (Bugs Resolvidos)
📌 Problemas com Cálculos e Fórmulas
ID-236 - Cálculo de excipiente baseado na cápsula de outra fórmula
Corrigimos o problema onde o cálculo do excipiente estava sendo realizado com base em cápsulas de outra fórmula, garantindo agora que o valor seja calculado corretamente para a fórmula atual.
ID-227 - Erro no cálculo do excipiente ao repetir venda de cápsula
Resolvemos a falha que ocorria ao duplicar uma venda de cápsula, onde o excipiente era calculado de forma incorreta. Agora o sistema realiza o cálculo com precisão.
ID-177 - Cálculo de dose com produtos de espécies diferentes
Ajustamos o cálculo de dose para casos onde existem produtos com espécies diferentes, evitando resultados inconsistentes.
ID-168 - Quantidade de excipiente calculada (BIOGARDEN)
Corrigimos a quantidade de excipiente que estava sendo calculada de forma errada, garantindo a precisão nos resultados.
ID-120 - Repetição de venda com excipiente errado ao manter cápsula/quantidade anterior
Resolvemos o problema onde, ao repetir uma venda mantendo a cápsula e quantidade anterior, o excipiente era calculado incorretamente.
ID-93 - Quantidade zerada em repetições da forma farmacêutica volume por qtde com cálculo percentual
Corrigimos a falha que resultava em quantidade zerada ao repetir formulações do tipo volume por quantidade com cálculo percentual.
ID-199 - Travamento ao excluir ordem de produção após edição
Corrigimos o problema que causava travamento do sistema ao tentar excluir uma ordem de produção que havia sido previamente editada, garantindo maior estabilidade na operação.
ID-182 - Edição para formas farmacêuticas diferentes de 'Cápsula' (DEHON - ITAPEMA)
Resolvemos o erro que impedia a edição correta de ordens de produção para formas farmacêuticas que não fossem do tipo 'Cápsula', ampliando a flexibilidade do sistema.
ID-181 - Geração de ordens sem itens a partir de Fórmula Padrão
Implementamos correção para evitar a geração de ordens de produção sem itens quando originadas de Fórmula Padrão, garantindo a integridade dos dados.
ID-179 - Ordenação de embalagens e cápsulas (BOTICA ARTESANAL)
Ajustamos a sequência incorreta de exibição de embalagens e cápsulas nas ordens de produção, proporcionando melhor organização visual.
ID-72 - Remoção indevida de lote ao editar ordem (BIOGARDEN)
Corrigimos o problema que causava a remoção acidental do lote da cápsula durante a edição de ordens de produção, preservando as informações importantes.
ID-75 - Corte na impressão de ordens de produção interna
Resolvemos o problema de formatação que fazia com que o último número fosse cortado na im
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Lote não disponivel — 27/03/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/527390
> Publicado em: 27/03/2025

Como Filtrar Lotes Antigos no Sistema
1° Passo: Acessar o Módulo de Lotes
Navegue até:
Estoque → Movimento → Lote
2° Passo: Alterar o Filtro Temporário (365 dias)
Na tela de lotes,
localize o ícone de filtro
na parte inferior:
📄
(papel com seta para baixo)
.
Clique nesse ícone para
ativar o filtro de 365 dias
(isso mostrará lotes do último ano).
3° Passo: Ajustar Filtros  (Parâmetros)
Se o lote desejado for
mais antigo que 365 dias
:
Acesse os
Parâmetros do Sistema
:
Atalho
: Pressione
CTRL + F
(buscar parâmetros)
OU
Navegue manualmente:
Arquivo → Parâmetro → Parâmetro
.
Configure os Filtros:
Abra a aba
Geral → Geral
.
Na seção
"Filtros (em dias)"
, ajuste:
Lote 1°
: Filtro padrão ao abrir o módulo.
Lote 2°
: Filtro ativado pelo botão de papel/seta (ícone do passo 2).

---

## 🟡 Alterar Unidade de Estoque - Manutenção Geral — 26/03/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/527350
> Publicado em: 26/03/2025

Alterar Unidade de Estoque - Manutenção Geral
1. Introdução
1.1 Informações importantes:
Esta tela modifica apenas a unidade de estoque do produto, não alterando a unidade de manipulação cadastrada.
A unidade de estoque e a unidade de manipulação podem ser diferentes, desde sejam da mesma natureza (massa, volume, etc).
Ao realizar a mudança da unidade de estoque, todos os campos relacionados a valor (valor de custo, valor referência, valor de venda, etc...) serão alterados proporcionalmente a conversão da unidade antiga para a nova. Por isso, recomendamos que o cliente tenha anotado os valores corretos para evitar possíveis confusões.
1.2 Qual a utilidade/Quando deve ser utilizada?:
Utilizamos esta tela para alterar a unidade de estoque cadastrada em um produto quando há necessidade, seja por alteração logística da farmácia ou cadastro incorreto através da tela de produtos, notas de entrada, etc.
2. Procedimento
2.1 Caminho para acesso:
Para acessarmos a tela de manutenção geral onde é feito o processo, devemos seguir o caminho indicado abaixo:
Obs: Caso o ícone "Manutenção Geral" não apareça para você, você deve solicitar a abertura de um ticket para um administrador da farmácia solicitando a liberação da permissão para seu usuário.
2.2 Preenchimento das informações necessárias:
Selecione o produto desejado para a alteração.
No campo da esquerda o sistema mostrará a unidade de estoque atual do produto, e no campo a direita, você deve preencher a nova unidade.
2.3 Confirmando a manutenção:
Para minimizar erros, o sistema pedirá uma última confirmação, portanto, confirme as informações inseridas, e se estiver tudo correto, confirme a manutenção.
2.4 Mensagem de êxito:
Caso tenha ocorrido tudo conforme o esperado, você receberá esta mensagem de êxito do sistema.
3. Exemplo prático
3.1 Detalhes do exemplo:
Para facilitar o entendimento, mostraremos o processo sendo feito com o produto "1 11111 - PRODUTO PARA TESTE".
Neste teste, o produto está cadastrado como unidade de estoque em "mg", faremos a alteração para "g".
3.2 Preenchimento das informações necessárias:
Selecionamos o produto, preenchemos o campo com a nova unidade de armazenamento, "g", e clicamos em "Salvar".
3.3 Confirmando a manutenção da unidade do produto:
Após validarmos as informações inseridas, confirmamos a manutenção.
3.4 Mensagem de êxito:
Como tudo estava correto, recebemos a mensagem de êxito.
3.5 Validando alterações:
Para validar o produto com a unidade de armazenamento atualizada, vá ao cadastro do produto seguindo o caminho da imagem abaixo e visualize a nova unidade cadastrada.
4. Conclusão
4.1 Considerações finais:
Após seguir todos os passos deste artigo, você terá alterado a unidade de estoque dos produtos desejados no Farma Fácil.
Caso ainda tenha alguma dúvida, fique a vontade para abrir um ticket através de nossa central de atendimento para que um de nossos analistas entre em contato o mais rápido possível para auxiliá-lo.
Att,
PrismaFive.

---

## 🟡 Inventário — 26/03/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/527303
> Publicado em: 26/03/2025

Inventário
O módulo de inventário tem como objetivo ajustar as quantidades dos produtos da farmácia de forma geral, sem a necessidade de incluir os itens manualmente por meio de acertos no estoque, proporcionando maior agilidade no processo. Um exemplo disso é a finalização do inventário no SNGPC.
1° Passo
Nós vamos em "Estoque -> Movimento -> Inventário"
2° Passo
Selecionamos os grupos que desejamos ajustar, sendo possível escolher mais de um grupo ao mesmo tempo.
Ou, então, podemos selecionar apenas o produto desejado
3° Passo
Após, temos as seguintes opções de filtro:
Mostrar Estoque Negativo
: Exibe os produtos com estoque negativo.
Mostrar Estoque Zerado
: Exibe os produtos com estoque zerado.
Mostrar Controlados
: Exibe os produtos com estoque controlado.
Somente Lotes Vencidos
: Exibe apenas os produtos com lotes vencidos.
Somente Estoque Zerado
: Exibe exclusivamente os produtos com estoque zerado.
Somente Estoque Negativo
: Exibe exclusivamente os produtos com estoque negativo.
No campo "Contagem", inserimos a quantidade desejada para o estoque atual. Por exemplo, no caso abaixo, onde o produto possui uma quantidade de 973 g, ao colocar 0 na contagem, o estoque será zerado.
Após salvar, caso não haja nenhuma inconsistência, o sistema exibirá a mensagem "Inventário realizado com sucesso". Nesse momento, o sistema criará automaticamente um acerto de estoque para ajustar a quantidade do produto conforme informado na coluna "Contagem". Se o produto for controlado, será necessário informar o motivo do acerto de estoque, conforme exigido pelo SNGPC.
Assim que a quantidade desejada for inserida, a tela para informar o motivo do acerto será exibida. Caso isso não aconteça, você pode pressionar a tecla "F2" para que a tela de motivos apareça.
Obs.: Para realizar o inventário, é recomendável concluir as ordens de manipulação ou retirar o ativo antes de iniciar o inventário, pois, se o lote estiver comprometido, não será possível zerar o estoque. O mínimo que pode ser registrado é a quantidade comprometida.
Tela do acerto

---

## 🟡 Tour Pelo Sync — 24/03/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/526664
> Publicado em: 24/03/2025

Tour Pelo Sync
1. INTRODUÇÃO
O Sync é uma plataforma que oferece diversas funcionalidades para o gerenciamento de atendimentos, comunicação e organização interna. A seguir, um resumo das principais funções disponíveis:
2.
DASHBOARD
:
Apresenta um panorama dos atendimentos realizados em períodos selecionados:
semanal, mensal ou anual
.
3.
KANBAN
:
Exibe todos os chamados registrados na plataforma.
Classifica os chamados em
novos, em andamento e finalizados
.
Mostra qual colaborador está atendendo cada chamado em andamento.
4.
CONVERSAS
:
Possui filtros avançados para facilitar a gestão da comunicação.
Filtro por número:
Permite selecionar o número que está recebendo mensagens.
Filtro por colaborador:
Mostra qual chamado está atribuído a cada funcionário.
Pesquisa personalizada:
Filtra por nome do cliente, telefone, atendente e canal de origem (WhatsApp, Instagram, Facebook).
Filtragem por
Tags
:
As
tags
são definidas pelo administrador e podem indicar a prioridade do chamado (ex.: "Crítico", "Urgente").
Mensagens não lidas ou vencidas:
Exibe mensagens que ainda precisam de atenção.
5.
ORÇAMENTO
:
na conversa com o cliente podemos analisar um jeito mais eficiente de enviar o orçamento para o
FarmaFacil
.
6.
E-MAILS
:
Funcionalidade similar a um sistema de e-mails convencional.
Permite selecionar o e-mail do remetente e enviar mensagens diretamente pelo Sync.
O E-mail que irá ser sincronizado tem que ser um E-mail já existente, recomendamos ser
GMAIL
6.
ATENDIMENTOS
:
Exibe os atendimentos em diferentes estados :
em andamento, cancelado ou concluído
.
Possibilita filtragem de atendimentos por nome, telefone, tipo (WhatsApp, e-mail, Instagram, Facebook), status, usuário e motivo (criado via configurações)
7.
ORÇAMENTOS
:
Apresenta todos os orçamentos registrados pelos colaboradores.
Oferece filtros por
data, origem, status (pendente, processando, calculado)
.
Mostra apenas orçamentos lançados via Sync.
8.
RELATÓRIOS
:
Contém diversas análises sobre atendimentos e desempenho dos colaboradores
Pesquisa de satisfação:
Permite verificar o feedback recebido dos clientes.
9.
MONITORAMENTO DE USUÁRIOS CONECTADOS
:
Exibe os horários de login e logout dos colaboradores. Caso o colaborador não tenha se desconectado do Sync, a coluna "Data de Expiração" indicará quando o sistema encerrará a sessão automaticamente.
10.
CLIENTES EM ATENDIMENTOS PROLONGADOS:
Destaca chamados abertos há mais tempo e ainda não finalizado
11.
ORÇAMENTO:
vai precisar inserir o Usuário ou pode filtrar sem Usuário, obrigatório a Data de Início e Data do Fim e a origem que gostaria de analisar, tem como confirmar pelo Status
12.
PESSOAS:
onde irá vincular os cadastros criado dentro do Sync, ou seja, é um banco diferente do
FarmaFacil
, os cadastros do Sync ficaram apenas no S
ync
.
13.
TAGS:
Onde pode ser criada as tags de acordo com a preferencia do cliente
Tags
:
pode ser alterada a cor conforme a sua preferência
14.
MÍDIAS:
Pode ser criado imagens com legendas, como folders promociona
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Integraçao com a Avant Fiscal — 27/02/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/523448
> Publicado em: 27/02/2025

Avant Fiscal: Solução Inteligente para Gestão Tributária em Farmácias
A
Avant Fiscal
é um sistema de controle tributário e inteligência fiscal desenvolvido especialmente para farmácias, garantindo mais segurança e praticidade na gestão fiscal desses estabelecimentos.
A plataforma possibilita a
consulta online
de diversas informações tributárias sobre produtos do varejo farmacêutico,
automatiza a atualização de tributos
no sistema de retaguarda e
realiza auditorias no cadastro de produtos
, identificando e corrigindo eventuais irregularidades fiscais.
Principais benefícios da Avant Fiscal
✅
Agilidade nos processos
– Automatiza a atualização dos tributos, garantindo um melhor controle sobre os impostos e evitando sonegações ou pagamentos em duplicidade.
✅
Consulta online 24h
– Acesso rápido e prático às informações fiscais dos produtos comercializados, facilitando a conferência de dados e esclarecimento de dúvidas.
✅
Auditoria em tempo real
– Monitoramento contínuo do cadastro de produtos, especialmente em relação a impostos federais e estaduais, assegurando conformidade tributária.
✅
Economia de tributos
– Identificação de produtos com impostos já recolhidos pelo fornecedor, evitando pagamentos desnecessários e gerando economia para a farmácia.
Atualmente, a Avant Fiscal já atende
mais de 500 empresas
, consolidando-se como uma solução eficiente e confiável no mercado farmacêutico. Para farmácias que desejam otimizar a gestão tributária e financeira, essa ferramenta representa um investimento estratégico, garantindo
segurança, economia e eficiência
nos processos fiscais.
Integração com Avant Fiscal: Passo a Passo
Com a integração da Avant Fiscal,
não é necessário alterar manualmente o cadastro do produto na aba tributação
. Todo o processo ocorre de forma automatizada, seguindo os dados fornecidos pela plataforma.
1) Configuração Inicial
Para ativar a integração, a farmácia deve fornecer:
🔹
Token
🔹
Cliente ID
Ambos devem ser informados na aba
Integração Fiscal
dentro do
Parâmetro
do sistema.
2) Atualização da Tributação
A tributação dos produtos pode ser atualizada de duas formas:
🔹
Atualização em Massa
Acesse a aba
Avant Fiscal
dentro do cadastro de produtos.
Selecione os filtros desejados para a atualização.
Clique em
Pesquisar
.
Para iniciar a atualização, clique em
Webservice
.
📌 O campo obrigatório é o codigo de barra no produto, este tem que estar preenchido para fazer a integração com a Avant Fiscal.
📌    O processo pode ser demorado, dependendo da quantidade de produtos e filtros aplicados.
🔹
Atualização Individual do Produto
Acesse o cadastro do produto específico.
Vá até a aba
Avant Fiscal
.
Consulte e atualize as informações tributárias conforme necessário.
Com esse processo,
toda a tributação do produto será automaticamente ajustada conforme os dados da Avant Fiscal
, garantindo maior precisão e conformidade fiscal.

---

## 🟡 FLORAL - VISÃO GERAL NO SISTEMA — 27/02/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/523354
> Publicado em: 27/02/2025

FLORAL - VISÃO GERAL NO SISTEMA
Os florais na prática farmacêutica fazem parte das terapias complementares e são utilizados para auxiliar no equilíbrio emocional dos pacientes. Eles são preparados a partir de essências florais diluídas em solução hidroalcoólica e são indicados com base nos estados emocionais do indivíduo.
Benefícios do Uso de Florais na Farmácia
Promovem o bem-estar emocional sem efeitos colaterais significativos.
São seguros e podem ser usados por qualquer faixa etária.
Possuem um custo acessível em comparação com outras terapias.
No sistema
FarmaFácil,
o primeiro passo é criar uma
forma farmacêutica
. Os campos mais importantes a serem preenchidos estão destacados abaixo:
Tipo:
define o método de cálculo que o sistema utilizará na forma farmacêutica, marcar como "floral"
Veículo:
define um veículo padrão para ser utilizado em florais (pode ser definido também no parâmetro geral, em
arquivo > parâmetro > parâmetro > manipulação > geral > veículo padrão
).
ML:
forma o cálculo da quantidade pesada. A prescrição de floral é sempre em gotas, então convertendo na forma farmacêutica também dará a quantidade em ml utilizada. Caso não seja preenchido, a "quantidade pesada" sairá zerada na ordem de manipulação, apenas com a quantidade de gotas).
Outros campos na forma farmacêutica podem ser marcados, dependendo da necessidade da farmácia, como por exemplo "Manter valor da tabela", que será explicado posteriormente.
O
cadastro de produto floral
deve ser feito em um grupo do
tipo floral,
e seguir o seguinte padrão nos campos destacados:
Para realizar a venda de florais, selecionaremos na venda como "homeopatia". Atenção, a forma farmacêutica continua sendo de florais, a aba "homeopatia" é apenas para indicar que é um cálculo diferente a ser utilizado.
Caso tente realizar a venda como "manipulação", o sistema irá bloquear a operação com a seguinte mensagem:
Na venda, será preenchido o volume do floral, os ativos e a quantidade de gotas prescrita. Neste momento, voltamos a questão comentada anteriormente de "MANTER VALOR DA TABELA".
Normalmente, o floral é cobrado pela quantidade de gotas utilizadas na manipulação. O sistema possui a "tabela floral", disponível em:
arquivo > venda > tabela floral.
Nesta tabela, definimos o volume a ser produzido (normalmente, é padronizado o volume), e o valor que irei cobrar no intervalo de gotas. No exemplo abaixo, quando tiver uma venda de 10ml de floral e utilizar entre 7 e 8 gotas na formulação, irei ter o valor de venda
total
de R$20,00.
O parâmetro "considerar valor tabela" na forma farmacêutica irá implicar no seguinte: caso esteja marcado, será vendido exatamente pelo valor que está na tabela. Não irá considerar embalagem, veículo, valor de forma farmacêutica, etc. Caso esteja desmarcado, o sistema fará o cálculo automático do valor da venda (considerando a quantidade em ml utilizada do produto, embalagem, veículo, etc). Repare nos exemplos abaixo:
Caso eu selecione uma quantidade de gotas que não e
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Gestão de Entrega - visão geral alterado — 26/02/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/523251
> Publicado em: 26/02/2025

A gestão de entregas é uma parte crucial do processo de vendas e logística, a
fim de garantir que suas operações sejam eficientes e transparentes. Com o
módulo “Gestão de entregas”, é possível acompanhar o status de cada venda,
desde o momento em que o pedido é recebido até o momento em que o produto
é entregue ao cliente. Essa visibilidade em tempo real ajuda a identificar
eventuais atrasos ou problemas e permite que a equipe tome medidas corretivas,
além de identificar áreas que precisam de melhorias.
1. CADASTROS INICIAIS
Para que possamos iniciar o uso da gestão de entrega, é importante adequarmos
o sistema farmafácil da maneira que torne mais eficiente o processo.
1.1Região: ARQUIVO > VENDA > REGIÃO
Ao incluirmos uma nova região, podemos parametrizar: o valor de entrega
padrão para a região, os dias e horários que há disponibilidade de entrega e,
caso exista, um entregador determinado para aquela região.
1.2. Entregador: ARQUIVO > VENDA > ENTREGADOR
No cadastro do entregador, podemos selecionar para quais regiões o mesmo
fará entregas, além dos dados cadastrais do mesmo:
1.3
Endereço do cliente
No cadastro do cliente, podemos incluir quantos endereços de entrega forem
necessários. Podemos ter um para o trabalho, para casa, para casa de outra
pessoa, etc.
Para que a taxa de entrega seja realizada corretamente, precisamos selecionar
no endereço a região de entrega que se localiza.
2.
VENDA
Ao invés de selecionarmos um local de entrega dentro da venda, gerando
imposto sobre a entrega, iremos selecionar o menu de romaneio de entrega
destacado abaixo:
3. ROMANEIO DE ENTREGA
Para cada romaneio de entrega, é possível adicionar uma ou mais vendas. Para
verificar quais estão selecionadas, é a parte destacada em vermelho:
Para adicionar mais vendas ao romaneio, clicamos no ícone no canto inferior
direito da tela, em azul.
Em cada venda, podemos notar que conseguimos selecionar os pr
odutos que
serão entregues (pode acontecer do cliente querer um produto entregue em
cada endereço, será explicado posteriormente como fazer) destacado em
verde.
3.1 Endereço para entrega
Podemos observar que os endereços cadastrados no item 1.3 estão presentes
no romaneio de entrega. Para selecionar qual item será entrego para qual
endereço, utilizamos os botões do meio destacados em azul.
Aqui, selecionamos o endereço trabalho do cliente Consumidor e atribui todos os
itens para o mesmo endereço. Podemos notas o número da venda também.
É importante lembrar que se adicionarmos vendas de clientes diferentes,
precisamos ficar atentos ao endereço que selecionamos a entrega.
Botões
3.2 Forma de pagamento
Após vincular todos os itens da venda a um endereço de entrega, determinar a
forma de pagamento, podemos imprimir o romaneio de entrega:
A taxa de entrega é determinada pela região, no romaneio conseguimos
visualizar o endereço de entrega, o entregador determinado para aquela região,
a forma de pagamento, contato do cliente (caso tenha cadastrado) e informações
sobre a venda.
A
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Notas de Versão 20.01.88.23 do FarmaFácil Desktop — 17/02/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/521764
> Publicado em: 17/02/2025

Notas da versão 20.01.88.22 do Farma Fácil Desktop
🗓 Data de lançamento: 17/02/2025
📌 Descrição da versão: Esta nova versão do Farma Fácil Desktop traz diversas melhorias e correções voltadas para a otimização do sistema, aprimoramento de funcionalidades e resolução de problemas. Confira os principais destaques:
🛠
Correções de defeitos:
#10664 - Seleção de excipientes na venda (APOTHEKA)
Ajustado o sistema para permitir a seleção correta de excipientes quando há mais de um vinculado ao produto na venda.
#10646 - Erro ao enviar orçamento/Sync (FARMATEC)
Corrigido o erro que impedia o envio de orçamentos e a sincronização de dados no FarmaFácil, garantindo que o processo ocorra sem interrupções.
ChatGPT said:
#10631 - Tributação PIS, COFINS e FCP em NFCe (Seiva Natural)
Ajustada a tributação para que os valores de PIS, COFINS e FCP sejam corretamente exibidos nas notas NFCe.
#10617 - Erro ao enviar orçamento calculado (PH24 - TODOS)
Corrigido o problema que impedia o envio de orçamentos calculados, afetando todos os clientes que utilizam o PH24.
#10615 - Importação e repetição de venda de pré-venda (TODOS)
Revisado o fluxo de importação e repetição de vendas provenientes de pré-venda, garantindo maior consistência nas informações.
#10606 - Exibição de excipiente ao converter orçamento em venda (TODOS)
Ajustado para que o excipiente vinculado ao produto seja exibido corretamente ao converter o orçamento em venda.
#10605 - Cálculo de excipiente em repetição de venda (BIOGARDEN)
Corrigido o cálculo incorreto do excipiente ao transformar orçamento em venda após repetir uma venda.
#10602 - Código de verificação na nota impressa (UP VET - BELO HORIZONTE)
Ajustado o sistema para que o código de verificação apareça corretamente na nota impressa para o provedor BHISS.
#10601 - Cálculo de excipiente em cápsulas (BIOGARDEN)
Corrigido para que o valor do excipiente seja considerado corretamente no total da venda para formas farmacêuticas do tipo cápsula.
#10600 - Cápsulas sem excipiente (FARMABIN)
Ajustado o comportamento para que formas de cápsulas não utilizem o excipiente quando configurado para desconsiderá-lo.
#10589 - Alteração de lote em modo de visualização (TODOS)
Corrigido o problema que permitia alterar o lote mesmo em modo de visualização. Agora, as alterações só são permitidas em modo de edição.
#10584 - Cálculo de custos em entrada de notas (Manutenção Importação de NFe)
Ajustado o cálculo de custos na entrada de notas quando há apenas um item na nota, garantindo maior precisão nos valores.
#10566 - Divergência de valor entre tela de fórmula e venda (TODOS)
Corrigida a divergência de valores exibidos ao repetir uma venda, mantendo a consistência entre a tela de fórmula e a tela de venda.
#10552 - Impressão de Ordem de Produção interna (Ordem Manipulação)
Ajustado o layout de impressão para que o último número da Ordem de Produção não seja cortado.
🚀
Implementação de melhorias:
1.
#10665 - Indicador de operação para NFe de devolução.
Implementada 
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 CBENEF - CÓDIGO DE BENEFÍCIO FISCAL — 31/01/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/519359
> Publicado em: 31/01/2025

O Código de Benefício Fiscal
é obrigatório em alguns estados brasileiros desde 2019,
e outras Unidades Federativas (UF) estudam a viabilidade de implementação do campo nos documentos fiscais eletrônicos.
O Código de Benefício Fiscal – conhecido pela sigla cBenef – é um campo utilizado na Nota Fiscal eletrônica (NF-e) e na Nota Fiscal de Consumidor eletrônica (NFC-e), para indicar que há
incentivos fiscais
naquela operação.
O termo
incentivo fiscal
é utilizado para indicar que as empresas receberam alguns benefícios fiscais, como carga tributária menor por determinado período ou diminuição, e até isenção de alguns impostos. Essas
medidas são criadas pelo Governo Federal ou Estadual para beneficiar
alguns setores ou regiões, como contrapartida, à geração de postos de trabalho e renda, por exemplo.
Atualmente,
os estados que exigem o preenchimento da tag
nos documentos fiscais eletrônicos são:
Distrito Federal, Goiás, Paraná, Rio Grande do Sul, Rio de Janeiro e Santa Catarina
.
O sistema Farma Fácil ja esta adequado(Versão
20.01.88.12 em diante
) a emissão do XML com a TAG CNBEF, para alimentar no sistema, você deve ir no cadastro do produto, ir na aba Tributação, e procurar o campo CODIGO DE BENEFICIO FISCAL
Outro detalhe, o sistema também tem o campo para ser informado dentro da nota fiscal para casos aonde precise informar um CBENEF diferente por causa do CFOP, para isso é só ir no modulo de Nota fiscal, informar os dados da nota, e na hora de inserir o item informar o codigo no campo COD. BENEFICIO.

---

## 🟡 CFOP 5102 - Venda de mercadoria adquirida ou recebida de terceiros — 31/01/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/519355
> Publicado em: 31/01/2025

CLIENTE, FAVOR VERIFICAR ANTES COM A CONTABILIDADE PARA QUE NÃO SEJAM COMETIDOS ERROS COM TRIBUTAÇÕES, O QUE PODERIA IMPLICAR MULTAS DOS ÓRGÃOS FISCALIZADORES CASO SEJAM UTILIZADAS INCORRETAMENTE.
Deixo a seguir o processo de troca de TRIBUTAÇÕES para grupos inteiros no sistema Farmafacil.
1. Utilizando o comando CTRL+F, abra a pesquisa por módulos e digite "MANUTENÇÃO GERAL" para acessar as opções.
2. No menu de Manutenção Geral, selecione a opção "ALTERAR TRIBUTAÇÃO DE GRUPOS".
3.  Clique na lupa para adicionar os grupos para troca.
4. Após selecionar quais grupos deseja alterar, basta sair da tela, e eles serão incluídos no campo de troca.
Selecione qual mudança deseja fazer na tributação do grupo inteiro.
A alteração pode ser feita individualmente ou em mais de uma opção, a critério do usuário.
5. Coloque a informação correta no campo desejado que será alterado.
Neste caso estou utilizando somente a opção CFOP sendo ela trocada para a Natureza
CFOP 5102 - Venda de mercadoria adquirida ou recebida de terceiros
6. Após as informações estarem confirmadas e validadas, basta clicar em salvar e confirmar para que o sistema inicie a mudança em todos os produtos do grupo selecionado.
Pronto, suas informações de tributação serão aplicadas a todos os produtos cadastrados no grupo selecionado.
E, NOVAMENTE, sempre consulte a sua contabilidade para que não ocorram situações ou problemas com os órgãos fiscalizadores.

---

## 🟡 SNGPC — 30/01/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/519106
> Publicado em: 30/01/2025

Sistema Nacional de Gerenciamento de Produtos Controlados (SNGPC)
O
Sistema Nacional de Gerenciamento de Produtos Controlados (SNGPC)
é um sistema desenvolvido pela
Agência Nacional de Vigilância Sanitária (ANVISA)
com o objetivo de monitorar a comercialização de medicamentos sujeitos a controle especial em farmácias e drogarias.
O que é o SNGPC?
O SNGPC é uma plataforma eletrônica que permite o envio de informações sobre a movimentação de medicamentos controlados de forma segura e eficiente. Ele é fundamental para garantir a rastreabilidade e evitar desvios ou uso indevido dessas substâncias.
Objetivos do SNGPC
Monitorar e controlar a dispensação de medicamentos sujeitos a controle especial.
Garantir a segurança do paciente e evitar o uso irregular de substâncias controladas.
Facilitar a fiscalização por órgãos reguladores.
Reduzir a burocracia e agilizar o processo de controle de medicamentos.
Quem deve utilizar o SNGPC?
Todas as
farmácias e drogarias privadas
que comercializam medicamentos sujeitos a controle especial devem obrigatoriamente aderir ao SNGPC. Unidades de saúde pública e farmácias hospitalares não são obrigadas a utilizar o sistema, pois possuem regulação diferenciada.
Como funciona o SNGPC?
O funcionamento do SNGPC é baseado no envio de informações eletrônicas para a ANVISA. O processo envolve:
Cadastro no SNGPC
– A farmácia ou drogaria deve possuir um Responsável Técnico (RT) cadastrado no sistema da ANVISA.
Registro de Movimentação de Produtos
– Todos os medicamentos controlados devem ser registrados no sistema, incluindo entradas (compras) e saídas (vendas ou perdas).
Envio Periódico de Arquivos XML
– As informações devem ser enviadas eletronicamente em formato XML para a ANVISA dentro dos prazos estipulados.
Regularização e Correção de Erros
– Caso haja inconsistências, o sistema permite a correção e reenvio dos arquivos.
Benefícios do SNGPC
Redução de erros
– Automatiza o controle e minimiza falhas no registro de medicamentos.
Maior segurança
– Garante o rastreamento eficaz de medicamentos controlados.
Facilidade de fiscalização
– Simplifica o trabalho dos órgãos de saúde pública.
Transparência e conformidade
– Mantém a farmácia em conformidade com as normas sanitárias.
Consequências do Não Cumprimento
Farmácias e drogarias que não aderirem ao SNGPC ou que enviarem informações incorretas estão sujeitas a penalidades, como:
Multas administrativas.
Suspensão do alvará sanitário.
Interdição do estabelecimento.
SNGPC no FarmaFácil
No sistema
FarmaFácil
, existem duas maneiras de fazer o envio das movimentações para o SNGPC:
Envio Automático via Webservice
– Até a data deste artigo (31/01/2024), essa funcionalidade ainda não foi reativada.
Envio Manual
– Para realizar o envio manual, consulte o artigo detalhado com imagens explicativas no seguinte link:
Exportação Manual SNGPC.
IMPORTANTE:
Antes de realizar qualquer ação para envio do SNGPC, é importante revisar alguns dados:
- Cadastro dos produtos controlados.
- Usuário e senh
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Erro na Emissão de Notas Fiscais (NF-e e NFS-e) devido a Caracteres Especiais — 29/01/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/518828
> Publicado em: 29/01/2025

Erro na Emissão de Notas Fiscais (NF-e e NFS-e) devido a Caracteres Especiais
Antes de qualquer ajuste nos dados,
valide se o certificado digital não está vencido ou com alguma inconsistência
, pois isso também pode impedir o envio da nota.
Identificamos que a presença de caracteres especiais em determinados campos pode causar falhas na assinatura digital e impedir o envio da nota fiscal.
Exemplo 1 – NFSe
Mensagem de erro:
"Não foi possível enviar NFSe!
00222 - Assinatura Digital não está íntegra ou nenhuma assinatura foi encontrada no arquivo enviado. @Assinatura não integra! Falha na verificação."
Causa:
O nome do cliente continha caracteres especiais.
Solução:
Removemos os caracteres e a nota foi enviada com sucesso.
🔹
Exemplo:
Antes:
PINÉRO
Depois:
PINERO
Exemplo 2 – NFe
Mensagem de erro:
*"Não foi possível exportar dados para arquivo NFe.
<Erro>         <Codigo>405</Codigo>         <Descricao>Assinatura Digital Inválida. Assinatura Inválida</Descricao>     </Erro>"*
Mensagem: "Não foi possível exportar dados para arquivo NFE
<Erro>
< Codigo>405 </Codigo>]
<Descricao>Assinatura Digital Invalida Assinatura Invalida> Descriao>
<Erro>
Causa:
O bairro e a cidade continham caracteres especiais.
Solução:
Ajustamos o nome do Bairro que continha os caracteres especiais e a nota foi emitida corretamente.
🔹
Exemplo:
Alteração no XML para remover caracteres especiais do Bairro.
Antes: Caixa DÀ 'Agua
Depois: Caixa da Agua

---

## 🟡 ASSOCIAÇÃO DE PRODUTOS — 22/01/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/517631
> Publicado em: 22/01/2025

ASSOCIAÇÃO DE PRODUTOS
A associação de matérias-primas refere-se à combinação de dois ou mais princípios ativos ou excipientes em uma formulação, com o objetivo de potencializar os efeitos terapêuticos, reduzir efeitos colaterais ou melhorar características farmacotécnicas, como estabilidade, sabor ou absorção. Essa prática é amplamente utilizada no desenvolvimento de medicamentos, garantindo que os componentes sejam compatíveis e seguros para o uso em conjunto.
No sistema FarmaFácil, esta associação pode ser feita no cadastro do produto, na aba "complemento".
Podemos definir a associação dos produtos considerando a forma farmacêutica a ser utilizada, e definindo o produto a ser associado:
Em relação ao tipo de cálculo, podemos escolher o melhor cálculo baseado na necessidade da farmácia:
somente ativo (percentual):
faz o cálculo do produto associado de forma percentual, baseando-se na quantidade pesada do ativo principal.
Configuração no produto:
Ordem de produção:
(quantidade do produto principal 0,3g, 10% de ativo associado = 0,003g
Se o tipo de cálculo utilizado na forma farmacêutica for de
volume
(por exemplo, sachês), ainda podemos definir uma associação por faixa de ativo utilizado. No exemplo abaixo, em uma venda de sachês, foi parametrizado que se o produto principal compor entre 50% a 80% do volume total do sachê, também terei 10% do produto associado.
ativo +  excipiente
(para cápsulas)
/ ativo + qsp
(para saches, cremes, etc)
:
utilizado quando preciso utilizar o produto associado baseado na quantidade total da fórmula a ser manipulada.
Configuração no produto
Ativo + excipiente
Ativo + QSP
somente ativo (quantidade):
quando uso o produto principal, obrigatoriamente vou usar a quantidade de ativo do associado, independente da prescrição do ativo principal.
Configuração do produto
Atenção: o cálculo do produto associado (somente quantidade), utiliza a prescrição em gramas. No exemplo acima, está configurando que estou usando 0,3g por cápsula.

---

## 🟡 ORÇAMENTO REJEITADO — 14/01/2025

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/515489
> Publicado em: 14/01/2025

ORÇAMENTO REJEITADO
Rastrear os motivos pelos quais um cliente rejeita um orçamento é uma prática essencial para qualquer empresa que busca melhorar seus processos e conquistar resultados mais eficazes. Esse registro permite identificar padrões de recusas, entender melhor as necessidades dos clientes e ajustar propostas futuras para atender às expectativas do mercado. Além disso, ter essas informações documentadas ajuda a aprimorar estratégias de negociação, ajustar preços, serviços ou produtos oferecidos, e, sobretudo, minimizar erros ou desalinhamentos. Ao investir nesse tipo de análise, a empresa se torna mais competitiva e preparada para atender de forma assertiva às demandas do público-alvo.
1.
CADASTRO DE JUSTIFICATIVAS
Inicialmente, iremos cadastrar as justificativas mais comuns para o cancelamento, e iremos resumir de forma breve o motivo. Acesse
ARQUIVO > VENDA > TIPO JUSTIFICATIVA
e cadastre os mais adequados para sua farmácia.
2. ORÇAMENTOS
No momento em que um orçamento é criado, ele é considerado automaticamente como “rejeitado”. No momento que ele for aprovado e convertido em venda, ele deixa de ser rejeitado.
3. ORÇAMENTOS REJEITADOS
Para justificarmos o motivo do orçamento rejeitado, acesso o módulo
VENDA > MOVIMENTO > ORÇAMENTOS REJEITADOS.
Você pode procurar o orçamento rejeitado por cliente, período de tempo, número específico, vendedor ou origem:
Após encontrar o orçamento que foi rejeitado, você deverá selecionar o
checkbox
destacado e editá-lo (botão editar ou tecla “J”) para inserir a justificativa. Informando o tipo, você também pode escrever de forma detalhada o motivo da rejeição, explicando o que ocorreu.
Caso este cliente tenha mudado de ideia, você só conseguirá utilizar o mesmo orçamento se for até a tela anterior e excluir a justificativa. Caso contrário, a seguinte mensagem aparecerá:
Para excluir a rejeição, selecione o
checkbox
e exclua a justificativa.
3. RELATÓRIO
O relatório de orçamentos rejeitados poderá ser filtrado por vendedor, médico, forma farmacêutica, produto, visitador, justificativa ou tipo justificativa, dependendo do objetivo da farmácia.
Exemplos:

---

## 🟡 Etiqueta de Preço - Acabado e Drogaria — 17/12/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/511705
> Publicado em: 17/12/2024

1) Etiqueta de preço de produto acabado
Entrar no
Arquivo\Produção\Etiqueta.
1. Passo:
Cria uma nova
etiqueta com a informação de acabado e informa os tamanhos correspondentes a etiqueta. Conforme imagem abaixo.
Os campos da Etiqueta tem que ser descrito dessa forma.
Descricao
Preco
2. Passo: Entra em
Arquivo\Parametro\Configurações Prismafive
e inseri a chave
Etiquetapreço.
3. Passo: Entra em
Arquivo\Produto\Relatorio.
Para inserir o produto acabado aperte o F2 que ira abrir a tela de pesquisa produto.
Observação:
não esquecer de colocar a quantidade de etiquetas que serão impressas.
2) Etiqueta de preço de produto Drogaria
Segue o mesmo processo de criação de etiquetas, lembrando que tem um artigo que identifica os campos para Drogaria.
CHAVES DE REGISTRO
NOME DA CHAVE
FUNÇÃO
PRECO
Informa o Preço do cadastro do produto.
CODIGOBARRAS
Informa o Código de barras do produto
DESCRICAOPRODUTO
Informa a descrição do produto Abreviado.
DESCRICAO2
Informa a Descrição do produto completo.
Segue o passo 2 e 3 descrito acima.

---

## 🟡 Notas de Versão 20.01.88.22 do FarmaFácil Desktop — 05/12/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/509565
> Publicado em: 05/12/2024

Notas da versão 20.01.88.22 do Farma Fácil Desktop
🗓 Data de lançamento: 05/12/2024
📌 Descrição da versão: Esta nova versão do Farma Fácil Desktop traz diversas melhorias e correções voltadas para a otimização do sistema, aprimoramento de funcionalidades e resolução de problemas. Confira os principais destaques:
🛠
Correções de defeitos:
1. #10573 - Erro no cálculo da quantidade de cápsulas e na quantidade pesada do Excipiente - TODOS:
Corrigido o cálculo incorreto das quantidades em fórmulas de cápsulas, garantindo precisão nos resultados e maior confiabilidade.
2. #10565 - Valor do excipiente cobrado duas vezes em fórmulas de cápsulas (Movimento Fórmula Venda) - ESSENZ:
Resolvido problema que duplicava a cobrança de excipientes, assegurando exatidão nos custos.
3. #10563 - Erro no cálculo da quantidade pesada na Ordem de Produção quando a quarentena está habilitada - TODOS:
Ajustado o cálculo da quantidade pesada de ativos e excipientes, eliminando inconsistências em ordens de produção.
4. #10561 - O sistema está exibindo um valor diferente na tela de fórmula e na tela de venda ao converter um orçamento em venda com desconto aplicado - TODOS:
Corrigido o cálculo para assegurar que os valores exibidos na tela de fórmula sejam consistentes com os apresentados na tela de venda após a conversão de um orçamento com desconto aplicado.
5. #10551 - Divergência de desconto ao transformar um orçamento em venda quando o desconto esta vinculado a um convênio (Manutenção Venda) - FLORACELL - MATRIZ:
Ajustada a aplicação de descontos para garantir o cumprimento das regras de convênio, eliminando discrepâncias ao transformar orçamentos em vendas.
6. #10548 - Dados da PH24 não são imputados no sistema quando não tem vendedor vinculado ao usuário - ARBORETUM x PH24:
Implementado suporte para que os dados do PH24 sejam processados corretamente, mesmo quando não há vendedor vinculado ao usuário, ampliando a flexibilidade do sistema.
7. #10547 - NFS-e de Novo Hamburgo não exibe a descrição dos serviços - FÓRMULA ANIMAL NOVO HAMBURGO:
Resolvido o problema que impedia a exibição da descrição dos serviços nas notas fiscais emitidas, garantindo conformidade e clareza.
8. #10545 - Não está permitindo diminuir a quantidades de cápsulas manualmente no adicional, quando há dobra de cápsula - BELZ VET:
Corrigido o erro que bloqueava a redução manual da quantidade de cápsulas em adicionais com dobra, assegurando maior flexibilidade nas configurações.
9. #10540 - Troca de embalagem já salva na venda - VIVA FARMÁCIA:
Corrigido o sistema para garantir que alterações manuais realizadas em embalagens durante o orçamento sejam mantidas ao convertê-lo em venda, evitando inconsistências no registro.
10. #10536 - Recebimentos saindo com a informação diferente da usada anteriormente - POPULAR de TAQUARI:
Ajustado o sistema para exibir valores recebidos via formas de pagamento a prazo ou convênio como crédito em loja, garantindo consistência nos registros.
11. #10528 - Vendas a prazo r
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Configuração do modulo de setor (PREVISÃO DE ENTREGA) — 29/11/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/508521
> Publicado em: 29/11/2024

Aqui poderemos controlar melhor o nosso fluxo de previsões de horários, ter uma visibilidade da nossa ocupação na produção e ainda controlar as previsões conforme os dias da semana.
Abaixo explicarei como devemos cadastrar e quais informações podemos preencher. Será demonstrado também como funciona na prática.
Observação importante: Caso deseje utilizar as previsões de entrega no formato anterior, basta não cadastrar/utilizar essa funcionalidade.
1° Realizar os cadastros dos horários:
Ao abrir ira demonstrar essa tela, onde podemos gerenciar a inclusão, edição e exclusão dos cadastros utilizados:
Ao incluir, teremos as seguintes informações para preencher:
Tempo mínimo:
devemos preencher nesse campo o tempo previsto que leva para realizar a produção da formula, se baseando no horario de funcionamento do laboratorio.  Assim sendo considerado para selecionar um horário no momento da formulação
Formas farmacêuticas:
Informamos quais formas farmacêuticas que irá participar desse setor.
Agendamento produção:
Esse campo será preenchido de forma automática ao informar os dias da semana e os horários de produção e intervalo. Após preenchimento, apenas informamos qual a quantidade de produção em cada faixa de horário (iremos ver a seguir um exemplo)
Como de exemplo, informei que o meu setor de cápsula é produzido nas segundas e quintas-feiras onde começo a produção a partir das 08:00 horas e o término às 18:00 horas, com um tempo de intervalo entre si de 4:00 horas e o meu tempo mínimo de 4:00 horas também. Após inclusão, informamos a quantidade de produção em cada intervalo, feito isso a forma farmacêutica já irá atender esses horários especificamente:
2° Funcionamento na tela de formulação:
Ao informar a forma farmacêutica, o sistema irá selecionar automaticamente o próximo horário disponível e o campo será bloqueado para edição direta (mas fique tranquilo, será possível editar esse horário).
Para acessar o painel de horários, clicamos na "lupa" ao lado
Clicando na lupa, teremos as seguintes informações:
Checar agendamento
: Aqui que poderemos mudar o horário de previsão da entrega, podendo alterar o horário e também a data da formulação.
Consultar período:
Podemos filtrar datas futuras (ou passadas) para ver como está o nosso setor de produção. Esse filtro foi fixado em 7 dias
Data, Dia, Horário Inicial/Final e Capacidade do período: Informações que realizamos no cadastro
A produzir e Status:
Aqui teremos a informação de quantas ordens de produção foram criadas para esse horário e sua taxa de ocupação
Como de exemplo, para alterar o horário da formulação devemos alterar as informações no campo checar agendamento e após isto realizar a busca, feito isso já irá mudar e precisamos apenas salvar:
Mantive o horário daquela formulação para as 08:00 Horas e realizei a criação da Ordem de produção, ao criar uma nova formulação podemos ver que a nossa taxa de ocupação está em 100% e com isso o sistema já sugeriu o próximo horário
Observação: Não tem restrição d
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Como cancelar uma venda no Farma Facil — 29/11/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/508505
> Publicado em: 29/11/2024

Em qualquer transação comercial, tanto para o vendedor quanto para o comprador, imprevistos podem surgir e a necessidade de cancelar uma venda pode se tornar uma realidade. Seja por erro no processamento, arrependimento por parte do cliente, ou mesmo questões administrativas, é fundamental saber os passos e as implicações desse processo. Neste artigo, abordaremos de maneira clara e objetiva como realizar o cancelamento de uma venda de forma eficiente.
No painel principal de venda, você deve selecionar a venda em questão a qual deseja efetuar o cancelamento, e então irá clicar no ícone de cancelamento, conforme imagem abaixo:
Caso seja uma venda de manipulação, e possua a ordem de produção o sistema irá fazer a seguinte pergunta:
Ao clicar em Sim, a venda será cancelada e a ordem de manipulação será excluída, com isso os estoques que estavam comprometidos, voltam a ficar disponíveis no estoque do sistema, o aconselhável então é que clique em Sim somente se o laboratório ainda não produziu a ordem em questão, mantendo dessa forma o estoque físico o mesmo do estoque no sistema.
Ao clicar em Não, apenas a venda será cancelada e a ordem seguirá ativa no sistema, logo os estoques que estão comprometidos junto a ordem de manipulação permanecem.
Após o procedimento ser realizado, no painel principal das vendas, a venda seguirá em exibição, porém o seu status irá mudar para Cancelada:

---

## 🟡 ENTRADA DE NFe - ALTERAR FORNECEDOR — 21/11/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/506978
> Publicado em: 21/11/2024

OS PASSOS INDICADOS NESTE ARTIGO SERVEM PARA CORRIGIR UMA NFe DE ENTRADA, ONDE JÁ NÃO É MAIS POSSÍVEL FAZER A EXCLUSÃO DA MESMA
ATENDE OS CASOS DE ERRO DE FORNECEDOR OU NUMERAÇÃO INDICADOS NA ENTRADA
IR AO MENU PESQUISAR MÓDULOS, CLICANDO NA LUPA INDICADA NA IMAGEM OU UTILIZANDO O ATALHO CTRL F
PESQUISAR POR "MANUTENÇÃO GERAL"
DENTRO DA MANUTENÇÃO GERAL, SIGA OS PASSOS INDICADOS NA IMAGEM
OBS: ATENTAR-SE A SEQUENCÊNCIA DOS PASSOS

---

## 🟡 Link de Pagamento do Sync - Paylink — 21/11/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/506973
> Publicado em: 21/11/2024

Link de Pagamento do Sync - Paylink
Cadastro e Acesso ao Sistema Paylink
O cliente precisa realizar o cadastro na plataforma
Paylink
, onde será necessário criar um
usuário
e uma
senha
para acessar o sistema.
Após o cadastro ser habilitado, o atendente da
Prismafive
deverá acessar o
Portal Prismafive
para configurar as informações do pagamento.
Configuração no Portal Prismafive
Acesse a seção de
Pagamento
no Portal.
Insira as seguintes informações:
Nome da Empresa
CNPJ
Usuário e senha
do Paylink
Integradora
O cliente pode optar se deseja ativar a segurança (
Safe Checkout
).
Sync do Cliente e Emissão de Link de Pagamento
Para garantir que o processo funcione corretamente, é essencial que os dados do cliente estejam atualizados. Utilize o
link de cadastro
para sincronizar as informações com o sistema
Farmafácil
e atualizar os dados no
Sync
.
Localize o cliente no
Sync
onde será gerado o link de pagamento.
Clique no ícone de "Cifrão" no canto inferior direito.
Preenchimento das Informações
Na tela que será exibida, insira os seguintes dados:
Nome do cliente
Documento
(RG ou CPF)
E-mail
Valor
Orçamento
Seleção do Orçamento
Selecione o orçamento correspondente. O sistema automaticamente preencherá o valor e o orçamento associados. Caso seja necessário incluir o valor de entrega, ajuste manualmente o valor antes de gerar o link de pagamento.
Envio e Validação do Link
Após confirmar as informações, o link será gerado.
Envie o link ao cliente através da conversa.
Caso deseje validar o link, copie-o e abra-o em um navegador.

---

## 🟡 CONTROLE DE RECLAMAÇÕES — 08/11/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/505346
> Publicado em: 08/11/2024

COMO INCLUIR E GERENCIAR O CONTROLE DE RECLAMAÇÕES DA SUA FARMÁCIA
Manter um gerenciamento eficiente dos controles de reclamação é essencial para o sucesso de uma farmácia. Esse processo permite que a farmácia identifique e resolva rapidamente problemas que podem impactar a satisfação dos clientes e a qualidade dos serviços prestados. Ao dar atenção às reclamações, a farmácia demonstra compromisso com a melhoria contínua e com a experiência do cliente, fortalecendo a confiança e a fidelização. Além disso, o monitoramento de reclamações auxilia na detecção de falhas operacionais que prejudicam a eficiência e a produtividade, promovendo ajustes que elevam o padrão de atendimento e tornam a farmácia mais competitiva e confiável no mercado.
No sistema FarmaFácil, você pode acessar este módulo pelo seguinte caminho:
VENDA > MOVIMENTO > CONTROLE DE RECLAMAÇÕES
A tela principal irá nos mostrar o número da venda, o cliente e o responsável por administrar as reclamações de acordo com o processo da farmácia. Podemos visualizar também o status da reclamação (aberto, em processo ou finalizado). Utilize os atalhos abaixo para incluir, excluir, pesquisar, visualizar ou editar reclamações.
O cadastro da reclamação é feita de maneira manual, ou seja, precisamos colocar o número da venda e a reclamação do cliente. A seleção das etapas do processo depende da farmácia, ficando aberta a um funcionário fazer a inclusão e deixar o status como aberta para o farmacêutico ou outro usuário verificar e começar o processo.
A farmácia pode adaptar este processo como achar viável para o seu funcionamento, visto que as etapas são manuais. Abaixo, segue exemplos de reclamações registradas.
Como podemos verificar, é possível marcar se a reclamação é procedente e deixar as ações tomadas para que este erro não aconteça novamente. Quanto mais detalhadas as informações, mais eficaz será este processo. Também é possível gerar um relatório com o resumo de reclamações e organizar por status, para verificar se existe alguma reclamação que não foi tratada ou está sem ação corretiva.
Além disso, o sistema nos informa no momento da venda se o cliente possui alguma reclamação, para que seja possível evitar mais insatisfações com o mesmo no momento da venda.

---

## 🟡 Como marcar um produto como "controlado" no sistema FarmaFácil — 31/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/503743
> Publicado em: 31/10/2024

COMO MARCAR UM PRODUTO COMO CONTROLADO QUANDO JÁ EXISTE ESTOQUE
Ao criar um produto, é fundamental classificá-lo corretamente como controlado, garantindo que as informações relevantes sejam registradas desde o início. Essa marcação não apenas assegura a conformidade com as regulamentações, mas também facilita a gestão do estoque, a rastreabilidade e a segurança no manuseio. Para isso, é necessário preencher três campos essenciais:
No entanto, caso essa classificação não tenha sido realizada durante a criação do produto, existem procedimentos alternativos que podem ser seguidos para corrigir essa situação. Neste artigo, abordaremos a importância da marcação adequada e os passos a serem tomados para regularizar produtos que foram inicialmente cadastrados sem essa classificação.
Passo 1:
Para marcar um produto como controlado, é necessário zerar o estoque do mesmo. Caso o estoque já esteja zerado, você pode pular estes passos e ir direto para o
passo 2.
Inicialmente, iremos gerar o relatório
"Posição de lotes"
para todos os lotes que possuem quantidade no sistema e iremos salvar estes relatórios, com a quantidade descrita. Acesse ESTOQUE > RELATÓRIO > POSIÇÃO LOTE e salve as informações geradas.
IMPORTANTE: É NECESSÁRIO CONCLUIR TODAS AS ORDENS DE MANIPULAÇÃO ANTES DE EMITIR ESTE RELATÓRIO E FAZER ACERTOS.
Passo 2:
Acesse ARQUIVO > UTILITÁRIO > MANUTENÇÃO GERAL e selecione a opção de "zerar estoque"
Atente-se a colocar o filtro do produto e selecionar o correto. Após, clique em "salvar" e confirme a manutenção. Este procedimento irá zerar todos os lotes do produto.
Passo 3:
Com o produto zerado, acesse o cadastro do mesmo em ARQUIVO > ESTOQUE > PRODUTO e edite os campos marcados abaixos, selecionando a lista de controlado, código DCB e marcando a classe terapêutica.
Passo 4:
Com o produto marcado como controlado, iremos realizar um acerto de estoque. Acesse ESTOQUE > MOVIMENTO > ACERTO DE ESTOQUE, e crie um novo acerto para o produto. Para produtos controlados, podemos fazer a entrada como
"SALDO INICIAL".
Preencha as informações de quantidade de acordo com o lote, salvos no passo 1. A justificativa deve ser escrita pela farmácia de forma que seja compreensível nos relatórios de controlados.
IMPORTANTE: É POSSÍVEL REALIZAR ESTA OPERAÇÃO APENAS UMA VEZ
O procedimento para marcar um produto como controlado é simples e rápido, e sua correta execução previne erros na entrega de relatórios controlados, garantindo a precisão e a conformidade necessárias. Agradecemos sinceramente pela parceria e confiança depositada em nossos serviços. Se você tiver qualquer dúvida ou precisar de assistência durante o processo, estamos à disposição para ajudar. Sua satisfação é a nossa prioridade!

---

## 🟡 DECLARAÇÃO DE CONFORMIDADE COM A LEI GERAL DE PROTEÇÃO DE DADOS PESSOAIS (LGPD) — 30/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/503431
> Publicado em: 30/10/2024

PrismaFive Software Ltda.
CNPJ:
72.216.518/0001-78
Endereço:
Avenida José Siqueira, nº 740, bairro Ressacada
Itajaí SC, 88307-311
DECLARAÇÃO DE CONFORMIDADE COM A LEI GERAL DE PROTEÇÃO DE DADOS PESSOAIS (LGPD)
A PrismaFive Software Ltda., empresa com sede na cidade de Itajaí SC e registrada sob o CNPJ 72.216.518/0001-78, declara para os devidos fins que implementou políticas e práticas internas para garantir o tratamento de dados pessoais em conformidade com as disposições da Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018 – LGPD), sancionada em agosto de 2018.
Desde 2021, a PrismaFive adotou medidas de proteção e adequação para assegurar a privacidade, a integridade e a segurança dos dados pessoais tratados em nossas operações, de acordo com as normas estabelecidas pela LGPD, incluindo:
Processos de Segurança da Informação
: Adotamos controles de segurança da informação para proteger dados contra acessos não autorizados, perdas acidentais, destruição, ou outros incidentes de segurança.
Políticas Internas
: Definimos políticas internas para o tratamento seguro dos dados pessoais, com treinamento e orientação aos colaboradores envolvidos no manuseio dessas informações.
Procedimentos de Atendimento aos Direitos dos Titulares
: Implementamos processos para atender aos direitos dos titulares de dados, permitindo acesso, correção e exclusão de dados pessoais mediante solicitação.
Consentimento e Finalidade
: Realizamos a coleta e o tratamento de dados pessoais com base em finalidades específicas, claras e legítimas, conforme previsto pela legislação.
Reafirmamos nosso compromisso contínuo com a adequação à LGPD e garantimos que qualquer informação pessoal tratada pela PrismaFive será manuseada de acordo com os princípios da boa-fé, transparência, segurança e privacidade.
Validade
Este documento permanece válido enquanto as diretrizes da LGPD estiverem sendo observadas pela PrismaFive, com revisões anuais para garantir a continuidade e atualização dos processos.
Itajaí, 12/07/2021
Marcos Cesar Floriani
| Diretor
Corpo Jurídico | BPH Advogados
PrismaFive Software Ltda.

---

## 🟡 Configurar impressoras no WTS — 24/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/502451
> Publicado em: 24/10/2024

Configurar impressora no Windows Terminal Server (WTS)
1º No atalho para a conexao remota, clicar em Mostrar Opções, ir na guia "Recursos Locais" e ligar a opção "Impressoras".
2º Acessar a maquina virtual e instalar a impressora "Brother DCP- 8085DN Printer", na porta colocar a mesma porta que esta em uso na maquina local (EX: TS002 (WKSS052: PRN11#3) (WKSS052 é o nome da  maquina no windows). <== Note que pra cada impressora instalada na sua maquina local vai mudar essa numeração
3º  Windows + R digitar Gpedit.msc e teclar ENTER, depois -> Configuracões do Computador -> Modelos Administrativos -> Componentes do Windows -> Serviços da Área de Trabalho
Remota -> Host de Sessão da Área de Trabalho Remota -> Redirecionamento de Impressora.Ativar a opção : Usar Primeiro o Driver de
Impressora Easy Print de Área de Trabalho Remota.
4º - Forçar o sistema a recarregar a nova política: no prompt de comando: gpupdate  /force

---

## 🟡 Introdução — 23/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/502254
> Publicado em: 23/10/2024

Introdução
Durante o processo de venda no Farma Fácil, após realizar a venda, é necessário efetuar o recebimento para gerar o documento fiscal correspondente. O sistema oferece ao usuário duas opções de documentos fiscais: a Nota Fiscal de Consumidor Eletrônica (NFC-e) e a Nota Fiscal de Serviço Eletrônica (NFS-e). A NFC-e é validada pelo Sefaz, enquanto a NFS-e é validada pela prefeitura. No entanto, é possível que o usuário enfrente um erro de "Operação Não Permitida" ao tentar realizar o recebimento. Este artigo explicará as possíveis causas desse erro e apresentará um tutorial passo a passo para resolver o problema.
Causa do Problema
Esse erro ocorre quando duas notas fiscais vinculadas a venda e uma das notas é uma NFCe com Status 'A ENVIAR'. Isso pode acontecer devido a uma falha de comunicação com o servidor no momento do recebimento, ou até mesmo por um erro humano, como a seleção incorreta do tipo de documento fiscal. Q
uando o sistema detecta essa duplicidade, ele imped
e a emissão do novo documento, retornando a mensagem de "Operação Não Permitida".
Solução
A solução para esse problema envolve identificar a NFCe  e inutilizar o documento fiscal que está associado à venda, para que seja possível emitir um novo documento correto. A seguir, detalhamos o passo a passo para resolver essa situação:
Passo 1: Identificar o Número do Documento Fiscal
1.1 Esse processo pode ser feito tanto pelo Sistema ou pelo Banco de Dados
Para consultar pelo Sistema, Vá em Caixa->Relatório->Notas Fiscais, no relatório precisa escolher a Classificação Analítico - > Tipo NFCe marcar a checkbox Exibir Itens NF (pois ela mostrará o número de vendas) -> Situação "A ENVIAR" e selecionar o período posterior a venda.
O sistema vai gerar um relatório semelhante ao da imagem, basta localizar o numero da venda e anotar o número da NFC-e, após isso vá até o passo 3.
Para consultar pelo banco de dados.
Primeiro, será necessário acessar o banco de dados para identificar o número do documento fiscal associado à venda. Para isso, execute o seguinte comando SQL:
SELECT
numeronotafiscal, tiponotafiscal
FROM
itemnotafiscal
WHERE
numerovenda
=
XXXX;
Substitua "XXXX" pelo número da venda que gerou o erro. O comando retornará os números dos documentos fiscais vinculados àquela venda e seus respectivos tipos.
Passo 2: Identificar o Tipo de Documento
Ao rodar o comando, você receberá uma lista de documentos vinculados à venda. Cada documento possui um número e um tipo, conforme a tabela abaixo:
Tipo 0
: NFSe - Nota Fiscal de Serviço eletrônico
Tipo 1
: NFe - Nota Fiscal eletrônica
Tipo 2
: NFCe - Nota Fiscal de Consumidor eletrônico
Tipo 3
: SAT
Você precisará apenas do número do documento fiscal, Quando o TIPONOTAFISCAL for igual a 2.
Realizando o processo no banco de dados precisa saber qual o Status da NFCe então precisará do segundo comando.
SELECT
numeronotafiscal, tiponotafiscal, situacaonfe, chavenfe, xmlnfe
FROM
notafiscal
WHERE
numeronotafiscal IN
(XXXX, XXX);
Substitua "XX
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Notas de Versão 20.01.88.21 do FarmaFácil Desktop — 23/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/502209
> Publicado em: 23/10/2024

Notas da versão 20.01.88.21 do Farma Fácil Desktop
🗓 Data de lançamento: 23/10/2024
📌 Descrição da versão: A versão 20.01.88.21 do Farma Fácil Desktop já está disponível. Esta atualização traz diversas melhorias e correções no sistema que visam aprimorar a experiência de uso e aumentar a eficiência das operações diárias. Aqui estão os principais destaques:
🛠
Correções de defeitos:
1. #10487 - Recalculo automático do sistema não está ocorrendo para repetições de cápsulas (Manutenção Venda) - BIOGARDEN.
Resolvido o problema que impedia o recalculo automático do sistema para repetições de fórmulas de cápsulas. A funcionalidade foi restaurada, permitindo que os usuários recebam os cálculos corretos da fórmula automaticamente, garantindo a precisão e eficiência no processo.
2. #10472 - Conciliação Bancária com erro ao vincular uma duplicata - DEHON - NAVEGANTES.
Corrigido o erro que ocorria durante o processo de conciliação bancária ao tentar vincular uma duplicata. O sistema agora permite transformar uma transação do extrato bancário em duplicata sem problemas.
3. #10471 - A emissão de NFS-e para Garibaldi está exigindo que o campo de e-mail do tomador seja preenchido (Nota Fiscal) - ESSENCIA GARIBALDI.
Ajustada a obrigatoriedade de preenchimento do campo de e-mail do tomador na emissão de Nota Fiscal de Serviço Eletrônica (NFS-e) para Garibaldi, atendendo às exigências locais.
4. #10463 - Data de vencimento sendo alterada incorretamente ao efetuar o pagamento de duplicatas (Manutenção Duplicata) - FORMULA ANIMAL - PIRACICABA.
Corrigido o fluxo que causava a alteração da data de vencimento, garantindo que a data de vencimento permaneça inalterada após o pagamento.
5. #10461 - Filtrar histórico no cadastro de Lote não está funcionando ao abrir o lote em edição - TODOS.
A funcionalidade de filtrar o histórico no cadastro de lote foi corrigida. O filtro agora opera corretamente ao abrir um lote em modo de edição.
6. #10460 - Erro ao puxar uma Pré-Venda - TODOS.
Resolvido o problema que impedia o carregamento das pré-vendas. O processo de puxar pré-vendas agora opera de maneira correta, garantindo que os usuários consigam acessar essa funcionalidade sem interrupções.
7. #10437 - Incidência de impostos sobre o custo do produto na entrada de nota fiscal não está atualizando os valores no cadastro dos produtos (Nota Fiscal Entrada) - MEDICAMENTUM.
Ajustado o cálculo de impostos sobre o custo do produto durante o lançamento de notas fiscais de entrada. Agora, os valores são corretamente atualizados no cadastro de produtos após a entrada da nota fiscal.
8. #10369 - O sistema não está calculando corretamente a quantidade de excipiente quando é realizada a dobra da quantidade de cápsulas da venda original - TODOS.
Corrigido o problema no cálculo do excipiente quando a quantidade de cápsulas da venda original era dobrada. O sistema agora calcula corretamente quantidade necessária de excipiente, conforme os ajustes realizados nas fórmulas.
9. #10203 - Valor do ex
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Nota Fiscal Exterior — 14/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/500611
> Publicado em: 14/10/2024

Entramos no cadastro do cliente e realizamos o cadastramos a cidade, estado , bairro e nela colocamos o codigo do IBGE (7 vezes o numero 9)
Se for uma pessoa física que não tem CPF pode usar o CPF: 999999999-99.
Caso de erro de IBGE, entra no pais e coloca.
Agora, entra no Caixa\Nota Fiscal e clica para adicionar e assim fazer a nota fiscal ja que o cadastro do cliente ja esta completo.
Sempre consulte com a contabilidade quais as informações serão lançadas na nota.
Tira o ISENTO da IE devido ao erro
de contribuinte de ICMS
alteramos o NCM: 61019090 único que passou
CSOSN: 300.
Local de entrega não preenchemos.

---

## 🟡 Reinicialização do Sync diretamente pelo robô — 02/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/498042
> Publicado em: 02/10/2024

### Como Atualizar a Rota de Internet no Sistema Sync
O sistema Sync é uma ferramenta essencial para o envio e sincronização de mensagens através da web. Contudo, um ponto importante a considerar é que ele depende da rota do provedor de internet para funcionar corretamente. Caso o provedor altere essa rota, o sistema Sync não realizará a troca automaticamente. Nesses casos, é necessário utilizar o comando “Force Reload” para garantir que o programa funcione com a nova configuração.
#### Passo a Passo para Realizar o Force Reload
Para reiniciar o sistema e atualizar a rota de internet, siga os passos abaixo:
**Abra a ferramenta Sync**: Inicie o programa em seu dispositivo.
2. **Acesse a opção “View”**: No canto superior esquerdo da interface, você encontrará a opção “View”. Clique sobre ela.
3. **Selecione “Force Reload”**: Após clicar em “View”, duas novas opções serão exibidas. Clique em “Force Reload”. Essa ação reiniciará o sistema, permitindo que o programa leia novamente a nova rota de internet.
#### Importância do Force Reload
Utilizar o “Force Reload” é um procedimento simples, mas extremamente eficaz, especialmente em situações em que a internet apresenta instabilidades. Esse comando garante que as mensagens sejam enviadas e sincronizadas corretamente para o navegador, evitando interrupções na comunicação.
Em resumo, ao utilizar o sistema Sync, é fundamental estar atento às mudanças na rota de internet do provedor. Ao seguir este guia e realizar o Force Reload, você garantirá um funcionamento otimizado do sistema, mantendo a eficiência nas suas comunicações.
### Conclusão
Manter a ferramenta Sync atualizada é essencial para um desempenho fluido e sem interrupções. A utilização do comando “Force Reload” é uma solução prática para lidar com alterações na rota de internet, assegurando que suas mensagens sejam sempre enviadas de maneira eficaz.

---

## 🟡 Configuração de impressora ARGOX. — 02/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/498008
> Publicado em: 02/10/2024

1- LOCALIZANDO A IMPRESSORA NO COMPUTADOR.
Para darmos início a configuração de sua impressora
ARGOX
, primeiramente você deve entrar na tela "
Dispositivos e Impressoras
", que pode ser acessada pressionando ao mesmo tempo a tecla "
WINDOWS
" e a tecla "
R
" do teclado e pesquisando por "
control printers
".
Nesta tela, na seção "
Impressoras
", procure pela impressora correta, neste caso, nomeada na instalação como "
ARGOX
".
Clique com o botão direito do mouse sobre a impressora e selecione "
Preferências de impressão
" para acessar suas configurações.
2- CONFIGURANDO O PAPEL DE ETIQUETAS.
Na tela "
Preferências de impressão de ARGOX
", devemos clicar em "
Novo...
" para criar um modelo de rótulo dentro da impressora e configurar suas dimensões.
Na tela de edição, você deve preencher os campos conforme tamanho informado por cliente, sendo obrigatório o preenchimento dos campos marcados com "
*
" neste artigo e, ao final, clicar no botão "
OK
" para salvar.
"
Nome
"
*
- Nome desse modelo, recomendamos utilizar o padrão "(
NúmeroDaEtiqueta
)
rotulo
(
NúmeroDaEtiqueta
)" para evitar possíveis erros por nomes similares, portanto, ficando "
3rotulo3
".
OBS: Ensinaremos a pegar o "
NúmeroDaEtiqueta
" mais a frente neste artigo, mas fique tranquilo, o nome do modelo pode ser editado a qualquer momento.
"
Tipo
"
*
- Modelo dos ribbons de etiqueta.
OBS: Em 99,9% dos casos a opção correta será a "
Etiquetas cortadas com molde
".
"
Largura
"
*
- Medida horizontal da etiqueta, de borda a borda, sem descontar logos ou detalhes, sendo o modelo mais comum "
100mm
" de largura.
"
Altura
"
*
- Medida vertical da etiqueta, de cima a baixo, sem descontar logos ou detalhes, sendo o modelo mais comum "
30mm
" de altura.
"
Esquerda
"
*
- Medida horizontal da borda da cartela esquerda da etiqueta, geralmente sendo entre "
1mm
" e "3
mm
".
"
Direita
"
*
- Medida horizontal da borda da cartela direita da etiqueta, geralmente sendo entre "
1mm
" e "3
mm
".
Após configurar corretamente o tamanho do rótulo da cliente, volte na tela "
Dispositivos e Impressoras
", clique com o botão direito, entre em "
Propriedades da impressora
" e copie o nome da instalação, neste caso, "
ARGOX
".
3- CONFIGURANDO AS CHAVES DE IMPRESSÃO DENTRO DO FARMA FÁCIL.
Acesse a guia "
Configurações PrismaFive
" através do atalho "
CTRL
+
F
" ou indo pelo caminho "
Arquivo
>>
Parâmetro
>>
Configurações PrismaFive
".
Na tela "
Configurações
", clique no botão "
Pesquisar
" e em seguida no botão "
Exibir chaves de configuração deste computador
" para filtrar apenas as chaves deste computador, e não de todos os computadores da farmácia.
Clique no botão "
Alterar configuração (Barra espaço)
" e edite as chaves já existentes, ou clique em "
Incluir configuração (Ins)
" e adicione as chaves utilizadas para impressão de etiquetas, sendo elas:
"
ETIQUETA
(
NúmeroDoRótulo
)"
*
- Exporta o posicionamento dos campos da etiqueta configuradas na aba "
ETIQUETAS
" para a impressora.
"
TAMANHOETIQUETA
(
NúmeroDoR
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Fator de perda! — 02/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/497970
> Publicado em: 02/10/2024

Na manipulação de medicamentos ou substâncias em farmácias de manipulação, o "fator de perda" refere-se à quantidade de matéria-prima que é desperdiçada ou perdida durante o processo de preparação ou manipulação. Esse fator pode ser causado por diversos motivos, como:
Resíduo no equipamento
: Parte do material pode ficar retida em equipamentos como balanças, recipientes ou instrumentos de manipulação.
Evaporação
: Algumas substâncias voláteis podem se perder no processo, especialmente em soluções líquidas.
Manipulação inadequada
: Pequenos erros ou variações no processo de pesagem, mistura ou envase podem resultar em perdas.
Degradação da substância
: Alguns ativos podem sofrer degradação devido a fatores como temperatura, luz ou umidade, o que pode reduzir a quantidade final disponível do princípio ativo.
Para configurar o Fator Perda no Farma fácil, deve-se ir no caminho
Arquivo>Produção>Forma Farmacêutica
Selecione a forma farmacêutica desejada, edite, e no campo FATOR PERDA, informe o fator desejado.
O campo fator perda é calculado multiplicando, por exemplo, se eu informo 1,05, ele vai multiplicar a quantidade de cada ativo por 1,05.
Por padrão ele aplica o fator somente nos ativos, se você quiser aplicar também no excipiente, devera marcar APLICA FATOR PERDA QSP.

---

## 🟡 CADASTROS — 02/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/497968
> Publicado em: 02/10/2024

MANUAL DE USO - CASHBACK
KISKADI
Este manual tem como objetivo sanar dúvidas em relação a como gerar o cashback da Kiskadi, e as dúvidas mais frequentes.
CADASTROS
Para gerar o cashback, é
obrigatório
no sistema farmafácil os seguintes cadastros:
DDD+celularnocadastrodo
vendedor;
CPFeDDD+celularnocadastrodo
cliente;
Além destes campos, podem ser obrigatórias outras
informações,
de acordo com a configuração previamente cadastrada no portal do Cashback Farma. Caso alguma informação no cadastro do cliente esteja faltando, será exibido uma mensagem ao tentar
gerar/resgataro
cashback.
CONSULTANDO SALDO DO
CASHBACK
Para saber se aquele cliente tem saldo de resgate disponível, iremosnateladeVENDASnosistema.Faremosavendadoclientee antesdefinalizar,iremospesquisarosaldopeloatalho
CTRL
+
F4
ou
o
atalho
F11
Caso o cliente tenha saldo disponível para resgate, será clicado em “
resgatar
cashback
“ e este desconto será aplicado na venda.
GERANDO NOVO
CASHBACK
Para gerar um novo cashback, iremos receber esta venda no
caixa.
Ao selecionar o número da venda, forma de pagamento, iremos pressionar novamente o atalho
CTRL + F4.
Ao selecionar a opção “SIM”, precisaremos também
SALVAR UM DOCUMENTO FISCAL.
O cashback
NÃO SERÁ GERADO
se não estiver vinculado a um documento fiscal no sistema. Esse documento pode ser cupom fiscal, SAT, nota de serviço.
Caso você
não tenha emissão de notas no sistema
, poderá solicitar ao nosso suporte para configurar um
p
rovedor fictício
,
ou seja, você irá salvar a nota no sistema, mas sem efetivamente
emiti-la
, pois não há conexão real para emissão.
Com isso, podemos ir no portal e verificar a pontuação
gerada,
baseado na regra de pontuação cadastrada no portal do
cashback.
VENDA - cashback gerado
NOVO CADASTRO - cliente gerando cashback pela primeira vez
TROCA
-
cashback
resgatado
CANCELANDO
CASHBACK
O cancelamento poderá ser feito quando o cashback estiver como “ATIVO” e/ou também como “RESGATADO”. Apenas cancelar a
venda ou excluir o caixa
NÃO
CANCELARÁ
O
CASHBACK.
Para
isso,
vamos fazer o seguinte
processo:
CAIXA > MOVIMENTO > FUNÇÕES
TEF
RELATÓRIO
CASHBACK
Podemos acompanhar a geração e resgate do cashback a partir do relatório disponível em CAIXA > RELATÓRIO > RELATÓRIO
CASHBACK, que apresenta as seguintes
informações:

---

## 🟡 Alteração do nome do lote — 02/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/497966
> Publicado em: 02/10/2024

Alteração da descrição de um lote cadastrado no sistema, sem necessidade de excluir nota fiscal de entrada
No ambiente de gestão de sistemas empresariais, é comum a necessidade de ajustes em informações previamente registradas. Um exemplo típico é a alteração de dados de lote já cadastrados, como em situações em que a descrição do lote foi inserido incorretamente na etapa de registro de uma nota fiscal de entrada. Este artigo abordará como realizar essa alteração de forma eficaz, sem precisar excluir a nota fiscal de entrada, utilizando a funcionalidade de manutenção geral do sistema.
Cenário:
Imagine que, ao registrar a nota fiscal de compra, o nome do lote foi inserido com um dígito a mais ou diferente do que consta no documento da nota fiscal. Em vez de excluir a nota e refazer o processo, é possível ajustar essa informação diretamente no sistema.
Passos para Realizar a Alteração do Lote:
Acesse o sistema e navegue até a opção
Arquivo > Utilitário > Manutenção Geral
.
Na janela de manutenção, localize e selecione a opção
Alteração do Lote
.
Insira os novos dados de lote corretos de acordo com a nota fiscal de compra.
Concluído o processo, valide a alteração do lote para que as mudanças sejam refletidas corretamente no sistema.
Esse procedimento é útil para evitar retrabalho e perda de tempo ao lidar com ajustes de informações em lotes cadastrados incorretamente. Com a função de manutenção geral, é possível corrigir esses dados sem a necessidade de excluir e reprocessar a nota fiscal de entrada.
LOTE AJUSTADO

---

## 🟡 Configuração de e-mail no Farma Fácil - GMAIL — 01/10/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/497741
> Publicado em: 01/10/2024

1- CONFIGURANDO O GMAIL DA CLIENTE.
Para darmos início, primeiramente faça
login
no
GMAIL
da cliente que será utilizado para os envios e n
o canto superior direito, clique sobre o ícone de perfil da conta para ter acesso a opção "
Gerenciar sua Conta do Google
".
Você será redirecionado para uma nova aba, onde deve digitar "
Senhas de app
" na barra de pesquisa.
Como uma medida de segurança adicional, o
GMAIL
solicitará a senha da conta novamente.
Após inserir a senha correta, clique em "
Próximo
".
Na próxima tela, insira o nome do aplicativo, neste caso, "
Farma Fácil
", para facilitar a organização das senhas de aplicativo da cliente e clique em "
Criar
".
Após isso, o
GMAIL
exibirá uma senha, que será utilizada na configuração dentro do
Farma Fácil
no passo 2 deste artigo.
2- CADASTRANDO O GMAIL NO FARMA FÁCIL.
Com a
senha de aplicativo
gerada no passo anterior, faça
login
no Farma Fácil com o usuário "
PRISMAFIVE
" e entre nos parâmetros de e-mail pelo caminho "
Parâmetros
>>
Geral
>>
Nfe/Sped
":
OBS: Nunca se esqueça de verificar se a farmácia possui filiais, pois, caso possua, o caminho para acesso será "
Filial
>>
Geral
>>
NFe/Sped
".
No bloco "
Email
", você poderá configurar o envio conforme solicitação da cliente, sendo obrigatório o preenchimento dos campos marcados com "
*
" neste artigo.
"
Serv. SMTP
"
*
- Provedor pelo qual o e-mail será enviado do sistema para o e-mail do cliente.
"
Porta
"
*
- Porta utilizada pelo provedor para enviar o e-mail do sistema para o e-mail do cliente.
"
Usuário
"
*
- GMAIL cadastrado no passo "
1- CONFIGURANDO O GMAIL DA CLIENTE
".
"
Senha
"
*
- Senha de aplicativo gerada no passo "
1- CONFIGURANDO O GMAIL DA CLIENTE
".
"
Assunto
" - Assunto do e-mail que será enviado pelo sistema.
"
Em cópia
" - E-mails secundários que também deverão receber os e-mails enviados pelo sistema, geralmente sendo o e-mail da contabilidade ou do proprietário da farmácia.
"
Autenticação
"
*
- Autenticação utilizada pelo
GMAIL
, obrigatoriamente deverão ser marcados apenas os campos "
SMTP exige conexão segura
" e "
TLS
".
"
Mensagem
" - Corpo do e-mail enviado pelo sistema.
OBS: Caso queira validar o funcionamento do envio de e-mail de maneira rápida, você pode clicar no ícone do envelope, onde você pode informar o destinatário, se deseja enviar um anexo, e os e-mails em cópia.
Após preencher todos os campos e clicar em "Salvar Parâmetro", o Farma Fácil estará pronto para fazer envios para os e-mails dos clientes.

---

## 🟡 Notas de Versão 20.01.88.20 do FarmaFácil Desktop — 24/09/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/495369
> Publicado em: 24/09/2024

Notas da versão 20.01.88.20 do Farma Fácil Desktop
🗓 Data de lançamento: 24/09/2024
📌 Descrição da versão: A versão 20.01.88.20 do Farma Fácil Desktop já está disponível. Esta atualização traz diversas melhorias e correções no sistema que visam aprimorar a experiência de uso e aumentar a eficiência das operações diárias. Aqui estão os principais destaques:
🛠
Correções de defeitos
1. #10430 - Alíquota de serviço sendo arredondada.
Corrigimos o arredondamento incorreto da alíquota de serviço, o que melhora a precisão nos cálculos tributários, evitando inconsistências e erros fiscais.
2. #10425 - Divergência de valores de contas no D.R.E (Relatório DRE).
Ajustamos a divergência nos valores de contas no relatório de Demonstração do Resultado do Exercício (DRE), proporcionando maior precisão na análise financeira.
3. #10424 - Ajustar o status das Notas de Serviço.
Agora, as Notas de Serviço alteram corretamente o status, garantindo um fluxo de trabalho mais confiável e evitando interrupções no processo de faturamento.
4. #10414 - TLS e SSL não salva por filial (Manutenção Filial).
Agora, as configurações de segurança (TLS e SSL) são mantidas corretamente para cada filial, garantindo maior segurança e estabilidade no sistema.
5. #10396 - Possível defeito na descrição do Rótulo CTRL + E.
Corrigimos o problema na descrição do rótulo do produto gerado após a exclusão do sinônimo vinculado ao produto, evitando interrupções no processo de geração das etiquetas.
6. #10389 - Relatório movimento caixa não mostra o número do cliente em recebimentos de convênio.
Agora o relatório exibe o número completo do cliente nas transações de convênios, facilitando a conferência e auditoria dos recebimentos.
7. #10382 - Duplicatas geradas pela nota de entrada estão sendo criadas com o nome do fornecedor em branco.
Corrigimos o problema onde duplicatas geradas na nota de entrada estavam sem o nome do fornecedor, garantindo maior controle sobre as contas a pagar.
8. #10379 - Aplicando fator de perda duas vezes no desmembramento.
Corrigimos a duplicação no fator de perda durante o desmembramento de itens, evitando perdas desnecessárias e melhorando o controle de estoque.
9. #10372 - Não está atualizando o saldo do produto, mesmo possuindo lote com quantidade.
O saldo de produtos agora é atualizado corretamente, assegurando que os dados de estoque sejam precisos e refletindo as quantidades reais em tempo real.
10. #10371 - Recebendo manipulação no SAT ao apertar Enter mesmo com a opção de optante ISS marcada no Parâmetro.
Ajustamos o comportamento ao utilizar o SAT com a opção optante ISS marcada, corrigindo erros de processamento ao pressionar "Enter".
11. #10367 - Erro ao gerar o relatório de posição de estoque financeiro (Relatório de Posição de Estoque).
Agora o relatório de posição de estoque financeiro é gerado sem problemas, permitindo análises de estoque mais confiáveis.
12. #10349 - Impressão da NFE sem protocolo de autorização SC.
Corrigimos o problema de impressão d
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Farmácia Popular - Cadastro de terminal. — 20/09/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/494825
> Publicado em: 20/09/2024

1- OBTENDO AS CREDENCIAIS DE LOGIN DO FARMÁCIA POPULAR.
OBS: Caso a Farmácia já possua as credenciais ou já tenha feito o login no portal do Farmácia popular, vá direto para o passo 2.
Para obter as credenciais de login do Farmácia Popular, primeiramente você deve acessar o banco de dados da farmácia, geralmente encontrado no caminho: "
C:\FarmaFacil\EXE\PgManager
" e executar o seguinte script:
"
select loginfarmaciapopular, senhafarmaciapopular from parametro
"
Caso o script tenha sido executado corretamente, o banco de dados nos retornará o login e senha do Farmácia Popular utilizado pela farmácia.
Utilizando estes dados, faça login no portal do Farmácia Popular, o qual pode ser acessado clicando
aqui
:
2- CADASTRO DO TERMINAL NO FARMÁCIA POPULAR.
No canto superior direito, procure no cabeçalho por "CADASTRO DE COMPUTADORES", e acesse a guia "CADASTRO MANUAL".
Irá ser aberto a guia de cadastro, onde você deve preencher:
"
Nome da Estação
" - Nome pelo qual este terminal será reconhecido. Não há um padrão específico, porém recomendamos cadastrar sempre pelo
Hostname
do computador.
"
Código da Estação
" - Código gerado pelo módulo de segurança do Farmácia Popular.
OBS: Para obter este código de segurança, vá no canto superior direito da página, clique no hiperlink para baixar o módulo de segurança do Farmácia Popular e execute o programa para obter o código correto do terminal que você está configurando.
Após preencher todos os campos e clicar em "Salvar", seu terminal já estará pronto para fazer vendas utilizando o convênio Farmácia Popular.

---

## 🟡 e-pharma — 03/09/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/490903
> Publicado em: 03/09/2024

Para começarmos a configuração, a farmácia deve ser conveniada ao E-pharma, pelo contato através do site
www.epharma.com.br
ou pelo telefone
(11) 4689-8686
ou ainda através do e-mail
contato@epharma.com.br
.
Antes de iniciar o processo de configuração no FarmaFácil é necessário de que o autorizador E-pharma esteja já instalado e configurado no computador pelo convênio.
* Esse procedimento só pode ser realizado se a versão do sistema for V.16.01.13.XX ou superior, devido a mudança do layout do e-pharma no cupom fiscal.
O
arquivo gerado não pode ficar zero no valor, se ficar não importar
1° Passo
Vamos em
"Arquivo -> Parâmetro -> Parâmetro"
ou caso tenha filial
"Arquivo -> Parâmetro -> Filial"
Depois vamos nas guias
"Geral -> Cartões/TEF"
e procuramos o campo
"E-Pharma"
Configuramos o caminho da instalação do convênio, no nosso caso estava como "C:\E-pharma", e inserimos essas informações e marcamos o campo "Habilitar"
2° Passo
Depois vamos nas guias
"Geral -> Convênios"
e procuramos o campo
"E-Pharma"
E inserimos o convênio que criamos anteriormente
3° Passo
No cadastro do cliente, é necessário que a mesma esteja vinculada a um convênio do mesmo, caso não esteja, basta criar o convênio em
"Arquivo -> Venda -> Convênios"
.
É importante colocar a informação "Dia recebimento", caso a cliente não saiba, coloque 30 dias
4° Passo
Após de criado, realizamos o vinculo no cadastro da cliente que irá utilizar o convênio, para que no momento do recebimento, a forma de pagamento venha automaticamente no caixa.
Como por exemplo, fiz um cadastro de cliente com o nome "E-pharma" e vinculei o convênio.
Depois de concluir as configurações e cadastros no sistema, solicite para que a cliente realize uma autorização no sistema do E-Pharma para que possamos realizar o teste.
Quando a cliente chegar nesta tela (imagem abaixo), significa de que a autorização foi gerada, e a partir dai, deixamos essa tela e aberto, pegamos o "Numero autorização" e continuamos o processo no nosso sistema.
O numero gerado copia somente os campos sem o zero e sem o numero do digito.
5° Passo
Vamos na tela de venda no sistema e realizamos o processo de venda, inserindo o vendedor, o cliente conveniado e o produto que foi liberado no sistema E-pharma
Obs.: Código barra do produto tem que estar igual ao do sistema E-pharma, se não, não irá puxar o desconto
Se a cliente desejar incluir na mesma venda um item que não seja pelo convênio o mesmo poderá ser informado normalmente, ao final da venda o valor desse item será incluído na forma de pagamento como à Vista.
Depois clicamos no atalho "Alt + F8" ou então clicamos em "F11" e vamos em "E-Pharma"
E inserimos a informação do código gerado no sistema do E-Pharma (imagem exemplo entre os passos 4 e 5) na tela que abrir, não sendo necessário colocar o digito.
Exemplo: no sistema E-Pharma veio "72390274-7", no nosso sistema colocamos "723902747", conforme o exemplo abaixo:
Após inserir, basta clicar em "Login", se ocorrer tudo corretamente, irá volta
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 DANFE - Nota fiscal Simplificada — 20/08/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/488103
> Publicado em: 20/08/2024

A Danfe Simplificada é uma versão reduzida do Documento Auxiliar da Nota Fiscal Eletrônica (DANFE) e oferece várias vantagens, dependendo do contexto e das necessidades específicas de uma empresa. Aqui estão algumas razões para gerar a Danfe Simplificada:
Redução de Custos
: A Danfe Simplificada utiliza menos papel e tinta, o que pode resultar em economia para empresas que imprimem grandes volumes de documentos.
Eficiência na Logística
: Em operações de entrega e transporte, a versão simplificada pode ser mais prática, facilitando o manuseio e a leitura do documento.
Facilidade de Impressão
: A Danfe Simplificada é ideal para impressoras de etiquetas, como a impressora Zebra, que é comumente usada para etiquetas e documentos menores.
Agilidade na Emissão
: A versão simplificada pode ser emitida e processada mais rapidamente, o que é vantajoso para empresas que necessitam de uma emissão ágil.
Adequação a Diversos Cenários
: Em algumas situações, como entregas rápidas ou quando a nota não precisa de detalhes extensivos, a Danfe Simplificada é suficiente para atender aos requisitos legais e operacionais.
Facilidade de Leitura
: Apesar de ser uma versão reduzida, a Danfe Simplificada ainda contém as informações essenciais necessárias para a identificação e o acompanhamento da nota fiscal.
Portanto, a escolha pela Danfe Simplificada pode proporcionar benefícios operacionais e financeiros, além de oferecer uma alternativa prática para a impressão e utilização do documento fiscal.
1. Abre o Parametro, na aba NFe/Sped, acesse as configurações e selecione uma das três opções disponíveis para impressão:
Normal
: Imprime a Danfe no formato padrão.
Simplificada (etiqueta)
: Imprime a Danfe no formato simplificado.
Ambas
: Permite escolher entre os formatos Normal e Simplificado para a emissão da nota.
2. Na seção "Caixa/Nota", clique no ícone para emitir a nota. Serão apresentadas as opções de "Emitir NFE" ou "Emitir NFE Simplificada".
A Danfe Simplificada pode ser impressa na impressora Zebra.

---

## 🟡 Notas de Versão 20.01.88.19 do FarmaFácil Desktop — 19/08/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/487755
> Publicado em: 19/08/2024

🗓 Data de lançamento: 19/08/2024
📌 Descrição da versão: A versão 20.01.88.18 do Farma Fácil Desktop já está disponível. Esta atualização traz diversas melhorias e correções no sistema que visam aprimorar a experiência de uso e aumentar a eficiência das operações diárias. Aqui estão os principais destaques:
🛠
Correções de defeitos
1. #10338 - Erro de estoque ao salvar fórmulas de homeopatia com a opção líquida marcada (Movimento Fórmula Homeopatia).
Ajustamos o sistema para garantir que as fórmulas de homeopatia com a opção "homeopatia líquida" marcada sejam salvas corretamente, mesmo quando o parâmetro de bloqueio de vendas ou fórmulas sem lote está ativado. Esse ajuste elimina o erro de estoque, proporcionando uma experiência mais confiável para os usuários que trabalham com fórmulas líquidas.
2. #10337 - Relatório Registro de Receituário Geral > Imprimir ativos e dosagens.
Agora, o relatório "Registro Receituário Geral" pode ser gerado e salvo em PDF, incluindo a impressão de dosagens e ativos, mesmo para fórmulas canceladas. Essa correção amplia a funcionalidade do relatório, permitindo um controle mais completo e detalhado.
3. #10325 - Aplicando fator de perda duas vezes no desmembramento.
Corrigimos o sistema para que o fator de perda seja aplicado de forma correta aos itens desmembrados, garantindo que os cálculos sejam precisos e evitando erros que poderiam afetar a gestão do estoque.
4. #10320 - Exibição do sinônimo do fornecedor na tela do Lote ao dar entrada via XML (Manutenção Lote).
Agora, ao processar uma nota fiscal de entrada via XML, o sistema exibe corretamente o sinônimo vinculado ao CNPJ do fornecedor na tela de lote, assegurando que todas as informações estejam alinhadas e facilmente acessíveis.
5. #10235 - Erro no cálculo da quantidade de cápsulas/excipiente em repetições onde é necessário dobrar a quantidade de cápsulas (Movimento Fórmula Venda).
Identificamos e corrigimos um erro relacionado ao cálculo de excipiente durante repetições de venda, especialmente quando o sistema dobrava a quantidade de cápsulas na fórmula. A partir desta atualização, sempre que o parâmetro "manter quantidade anterior de cápsula" estiver ativado e houver necessidade de alteração na quantidade de cápsulas, o sistema irá exibir um alerta. Esse alerta informará ao usuário que a quantidade calculada de ativos excede a capacidade suportada pela quantidade de cápsulas informada na fórmula. Nesse caso, o excipiente será zerado automaticamente, permitindo ao usuário analisar a situação e tomar a melhor decisão.
6. #10228 - Não mostra a associação no complemento da fórmula Venda (Movimento Fórmula Venda).
Corrigido o problema de exibição da associação de produtos na aba "Complemento Fórmula Venda". Esse ajuste é especialmente relevante para produtos que utilizam cálculos específicos, como "Ativo + QSP", "Ativo + Excipiente", "Somente Ativo (percentual)" e "Somente Ativo (quantidade)". Agora, ao visualizar ou editar esses produtos, as informações são apre
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Cancelamento de Notas Fiscais: Tudo que você precisa saber — 19/08/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/487690
> Publicado em: 19/08/2024

O cancelamento de notas fiscais é um procedimento comum no dia a dia de empresas,
mas que exige atenção e conhecimento das regras para evitar problemas com o Fisco.
Seja por erros no preenchimento,
desistência da compra ou qualquer outro motivo,
é fundamental entender como funciona o processo de cancelamento,
tanto dentro quanto fora do prazo legal.
Cancelamento dentro do prazo de 24 horas
A regra geral é que o cancelamento de uma Nota Fiscal Eletrônica (NF-e) ou Nota Fiscal de Consumidor Eletrônica (NFC-e) deve ser realizado dentro de 24 horas após sua autorização de uso pela Secretaria da Fazenda (SEFAZ).
Nesse período,
o processo é relativamente simples e pode ser feito diretamente pelo sistema emissor de notas fiscais,
sem necessidade de justificativas ou autorizações adicionais.
Cancelamento após 24 horas: O que fazer?
Após o prazo de 24 horas,
o cancelamento se torna mais complexo e as regras variam de acordo com o estado.
Em Santa Catarina,
por exemplo,
o cancelamento de NF-e e NFC-e após 24 horas é permitido,
mas exige um procedimento específico:
Justificativa:
É necessário apresentar uma justificativa plausível para o cancelamento extemporâneo,
como erro no preenchimento,
desistência da compra ou outros motivos que comprovem a necessidade do cancelamento.
Carta de Cancelamento:
Deve ser emitida uma Carta de Cancelamento Eletrônica (CC-e) informando o motivo do cancelamento e a chave de acesso da NF-e ou NFC-e a ser cancelada.
Autorização da SEFAZ:
A SEFAZ analisará o pedido e,
se a justificativa for considerada válida,
autorizará o cancelamento.
Dicas importantes:
Consulte a legislação do seu estado:
As regras para cancelamento de notas fiscais após 24 horas podem variar.
Consulte a legislação específica do seu estado para saber os procedimentos e prazos.
Mantenha os documentos organizados:
Guarde todos os documentos relacionados à operação,
como contratos,
pedidos de compra e comprovantes de pagamento,
para facilitar a justificativa do cancelamento,
se necessário.
Busque ajuda de um contador:
Em caso de dúvidas ou situações complexas,
consulte um contador para garantir que o processo seja realizado corretamente e evitar problemas com o Fisco.
Conclusão
O cancelamento de notas fiscais é um procedimento que exige atenção e conhecimento das regras.
Ao seguir os procedimentos corretos e estar atento aos prazos,
você garante a conformidade fiscal do seu negócio e evita transtornos com a Receita Federal.

---

## 🟡 Como é Feito o Processo de Emissão de Vendas para Fórmulas de Cápsula — 02/08/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/485329
> Publicado em: 02/08/2024

O sistema de gestão FarmaFácil oferece uma maneira eficiente de gerenciar a emissão de vendas para fórmulas de cápsula, agilizando o processo e garantindo a precisão das informações. Este guia passo a passo, complementado pelo tutorial em vídeo detalhado, irá orientá-lo durante todo o processo.
1. Acessando o Módulo de Vendas:
Inicie o sistema FarmaFácil e navegue até o módulo de vendas.
Clique em "Nova Venda" para iniciar o processo.
2. Identificando o Cliente:
Busque o cliente pelo nome ou CPF.
Se o cliente for novo, cadastre-o no sistema.
3. Selecionando a Fórmula:
Acesse a seção de "Fórmulas" e localize a fórmula desejada.
Utilize a barra de pesquisa para encontrar a fórmula rapidamente.
4. Informando a Quantidade:
Especifique a quantidade de cápsulas desejada pelo cliente.
O sistema calculará automaticamente o valor total da venda.
5. Adicionando Informações Adicionais (Opcional):
Se necessário, adicione informações como posologia, modo de usar e observações importantes.
Essas informações podem ser impressas na etiqueta da fórmula.
6. Finalizando a Venda:
Clique em "Finalizar Venda" para concluir o processo.
O sistema gerará um comprovante de venda para o cliente.
7. Imprimindo a Etiqueta (Opcional):
Se desejar, imprima a etiqueta da fórmula com as informações relevantes.
A etiqueta pode ser colada no frasco da fórmula para facilitar a identificação.
8. Gerenciando o Estoque:
O sistema FarmaFácil atualizará automaticamente o estoque da fórmula após a venda.
Você poderá acompanhar o histórico de vendas e o estoque disponível no sistema.
Dicas Adicionais:
Utilize o atalho "F9" para agilizar a busca de fórmulas.
Aproveite o campo de observações para adicionar informações personalizadas.
Consulte o tutorial em vídeo para visualizar o processo completo.
Ao seguir este guia e assistir ao tutorial em vídeo, você dominará o processo de emissão de vendas para fórmulas de cápsula no sistema FarmaFácil, otimizando o atendimento ao cliente e garantindo a eficiência do seu negócio.

---

## 🟡 Notas de Versão 20.01.88.18 do FarmaFácil Desktop — 01/08/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/485073
> Publicado em: 01/08/2024

🗓 Data de lançamento: 01/08/2024
📌 Descrição da versão: A versão 20.01.88.18 do Farma Fácil Desktop já está disponível. Esta atualização traz diversas melhorias e correções no sistema que visam aprimorar a experiência de uso e aumentar a eficiência das operações diárias. Aqui estão os principais destaques:
🛠
Correções de defeitos
1. #10299: Erro ao gerar o relatório de Posição de Estoque Financeiro (Relatório de Posição de Estoque).
Corrigido o problema de estouro do campo ao gerar o relatório, assegurando melhor controle financeiro.
2. #10295: Problema ao salvar a Alíquota ISS na configuração da filial (Manutenção Filial - Aba Cupom Fiscal / NFCe / SAT).
O sistema agora mantém as informações inseridas no campo de Alíquota de ISS, evitando transtornos nas configurações tributárias.
3. #10292: O sistema não está atualizando corretamente o campo "custo referência" na tela de produto quando existe outras despesas no xml - TODAS.
O campo "valor de referência" agora é atualizado corretamente, refletindo todas as despesas associadas.
4. #10289: Não está puxando a etiqueta anterior nas repetições de vendas.
Corrigido o problema onde a etiqueta anterior da venda não era exibida nas repetições de vendas, assegurando maior eficiência e precisão na impressão de etiquetas.
5. #10254: Repetição multiplicando o QSP/Excipiente pela quantidade de fórmulas duas vezes nas fórmulas de cápsulas.
Corrigido o cálculo do QSP/Excipiente na repetição da fórmula, evitando desperdícios e erros nas fórmulas.
6. #9740: Valor de custo do QSP em Pré Vendas - TODOS.
O sistema agora calcula automaticamente o valor de custo do QSP, assegurando eficiência e precisão nos cálculos.
7. #9711: Descrição dos itens ao incluir na fórmula padrão - DEHON - CONCORDIA.
A descrição dos itens do produto agora é exibida corretamente, garantindo clareza e precisão.
8. #9298: Campo Bairro Receituário Geral - BOTICA DA TERRA - MATRIZ.
O campo "bairro" foi reposicionado para exibição correta, evitando erros em registros.
9. #8671: Tratamento do campo Horas Previsão Entrega quando possui setor cadastrado - INTERNO.
Incluído tratamento para evitar erros ao remover informações do campo, resultando em maior flexibilidade no planejamento de entregas.
10. #8649: Relatório Orçamentos Rejeitados - MAGISTRALE - RIO DE JANEIRO.
A data do orçamento agora é exibida corretamente, facilitando a análise de orçamentos rejeitados.
11. #8941: Erro relatório receitas e despesas - ARTEFARMA - SALINAS.
Corrigido o problema onde não estava sendo exibidas as vendas recebidas via forma de pagamento tranferência no relatório, garantindo relatórios financeiros mais precisos e confiáveis.
🚀
Implementação de melhorias
1. #10328: Após salvar a edição do item da nota o sistema não deve processar todos os itens da NF entrada - TODOS.
Agora, apenas o item editado é processado, reduzindo significativamente o tempo de processamento.
2. #10300: Nota de serviço de Jaciara - MT está sendo transmitida mas não está atualizando o status 
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Medicamento zolpidem terá alteração no tipo de receita para prescrição e venda - ANVISA — 01/08/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/485072
> Publicado em: 01/08/2024

💊A partir de 1º de agosto de 2024 a Notificação de Receita B (azul) passa a ser obrigatória para a prescrição e a dispensação de todos os medicamentos à base de zolpidem, independentemente da concentração da substância.
A receita tipo B exige que o profissional prescritor seja previamente cadastrado na autoridade local de vigilância sanitária.
Os medicamentos, incluindo aqueles com embalagem com tarja vermelha, poderão ser dispensados nas farmácias até o final do seu prazo de validade, mediante a apresentação de Notificação de Receita B, em cor azul.
Até 1º de dezembro de 2024, os fabricantes desses medicamentos poderão fabricá-los com a embalagem com tarja vermelha.  Após essa data, todos os medicamentos fabricados à base de zolpidem já deverão conter a tarja preta em sua embalagem, conforme é exigido para os medicamentos da Lista B1 da Portaria SVS/MS 344/1998.
Lembramos que, nas farmácias, os medicamentos com zolpidem, tanto em embalagens com tarja vermelha quanto preta, poderão ser dispensados até o final do seu prazo de validade, mediante a apresentação de Notificação de Receita B, em cor azul.
Notícia completa no link:
https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2024/medicamento-zolpidem-tera-alteracao-no-tipo-de-receita-para-prescricao-e-venda
Qual é o procedimento a ser adotado no sistema?
Conforme mencionado no trecho acima:
"os medicamentos com zolpidem, tanto em embalagens com tarja vermelha quanto preta, poderão ser dispensados até o final do seu prazo de validade, mediante a apresentação de Notificação de Receita B, em cor azul. "
Nesse caso, a orientação é manter o cadastro e estoque atual do que já existe na farmácia, bem como seguir realizando as movimentações normalmente e quando for feita uma nova aquisição/compra,
cadastrar um novo produto
já com a nova lista informada no cadastro, isso garante que possa movimentar normalmente ambos e evita problemas com a fiscalização e retenção da receita correspondente. Não orientamos que seja feita alteração cadastral.

---

## 🟡 Lista de produtos proibidos pelo Código Mundial Antidopagem - Lei nº 14.806, de 11 de janeiro de 2024 — 31/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/484716
> Publicado em: 31/07/2024

A Lei nº 14.806, de 11 de janeiro de 2024, altera a Lei nº 6.360, de 23 de setembro de 1976, e estabelece que os laboratórios farmacêuticos devem incluir alertas nos rótulos, bulas e materiais de propaganda e publicidade de seus produtos sobre a presença de substâncias cujo uso é considerado doping. Essa medida visa aumentar a transparência e a segurança para atletas e consumidores em geral, evitando o uso inadvertido de substâncias proibidas pelo Código Mundial Antidopagem.
A lei foi sancionada pelo Presidente Luiz Inácio Lula da Silva e entra em vigor após 180 dias da sua publicação. A implementação dessa lei é vista como um avanço importante pela comunidade esportiva, pois facilita o cumprimento das regras antidoping e protege a integridade dos atletas​
(
Planalto
)
​​
(
Portal da Câmara dos Deputados
)
​​
(
Serviços e Informações do Brasil
)
​.
Detalhamento das substâncias que fazem parte da lista:
Lista de Substâncias
Para configurar o sistema e atender a nova lei, o processo sugerido é:
1 -
Alerta na venda:
Inclua uma observação no cadastro do produto (Aba Observação > Venda), indicando que este faz parte da lista de substâncias.
Texto sugerido:
"Atenção: Este medicamento contém substâncias proibidas pelo Código Mundial Antidopagem. Consulte seu médico ou farmacêutico antes de usar."
2 -
Alerta na ordem de produção:
Inclua uma observação no cadastro do produto (Aba Observação > Ordem Manipulação), indicando que este faz parte da lista de substâncias.
Texto sugerido:
"Atenção: Este medicamento contém substâncias proibidas pelo Código Mundial Antidopagem. Consulte seu médico ou farmacêutico antes de usar."
3 -
Alerta no rótulo:
Incluir no campo descrição rótulo do cadastro do produto que faz parte da lista de substâncias a descrição abaixo:
Texto sugerido: "
CONTÉM SUBST. CONSIDERADA DOPING"
Por fim, ao gerar a venda o resultado será:
Na tela da venda:
1 -
2 -
Na Ordem de manipulação impressa:
Rótulo de venda:

---

## 🟡 Importância da Cor das Cápsulas na Manipulação de Medicamentos — 29/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/484174
> Publicado em: 29/07/2024

Importância da Cor das Cápsulas na Manipulação de Medicamentos
A cor das cápsulas desempenha um papel significativo na manipulação de medicamentos, impactando diversos aspectos importantes. Abaixo, detalhamos os principais pontos a serem considerados:
Identificação e Diferenciação
As cores variadas das cápsulas são amplamente utilizadas para identificar e diferenciar medicamentos, doses ou fórmulas distintas. Essa prática é especialmente útil em farmácias e hospitais, onde há uma grande diversidade de medicamentos em uso. Diferenciar visualmente os medicamentos ajuda a prevenir erros na administração e a garantir que os pacientes recebam o tratamento correto.
Preferências do Paciente
As preferências dos pacientes também podem influenciar a escolha da cor das cápsulas. Alguns pacientes têm aversões ou preferências por certas cores, o que pode afetar sua adesão ao tratamento. Ao considerar as preferências individuais dos pacientes, é possível melhorar a aceitação e a continuidade do tratamento.
Proteção contra Luz
Determinadas cores de cápsulas podem oferecer proteção adicional contra a luz, sendo cruciais para medicamentos que são sensíveis à luz. A exposição à luz pode degradar alguns compostos farmacêuticos, comprometendo sua eficácia e segurança. Portanto, a escolha de cápsulas com cores que bloqueiem a luz pode ajudar a preservar a estabilidade dos medicamentos.
Cápsulas sem Dióxido de Titânio (TiO₂)
Recentemente, o uso de cápsulas sem dióxido de titânio tem se tornado mais comum, principalmente devido a preocupações regulatórias e de saúde. O dióxido de titânio é frequentemente usado como agente de opacidade e corante branco, mas algumas questões foram levantadas sobre sua segurança em alimentos e medicamentos. Abaixo, destacamos algumas considerações sobre o uso dessas cápsulas na manipulação:
Transparência e Opacidade
Sem dióxido de titânio, as cápsulas podem ser mais transparentes ou translúcidas, permitindo a visualização do conteúdo interno. Essa característica pode ser tanto estética quanto funcional, dependendo do tipo de medicamento.
Proteção contra Luz
Cápsulas sem dióxido de titânio oferecem menos proteção contra a luz, o que é uma consideração importante para medicamentos sensíveis à luz. Nestes casos, pode ser necessário o uso de materiais alternativos ou embalagens adicionais para proteger o medicamento.
Aceitabilidade do Paciente
Alguns pacientes podem preferir ou necessitar de cápsulas sem dióxido de titânio devido a alergias, sensibilidades ou preocupações de saúde. Adaptar as cápsulas às necessidades dos pacientes pode melhorar sua aceitabilidade e adesão ao tratamento.
Estabilidade e Integridade do Medicamento
É crucial garantir que a ausência de dióxido de titânio não comprometa a estabilidade ou a integridade do medicamento. Testes de estabilidade e estudos de compatibilidade são essenciais para assegurar que o medicamento permaneça eficaz e seguro ao longo do tempo.
Regulamentações
A escolha por cápsulas sem dióxido de ti
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Como Emitir Vendas a Partir de Pré-Vendas — 24/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/483495
> Publicado em: 24/07/2024

A rotina de vendas em farmácias pode ser otimizada com o uso de pré-vendas, um recurso que simplifica a emissão de novas vendas a partir de fórmulas pré-cadastradas. Essa funcionalidade agiliza o atendimento, reduzindo a necessidade de digitar manualmente cada item e dosagem da fórmula.
O que é uma Pré-Venda?
Uma pré-venda é um modelo de venda que contém informações detalhadas sobre uma fórmula específica, incluindo:
Nome da Fórmula:
Identificação da fórmula para fácil referência.
Itens da Fórmula:
Lista completa dos medicamentos e insumos que compõem a fórmula, com suas respectivas dosagens.
Instruções de Preparo:
Orientações sobre como manipular e preparar a fórmula.
Outras Informações Relevantes:
Dados adicionais como validade, condições de armazenamento e precauções.
Como Funciona a Emissão de Venda a Partir de Pré-Venda:
Seleção da Pré-Venda:
O vendedor seleciona a pré-venda desejada a partir de uma lista de fórmulas pré-cadastradas.
Ajuste das Informações:
O sistema carrega automaticamente os dados da pré-venda, incluindo itens, dosagens e instruções. O vendedor pode fazer ajustes na quantidade, adicionar ou remover itens, personalizar informações do cliente e definir condições de pagamento.
Geração da Venda:
Com as informações ajustadas, o sistema gera a venda, replicando os dados da pré-venda e incorporando as modificações realizadas.
Revisão e Finalização:
O vendedor revisa os detalhes da venda, confirma as informações e finaliza o processo.
Benefícios da Emissão de Venda a Partir de Pré-Venda:
Agilidade:
Reduz o tempo de atendimento, eliminando a necessidade de digitar manualmente cada item da fórmula.
Precisão:
Minimiza o risco de erros na dosagem e composição da fórmula.
Padronização:
Garante a consistência na preparação das fórmulas, seguindo as instruções pré-definidas.
Eficiência:
Otimiza o fluxo de trabalho, permitindo que os vendedores se concentrem em outras atividades.
Satisfação do Cliente:
Proporciona um atendimento mais rápido e eficiente, melhorando a experiência do cliente.
Tutorial em Vídeo:
Para um guia prático e detalhado sobre como utilizar a funcionalidade de emissão de venda a partir de pré-venda, assista ao tutorial abaixo:

---

## 🟡 Como é feito o processo de repetição de formulas para gerar novas vendas — 24/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/483487
> Publicado em: 24/07/2024

A repetição de fórmulas é uma funcionalidade poderosa que agiliza e otimiza o processo de vendas, permitindo que você replique vendas anteriores com facilidade e rapidez. Essa ferramenta é especialmente útil em cenários onde há recorrência de pedidos semelhantes.
Como Funciona a Repetição de Fórmulas:
Seleção da Venda Base:
O primeiro passo é identificar a venda que servirá como modelo para a repetição.
Ajuste das Informações:
Após selecionar a venda base, você poderá fazer os ajustes necessários para a nova venda. Isso inclui alterar quantidades, atualizar preços, adicionar ou remover produtos, modificar informações do cliente e personalizar as condições de pagamento.
Geração da Nova Venda:
Com as informações ajustadas, o sistema gerará automaticamente uma nova venda, replicando os dados da venda base e incorporando as modificações realizadas.
Revisão e Finalização:
Antes de finalizar a venda, revise cuidadosamente todos os detalhes para garantir a precisão das informações. Após a confirmação, a nova venda será registrada no sistema, pronta para ser processada.
Benefícios da Repetição de Fórmulas:
Agilidade:
Reduz o tempo gasto na criação de novas vendas, eliminando a necessidade de inserir manualmente todos os dados.
Precisão:
Minimiza o risco de erros, pois as informações são replicadas da venda base, garantindo a consistência dos dados.
Eficiência:
Otimiza o processo de vendas, permitindo que a equipe se concentre em atividades mais estratégicas.
Escalabilidade:
Facilita o atendimento a um grande volume de pedidos, especialmente em empresas com vendas recorrentes.
Tutorial em Vídeo:
Para um guia prático e detalhado sobre como utilizar a funcionalidade de repetição de fórmulas, assista ao tutorial em vídeo disponível

---

## 🟡 Procedimento para Criação de Artigo para Central de Ajuda — 23/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/483306
> Publicado em: 23/07/2024

Para publicar o seu primeiro artigo, vá até o menu MOVIDESK e clique em
Configurações
. No campo da
Base de conhecimento
, clique em
Artigos
.
Segue MODELO DE ARTIGO:
https://prismafive.movidesk.com/kb/pt-br/article/476984/
ajustar-valores
💡DICAS DE TEMAS PARA ARTIGOS:
Melhorias liberadas nas versões para isto pesquise no redmind, pois na tarefa há uma explicação detalhada que pode ser aprovetada
Dúvidas de clientes
Procedimentos internos para analistas de suporte – neste caso o artigo deve ser parametrizado como NÃO visível para clientes.
Artigos que necessitam de revisão deve ser criados novos artigos para que estes fiquem vinculado ao seu nome e o antigo deve ser eliminado ou suspenso
Para escrever um novo artigo, basta clicar no sinal de
mais
, o botão verde na parte superior da tela.
Uma nova aba se abrirá com os campos para escrever o
Título
, o
Conteúdo
e o
Resumo
do artigo. Além disso, aparecerão uma série de Configurações acerca da visibilidade do artigo e também a sua classificação de acordo com o menu e a categoria, entre outras opções.
1. Título
: campo no qual você adiciona o título do seu artigo que deve ser sempre em minúsculo. Utilize um título que reflita claramente o problema ou a tarefa abordada no artigo.
2. Link permanente
: link gerado para acessar o seu artigo. Você pode editá-lo como quiser clicando no ícone de lápis.
3. Conteúdo
: corpo do texto, o artigo em si. É possível inserir links, imagens, vídeos, gifs e conteúdo html, além de possuir várias ferramentas de configuração. Divida o processo em etapas claras e numeradas. Use capturas de tela e vídeos para ilustrar os passos, quando necessário e evitando jargões técnicos desnecessários. Cada arquivo anexado deve ter, no máximo 10 MB.
4. Resumo
: pequena descrição do conteúdo do artigo que será exibida na pesquisa de artigos. Pode não ser informado. Nessa ocasião, serão mostrados na pesquisa os primeiros caracteres do texto.
As
CONFIGURAÇÕES
ao publicar um artigo
Nas configurações, é possível definir aspectos acerca da visibilidade do artigo a ser publicado.
1. Artigo visível na central de ajuda
: escolha as opções de
checkbox
(uma ou mais) que deseja marcar para configurar a visibilidade do seu artigo publicado.
2. Pública
: o artigo ficará visível ao público em geral.
3. De clientes cadastrados
: o artigo ficará visível apenas para clientes logados no Movidesk. Dentro dessa configuração, você ainda pode escolher uma, entre as três opções de
radiobutton
:
Permitir todos os clientes
,
Permitir os seguintes perfis de acesso
ou
Permitir as seguintes pessoas
.
4. De agentes
: o artigo ficará visível apenas para agentes logados no Movidesk. Dentro dessa configuração você pode escolher uma, entre as quatro opções de
radiobutton
:
Permitir todos os clientes
,
Permitir os seguintes perfis de acesso
,
Permitir as seguintes equipes
ou
Permitir as seguintes pessoas
.
5. Avaliação do artigo: ao manter essa opção selecionada, você permitirá que os leitores avaliem o artigo publicado
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Manutenção de Vendas: Como Reter a Receita de Produtos Acabados e de Drogaria Não Controlados — 23/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/483303
> Publicado em: 23/07/2024

Neste artigo, vamos abordar a importância da Manutenção de Vendas e como você pode utilizar essa funcionalidade para reter a receita de produtos acabados e de drogaria não controlados. Acompanhe o vídeo tutorial abaixo para um guia passo a passo,
🎥Assista ao Vídeo Tutorial

---

## 🟡 Manutenção de Vendas: Como transformar orçamentos em Vendas — 23/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/483302
> Publicado em: 23/07/2024

A função "Manutenção de Vendas" permite gerenciar seus orçamentos de forma eficiente e transformá-los em vendas concretizadas. Neste artigo, vamos te guiar passo a passo por esse recurso e mostrar como ele pode facilitar sua rotina e aumentar seus resultados.
🎥Assista ao Vídeo Tutorial e saiba como converter orçamentos em vendas:
➡️ Veja também os artigos relacionados

---

## 🟡 Manutenção de Venda: Como é gerada uma venda para produtos acabados e drogaria — 23/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/483300
> Publicado em: 23/07/2024

Você sabe como utilizar a função Manutenção de Venda para gerar vendas de produtos acabados e drogaria? 🤔 Se a resposta for "não" ou se você quiser aprimorar seus conhecimentos, nosso novo vídeo tutorial é exatamente o que você precisa!
Neste vídeo, vamos te mostrar passo a passo como realizar uma venda utilizando a função Manutenção de Venda. Você aprenderá:
🔹 Como acessar a função Manutenção de Venda
🔹 Passos detalhados para incluir produtos acabados na venda
🔹 Dicas para otimizar o processo e evitar erros comuns
🔹 E muito mais!
➡️  Veja também o artigo relacionado.

---

## 🟡 Bloquear reimpressão de venda/ordem — 23/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/483249
> Publicado em: 23/07/2024

Para bloquear a reimpressão das ordens e das vendas, existe uma nova função para isso no Farma Fácil.
Basta seguir o caminho: ARQUIVO>PARAMETRO>PARAMETRO
Após estar na tela de PARAMETROS, só ir na aba GERAL>IMPRESSÃO e marcar a opção BLOQUEAR REIMPRESSÃO DE VENDA;ORDEM.
Com essa opção marcada, quando for reimpresso uma venda ou ordem, o sistema pedira a senha de administrador para concluir o processo.

---

## 🟡 PREVISÃO DE ENTREGA DA FORMULA — 23/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/483080
> Publicado em: 23/07/2024

PUXA A MESMA PREVISÃO DE ENTREGA NAS PRÓXIMAS FÓRMULAS AUTOMATICAMENTE.
1- PARÂMETRO > MANIPULAÇÃO > GERAL
2- MARQUE A OPÇÃO 'USAR O HORÁRIO DA ÚLTIMA FÓRMULA ADICIONADA'.
3- VENDA > VENDA > INCLUIR NOVA VENDA.
4- MANIPULAÇÃO > PREVISÃO DA PRODUÇÃO.
AUTOMATICAMENTE, AS PRÓXIMAS FÓRMULAS JÁ PUXAM COM A MESMA PREVISÃO DA PRODUÇÃO.

---

## 🟡 Configuração de fase na Formula Padrão — 22/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/482866
> Publicado em: 22/07/2024

FASE
O ciclo de vida ou fases da ordem de produção passa por algumas etapas para ser concluída. Dessa forma, as etapas determinam os passos concluídos até que seja cancelado ou encerrado.
Fase
: serve para definir em qual etapa o produto será aplicado na fórmula. Geralmente usada onde a produção é feita em fases separadamente. Uma parte dos produtos é usada na fase aquosa e outra parte na fase oleosa, como exemplo.
Isso engloba o controle de produção da
formula padrão
: Cápsulas, cremes, pomadas e outras formas farmacêuticas possuem diferentes processos de produção, que exigem uma ordem específica de manipulação dos ativos.
Para configuração das fases seguir os passos a seguir:
ARQUIVO>PRODUÇÃO>FORMULA PADRÃO
Selecione e edite cada ativo da formula para adicionar sua respectiva fase e salve:
Ao criar e imprimir a sua formula padrão na ordem de produção constará um campo novo, o campo fase:
Procedimento bem simples que garante a controle da ordem em que os ativos serão manipulados, essa flexibilidade permite ao farmacêutico adaptar a ordem de manipulação às necessidades específicas de cada fórmula, assegurando a qualidade e segurança do medicamento final.

---

## 🟡 Campos ETIQUETA DE PRECO DROGARIA — 19/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/482541
> Publicado em: 19/07/2024

CHAVES DE REGISTRO
NOME DA CHAVE
FUNÇÃO
PRECO
Informa o Preço do cadastro do produto.
CODIGOBARRAS
Informa o Código de barras do produto
DESCRICAOPRODUTO
Informa a descrição do produto Abreviado.
DESCRICAO2
Informa a Descrição do produto completo.

---

## 🟡 Notas de Versão 20.01.88.17 do FarmaFácil Desktop — 12/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/481305
> Publicado em: 12/07/2024

🗓 Data de lançamento: 12/07/2024
📌 Descrição da versão: A versão 20.01.88.17 do Farma Fácil Desktop já está disponível. Esta atualização traz diversas melhorias e correções no sistema que visam aprimorar a experiência de uso e aumentar a eficiência das operações diárias. Aqui estão os principais destaques:
🛠
Correções de defeitos
1.#10258 - Formas de pagamento sendo inseridas indevidamente (Manutenção Caixa).
Corrigido o problema onde as formas de pagamento estavam sendo inseridas indevidamente na tela de caixa, evitando erros de pagamento e garantindo que as transações sejam registradas corretamente.
2. #10240 - Não está sendo envido notas Fiscais de Serviço quando a retenção é por parte do TOMADOR.
Ajustado o envio de notas fiscais de serviço quando a retenção é realizada pelo tomador, assegurando que todas as notas fiscais sejam enviadas corretamente, evitando problemas de conformidade fiscal e garantindo a precisão nas retenções de impostos.
3. #10237 - Erro na estrutura do totalizador para NFC-e no SPED PIS/COFINS (Manutenção Arquivo SPED).
Corrigido a estrutura do totalizador para NFC-e no SPED PIS/COFINS, garantindo conformidade dos relatórios fiscais, evitando possíveis multas e problemas com auditorias.
4. #10227 - Dotz com erro ao puxar o relatório de envio (Integração Dotz - Manutenção de Arquivos).
Ajustada a integração com o Dotz para garantir que o relatório de envio funcione corretamente, garantido dessa forma, que as integrações funcionem sem problemas, melhorando a eficiência e a precisão dos dados.
5. #10226 - O sistema não está atualizando o horário do relógio no rodapé.
O sistema está atualizando corretamente o horário do relógio no rodapé, assegurando que os horários exibidos estejam sempre atualizados e corretos.
6. #10219 - Erro ao salvar as configurações de etiquetas para fórmulas padrão utilizando o modelo 4 (Manutenção Etiquetas).
Resolvido os problemas identificados ao salvar as configurações de etiquetas para fórmulas padrão utilizando o modelo 4, garantido a personalização das etiquetas, melhorando a organização e a eficiência no controle de fórmulas.
7. #10218 - Ao enviar uma nota fiscal de serviço o sistema está retornando que a unidade de serviço está errada, povedor IPM do município São Gonçalo do Sapucaí.
Corrigido o retorno de erro na unidade de serviço ao enviar notas fiscais de serviço, especialmente para o provedor IPM do município de São Gonçalo do Sapucaí, garantindo que as notas fiscais sejam aceitas e processadas sem erros, evitando atrasos e problemas de conformidade.
8. #10149 - Erro nos somatórios de valores no Relatório de D.R.E ao utilizar conciliação bancária (Relatório D.R.E).
Corrigido o erro identificado nos somatórios de valores no relatório de D.R.E ao utilizar conciliação bancária, garantindo a precisão dos relatórios financeiros, essenciais para a tomada de decisões informadas.
9. #9867 - Diferença no Relatório Posição de Estoque Financeiro X Registro 74 Sintegra - EXATA FARMACIA.
Eliminada a
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Contas a pagar — 09/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/480464
> Publicado em: 09/07/2024

Contas a pagar
O objetivo de contas a pagar é gerenciar e controlar as obrigações financeiras da sua empresa. Isso envolve o registro, acompanhamento e pagamento de todas as despesas e dívidas que a empresa tem com fornecedores, prestadores de serviços e outras partes.
Em resumo, a gestão de contas a pagar é fundamental para a saúde financeira e a operação eficiente de uma empresa, contribuindo para a sustentabilidade e o crescimento do negócio.
Para utilização da ferramenta contas a pagar deve ser acessado o menu:
A Pagar -> Movimento -> Contas a Pagar
Neste menu são apresentadas as duplicatas a serem pagas que foram lançadas automaticamente via entrada de nota fiscal ou
via inclusão manual, temos também algumas opções como:
1->
Procurar Duplicata (F2)
2->
Visualizar Duplicata Corrente (F3)
3->
Apresentar as Duplicatas Pagas (F5)
4->
Incluir Duplicata (Insert)
5->
Alterar Duplicata (barra de espaço)
6->
Excluir Duplicata (Delete)
7->
Pagar Duplicata (F6)
9->
Baixar Duplicata em Lote
9->
Cancelar Pagamento de Duplicata (F7)
Para inclusão manual de uma duplicata, os campos devem ser preenchidos conforme apresentado abaixo, sendo obrigatório o preenchimento dos campos circulados:
Para pagamento das duplicatas é necessário apenas informar a data de pagamento e valor pago, sendo possível também informar uma observação.
O item 8 é bem perigoso pois coloca todas as duplicatas como paga em lote, sem precisar entrar uma a uma, após clicar em salvar.

---

## 🟡 Notas de Versão 20.01.88.16 do FarmaFácil Desktop — 03/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/479366
> Publicado em: 03/07/2024

Data de Liberação: 02 de Julho de 2024
Melhoria Implementada:
- Tarefa 10246:
Validação dos meios de pagamentos do SEFAZ para PIX nas emissões de NFC-e (Cupom Fiscal Eletrônico).
A partir de 01/07/2024, novas validações para meios de pagamento do SEFAZ entraram em vigor para emissões de cupons eletrônicos. Com essa nova validação, o SEFAZ está recusando o envio de NFC-e com a forma de pagamento PIX que esteja fora dos novos padrões. Esta atualização garante que o FarmaFácil Desktop esteja em conformidade com essas novas exigências, evitando problemas na emissão dos cupons fiscais.
Para mais detalhes sobre as novas validações do SEFAZ, acesse o documento oficial
https://www.nfe.fazenda.gov.br/portal/exibirArquivo.aspx?conteudo=T1W3L10vCC4=
Observação:
Critério de Adoção das Unidades Federativas (UFs):
- Cabe destacar que a adoção dessas novas validações pode variar conforme a legislação de cada Unidade Federativa (UF). Recomendamos verificar com a secretaria da fazenda de sua UF para confirmar a necessidade de conformidade com esses novos requisitos.
- O pacote da versão 20.01.88.15 também foi ajustado para incluir a melhoria realizada para a adequação das novas validações pelo SEFAZ. O executável (exe) e a biblioteca Prisma5NFCe.dll foram atualizados.

---

## 🟡 Introdução — 03/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/479357
> Publicado em: 03/07/2024

Introdução
O PrismaSync é uma ferramenta desenvolvida pela PrismaFive para integrar o sistema de gestão FarmaFácil com o WhatsApp da Meta. Embora nossa solução ofereça uma comunicação eficiente e integrada, é importante entender que qualquer banimento no WhatsApp é resultado de violações das políticas da própria plataforma, e não do uso do PrismaSync.
Por Que Contas São Banidas no WhatsApp?
Spam e Mensagens em Massa
Envio de mensagens em massa ou conteúdo de spam.
Conteúdo Ilegal e Abusivo
Compartilhamento de material ilegal, abusivo ou que incite violência.
Comportamento Suspeito
Atividades que possam ser consideradas suspeitas pela plataforma, como criar muitas contas em pouco tempo.
Violações Repetidas
Reincidência em violações dos termos de serviço, mesmo após advertências.
Entendendo o Papel do PrismaSync
O PrismaSync atua apenas como uma ponte entre o FarmaFácil e o WhatsApp, facilitando a comunicação e a gestão de informações. Ele não interfere nas políticas de uso do WhatsApp e não tem a capacidade de influenciar ou causar o banimento de contas.
Como Evitar o Banimento
Para evitar que sua conta seja banida no WhatsApp enquanto utiliza o PrismaSync, é crucial seguir as diretrizes da Meta. Algumas práticas recomendadas incluem:
- Evitar o envio de mensagens em massa não solicitadas.
- Respeitar as leis e evitar compartilhar conteúdo ilegal ou ofensivo.
- Manter um comportamento que não levante suspeitas, como evitar ser bloqueado por muitos usuários em pouco tempo.
O Que Fazer em Caso de Banimento
Se sua conta for banida, recomendamos revisar as políticas de uso do WhatsApp e verificar se alguma regra foi violada. Caso acredite que o banimento foi injusto, entre em contato com o suporte do WhatsApp para solicitar uma revisão.
Para mais informações sobre os motivos de banimento no WhatsApp, consulte o artigo oficial da Meta: Regras do WhatsApp
https://faq.whatsapp.com/465883178708358/?locale=pt_BR
Conclusão
O PrismaSync é uma ferramenta projetada para melhorar a eficiência da comunicação no seu negócio, sem violar as políticas do WhatsApp. Seguir as diretrizes da plataforma é essencial para garantir uma experiência de uso contínua e segura.

---

## 🟡 Notas de Versão 20.01.88.16 do FarmaFácil Desktop — 03/07/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/479339
> Publicado em: 03/07/2024

🗓 Data de lançamento: 02/07/2024
📌 Descrição da versão: A versão 20.01.88.16 do Farma Fácil Desktop já está disponível. Nesta atualização foi implementada a seguinte melhoria:
#10246: Validação dos meios de pagamentos do SEFAZ para PIX nas emissões de NFC-e (Cupom Fiscal Eletrônico).
A emissão de NFC-e foi ajustada para atender às novas validações implementadas pelo SEFAZ. Essas atualizações têm como objetivo aprimorar a precisão e a segurança nas transações eletrônicas realizadas por meio de NFC-e (Nota Fiscal de Consumidor Eletrônica). Elas incluem a implementação de novos códigos para PIX dinâmico e PIX estático, além da integração completa dos dados exigidos pelo SEFAZ. Essas mudanças foram realizadas para assegurar que todas as transações realizadas pelo sistema estejam em conformidade com as novas normas a partir de 01/07/2024, evitando possíveis problemas operacionais.

---

## 🟡 Possíveis Causas da Não Sincronização dos Orçamentos do PRISMASYNC com o FarmaFácil — 28/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/478706
> Publicado em: 28/06/2024

A sincronização dos orçamentos do PRISMASYNC com o FarmaFácil é crucial para garantir que todas as operações de orçamento sejam processadas corretamente. Quando a sincronização falha, pode causar grandes inconvenientes para os usuários. Aqui estão algumas possíveis causas para esse problema e como resolvê-las:
1. Data e Hora Incorretas no Windows
Uma das causas mais comuns da falha de sincronização é a data e hora incorretas no sistema operacional Windows. Os sistemas dependem de uma data e hora precisas para autenticar e registrar as transações corretamente. Se o relógio do seu sistema estiver incorreto, pode causar falhas na comunicação entre os sistemas PRISMASYNC e FarmaFácil.
Como Corrigir:
1. Clique com o botão direito do mouse no relógio na barra de tarefas do Windows.
2. Selecione "Ajustar data/hora".
3. Certifique-se de que a opção "Ajustar automaticamente" esteja ativada.
4. Caso precise ajustar manualmente, clique em "Alterar" sob "Definir data e hora manualmente" e ajuste a data e hora corretamente.
2. Serviço SyncPrismaSyncWeb
O serviço SyncPrismaSyncWeb é responsável pela sincronização dos dados entre os sistemas. Se este serviço não estiver funcionando corretamente, a sincronização falhará.
Como Verificar e Reiniciar o Serviço:
1. Acessar o Gerenciador de Serviços do Windows:
Pressione simultaneamente a tecla Windows + R para abrir a caixa de diálogo "Executar".
- Digite `services.msc` e pressione Enter. Isso abrirá a janela de Serviços do Windows.
2. Localizar e Gerenciar o Serviço SyncPrismaSyncWeb:
Na lista de serviços, procure pelo serviço chamado SyncPrismaSyncWeb.
- Verifique o status do serviço:
- Se o serviço estiver rodando, clique em "Reiniciar".
- Se o serviço estiver parado, clique em "Iniciar".
3. Verificar a Sincronização:
- Após reiniciar ou iniciar o serviço, aguarde alguns minutos para que o sistema tente sincronizar os orçamentos novamente.
- Verifique se os orçamentos voltaram a sincronizar corretamente no sistema.
3. Conexão de Rede
Problemas de conectividade com a rede podem impedir a comunicação entre PRISMASYNC e FarmaFácil. Verifique se a sua conexão com a internet está estável e funcionando corretamente. Caso perceba instabilidade entrar em contato com seu provedor.
O Que Fazer se os Orçamentos Ainda Não Sincronizarem
Se, mesmo após seguir esses passos, os orçamentos ainda não estiverem sendo sincronizados, é necessário abrir um ticket ou entrar em contato com o suporte técnico para uma assistência mais detalhada. O suporte técnico poderá fornecer uma análise mais aprofundada e soluções específicas para o seu ambiente.
Esperamos que essas dicas ajudem a resolver os problemas de sincronização e garantam um funcionamento suave entre PRISMASYNC e FarmaFácil.

---

## 🟡 Como gerar relatório de estoque de produtos SUJEITOS A CONTROLE ESPECIAL e ANTIMICROBIANOS. — 27/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/478486
> Publicado em: 27/06/2024

Para gerar um relatorio aonde conste a posição de estoque somente de produtos SUJEITOS A CONTROLE ESPECIAL e ANTIMICROBIANOS, independentemente do grupo aonde estejam no sistema,
basta seguir o caminho:
VENDA>RELATORIO>CONTROLADOS MANIPULAÇÃO(PARA MATERIAS PRIMAS)
OU
VENDA>RELATORIO>CONTROLADOS DROGARIA(PARA DROGARIA)
APÓS ISSO SELECIONAR O FILTRO >POSIÇÃO DE LOTES
Após isso o sistema nos traz o relatório em tela com a posição de estoque do momento em que o relatório foi gerado.

---

## 🟡 Cadastro de natureza de operação (CFOP) — 27/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/478473
> Publicado em: 27/06/2024

O que é CFOP?
CFOP (Código Fiscal de Operações e Prestações) é um código utilizado no Brasil para identificar a natureza das operações de circulação de mercadorias e prestação de serviços. Essencial para a emissão de documentos fiscais e escrituração contábil, o CFOP classifica operações como vendas, transferências, devoluções, importações e exportações, garantindo a correta aplicação de tributos e a conformidade legal das empresas.
Sistema
Para chegar no modulo de NATUREZA DE OPERAÇÃO no sistema, deve-se seguir o caminho ARQUIVO>PARAMETRO>NATUREZA DE OPERAÇÃO
Já dentro do modulo, teremos essa tela
1 = Pesquisar natureza. 2 = Visualizar natureza. 3 = Incluir natureza. 4 = Alterar natureza. 5 = Excluir natureza. 6 = Voltar.
Após clicar no botão de Incluir natureza. teremos a seguinte tela:
Código = Código referente a natureza a ser criada.
Descrição = Nome referente a natureza a ser criada.
Tipo = Checkbox para marcar se a natureza é referente a entrada de produtos, ou saída.
Exportar Sintegra = Checkbox para marcar quando movimentações feitas nesse CFOP devem ser exportadas no arquivo SINTEGRA.
Exportar Bloco X = Checkbox para marcar quando movimentações feitas nesse CFOP devem ser exportadas no arquivo Bloco X.
Exige documento referenciado = Obriga que na nota utilizando essa natureza, seja referenciado uma nota.

---

## 🟡 Como ter acesso ao Relatório de Controlado Drogaria? — 27/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/478465
> Publicado em: 27/06/2024

CONTROLADO DROGARIA
O relatório de Controlado Drogaria serve para monitorar e documentar a movimentação de medicamentos controlados em uma farmácia ou drogaria. Este relatório é essencial para cumprir as regulamentações legais e garantir o uso responsável desses medicamentos. Aqui estão algumas das principais finalidades do relatório de Controlado Drogaria:
Conformidade Legal:
Assegura que a drogaria esteja em conformidade com as leis e regulamentos sobre a venda e distribuição de medicamentos controlados.
Rastreamento de Estoque:
Permite o acompanhamento preciso do estoque de medicamentos controlados, evitando perdas e desvios.
Auditoria e Fiscalização:
Facilita auditorias e inspeções realizadas por órgãos reguladores, como a Anvisa, fornecendo registros detalhados de todas as transações envolvendo medicamentos controlados.
Documentação Completa:
Mantém um registro completo de todas as entradas e saídas de medicamentos controlados, incluindo informações sobre fornecedores, clientes, quantidades e datas.
Para gerar o relatório de control
ado
drogaria, é imprescindível que a farmácia possua acesso às classificações MD ou D. Caso possua apenas a classificação M, não será possível ativar esta funcionalidade. Para proceder com a ativação, é necessário acessar o parâmetro correspondente:
Caminho do parâmetro:
Arquivo > Parâmetro > Parâmetro
Na aba "Drogaria", encontrará a opção de "Habilitar
Drogaria":
Após realizar este ajuste, o relatório estará disponível na aba
"Venda > Relatório > Controlado Drogaria":
Por favor, siga os passos mencionados para habilitar corretamente o relatório
controlado
drogaria conforme necessário.
窗体顶端
窗体底端

---

## 🟡 Cadastro de ensaios de farmacopeia — 27/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/478458
> Publicado em: 27/06/2024

O que são ensaios de farmacopeia?
Ensaios de farmacopeia são procedimentos padronizados utilizados para avaliar a qualidade, pureza, potência e identidade de medicamentos. Eles garantem que os produtos farmacêuticos atendam aos rigorosos padrões estabelecidos, assegurando a segurança do paciente e a conformidade regulamentar. Esses ensaios são fundamentais para manter a confiança no sistema de saúde e garantir que apenas medicamentos seguros e eficazes estejam disponíveis no mercado.
Sistema:
Para cadastrar um ensaio, deve-se seguir o caminho ARQUIVO>PARAMETRO>ENSAIO:
Após entrar na tela de ENSAIO, vai ter as opções de ADICIONAR/ALTERAR/EXCLUIR
Após clicar para inserir um ensaio, você informará a DESCRIÇÃO do ensaio, e a qual FARMACOPEIA ele responde:
Após ensaios cadastrados, eles já poderão ser vinculados ao cadastro de produtos para ser feita analise dos mesmos.

---

## 🟡 Cadastro de Farmacopeia — 27/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/478444
> Publicado em: 27/06/2024

O que é uma farmacopeia?
A farmacopeia é um compêndio oficial que estabelece normas e especificações para garantir a qualidade, segurança e eficácia dos medicamentos. Contendo monografias detalhadas, métodos de análise padronizados, diretrizes de armazenamento e rotulagem, e boas práticas de fabricação, a farmacopeia assegura que os produtos farmacêuticos atendam a rigorosos padrões de qualidade. Exemplos de farmacopeias reconhecidas incluem a Farmacopeia dos Estados Unidos (USP), a Farmacopeia Europeia (EP) e a Farmacopeia Brasileira (FB).
Sistema:
Para cadastrar uma farmacopeia no sistema, deve-se seguir o caminho ARQUIVO>PARAMETRO>FARMACOPEIA:
Com a tela de farmacopeia aberta, temos os botões de ADICIONAR/ALTERAR/EXCLUIR:
Após clicar no INCLUIR, informaremos somente o NOME DA FARMACOPEIA, e uma OBSERVAÇÃO se necessária:
Após isso esta criado a farmacopeia, após isso, só seguir para o cadastro de ENSAIOS.

---

## 🟡 Siproquim | Portaria 240 — 26/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/478154
> Publicado em: 26/06/2024

Neste artigo, você aprenderá como ajustar os
cadastros de produtos
para após
realizar a exportação do arquivo
do PrismaFive para importar no  Siproquim.
A importação deve ser realizada t
odos os meses até o dia 15 do mês.
➡️O Siproquim (Sistema de Controle e Fiscalização de Produtos Químicos) é um
sistema desenvolvido pela Polícia Federal do Brasil
para controlar e fiscalizar produtos químicos que podem ser utilizados na fabricação ilegal de drogas ou em atividades ilícitas. Ele regula a produção, comércio, transporte, armazenamento, uso e destino final desses produtos. O objetivo principal do Siproquim é monitorar e regular a circulação de substâncias químicas sujeitas a controle especial, como precursores químicos e produtos químicos controlados. Isso ajuda a identificar e prevenir desvios, irregularidades ou uso indevido dessas substâncias, contribuindo para o combate ao tráfico de drogas e outras atividades ilícitas relacionadas.
Empresas e entidades que lidam com esses produtos devem seguir as regulamentações e procedimentos estabelecidos pelo Siproquim para garantir o controle adequado e promover a segurança pública.
Em resumo, o Siproquim desempenha um papel fundamental na proteção da sociedade, assegurando o cumprimento da legislação e promovendo o controle e segurança dos produtos químicos no Brasil.
Ajustando os cadastros de produto
Primeiramente devemos ajustar o cadastro de produto, onde iremos informar o código Siproquim de cada produto que deve ser exportado
1° Passo: Vamos em "Arquivo -> Estoque -> Produto" e editamos o produto que desejamos
2° Passo: Ao editar,  informamos seu NCM na aba "Matéria prima"
Obs.: é necessário ter essas informações obrigatoriamente para que possa contabilizar as movimentações.
.
3° Passo: Vamos nos seguintes caminhos, "Complemento" e depois "Dados Adicionais", após isto terá o campo na qual informamos qual código deve ser para o produto.
Obs.: Caso o código Siproquim não apareça, é porque não foi informado NCM no produto ou o NCM informado não pertence ao Siproquim.
Conforme exemplo abaixo:
Caso o NCM que está cadastrado no produto esteja diferente do que está cadastrado na lista de código Siproquim, irá mostrar a mensagem abaixo:
OBS: A partir da versão 88.14 a concentração e densidade para exportação do arquivo enviado para o Siproquim devem ser registradas na nota fiscal de entrada, de acordo com o que está especificado na nota fiscal, levando em consideração os campos da imagem abaixo.
Já, as densidades do lote e cadastro do produto são utilizadas para cálculos farmacêuticos em fórmulas, por outro lado, caso os dados não estejam presentes na nota fiscal de entrada, serão considerados os dados da aba do lote para exportação do arquivo com as movimentações do Siproquim, o sistema atua dessa forma para atender as informações de forma correta e evitar que o arquivo seja exportado sem os dados necessários para validação no sistema da PF.
Após ajustar os cadastros, já estará contabilizando as movimentaçõ
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Não Ligue para o Suporte da PrismaFive: Abra um Ticket e Interaja no Ticket Quando Necessário — 24/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/477588
> Publicado em: 24/06/2024

Hoje, queremos conversar sobre uma maneira importante de garantir que suas necessidades sejam atendidas de forma rápida e eficiente: usar nosso sistema de tickets em vez de ligar para o suporte. Entendemos que ligar para falar com alguém pode parecer mais direto, mas há muitas vantagens em usar nosso sistema de tickets.
1. Resolução Mais Precisa
Quando você abre um ticket, você pode detalhar seu problema com calma e fornecer todas as informações necessárias. Isso ajuda nosso time a entender melhor o que está acontecendo e a encontrar a solução mais adequada. Imagine que você está escrevendo uma carta explicando um problema. Quanto mais detalhes você incluir, melhor será a resposta. Por exemplo:
- Descreva o problema que está ocorrendo.
- Inclua prints (capturas de tela) do erro ou da falha.
- Informe os passos que você seguiu antes de encontrar o problema.
- Mencione qualquer mensagem de erro que apareceu.
2. Acompanhamento Facilitado
Com o ticket, você pode acompanhar o andamento da sua solicitação. Isso é como acompanhar uma encomenda pelo correio. Você sabe exatamente onde está seu pedido e o que está acontecendo com ele. Se precisar adicionar mais informações ou perguntar algo, basta enviar uma mensagem no mesmo ticket. Não precisa começar do zero toda vez que tiver uma dúvida. Por exemplo:
- Se o problema mudar ou ocorrer um novo erro, você pode atualizar o ticket.
- Se você descobrir algo novo sobre o problema, informe no ticket.
3. Disponibilidade do Analista
Os analistas, que são as pessoas que resolvem os problemas, muitas vezes estão ocupados ajudando outros clientes. Quando você liga, pode ser que o analista responsável pelo seu caso esteja atendendo outra pessoa. Interagir pelo ticket garante que sua mensagem chegue diretamente a ele assim que ele estiver disponível. Pense nisso como deixar um recado detalhado para que ele possa responder da melhor maneira possível.
4. Organização e Eficiência
Usar o sistema de tickets ajuda a organizar todas as solicitações de forma eficiente. Isso significa que menos coisas se perdem pelo caminho e tudo pode ser tratado mais rapidamente. Ligar várias vezes para explicar o mesmo problema pode causar confusão, mas um ticket bem detalhado mantém todas as informações em um só lugar. Por exemplo:
- Todos os detalhes do seu problema ficam registrados no ticket.
- O analista pode ver todo o histórico de comunicação e entender melhor a situação.
5. Tempo de Atendimento (SLA)
Todo ticket, uma vez aberto, já começa a contabilizar o tempo de atendimento (SLA - Service Level Agreement). Isso significa que assim que você abre um ticket, o tempo para resolução do seu problema começa a ser contado, garantindo que seu caso seja tratado com prioridade. Por exemplo:
- Se você abrir um ticket e incluir todas as informações necessárias, o analista pode começar a trabalhar na sua solicitação imediatamente.
- Isso é mais rápido do que esperar para falar com alguém por telefone e explicar o problema do zero.
6. Recursos A
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 🗓 Data de lançamento: 20/06/2024 — 21/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/477101
> Publicado em: 21/06/2024

🗓 Data de lançamento: 20/06/2024
📌 Descrição da versão:
A versão 20.01.88.15 do Farma Fácil Desktop já está disponível. Nesta atualização existem correções e melhorias importantes no sistema que visam proporcionar uma melhor experiência de uso. A seguir, são listadas as principais alterações realizadas:
🛠 Correções de defeitos
#10200 - O sistema não está calculando o fator de correção nas ordens de produção de fórmula padrão quando o cálculo está em UFC.
Corrigido o problema que afetava o cálculo das ordens de produção utilizando Fórmula Padrão quando configurado em Unidades de Fórmula Convencional (UFC), garantindo cálculos precisos.
#10194 - Erro ao realizar vendas de homeopatia quando a filial de produção é diferente da que está fazendo a venda (Movimento Fórmula Homeopatia).
Ao lançar a fórmula de homeopatia, o sistema valida o estoque considerando a filial de produção, e não a filial que está fazendo a venda, garantindo um processo de venda eficiente.
#10175 - Erro de envio das notas quando a descrição do produto é muito longa SIMPLISS.
Incluído campo para ajustar o limite de caracteres que é enviado ao webservice, permitindo o envio de notas fiscais sem erros, mesmo em casos de notas com muitos itens ou descrições extensas.
#10171 - O sistema não está localizando o produto pelo código de barras secundário.
Ajustado o sistema para localizar os produtos tanto pelo código de barras principal quanto pelo secundário, proporcionando buscas precisas e eficientes independentemente do código de barras utilizado.
#10160 - Não é possível abrir o relatório de Bula.
A fim de evitar transtornos e garantir uma experiência consistente o relatório de bula foi oculto do sistema.
#10152 - Relatório Caixa por Forma farmacêutica/Grupo x Movimentação Caixa não estão apresentado os mesmos valores.
A correção realizada no relatório Caixa por Forma farmacêutica/Grupo garante que todas as transações, independentemente das datas de recebimento (mesmo ao agrupar dados de vários dias) sejam contabilizadas corretamente.
#10145 - Erro na emissão de NFS-e de Bento Gonçalves - RS.
Corrigido o problema no envio da nota, garantindo que as notas confirmadas pela prefeitura sejam exibidas corretamente no sistema e eliminando a necessidade de tentativas repetidas de envio.
#10135 - Emissão NFS-e (Erechim) com problemas.
Corrigido o erro de 'serviço não implementado' para o provedor e alteração do status das NFS-e após a confirmação no site da prefeitura, garantindo um processo de envio sem interrupções.
#10117 - Diferenças apuradas com valores invertidos no Relatório Movimento Caixa.
Corrigido o erro apresentado nas diferenças apuradas no fechamento de caixa, onde o saldo positivo são valores a mais de dinheiro e o saldo negativo são valores a menos de dinheiro.
#10104 - Baixa em lote de duplicatas a pagar estão sendo exibidas duplicadas na tela de baixa.
A correção garante que as duplicatas a serem pagas sejam exibidas corretamente na tela de baixa em lote, refletindo apenas o
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Notas de Versão PrismaSync 4.9.2 — 21/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/477100
> Publicado em: 21/06/2024

🚀 Implementação de Melhorias:
• Atualizações de Segurança e Correções de Vulnerabilidades: Foram realizadas atualizações importantes para reforçar a segurança da aplicação, garantindo maior proteção contra possíveis ameaças e vulnerabilidades.
• Melhorias Pontuais de Performance: Implementamos otimizações que melhoram o desempenho geral da aplicação, proporcionando uma experiência mais fluida e responsiva.
• Otimização do Monitoramento de Desempenho: Aperfeiçoamos as formas de monitoramento do desempenho da aplicação, permitindo uma detecção e correção mais ágil de eventuais problemas.
🛠 Correção de Defeitos:
• Sincronização de Mensagens: As mensagens enviadas pelo celular ou WhatsApp Web agora estão sendo corretamente sincronizadas no PrismaSync, garantindo que todas as comunicações sejam registradas e acessíveis em um único lugar.
• Função de Apagar Mensagens: Corrigimos a funcionalidade de apagar mensagens, que agora está operando conforme o esperado, permitindo que os usuários gerenciem suas conversas com mais eficácia.
• Correção no Envio de Mensagens com Imagens: Resolvemos o problema que impedia o envio de mensagens ao cliente quando a conversa era iniciada com uma imagem. Agora, todas as mensagens são entregues corretamente, independentemente de como a conversa foi iniciada.

---

## 🟡 Saiba como Ajustar Valores markup ou valor de venda — 21/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/476984
> Publicado em: 21/06/2024

O objetivo deste artigo é orientar os usuários do sistema FarmaFácil sobre como utilizar a ferramenta de ajuste de valores disponível na manutenção geral. Ele fornece um passo a passo detalhado para acessar, selecionar grupos de produtos, aplicar ajustes de
markup ou valor de venda
. O artigo visa garantir que os usuários possam realizar ajustes de maneira eficiente e precisa.
Acessando a Ferramenta de Ajuste de Valores
1. Navegação no Menu:
Acesse: ARQUIVO > UTILIÁRIO > MANUTENÇÃO GERAL.
2. Localizando a Opção de Ajuste:
Na tela que se abrir, localize e selecione a opção Ajustar Valores.
3. Selecionando os Grupos de Produtos:
Na próxima tela, informe o grupo ou grupos para os quais deseja fazer a manutenção de valores.
Vai abrir essa tela e você clica no + para adicionar o(s) grupo(s):
4. Confirmando a Seleção:
Após selecionar os grupos, clique em Sair para retornar à tela principal do ajuste.
Filtrando e Visualizando Produtos
1. Aplicar Filtro:
Na tela principal, já com os grupos selecionados, clique em Filtrar. Serão exibidos todos os produtos relacionados aos grupos selecionados.
Ficará assim:
Ajustando os Valores
1. Escolha do Tipo de Ajuste:
O ajuste dos valores pode ser feito com base no Markup ou no Valor de Venda do produto.
2. Ajuste pelo Markup:
Se o ajuste for pelo markup, o percentual informado será somado ao valor já existente no markup do produto. Exemplo: Se o markup atual de um produto é 50% e você aplica um ajuste de 100%, o novo markup será 150% (100% do ajuste + 50% existente).
3. Ajuste pelo Valor de Venda:
Se o ajuste for pelo valor de venda, o percentual informado será somado ao valor de venda atual do produto. Exemplo: Se o valor de venda atual é R$ 100 e você aplica um ajuste de 50%, o novo valor de venda será R$ 150 (R$ 100 + 50%).
Fixando Markup para Todos os Produtos de um Grupo
1. Ajuste Manual do Markup:
Para fixar o markup em 100% para todos os produtos de um grupo, clique três vezes no valor do markup do produto na lista. Informe o novo valor desejado e repita o processo para todos os produtos da lista.
2. Salvar Alterações:
Após realizar a edição, clique no ícone do disquete para salvar as alterações.
➡️🚩Correção de Ajustes Incorretos Realizado pelo Usuário
1. Revertendo Ajustes:
CASO O USUÁRIO TENHA APLICADO UM PERCENTUAL INCORRETO, BASTA DESFAZER O PROCESSO. Exemplo: se foi adicionado um ajuste de 30% no tipo de ajuste Valor de Venda, para desfazer basta realizar o mesmo filtro e parametrização e no campo percentual de ajuste informar um valor de redução negativo.
Passos Simples para Calcular a Redução
1. Entenda a Situação Inicial e Final:
- Você começou com R$100.
- Aumentou 30%, então o valor foi para R$130.
2. Calcule a Diferença:
- O valor aumentou de R$100 para R$130, uma diferença de R$30.
- Diferença = R$130 - R$100 = R$30.
3. Calcule a Porcentagem de Redução Necessária:
- Você quer saber quanto precisa reduzir R$130 para voltar a ser R$100.
- Para isso, você precisa calcular qual porcentagem de R$130 é 
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 🗓 Data de Lançamento: 06/06/2024 — 18/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/476257
> Publicado em: 18/06/2024

🗓 Data de Lançamento: 06/06/2024
📌 Descrição da Versão:
A versão 20.01.88.14 do FarmaFácil Desktop já está disponível! Esta atualização inclui importantes correções e melhorias para proporcionar uma melhor experiência de uso. Confira os detalhes das principais alterações abaixo:
-----------------------------
🛠 Correções de Erros
1. 10129 - Erro na Reimpressão das Dinamizações
- Corrigido um problema que ocorria durante a reimpressão das dinamizações, garantindo que o processo seja realizado corretamente sem interrupções.
2. 10126 - Arquivo Exportado do Siproquim com Movimentação Errada
- Resolvido o problema que gerava uma movimentação incorreta no arquivo exportado para o Siproquim, assegurando a precisão dos dados exportados.
3. 9743 - Erro no Cálculo da Quantidade de Excipiente em Repetições
- Corrigido um erro que afetava o cálculo da quantidade de excipiente em repetições de pedidos, especialmente em casos onde a quantidade de cápsulas da venda original era dobrada.
-----------------------------
🚀 Melhorias Implementadas
4. 9599 - Integração com API PH24
- Implementada a integração com a API PH24, melhorando a comunicação e sincronização de dados entre o FarmaFácil Desktop e os sistemas externos compatíveis.
👥 Notas Adicionais:
Recomendamos que todos os usuários solicitem a atualização para esta nova versão para garantir a melhor performance e funcionalidade do FarmaFácil Desktop. Para realizar a atualização, basta abrir um ticket em nossa central de suporte.

---

## 🟡 Como Configurar e Utilizar Orçamentos em Forma de Imagem no Farma Fácil — 17/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/475908
> Publicado em: 17/06/2024

Os orçamentos são essenciais para informar valores aos clientes e facilitar o fechamento de vendas. Pensando nisso, a Prisma Five desenvolveu uma maneira inovadora de enviar orçamentos: Orçamentos por Imagem. Neste artigo, vamos detalhar o passo a passo para configurar e utilizar essa funcionalidade no sistema Farma Fácil.
Passo 1: Configurando Mensagens Padrão
Acesse o Farma Fácil
: Abra o sistema e selecione a opção
ARQUIVO > VENDA >
MENSAGEM PADRÃO
. Alternativamente, você pode pressionar
CTRL + F
e buscar por "MENSAGEM PADRÃO".
Passo 2: Selecionando Modelos de Orçamento
Acesse o módulo de mensagens padrão
: Dentro deste módulo, localize e selecione a opção com a tag
CALCULADO
.
Editar o modelo
: Clique em
EDITAR
para configurar o modelo de mensagem de orçamento conforme sua necessidade.
Passo 3: Orçamento por Imagem
Visualizando o modelo de imagem
: No módulo de edição, a opção
GERAL
estará selecionada por padrão.
Selecionar o modelo 2
: Clique duas vezes na imagem do modelo 2 para abrir o módulo de edição de imagem. Após selecionar o MODELO 2, clique para salvar para começar a
utilizá-lo
Passo 4: Editando o Modelo
Personalizando o orçamento
: Dentro do módulo de edição, você pode dar dois cliques em qualquer informação que deseja alterar, seja texto, imagem ou layout das informações.
Importante
: As informações entre colchetes são consideradas
TAGS
e são utilizadas pelo sistema para inserir automaticamente os dados contidos no orçamento. NÃO edite ou exclua essas informações, pois isso pode comprometer a qualidade e a clareza do seu orçamento.
Agora que você já selecionou o Modelo 2 de orçamento e personalizou a imagem para refletir a identidade da sua farmácia, vamos ver como utilizar essa nova função para criar e enviar um orçamento.
Passo 1: Enviando o Orçamento do Prisma Sync para o Farma Fácil
Gerando o orçamento
: No PrismaSync, clique no ícone de orçamentos para abrir uma nova tela.
Envie a receita
: Se o cliente enviou uma foto da receita, selecione a imagem e envie o orçamento. Caso o cliente não tenha enviado uma foto da receita, você pode proceder sem anexar uma imagem.
Passo 2: Gerando o Orçamento no Sistema
Acesse o módulo de orçamento
: Na tela principal do Farma Fácil, selecione o módulo
VENDA
> SYNC ORÇAMENTO
.
Filtre as buscas
: Na tela de orçamento, selecione o período que deseja filtrar ou preencha o campo “IDENTIFICADOR” com o número do cliente conforme consta no Prisma Sync.
Selecione o orçamento
: Após filtrar os orçamentos, escolha o orçamento do cliente e clique no ícone de
VENDA
ou pressione
ALT + V
.
Lance a venda
: O sistema abrirá a tela de venda. Realize a venda normalmente, lembrando de selecionar a opção
ORÇAMENTO
no canto superior direito.
Verifique a receita
: Se necessário, clique no ícone de
IMAGEM
para visualizar a receita.
Salve a venda
: Depois de lançar a venda, salve-a e feche a tela de venda para retornar ao módulo
SYNC
ORÇAMENTO
.
Passo 3: Confirmando e Enviando o Orçamento
Confirme o orçamento
: Apó
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Guia Completo dos Relatórios do FarmaFácil — 16/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/475844
> Publicado em: 16/06/2024

O FarmaFácil é uma solução completa para gestão de farmácias de manipulação e drogarias, oferecendo uma ampla gama de relatórios que ajudam na administração e controle dos processos. A seguir, detalhamos cada tipo de relatório disponível, agrupados por categorias:
Relatórios de Estoque
1. Movimento de Estoque: Registra todas as entradas e saídas de produtos, permitindo o acompanhamento detalhado do fluxo de mercadorias.
2. Movimento de Lote: Acompanha a movimentação de lotes específicos, essencial para rastreabilidade e controle de validade.
3. Posição de Estoque: Fornece uma visão consolidada do estoque atual, incluindo quantidades e valores.
4. Estoque Mínimo Máximo: Auxilia no controle de níveis de estoque, indicando quando é necessário realizar reposições.
5. Compras por Produto: Detalha as compras realizadas por produto, facilitando o controle de despesas e a gestão de fornecedores.
6. Nota Fiscal de Entrada: Registra todas as notas fiscais recebidas, fundamental para a conformidade fiscal e controle de estoque.
7. Lote por Fornecedor: Relatório que vincula lotes a seus respectivos fornecedores, importante para a rastreabilidade e controle de qualidade.
8. Produtos a Vencer: Lista os produtos com datas de vencimento próximas, essencial para evitar perdas e garantir a qualidade dos produtos comercializados.
9. Relatório de Compras: Resumo das compras realizadas em um determinado período, facilitando o controle financeiro e de estoque.
10. SNGPC: Relatórios específicos para o Sistema Nacional de Gerenciamento de Produtos Controlados, garantindo a conformidade com a legislação.
11. Recolhimento de ICMS: Relatório para controle de impostos sobre circulação de mercadorias, ajudando na conformidade tributária.
12. Acerto de Estoque: Permite ajustes manuais no estoque, essencial para correções e auditorias.
13. Consumo por Produto: Relatório que detalha o consumo de produtos, útil para planejamento e controle de estoque.
14. Transferência de Estoque: Registra transferências de estoque entre unidades ou locais, facilitando a gestão logística.
15. Cobertura de Estoque: Informa sobre o tempo de cobertura do estoque atual com base no consumo médio, ajudando na gestão de reposições.
Relatórios de Vendas
1. Emissão de Rótulos: Relatório para a emissão de rótulos de produtos, essencial para a conformidade e apresentação dos produtos.
2. Vendas por Médico: Detalha as vendas associadas a prescrições médicas, importante para a análise de demanda e relacionamento com médicos.
3. Vendas por Período: Resumo das vendas realizadas em períodos específicos, facilitando a análise de desempenho.
4. Vendas por Produto: Relatório que detalha as vendas por produto, essencial para a gestão de estoque e análise de popularidade dos itens.
5. Vendas por Cliente: Acompanha as vendas realizadas para cada cliente, ajudando na análise de comportamento de compra e fidelização.
6. Vendas por Vendedor: Detalha as vendas realizadas por cada vendedor, importante para a análise de de
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Volume Padrao de capsulas — 13/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/475464
> Publicado em: 13/06/2024

No sistema de gestão de farmácias FarmaFácil, a configuração correta do volume das cápsulas é essencial para assegurar a precisão das dosagens e a eficiência no processo de manipulação. Este artigo fornecerá uma visão geral sobre como configurar o volume padrão das cápsulas utilizando as informações fornecidas e como isso se aplica no sistema.
Tabela de Capacidades de Cápsulas
Tamanho da Cápsula
Volume Teórico (ml)
Peso Médio de Enchimento (mg)
000
1.37
615 (leve), 960 (médio), 1370 (pesado)
00
0.95
430 (leve), 665 (médio), 950 (pesado)
0
0.68
305 (leve), 475 (médio), 680 (pesado)
1
0.50
225 (leve), 350 (médio), 500 (pesado)
2
0.37
165 (leve), 260 (médio), 370 (pesado)
3
0.30
135 (leve), 210 (médio), 300 (pesado)
4
0.21
95 (leve), 145 (médio), 210 (pesado)
5
0.14
60 (leve), 90 (médio), 130 (pesado)
Configuração no Sistema FarmaFácil
Para configurar o volume das cápsulas no sistema FarmaFácil, siga os passos abaixo:
1. Acesso ao Módulo de Configuração:
- Navegue até o menu principal do sistema e selecione o módulo de configuração de cápsulas.
2. Seleção do Tipo de Cápsula:
- Escolha o tipo de cápsula que deseja configurar. Por exemplo, se estiver configurando cápsulas do tipo '00', selecione a opção correspondente no sistema.
3. Preenchimento dos Dados:
- Preencha os campos conforme a tabela de capacidades de cápsulas.
- Volume Interno (ml): Digite o volume teórico da cápsula conforme a tabela. Para a cápsula '00', insira `0,95 ml`.
- Volume Total (ml): Insira o volume total se houver necessidade. No exemplo da cápsula '00', este valor seria `2,90 ml`.
4. Salvar Configurações:
- Após preencher todos os campos necessários, clique no botão de salvar para armazenar as configurações.
Considerações Finais
A configuração correta do volume das cápsulas garante que o sistema FarmaFácil possa calcular com precisão as dosagens necessárias para cada receita, evitando erro e assegurando a satisfação do cliente.
Se houver dúvidas ou dificuldades durante o processo de configuração, recomenda-se consultar o suporte técnico do sistema ou os manuais de ajuda disponíveis na plataforma.
Exemplos Visuais
A imagem abaixo exemplifica como a configuração deve ser feita no sistema para uma cápsula do tipo '00':
Conclusão
A configuração precisa do volume das cápsulas é um passo crucial no processo de manipulação de medicamentos. Seguir as orientações descritas neste artigo ajudará a garantir a eficácia do sistema FarmaFácil e a precisão das dosagens preparadas.
Se precisar de assistência adicional, não hesite em entrar em contato com nosso suporte técnico.

---

## 🟡 Configuração Gmail FarmaFácil — 07/06/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/474468
> Publicado em: 07/06/2024

Configurando o Gmail no FarmaFácil: Um Guia Passo a Pas
so
O Gmail é uma ferramenta essencial para comunicação e gerenciamento de e-mails, e integrá-lo com outros serviços pode ser crucial para a eficiência operacional de empresas como a FarmaFácil. Neste guia, vamos abordar o processo detalhado para configurar sua conta Gmail no FarmaFácil, garantindo segurança e funcionalidade.
Passo 1: Acesso às Configurações da Conta do Google
O primeiro passo é acessar as configurações da sua conta do Google. Para isso, siga os passos abaixo:
Faça login na sua conta do Gmail.
2. Clique na sua foto de perfil no canto superior direito da página e selecione "Gerenciar sua conta do Google".
Passo 2: Configurações de Segurança
Dentro do painel de gerenciamento da conta, navegue até a aba "Segurança". Aqui, você encontrará várias opções relacionadas à segurança da sua conta.
Passo 3: Ativar Verificação em Duas Etapas
É fundamental garantir a segurança da sua conta habilitando a Verificação em Duas Etapas. Este processo adiciona uma camada extra de segurança exigindo uma segunda forma de autenticação para acessar sua conta.
Passo 4: Gerar Senha para Aplicativos
Após ativar a Verificação em Duas Etapas, você terá a opção de gerar senhas específicas para aplicativos. Esta etapa é essencial para permitir que o FarmaFácil se conecte à sua conta do Gmail de forma segura.
Dentro das configurações de segurança, encontre a opção "Senhas de app" e selecione "Outro (Nome personalizado)".
2. Insira um nome para identificar o aplicativo, por exemplo, "FarmaFácil", e clique em "Gerar". Uma senha exclusiva será gerada para esse aplicativo.
Passo 5: Configuração no FarmaFácil
Com a senha gerada, agora é hora de configurar sua conta no FarmaFácil. Siga estas etapas:
Abra as configurações de integração SMTP no FarmaFácil.
2. Insira as seguintes informações:
- Servidor SMTP: smtp.gmail.com
- Porta: 587
- Usuário: Seu endereço de e-mail do Gmail (EmailCliente@gmail.com)
- Senha:
Insira a senha gerada no passo anterior.
- Autenticação: Sim
- TLS: Sim
Após inserir todas as informações, salve as configurações e teste a conexão para garantir que tudo esteja funcionando corretamente.
Seguindo este guia passo a passo, você poderá configurar sua conta do Gmail no FarmaFácil de forma segura e eficiente, garantindo uma comunicação fluida e eficaz em sua empresa.

---

## 🟡 Como obter o selo de verificação no WhatsApp Business — 31/05/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/472935
> Publicado em: 31/05/2024

O selo verde de verificação no WhatsApp Business é um distintivo de confiança e autenticidade que pode aumentar a credibilidade da sua empresa. No entanto, para obtê-lo, é necessário seguir alguns requisitos e passos específicos. Este artigo fornecerá orientações detalhadas sobre como garantir o selo verde no WhatsApp Business.
Requisitos para o selo verde WhatsApp:
1.Gerenciador de negócios verificado: Configure o Gerenciador de Negócios com autenticação de dois fatores e certifique-se de que o nome de exibição corresponda ao nome da sua empresa.
2.Avaliação de alta qualidade: Mantenha uma presença profissional e envolvente em sua conta do WhatsApp Business.
3. Conformidade com os termos do WhatsApp: Certifique-se de não violar os termos de uso do WhatsApp e sua Política Comercial.
4. Marca notável e respeitável: Tenha uma marca reconhecida e respeitada no mercado.
5. **Atividades online e offline: Possua um link para uma página no Facebook com pelo menos 10.000 curtidas orgânicas, um site de negócios de qualidade e exposição suficiente na mídia.
Guia passo a passo para solicitar o selo verde:
1. Acesse o Gerenciador de Negócios do Facebook e navegue até Conta > Contas do WhatsApp > Gerenciador do WhatsApp.
2. Selecione o número de telefone associado à conta que deseja aplicar para o selo verde.
3. Clique em "Enviar Solicitação" e preencha todas as informações necessárias.
4. Aguarde o processo de revisão, que geralmente leva de 5 a 7 dias úteis.
5. Continue usando sua conta do WhatsApp Business normalmente durante o período de revisão.
6. Se a solicitação for negada, você ainda pode usar sua conta sem restrições.
7. Se a solicitação for aprovada, o selo verde será automaticamente exibido na sua conta do WhatsApp Business.

---

## 🟡 Procedimento para Exclusão de Movimentações e Imagens de Receitas no FarmaFácil — 28/05/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/472349
> Publicado em: 28/05/2024

Procedimento para Exclusão de Movimentações e Imagens de Receitas no FarmaFácil
No sistema FarmaFácil, o usuário administrador tem acesso a várias opções de manutenção através do menu UTILITÁRIO. Entre essas opções, estão as funcionalidades de EXCLUIR MOVIMENTAÇÃO e EXCLUIR IMAGENS DE RECEITAS. Utilizar essas ferramentas é essencial para manter o desempenho do sistema, especialmente quando se trata de dados com mais de 10 anos.
Essas funções foram desenvolvidas para que bancos de dados com movimentações de vários anos possam excluir determinados períodos que já não são mais necessários, como repetições de vendas ou pesquisas de histórico de clientes muito antigos. Com isso, o sistema ganha mais performance e o banco de dados fica mais compacto, gerando resultados diários com melhor desempenho e agilidade.
Benefícios da Limpeza de Dados
Realizar a limpeza de dados antigos é uma boa prática para garantir que o sistema opere de forma eficiente e rápida. A exclusão de dados que não são mais necessários pode melhorar significativamente a performance do sistema, reduzindo o tempo de resposta e a carga no banco de dados.
Utilizando a função específica do sistema Farma Fácil para excluir movimentações antigas, sua farmácia pode alcançar os seguintes benefícios:
Melhoria na Performance:
A redução do volume de dados aumenta a velocidade de processamento, permitindo que o sistema execute operações e consultas mais rapidamente.
Banco de Dados Compacto:
Com menos dados para gerenciar, o banco de dados se torna mais compacto, facilitando sua manutenção e gerenciamento.
Agilidade nas Operações Diárias:
Um sistema mais rápido e eficiente resulta em operações diárias mais ágeis, melhorando a produtividade da farmácia.
Redução da Carga no Sistema:
A exclusão de dados desnecessários diminui a carga no sistema, liberando recursos para outras tarefas importantes.
Manutenção Facilitada:
Um banco de dados menor e mais organizado é mais fácil de manter, o que pode reduzir o tempo de processamento na realização de backup.
PASSO A PASSO PARA EXECUTAR OS PROCEDIMENTOS
EXCLUIR MOVIMENTAÇÃO
Descrição:
Esta funcionalidade permite ao Administrador do sistema excluir registros de movimentações no sistema até uma data especificada. As movimentações a serem excluídas incluem todas as transações registradas,
como vendas, compras, ajustes de estoque, caixa, notas de entrada, entre outros.
Como usar:
Acesse o menu UTILITÁRIO.
Selecione a opção EXCLUIR MOVIMENTAÇÃO.
Informe a data limite até a qual as movimentações serão excluídas. (A data limite será o período de corte/exclusão da movimentação. Suponhamos que você possua um banco de dados com 10 anos de movimentação, e deseja excluir 5 anos de movimentação. O período final que será informado é 31/12/2019. O sistema irá manter apenas as movimentações a partir de 01/01/2020 até a data atual.)
Nota
: Recomendamos realizar a exclusão em etapas para maior segurança e controle. Se você tem 10 anos de dados, pode fazer a exclusão em 5 etap
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Sua Impressora Não Imprime? Saiba o Que Fazer Antes de Abrir um Ticket (Pré-requisitos) — 21/05/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/470602
> Publicado em: 21/05/2024

Para garantir um atendimento eficiente e focado no nosso escopo de trabalho, criamos este guia com procedimentos que devem ser
seguidos antes de abrir um ticket de suporte referente
a problemas de impressão.
A PrismaFive é responsável apenas pela configuração do sistema  Farmafácil para realizar a impressão.
Problemas gerais de impressão NÃO fazem parte do nosso escopo de trabalho.
Verificação Inicial: Impressão de Página de Teste
Antes de abrir um ticket,
por favor, siga as etapas abaixo para verificar a funcionalidade da sua impressora:
1. Imprima uma Página de Teste:
- No Windows, clique no botão Iniciar e depois em Configurações (ícone de engrenagem).
- Vá para Dispositivos e clique em Impressoras e scanners.
- Encontre sua impressora na lista, clique nela e depois clique em Gerenciar.
- Clique em Imprimir página de teste.
2. Resultado da Impressão de Teste:
-
Se a folha de teste não imprimir ou imprimiu de forma incorreta:
O
problema está fora do nosso escopo de suporte
e deve ser tratado por um técnico de informática. Verifique as dicas abaixo antes de chamar o técnico.
-
Se a folha de teste imprimir e esta correta
, mas houver problemas ao imprimir através do Farmafácil: Entre em contato com o nosso suporte abrindo um ticket.
Dicas para Solução de Problemas de Impressão
Caso a impressora não esteja imprimindo a folha de teste, siga estas dicas para tentar resolver o problema antes de chamar o técnico de informática:
1. Reinicie o computaodor
- Muitos problemas já são resolvidos com este passo
2. Verifique as Conexões:
- Certifique-se de que todos os cabos estejam conectados corretamente. Verifique o cabo de energia e o cabo USB (ou cabo de rede, se a impressora for de rede).
-Troque a Porta USB:
Desconecte o cabo USB da porta atual, conecte-o em outra porta USB disponível e reinicie a impressora.
- Se estiver usando uma impressora sem fio, certifique-se de que ela esteja conectada à rede Wi-Fi corretamente.
3
. Reinicie a Impressora:
- Desligue a impressora pressionando o botão de ligar/desligar. Aguarde alguns segundos e ligue-a novamente.
4. Verifique os Níveis de Tinta/Toner e Papel:
- Abra a bandeja de papel e certifique-se de que há papel suficiente.
- Verifique os cartuchos de tinta ou toner. Se estiverem vazios ou quase vazios, substitua-os.
5. Verifique a fila de impressão
- Verifique a fila de impressão para ver se há documentos pendentes que possam estar bloqueando a impressão. Cancele ou exclua esses documentos, se necessário.
Chamando um Técnico de Informática
Se, após seguir estas dicas, a
impressora ainda NÃO imprimir a folha de teste
, será necessário chamar um técnico de informática para resolver o problema. O técnico deve garantir que a impressora esteja funcionando corretamente e
consiga imprimir a folha de teste. S
omente após essa confirmação, caso ainda haja problemas de impressão de arquivos através do sistema Farmafácil, um ticket de suporte deve ser aberto com a PrismaFive.
Abrindo um Ticket de Suporte com a PrismaF
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Erro ao instalar impressora via rede - Com configurar a impressora via porta LPR — 20/05/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/470330
> Publicado em: 20/05/2024

Introdução
Instalar uma impressora via rede no Windows pode resultar em erros frustrantes, como a mensagem "NÃO FOI POSSÍVEL INSTALAR A IMPRESSORA NO WINDOWS". Felizmente, é possível contornar este problema configurando a impressora através de uma porta LPR (Line Printer Remote). Este guia detalhado explicará o passo a passo necessário para realizar essa configuração.
Passo 1: Ativar o Monitor de Porta LPR
Acesse o Painel de Controle
:
Clique no botão Iniciar e selecione
Painel de Controle
.
Navegue até
Programas e Recursos
.
No canto esquerdo, selecione
Ativar ou Desativar Recursos do Windows
.
Habilite o Monitor de Porta LPR
:
Na janela que abrir, encontre a pasta
Serviços de Impressão e Documentos
.
Marque a opção
Monitor de Porta LPR
.
Realize esse processo tanto na máquina onde você deseja instalar a impressora quanto na máquina à qual a impressora está fisicamente conectada via cabo. É obrigatório realizar em ambas as máquinas.
Passo 2: Adicionar uma Impressora
Acesse Dispositivos e Impressoras
:
No
Painel de Controle
, selecione
Dispositivos e Impressoras
.
Clique em
Adicionar uma impressora
.
Selecionar Impressora
:
Na janela que abrir, escolha a opção
A impressora que eu quero não está na lista
.
Passo 3: Configuração Manual da Impressora
Adicionar uma Impressora Local ou de Rede
:
Selecione a opção
Adicionar uma impressora local ou de rede usando configurações manuais
.
Passo 4: Configurar a Porta LPR
Criar uma Nova Porta
:
Na aba seguinte, selecione
Criar uma nova porta
e escolha
Porta LPR
.
Uma nova tela aparecerá com dois campos para preencher.
Preencher Campos de Configuração
:
No primeiro campo, insira o
nome da máquina
à qual a impressora está fisicamente conectada.
No segundo campo, insira o
nome da impressora
conforme consta na máquina à qual ela está fisicamente conectada.
Conclusão
Depois de seguir esses passos, a impressora aparecerá no painel de
Dispositivos e Impressoras
e estará pronta para uso. Faça um teste de impressão para garantir que tudo está funcionando corretamente. No caso de integração com softwares específicos como o Farma Fácil, use o nome que consta no painel de controle para configurar a impressora.
Observação
: Em alguns casos, pode ser necessário inserir o nome da máquina antes do nome da impressora ao configurá-la.
Seguindo este guia, você deve conseguir instalar sua impressora de rede sem problemas, utilizando a configuração de porta LPR para contornar os erros de instalação típicos do Windows.

---

## 🟡 Falhas na impressão possíveis causas — 10/05/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/468596
> Publicado em: 10/05/2024

Existem várias causas para falhas de impressão:
1. Mais de uma impressora com o mesmo nome:
Ter duas impressoras com o mesmo nome pode causar problemas na impressão, resultando em falhas intermitentes. Para resolver essa questão:
-
Impressoras Locais
: A equipe de suporte pode realizar o procedimento de renomear a impressora.
-
Impressoras Compartilhadas
: É recomendável orientar a farmácia ou o responsável pelo local a solicitar a assistência de um técnico de informática para renomear uma das impressoras.

---

## 🟡 Comunicado Ativação Contingência - Nota Fiscal — 08/05/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/468098
> Publicado em: 08/05/2024

ATENÇÃO: O ENVIO DE DOCUMENTOS FISCAIS FOI NORMALIZADO. POR FAVOR, AQUELES QUE ATIVARAM A CONTINGÊNCIA, DESMARQUEM ESSA OPÇÃO.
------------------------------------------------------------------------------------------------------------------------------------------------AVISO ENVIADO DIA 07/MAIO----------------------------------------------------------------------------------------------------------------------------------------
Prezado cliente,
URGENTE
Gostaríamos de informar que estamos enfrentando problemas no envio de notas fiscais pelo sistema FARMAFÁCIL, devido à instabilidade do Sefaz. Este cenário é consequência das dificuldades ocasionadas pelas enchentes que afetam o estado do RS, resultando na ativação da contingência em todos os Documentos Fiscais Eletrônicos (DFes) nos ambientes autorizadores pertencentes ao AN-RS.
Para contornar temporariamente essa situação, recomendamos a
ativação da contingência
, seguindo as instruções detalhadas no seguinte artigo: ➡️Como Emitir Documentos Fiscais em Contingência:
https://prismafive.movidesk.com/kb/pt-br/article/467829/
como-emitir-documentos-fiscais-em-contingencia
Pedimos gentilmente que o usuário administrador do seu sistema FarmaFácil siga essas orientações.
Estamos à disposição para prestar qualquer suporte técnico necessário e esclarecer eventuais dúvidas.
Fonte: SEFAZ VIRTUAL RS - Avisos
https://dfe-portal.svrs.rs.gov.br/Nfe/Avisos
Atenciosamente,
Suporte PrismaFive.
Fone(47) 3045-9800 opção 2.

---

## 🟡 Como Emitir Documentos Fiscais em Contingência — 07/05/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/467829
> Publicado em: 07/05/2024

Este guia visa orientar o Analista de Suporte em como proceder em situações onde seja necessária a emissão de Documentos Fiscais em Contingência por parte dos clientes Prisma Five.
O que é Nota Fiscal ou NFC-e em Contingência?
Nota Fiscal ou NFC-e em contingência é um termo utilizado na área de contabilidade e gestão fiscal para se referir a uma situação na qual a emissão da nota fiscal eletrônica não pode ser feita de forma regular e automática, conforme estabelecido pela legislação tributária. Isso pode ocorrer por diversos motivos, como problemas técnicos no sistema da empresa, falhas na comunicação com o servidor da Secretaria da Fazenda, ou qualquer outra situação que impeça a geração normal da nota fiscal.
Nessas situações, a empresa pode optar por emitir a nota fiscal em contingência, ou seja, de forma alternativa, garantindo assim a continuidade das suas operações comerciais e o cumprimento das obrigações fiscais. Existem diferentes tipos de contingência, como a
contingência offline
, onde a nota fiscal é emitida sem a necessidade de conexão com a internet, e a
contingência SVC
(Sefaz Virtual de Contingência), onde a nota fiscal é transmitida para a Secretaria da Fazenda de forma diferenciada, para posterior autorização.
É importante ressaltar que, mesmo emitida em contingência, a nota fiscal tem validade jurídica e fiscal, desde que respeitadas as normas estabelecidas pela legislação tributária.
Como habilitar Nota Fiscal Eletrônica em Contingência dentro do Farma Fácil?
Dentro do Farma Fácil, é possível habilitar a emissão de
Nota Fiscal Eletrônica em Contingência no modo SVC
(Sistema de Validação e Autenticação de NF-E). Não é possível habilitar a opção "Nota Fiscal em Contingência Offline" para Notas Fiscais Eletrônicas, função disponível apenas para emissão de NFC-e.  Para habilitar a contingência para NF-e ou NFC-e, siga o processo abaixo:
- Habilitar a contingência dentro da tela "Parâmetros" no Farma Fácil.
Clique em "Arquivo", em seguida "Parâmetro". Na tela que se abrirá, atente-se: para clientes com filiais, deve-se acessar o menu
FILIAL
. Em clientes sem filiais, acessar o menu
PARÂMETRO
, conforme imagem abaixo:
- Selecionar a opção "Nota Fiscal em Contingência"
Para Notas Fiscais Eletrônicas em contingência, selecione a aba
NFe/Sped
, em seguida marque a opção
Emitir NF-e em contingência
, depois clique em
Salvar
, conforme imagem abaixo:
Após este processo, o sistema estará emitindo Notas Fiscais Eletrônicas em caráter de contingência.
Como habilitar a emissão de NFC-e em Contingência dentro do Farma Fácil?
Para emissão de NFC-E em contingência, ainda na tela de
"Parâmetro"
, acesse a aba
CupomFiscal/NFCe/Sat
e marque a função de acordo com a necessidade do cliente:
- Emitir NFC-e em contingência
: situação adequada para quando os servidores do Governo Federal estejam indisponíveis por catástrofes, manutenções ou outros motivos. Neste caso, é possível habilitar o NFC-e em contingência para envio posterior dos documentos fis
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Configuração da Nota Fiscal de Serviço (NFSe) no FarmaFacil — 26/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/466073
> Publicado em: 26/04/2024

Configuração da Nota Fiscal de Serviço (NFSe) no FarmaFacil
A emissão de Notas Fiscais de Serviço Eletrônicas (NFSe) é uma prática crucial para empresas, incluindo farmácias de manipulação. Este guia passo a passo aborda os requisitos e processos para configurar a NFSe no sistema FarmaFacil.
Passo 1: Verificar o Provedor Utilizado pela Prefeitura
Antes de iniciar a configuração, é essencial saber qual provedor a prefeitura utiliza para emissão de NFSe. Isso pode ser verificado durante o login no portal da prefeitura ou através do site da TecnoSpeed.
Passo 2: Requisitos para Configuração
Antes de iniciar a configuração no sistema FarmaFacil, certifique-se de ter as seguintes informações:
CNPJ da empresa
Inscrição Municipal
ID CNAE (Código de Tributação do Município)
Código de Atividade da Farmácia (Item da lista de serviços)
Alíquota de ISS
Certificado Digital
Login e senha de acesso ao portal da prefeitura
WebService utilizado pela prefeitura para emissão das notas de serviço
Manual de Integração
Regime de tributação da empresa
Passo 3: Configuração no Sistema FarmaFacil
Acesse Arquivo > Parâmetro > Parâmetro ou Filial (se houver filial).
Certifique-se de que os dados como CNPJ, Inscrição Municipal e Regime de Tributação estejam corretamente informados, pois são cruciais para o envio das notas.
Na aba NFE deve-se colocar o caminho da logo e informar o código CNAE e qual tipo de nota será emitido e vincular o certificado digital válido.
Passo 4: Configuração do Provedor Dentro do FarmaFacil
Na aba NFSe/CFSe basta localizar o Campo Provedor NFSe e clicar no simbolo de inserir
Após isso abrirá a tela de configuração de provedor onde deverá ser informado o campo nome do provedor, nome da pasta de schema do provedor, padrão do provedor e formato da aliquota.
Existem oito padrões de configurações disponíveis no FarmaFacil. Os mais utilizados são:
ABRASF:
Configuração inicial do sistema, com configurações de link e código fonte menos utilizáveis atualmente.
IPM:
Utilizado para o provedor IPM, com um link padrão específico.
NFSeNet:
Utilizado pelo provedor Bauhaus, onde o sistema gera um arquivo TXT para importação pelo aplicativo.
São Paulo - SP:
Exclusivo para a cidade de São Paulo.
DLLPrismaFive e DLLPrismaFiveX:
Utiliza o projeto ACBR, configurável para várias cidades através de um único componente/DLL.
https://prismafive.movidesk.com/kb/pt-br/article/466115/
configurar-provedor-de-nfse-no-padrao-dllprismafive
TecnoSpeed:
Integração terceirizada paga por CNPJ.
Passo 5: Preenchimento das Informações da NFSe no FarmaFacil
Após configurar o provedor, ainda na aba NFSe/CFSe e preencha as demais informações necessárias. Certifique-se de preencher todos os campos obrigatórios, identificados em vermelho.
Após salvar as configurações basta testar a emissão.
Seguindo este guia passo a passo, a configuração da NFSe no sistema FarmaFacil estará completa, permitindo a Lançamento de notas fiscais de serviços eletrônicas de forma eficientes. Certifique-se de reali
[... conteúdo truncado para otimizar contexto ...]

---

## 🟡 Atualização de Preços Santa Cruz — 24/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/465472
> Publicado em: 24/04/2024

1º LISTA DE PREÇOS!
Para gerar uma lista dos medicamentos, e essa lista ser importada no Farma Fácil, é preciso entrar no site
https://clientes.stcruz.com.br/portal-nsd/#/login
e logar com seus credenciais (Caso não saiba seu login e senha, entrar em contato com seu vendedor da santa cruz e solicitar)
Logado no site da stcruz, para gerar o arquivo, é só clicar no ícone
Após clicar no ícone, você vai informar os filtros corretamente.
ESTADO
é o estado aonde fica a farmácia,
TIPO LISTA
é sempre a padrão santa cruz,
TIPO SUBLISTA
quase sempre é medicamentos mas pode ser também a de perfumaria, e o
TIPO DO ARQUIVO
é texto.
2º IMPORTAÇÃO DO ARQUIVO!
Após gerado o arquivo, é só ir no sistema, no caminho ARQUIVO>UTILITARIO>IMPORTAÇÃO ARQUIVOS
Já na tela, tu vai em IMPORTAÇÃO DE ARQUIVO, e seleciona a opção SANTA CRUZ, após isso só encontrar o arquivo que foi gerado no site, e importa!

---

## 🟡 Médicos que mais venderam no período - GRAFICO — 24/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/465438
> Publicado em: 24/04/2024

Dentro do sistema Farma Fácil, você pode pesquisar os médicos que mais venderam no período, de diversas formas, nesse artigo ensinaremos como gerar o relatório no formato de GRAFICO.
1° - Para isso, precisaremos seguir o caminho dentro do sistema, VENDAS>RELATORIO>VENDAS POR MEDICO:
2° - Após isso, com a tela de filtros do relatório aberta, selecionar a opção GRAFICO, e selecionar os filtros desejados:
QUANTIDADE: RELATORIO SERA SOBRE O MEDICO QUE MAIS TEVE QUANTIDADE DE VENDAS NO PERIODO SELECIONADO.
VALOR: RELATORIO SERA SOBRE OS MEDICOS QUE MAIS VENDERAM EM VALOR NO PERIODO SELECIONADO.
MEDICO: RELATORIO SERA ORDENADO ENTRE OS MEDICOS QUE MAIS MOVIMENTARAM OU POR QUANTIDADE OU POR VALOR.
ESPECIALIDADE: RELATORIO SERA ORDENADO DE ACORDO COM AS ESPECIALIDADES QUE MAIS MOVIMENTARAM OU POR QUANTIDADE OU POR VALOR.
MOSTRAR: CAMPO AONDE GERALMENTE JA VEM COM 10 SELECIONADO, NELE VOCÊ PODE SELECIONAR QUANTOS MEDICOS OU ESPECIALIDADES VOCÊ QUER QUE O RELATORIO TRAGA(POR EXEMPO, SE ESTIVER 10 NO CAMPO, ELE TRARA OS 10 MEDICOS OU ESPECIALIDADES QUE MAIS MOVIMENTARAM OU POR QUANTIDADE OU POR VALOR)
3º - Após selecionar os filtros, o relatório será retornado em tela:

---

## 🟡 Guia de cadastro e controle de usuários e grupos — 23/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/465156
> Publicado em: 23/04/2024

➡️ Neste guia, vamos explicar de forma simples como administrar usuários em um sistema, permitindo adicionar, editar e gerenciar perfis de acesso de maneira eficiente. Este procedimento é útil especialmente em ambientes como farmácias, onde é necessário controlar com precisão quem pode acessar quais recursos.
Passo 1: Acessando o Menu de Usuários
Para começar, abra o sistema e navegue até o menu de acesso. Geralmente, isso envolve clicar em "Acesso", depois "Arquivo" e finalmente "Usuário".
Passo 2: Adicionando ou Editando Usuários
- Adicionar Usuário Novo:
Para adicionar um novo usuário, clique no ícone de adição (+).
- Editar Usuário Existente:
Se precisar editar um usuário já cadastrado, use o ícone do lápis.
Preencha os dados solicitados corretamente,e selecione o nível, que nesse caso tratamos de
usuário e administrador:
- Administrador:
Não precisa de senha para certas operações, como liberar descontos.
- Usuário Comum:
Requer a senha de um administrador para liberar descontos.
Passo 3: Criando e Gerenciando Grupos
Você também pode criar grupos para organizar usuários em funções específicas,  como no exemplo abaixo:
Para gerenciar o grupo criado é necessário acessar Acesso>Movimento>Acesso Usuário
Segue o mesmo padrão de criação e edição.
Primeiro passo é selecionar o grupo a ser gerenciado.
Segundo passo é selecionar o modulo especifico que será feita a vinculação com o grupo, por exemplo:
Você pode liberar apenas módulos que a sua farmacêutica utiliza, não possui a necessidade de ter acesso ao modulo de administradora de cartão.
Passo 4: Atribuindo Funções aos Usuários do grupo
Após escolher o módulo, pode escolher as funções que o usuário desse grupo consegue ter acesso.
➡️É importante designar um usuário específico na farmácia para gerenciar essas configurações de usuários e grupos.
Com esses passos simples, você poderá administrar os usuários do sistema de forma eficiente, garantindo que apenas as pessoas certas tenham acesso às funcionalidades necessárias para suas tarefas diárias na farmácia.

---

## 🟡 Registro Manual de DLLs quando dá o Erro de Classe não Registrada para Emissão de Documentos Fiscais no FarmaFacil. — 22/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/464931
> Publicado em: 22/04/2024

Esse processo é utilizado quando por algum bloqueio do sistema, o arquivo de extensão .BAT do MENUTESTE é bloqueado por sistema, antivírus, entre outros.
Mas para uma introdução mais assertiva, o que são DLL's?
DLLs (Dynamic Link Libraries) são arquivos que contêm código e dados que podem ser usados por mais de um programa ao mesmo tempo. Eles permitem que diferentes programas compartilhem recursos, como funções e procedimentos, economizando espaço em disco e facilitando a manutenção. DLLs ajudam a organizar e modularizar o código de um programa, tornando-o mais fácil de desenvolver e atualizar. Em resumo, são como bibliotecas de código reutilizáveis que múltiplos programas podem acessar simultaneamente.
O erro "Classe não registrada" no FarmaFácil
O erro pode acontecer em algumas situações relacionadas a envio, estorno, validação de notas fiscais, entre outros,  conforme imagem abaixo:
Então para o registro correto das DLL's de forma manual no Windows, visando a correção do problema, vamos ao processo:
Em sistema operacional 32 BITS:
1° passo
:  Copiar e Colar as DLL's "capicom.dll, msxml5.dll e msxm5lr.dll"  para a pasta System32 do Windows (C:\Windows\System32).
2° passo:
Execute o CMD como Administrador.
3° passo:
Execute cada comando abaixo, de forma individual:
%SystemRoot%\system32\regsvr32 capicom.dll
Em seguida, o próximo comando:
%SystemRoot%\system32\regsvr32 msxml5.dll
Em computadores com Windows 7 ou superior, com arquitetura 64 Bits:
1° passo
:  Copiar e Colar as DLL's "capicom.dll, msxml5.dll e msxm5lr.dll"  para a pasta SysWOW64 do Windows (C:\Windows\SysWOW64).
2° passo:
Execute o CMD como Administrador.
3° passo:
Execute cada comando abaixo, de forma individual:
%SystemRoot%\Syswow64\regsvr32 capicom.dll
Em seguida, o próximo comando:
%SystemRoot%\Syswow64\regsvr32 msxml5.dll
Após a execução dos comandos e as mensagens de êxito, tente emitir Notas Fiscais à partir do FarmaFácil.
Sistema operacional 32 Bits
:
Copiar e colar as DLL
's citadas acima para a pasta System
3
2
.
(
c
:
\Windows
\System32
) Executar o CMD como administrador
, copiar e colar no CMD as linhas abaixo de forma individual
:

---

## 🟡 Cadastro de usuários - SYNC — 19/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/464629
> Publicado em: 19/04/2024

A Importância de Ter Seu Próprio Login e Senha no PrismaSync
O PrismaSync é muito mais do que uma simples plataforma; é uma ferramenta essencial para conectar pessoas, ideias e projetos. No entanto, sua utilidade vai além da mera conveniência. A segurança e a privacidade dos nossos usuários são fundamentais, e é por isso que cada indivíduo deve possuir seu próprio login e senha para acessar o PrismaSync. Aqui estão algumas razões pelas quais isso é tão importante:
Identificação Precisa
:
Ter um login pessoal permite que o PrismaSync identifique com precisão cada usuário. Isso é crucial para garantir que apenas as pessoas autorizadas tenham acesso à plataforma. Ao usar seu próprio login, você ajuda a manter a integridade do sistema e a proteger as informações compartilhadas dentro dele
.
Controle de Acesso
: Com seu próprio login e senha, você tem controle total sobre quem pode acessar sua conta. Isso significa que você pode garantir que suas informações permaneçam privadas e seguras. Além disso, caso haja necessidade de revogar o acesso de alguém, você pode fazê-lo facilmente, sem afetar outras contas.
Responsabilidade Individual
: Ao atribuir a cada usuário seu próprio login, promovemos a responsabilidade individual. Cada pessoa é responsável por suas ações
dentro da plataforma. Isso cria um ambiente de responsabilidade mútua e incentiva o uso ético e responsável do PrismaSync.
Rastreabilidade
: Se cada usuário tiver seu próprio login, fica mais fácil rastrear atividades e identificar possíveis problemas de segurança. Isso é essencial para manter a integridade do sistema e proteger contra atividades maliciosas.
Para cadastro de usuário no PrismaSync, é necessário ir até a aba de USUÁRIOS > ADICIONAR, conforme imagem abaixo:
Lembrando que somente usuário administradores tem acesso a esta aba.
Já na aba de Cadastro, existem alguns campos a serem preenchidos:
Nome
: Inserir no nome do usuário.
E-mail
:
Neste campo, pode ser preenchido com e-mail real ou e-mail fictício:
Exemplo: o nome de sua farmácia é FORMULAS, pode ser cadastrado como usuario@formulas.com
Senha:
definir senha de acesso.
Perfil:
neste campo, você define se será usuário comum ou administrador.
Empresa:
neste campo aparece o nome de sua Farmácia, caso tenha filiais, poderá ser listada também.
Opções adicionais:
Atendimento:
Define se o usuário fará ou não atendimento (troca de mensagens, iniciar/finalizar atendimentos).
Ativo:
Define se o usuário ficará ativo ou inativo.
Bloquear
transferência
:
Com esta opção ativa, este usuário não conseguirá fazer transferências de seu atendimento ou de outros usuários.

---

## 🔴 Como Evitar o Bloqueio das Contas do WhatsApp para Farmácias de Manipulação: Orientações e Recuperação da Conta — 16/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/463747
> Publicado em: 16/04/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Importante Ler instruções da FAQ do Whastapp e Orientações da Anfarmag sobre como proceder em caso de bloqueio:
➡️
Clique Aqui
para visualizar as orientações do
Whastapp
banimento e como recuperar
➡️   Clique Aqui
para visualizar as orientações de quem é associado da
Anfarmag
sobre banimento e como recuperar
Segue abaixo algumas informações adicionais:
Com o aumento dos bloqueios de contas do WhatsApp utilizadas por farmácias de manipulação, é essencial estar atento aos Termos de Serviço e à Política de Mensagens do WhatsApp para minimizar o risco de bloqueio ou manter a conta ativa. Abaixo estão alguns pontos fundamentais a serem observados:
1. Mantenha um Perfil Completo no WhatsApp :
Certifique-se de que seu perfil do WhatsApp  contenha informações de contato relevantes para os pacientes ou consumidores, como endereço de e-mail, endereço do site ou número de telefone.
2. Contate Apenas Usuários Autorizados:
Entre em contato com usuários do WhatsApp somente se eles forneceram seus números de celular e concordaram em ser contatados. Desenvolva seu próprio método de adesão para contato.
3. Proteja Dados Confidenciais:
Evite divulgar ou solicitar aos clientes informações sensíveis, como números completos de cartão de pagamento, números de conta bancária ou documentos de identidade, exceto quando exigido por normas legais, como a LGPD.
4. Cumpra Normas Sanitárias Vigentes:
Esteja ciente de que a comercialização de drogas sujeitas a prescrição médica por meio do WhatsApp não é permitida. No entanto, é permitido vender suplementos alimentares que não representem riscos à saúde.
5. Evite o Envio de Mensagens Automáticas ou em Massa Não Autorizadas:
Não utilize mensagens automáticas ou em massa sem autorização prévia. O envio inadequado de mensagens pode resultar em restrições à sua conta.
6. Recomendamos também utilizar a API oficial do Whastapp para integração com o Sync
Recomendamos o uso da API Oficial do WhatsApp para uma solução mais estável e eficaz. Iniciar o processo de validação para utilizar a API oficial do WhatsApp garantirá uma integração consistente e menos suscetível a interrupções. Você pode                      encontrar detalhes sobre como proceder neste processo em nossa documentação disponível aqui:
API Oficial do WhatsApp para Integração:
https://prismafive.movidesk.com/kb/pt-br/article/454086/prismasync-numero-via-api-whatsapp-oficial?ticketId=&q=
Certifique-se de adaptar essas diretrizes às necessidades específicas da sua empresa e às políticas atuais do WhatsApp Business.
Como Recuperar uma Conta Bloqueada no WhatsApp Business:
Se sua conta do WhatsApp  foi bloqueada, você pode seguir estas etapas para tentar recuperá-la:
1. Verifique o Aviso de Bloqueio:
O WhatsApp normalmente enviará uma notificação informando sobre o bloqueio e o motivo específico. Leia com atenção para entender a causa do bloqueio.
2. Acesse o Link de Recuperação Fornecido:
O WhatsApp geralmente fornece um link ou processo de recuperação direto na notificaç
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 O que é NFSE? — 03/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/460907
> Publicado em: 03/04/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O que é NFSE?
A Nota Fiscal de Serviços Eletrônica (NFS-e) é um documento de existência digital, gerado e armazenado eletronicamente em Ambiente Nacional pela Receita Federal do Brasil ou pela prefeitura municipal, para documentar as operações de prestação de serviços.
Coexistem potencialmente cerca de 5.570 legislações e Notas Fiscais de Serviços diferentes, uma para cada município.
Problema de RPS
Nesse exemplo a baixo o WebService da prefeitura de Teresina não aceita envio de nota fora da sequencia e também com  a data de emissão divergente do envio, quando a cliente realizava a emissão das notas com data diferente da atual a prefeitura retornava o erro e a nota ficava como
ENVIADA
, impossibilitando a edição e subsequente a nova tentativa de envio da mesma e da próxima nota devido o pré-requisitos do município em questão.
Erro apresentado:
Cliente fica engessado sem poder realizar as alterações necessárias para a nova tentativa de envio.
Foi implementado um novo parâmetro a partir da versão
2001.7900
que viabiliza que o cliente possa realizar a edição sem intervenção no banco de dados.
Arquivo > Parâmetro > Parâmetro > NFS-e/CFSe > Provedor NFS-e > Permitir Edição
Demonstração:
Edição aberta:
Após a alteração está novamente como
A ENVIAR:

---

## 🔴 SPED Fiscal: Um Guia para Farmácias de Manipulação — 03/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/460877
> Publicado em: 03/04/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O Sistema Público de Escrituração Digital (SPED) é uma iniciativa do governo brasileiro que visa modernizar e unificar a escrituração fiscal e contábil das empresas. Entre os diversos subprojetos do SPED, destaca-se o SPED Fiscal, que se refere à escrituração fiscal digital das operações das empresas.
O que é o SPED Fiscal?
O SPED Fiscal consiste na obrigação de transmitir eletronicamente, em formato digital, os livros fiscais e os documentos de interesse das administrações tributárias. Ele é composto pelo Livro de Controle de Produção e Estoque (Bloco K), pela Escrituração Fiscal Digital (EFD), que contempla o ICMS e o IPI, e pelo Sistema Público de Escrituração Digital das Contribuições (SPED Contribuições), que abrange PIS e COFINS.
Quais Farmácias de Manipulação Estão Sujeitas à Emissão?
Todas as farmácias de manipulação que estejam enquadradas nas condições estabelecidas pela legislação tributária estão sujeitas à emissão do SPED Fiscal. É fundamental que a contabilidade da empresa e os profissionais responsáveis pela área fiscal estejam cientes das obrigações e requisitos específicos aplicáveis ao setor.
Para Que Serve o SPED Fiscal?
O SPED Fiscal tem como principal objetivo promover a simplificação e a integração das informações fiscais das empresas, além de aumentar a eficiência na fiscalização tributária. Ele proporciona maior transparência e agilidade nos processos, reduzindo a burocracia e os custos relacionados à emissão e armazenamento de documentos fiscais.
Como Funciona o Processo de Geração do SPED Fiscal?
O processo de geração do SPED Fiscal em uma farmácia de manipulação envolve várias etapas, desde a configuração prévia do sistema até a exportação do arquivo final. A seguir, apresentamos um passo a passo simplificado:
Cadastro da Contabilidade:
No sistema de gestão utilizado pela farmácia, é necessário cadastrar os dados do contabilista responsável. Essa etapa é crucial para garantir a correta geração e transmissão das informações fiscais.
Arquivo > Parâmetro > Contabilista:
Marcação do Perfil do SPED nos Parâmetros do Sistema:
A contabilidade deve fornecer as orientações necessárias para marcar os parâmetros relacionados ao SPED Fiscal no sistema de gestão da farmácia. É importante verificar se será necessário gerar o SPED ICMS, o SPED PIS/COFINS ou ambos.
Arquivo > Parametro > Paramentro > NFe/Sped > Configurações Sped Fiscal
Cadastro dos Produtos:
Todos os produtos comercializados pela farmácia devem estar devidamente cadastrados no sistema, com informações como NCM, tributação, alíquota de ICMS, CST e CFOP preenchidas.
Arquivo > Estoque > Produto > Tributação
Cadastro dos Fornecedores:
Os fornecedores, especialmente aqueles cujos produtos são importados através de XML de entrada, devem estar cadastrados no sistema com todas as informações fiscais relevantes, como CNPJ, inscrição estadual, endereço completo e código IBGE da cidade.
Arquivo > Estoque > Fornecedor
Registro das Notas Fiscais de Entrada:
É imprescindível que tod
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Procedimento para Registro de Treinamento Interno na PrismaFive — 02/04/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/460655
> Publicado em: 02/04/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Na PrismaFive, reconhecemos a importância de manter registros precisos de todos os treinamentos internos realizados. Estes registros não apenas garantem a conformidade com os requisitos regulatórios, mas também fornecem uma base para avaliação e melhoria contínua dos programas de treinamento. Portanto, é crucial seguir um procedimento claro para documentar e relatar cada sessão de treinamento interna.
Passo 1: Preencher o Formulário de Treinamento Interno
Sempre que ocorrer um treinamento interno na PrismaFive, o primeiro passo é preencher o formulário em anexo. Este formulário contém campos importantes para capturar informações essenciais sobre o treinamento, incluindo data, horário, local, tema, instrutor e lista de participantes.
Passo 2: Coletar Assinaturas dos Participantes
Após a conclusão do treinamento, é importantel coletar as assinaturas de todos os participantes no formulário de treinamento. As assinaturas servem como prova de que os funcionários participaram da sessão e concordam com o conteúdo abordado.
Passo 3: Entregar o Formulário para o  RH da PrismaFive
O próximo passo é entregar o formulário preenchido e assinado para Kamili, que é responsável pelo departamento de Recursos Humanos na PrismaFive. Kamili será encarregada de revisar o formulário, arquivá-lo adequadamente e garantir que todas as informações relevantes sejam registradas no sistema de gestão de treinamento da empresa.
Benefícios do Procedimento de Registro de Treinamento Interno
Seguir este procedimento estruturado oferece uma série de benefícios para a PrismaFive:
1. Conformidade Regulatória: Manter registros precisos de treinamentos internos é essencial para garantir conformidade com regulamentos e normas da indústria.
2. Avaliação de Eficácia: Os registros detalhados permitem que a empresa avalie a eficácia de seus programas de treinamento, identificando áreas de melhoria e ajustando o conteúdo conforme necessário.
3. Desenvolvimento de Funcionários: O acesso a registros históricos de treinamento permite à empresa acompanhar o desenvolvimento individual dos funcionários ao longo do tempo e identificar oportunidades de crescimento e progresso.
4. Transparência e Responsabilidade: Ao coletar assinaturas dos participantes, a PrismaFive promove transparência e responsabilidade em relação ao envolvimento dos funcionários nos treinamentos oferecidos.
Em suma, seguir este procedimento para registro de treinamento interno é fundamental para o sucesso e a eficácia dos programas de desenvolvimento de funcionários na PrismaFive. Ao manter registros precisos e atualizados, a empresa demonstra seu compromisso com o crescimento e o desenvolvimento contínuo de sua equipe, contribuindo assim para o sucesso organizacional a longo prazo.

---

## 🔴 Por que há lentidão no sistema? Guia para Clientes — 28/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/460061
> Publicado em: 28/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Artigo sem tradução para esse idioma
Tente outro idioma ou clique no botão abaixo:
Ir para o idioma padrão

---

## 🔴 Monitoramento e Acompanhamento do MAPA Veterinário: Uma Visão Abrangente — 27/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/459877
> Publicado em: 27/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

No contexto da manipulação veterinária, o MAPA (Ministério da Agricultura, Pecuária e Abastecimento) desempenha um papel crucial na regulamentação e monitoramento das atividades relacionadas à produção e manipulação de produtos veterinários. Este artigo visa elucidar o conceito de MAPA veterinário, sua importância, e as obrigações inerentes ao envio de relatórios ao Ministério da Agricultura.
O que é o MAPA Veterinário?
O MAPA Veterinário se refere ao conjunto de normas, procedimentos e regulamentações estabelecidas pelo Ministério da Agricultura, Pecuária e Abastecimento, direcionadas especificamente ao controle e fiscalização das atividades relacionadas à manipulação de produtos veterinários. Este órgão governamental é responsável por assegurar a qualidade, segurança e eficácia dos produtos utilizados na saúde animal, bem como garantir o cumprimento das legislações pertinentes.
Para que serve o MAPA Veterinário?
O MAPA Veterinário desempenha diversas funções essenciais no contexto da manipulação de produtos veterinários:
Regulamentação e Fiscalização
: Estabelece normas e regulamentos para a produção, manipulação, armazenamento e comercialização de produtos veterinários, garantindo a conformidade com padrões de qualidade e segurança.
Controle de Qualidade
: Monitora a qualidade dos insumos utilizados na produção de medicamentos veterinários, bem como a eficácia e segurança dos produtos finais.
Proteção da Saúde Animal
: Visa proteger a saúde e o bem-estar dos animais, assegurando que os produtos veterinários disponíveis no mercado sejam seguros e eficazes.
Prevenção de Riscos à Saúde Pública
: Contribui para evitar a disseminação de doenças zoonóticas e minimizar os riscos associados ao uso inadequado de produtos veterinários.
Obrigatoriedade de Envio ao Ministério da Agricultura
Em conformidade com as diretrizes estabelecidas pelo MAPA, as empresas que atuam na manipulação de produtos veterinários são obrigadas a enviar relatórios periódicos ao Ministério da Agricultura. Estes relatórios geralmente incluem informações detalhadas sobre as atividades desenvolvidas pela empresa, bem como dados relevantes sobre a produção, controle de qualidade e comercialização de produtos veterinários.
Modelo do Relatório
Embora o formato exato dos relatórios possa variar de acordo com as especificidades de cada empresa e as exigências regulatórias locais, um modelo básico de relatório para envio ao Ministério da Agricultura pode incluir as seguintes seções:
Informações da Empresa
: Nome da empresa, endereço, CNPJ, dados de contato.
Descrição das Atividades
: Detalhamento das atividades realizadas pela empresa, incluindo produção, manipulação, armazenamento e comercialização de produtos veterinários.
Controle de Qualidade
: Descrição dos procedimentos adotados para garantir a qualidade e segurança dos produtos, incluindo análises laboratoriais, controle de estoque e monitoramento de prazos de validade.
Registros de Produção
: Dados sobre os produtos fabricados, 
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Como Executar o Ping no Windows para Identificar Falhas de Comunicação — 27/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/459858
> Publicado em: 27/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O Ping é uma ferramenta fundamental no mundo da tecnologia da informação, especialmente para profissionais de suporte técnico. Ele é usado para verificar a conectividade entre dispositivos em uma rede, identificar problemas de comunicação e diagnosticar falhas de conexão. Neste artigo, vamos explicar o que é o Ping, para que serve e como executá-lo no sistema operacional Windows para agilizar a solução de problemas de sistema causados por queda de comunicação com o servidor.
O que é o Ping?
O Ping é um comando utilizado para testar a conectividade entre dois dispositivos em uma rede. Ele envia pacotes de dados de um dispositivo para outro e mede o tempo que leva para esses pacotes serem enviados e retornarem. Se o dispositivo de destino responder, isso indica que há uma conexão ativa entre os dispositivos.
Para que serve o Ping?
O Ping é uma ferramenta versátil e útil para diversas finalidades:
Verificar Conectividade
: O Ping é usado para verificar se um dispositivo pode se comunicar com outro na rede. Isso é crucial para identificar se há problemas de conexão entre computadores, servidores, roteadores ou outros dispositivos de rede.
Diagnosticar Problemas de Rede
: Quando ocorrem problemas de conexão, como lentidão na rede ou indisponibilidade de serviços, o Ping pode ser usado para diagnosticar a causa raiz. Se um dispositivo não responder ao Ping, isso pode indicar uma falha na rede ou no próprio dispositivo.
Identificar Latência
: O tempo que leva para os pacotes de dados irem e voltarem, conhecido como latência, pode ser medido usando o Ping. Uma latência alta pode indicar congestão na rede ou problemas de roteamento.
Como Executar o Ping no Windows?
Executar o Ping no Windows é simples e pode ser feito através do Prompt de Comando. Aqui está o passo a passo:
Abrir o Prompt de Comando
: Pressione as teclas
Win + R
para abrir a caixa de diálogo "Executar", digite "cmd" e pressione Enter. Isso abrirá o Prompt de Comando.
Digite o Comando Ping
: No Prompt de Comando, digite os comandos abaixo de acordo com seu objetivo. Substitua "[endereço IP ou nome do host]" pelo endereço IP ou nome do host do dispositivo que você deseja pingar, conforme os exemplos abaixo:
Pressione Enter
: Após digitar o comando, pressione Enter. O Ping começará a enviar pacotes de dados para o endereço especificado e exibirá os resultados na tela.
Para encerrar:
Para encerrar pressione CTRL + C
Ping básico:
Ping contínuo:
Em casos onde é necessário realizar um acompanhamento, é possível executar ping e gravar o resultado em um txt no local de sua preferência que será especificado no comando:
Interprete os Resultados
: O Ping exibirá informações como o tempo de ida e volta dos pacotes de dados, bem como estatísticas de perda de pacotes. Se o dispositivo responder ao Ping, isso indica uma conexão ativa. Se não houver resposta, pode indicar um problema de comunicação.
Conclusão
O Ping é uma ferramenta valiosa para profissionais de suporte técnico, permitindo diagnosticar pr
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Entendendo a Instabilidade do Sistema na PrismaFive: Por que o Sistema Cai? — 27/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/459836
> Publicado em: 27/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Análise das Razões da Instabilidade do Sistema na PrismaFive
A estabilidade do sistema é crucial para o funcionamento eficiente de qualquer plataforma ou aplicação, incluindo o sistema FarmaFacil. Quando enfrentamos quedas inesperadas, travamentos ou lentidão no sistema, é fundamental investigar as causas para implementar medidas corretivas adequadas. Neste artigo, examinaremos as principais razões que podem levar à instabilidade do sistema FarmaFacil, conforme descritas no texto fornecido, e discutiremos possíveis soluções para esses problemas.
1. Problemas de Infraestrutura de Rede:
Uma das causas primárias de instabilidade do sistema pode ser atribuída a problemas na infraestrutura de rede. Interrupções na comunicação entre dispositivos e servidores podem resultar em quedas de conexão e falhas no sistema. Isso pode ser causado por uma variedade de fatores, como problemas de roteamento, congestionamento de rede ou falhas de equipamentos de rede.
Para mitigar esses problemas, é essencial garantir uma rede estável e confiável. Realizar testes de conectividade de rede regularmente e monitorar a infraestrutura de rede para detectar possíveis pontos de falha são práticas recomendadas. A Leia também:
Identificando falhas de comunicação executando um PING
2. Sobrecarga de Servidor:
Se o servidor da farmácia estiver sobrecarregado devido a um grande volume de tráfego ou processamento intensivo, isso pode levar a quedas no sistema. Monitorar a carga do servidor e otimizar sua capacidade são medidas essenciais para prevenir essas instabilidades.
3. Atualizações de Software Mal Sucedidas:
Atualizações de software incompletas ou mal sucedidas podem introduzir bugs e incompatibilidades que resultam em falhas no sistema. É fundamental realizar atualizações de software de forma cuidadosa e monitorar qualquer impacto adverso no desempenho do sistema. Implementar procedimentos de teste rigorosos antes de aplicar atualizações em produção, realizar backups completos do sistema e manter registros detalhados das alterações realizadas são práticas recomendadas para garantir uma atualização de software bem-sucedida e minimizar o risco de instabilidade do sistema. Leia também:
Como é executado e como acompanhar o backup do banco de dados do sistema
4. Problemas de Hardware:
Falhas de hardware, como discos rígidos defeituosos ou problemas de memória, podem causar instabilidades no sistema. Realizar manutenção preventiva, como verificações regulares de integridade do hardware e substituição de componentes defeituosos, pode ajudar a mitigar esses problemas. Além disso, implementar práticas de monitoramento de hardware em tempo real e sistemas de alerta precoce pode ajudar a identificar e resolver problemas de hardware antes que afetem o desempenho do sistema.
Procedimentos de Resolução:
Para resolver problemas de instabilidade do sistema, é essencial conduzir uma análise detalhada das possíveis causas e implementar medidas corretivas adequadas.
Isso pode incluir a realiz
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Facilitando a Vida dos Clientes do Sistema FarmaFácil: A Inclusão da Espécie da Cápsula por Forma Farmacêutica — 27/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/459828
> Publicado em: 27/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Facilitando a Vida dos Clientes do Sistema FarmaFacil: A Inclusão da Espécie da Cápsula por Forma Farmacêutica
No mundo da farmácia, a eficiência e a precisão são fundamentais. Para atender às necessidades dos nossos clientes e garantir uma experiência ainda mais fluida e confiável, desenvolvemos uma melhoria significativa no sistema FarmaFacil: a inclusão da espécie da cápsula por forma farmacêutica. Essa atualização visa simplificar o processo de seleção de cápsulas, garantindo que os clientes recebam exatamente o que precisam, de forma rápida e precisa.
Como Funciona:
Cadastro de Espécies de Cápsulas:
Para começar, é necessário cadastrar todas as espécies de cápsulas utilizadas pela farmácia. Isso é feito facilmente no menu Arquivo > Produção > Especificação Cápsula. Aqui, todas as espécies são listadas, garantindo que nenhuma seja esquecida.
Cadastro de Formas Farmacêuticas:
Em seguida, é preciso cadastrar uma forma farmacêutica para cada espécie de cápsula e informar a espécie correspondente. Isso é feito no menu Arquivo > Produção > Forma Farmacêutica. Essa etapa é crucial para garantir a associação correta entre as espécies de cápsulas e suas formas farmacêuticas.
Cadastro de Cápsulas:
Com as formas farmacêuticas cadastradas e associadas às espécies de cápsulas, é hora de informar a espécie em cada cadastro de cápsula. Isso é feito no menu Arquivo > Estoque > Produto. Aqui, além de cadastrar as informações básicas sobre o produto, como nome e quantidade, agora também é possível especificar a espécie da cápsula.
Benefícios:
Precisão na Seleção de Cápsulas:
Com a espécie da cápsula associada à forma farmacêutica, o sistema garante uma seleção precisa das cápsulas necessárias para cada cliente.
Rapidez no Atendimento:
Com todas as informações devidamente cadastradas, o processo de venda se torna mais ágil, permitindo que os clientes sejam atendidos de forma rápida e eficiente.
Redução de Erros:
Ao eliminar a possibilidade de seleção incorreta de cápsulas, reduzimos significativamente o risco de erros e retrabalho, garantindo a satisfação do cliente e a integridade do serviço prestado.
Conclusão:
A inclusão da espécie da cápsula por forma farmacêutica no sistema FarmaFácil representa um avanço significativo no atendimento às necessidades dos nossos clientes. Ao simplificar e otimizar o processo de seleção de cápsulas, estamos elevando o padrão de excelência do nosso serviço e garantindo uma experiência ainda mais satisfatória para todos os envolvidos. Estamos comprometidos em continuar buscando maneiras de aprimorar o sistema FarmaFácil e proporcionar as melhores soluções para os nossos clientes.
Com essa melhoria implementada, estamos confiantes de que estamos facilitando significativamente a vida dos nossos clientes e elevando o nível de excelência do nosso serviço. Estamos comprometidos em continuar inovando e melhorando para atender às necessidades em constante evolução do mercado farmacêutico.

---

## 🔴 Configurar a emissão de NFC-e no sistema FarmaFacil — 26/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/459777
> Publicado em: 26/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Após ter obtido as informações de pré-requisitos descritas no passo a passo
Pré requisitos para a emissão de NFC-e
será necessário realizar a configurações no sistema para habilitar a emissão do NFC-e.
Caso o cliente possua um ECF e esteja substituindo esse equipamento pela emissão do NFC-e, necessário desabilitar a impressora fiscal nos parâmetros do sistema acessando o caminho abaixo:
Arquivo > Parâmetro > Configurações PrismaFive > Chave IMPFISCAL = 0
Importante:
Nesses casos, antes de desabilitar o ECF converse com o cliente e certifique-se de que ele emitiu todos os relatórios necessários, bem como todas as reduções Z, leitura X e demais documentos enviados para a contabilidade. Após a desvinculação do ECF a farmácia deverá solicitar a contabilidade para fazer a baixa do equipamento no SAT (Secretaria de Administração Tributária) e arquivá-lo durante 5 anos.
Feito isso, o próximo passo é cadastrar o documento fiscal 65 nos tributos acessando o caminho abaixo, isso porque dentro os tipos de documentos fiscais existentes, o NFC-e representa o documento fiscal de código 65.
Arquivo > Parâmetro > Tributos > Inserir
Feito isso, a primeira emissão será feita em ambiente de homologação, para habilitar o ambiente de homologação siga os passos:
Importante:
Nem todos os estados obrigam que a primeira emissão seja no ambiente de homologação, certifique-se antes de iniciar e se for o caso, configure direto no ambiente de produção.
Arquivo > Parâmetro > Parâmetro > Aba NFe/SPED > Ambiente homologação
Após habilitar o ambiente de homologação informe o CSC/Token correspondentes nos campos acessando o caminho abaixo:
Arquivo > Parâmetro > Parâmetro > Aba Cupom Fiscal/NFCe/SAT
Tendo as configurações acima gere uma venda teste contendo um produto com a tributação adequada, realize o recebimento e posterior cancelamento do mesmo para validar e habilitar o ambiente de produção.
A emissão e cancelamento do cupom em ambiente de homologação, na maioria dos casos significa que o ambiente de produção está pronto para ser configurado, para isso habilite o ambiente de produção no sistema conforme abaixo:
Arquivo > Parâmetro > Parâmetro > Aba NFe/SPED > Ambiente produção
Após habilitar o ambiente de produção informe o CSC/Token correspondentes nos campos conforme imagem do 4º passo e prossiga com o teste de recebimento. Após a emissão do cupom em ambiente de produção a farmácia estará pronta para fazer as emissões.
Caso ocorra a mensagem abaixo na tela do caixa durante os testes:
Marque a opção abaixo na tela de parâmetros do sistema, mesmo que a farmácia tenha filial integrada essa opção precisa ser marcada.
Abaixo link dos painéis de monitoramento da Sefaz para consultar a disponibilidade dos ambientes.
http://www.nfce.se.gov.br/portal/painelMonitor.jsp
https://dfe-portal.svrs.rs.gov.br/Nfce/Consulta

---

## 🔴 Como é executado e como acompanhar o BACKUP do banco de dados do sistema FARMAFÁCIL — 25/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/459456
> Publicado em: 25/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

A responsabilidade de manter um backup atualizado e diário do banco de dados é do cliente e neste artigo descrevemos o procedimento de como realizar este processo critico para o seu negócio.
➡️
Clique Aqui
e saiba a importância do processo de backup para o seu negócio.
No servidor da farmácia deve estar instalado e executando o aplicativo responsável por executar o backup diário, este aplicativo é chamado de
BackupFF,
ele é responsável por executar e salvar o backup de acordo com as configurações de horário e local onde o arquivo será salvo, essas configurações são definidas em conjunto com a farmácia no momento da implantação ou uma troca de servidor. O aplicativo está sempre no servidor, na pasta
:
C:\FarmaFaciI\BackupFF
Após o aplicativo de
BackupFF
ser executado, um ícone será exibido no canto inferior direito do seu monitor juntamente com os demais ícones do Windows.
Quando o aplicativo está sendo executando, para abrir e ter acesso as configurações de execução do backup basta dar duplo clique ou clicar com o botão direito > opção Abrir.
IMPORTANTE:
Caso o ícone não esteja presente ou não inicialize automaticamente após reiniciar
o
servidor, por exemplo, entre em contato com o suporte, pois para que o backup seja feito o aplicativo precisa estar sendo executado.
Na
tela
principal
em
Arquivo
>
Configurações
podem
ser
configurados horários em que o backup será executado (o backup pode ser programado para executar várias vezes ao dia) e os locais
onde
cada
arquivo
gerado
será
salvo (Orientamos salvar o arquivo de dados em locais diferentes do disco local C: do servidor, conforme descrito acima em
'Armazenamento Adequado do Backup'
).
No campo
horário Backup
são informados os horários em que a cópia será realizada automaticamente, ou seja, no exemplo abaixo será executado três vezes ao dia (o tempo de execução varia de acordo com o tamanho da base de dados) e será salvo na pasta padrão
(C:\FarmaFacil\BackupFF\Backup - Pasta padrão)
e nos demais locais informados como:
(D:\BACKUP FARMA FACIL),
caso não
hajam
outros
locais
informados, os
arquivos
gerados
sempre serão
salvos
no
caminho
padrão:
IMPORTANTE:
Conforme a imagem, por padrão o separador das horas e minutos é ';' ponto e vírgula.
Caso opte por realizar o backup manualmente, utilize a opção:
Arquivo > principal > Iniciar backup
, esse processo normalmente é utilizado em caso de manutenção ou eventuais trocas de servidor.
O arquivo gerado é composto pelo
nome da Farmácia +
CNPJ
+ Versão atual do sistema + data e hora em que foi
gerado
e será salvo nos locais de acordo com o que foi configurado no aplicativo.
Por que o Backup dos Dados é Importante?
1. Garantia de Continuidade:
Fazer backup regularmente garante que sua farmácia possa continuar funcionando mesmo se houver falhas no sistema,  roubo de computadores , ataques cibernéticos. Sem backup, você corre o risco de interromper serviços e prejudicar a reputação do seu negócio.
2. Proteção contra Perdas de Dados:
Incidentes como exclusão ac
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Bem vindo(a) a nossa Base de Conhecimento! 💻🧪📚💊 — 22/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/458881
> Publicado em: 22/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Olá e seja muito bem-vindo!😀
É um prazer recebê-lo em nossa plataforma!
Aqui, você encontrará todo o suporte necessário para sua jornada. Estamos aqui para ajudá-lo a encontrar informações, solucionar dúvidas sobre nossos produtos e configurar recursos sempre que necessário. Além disso, nossa missão é enriquecer seu conhecimento sobre nossos sistemas PrismaFive, proporcionando uma experiência ainda mais completa.
Nossa base de conhecimento está estruturada em tópicos acessíveis e pesquisáveis, à sua esquerda. Fique à vontade para explorar o conteúdo que mais se adequa às suas necessidades!
Além disso, lembre-se de que também há uma opção de pesquisa por palavra-chave na aba superior, permitindo que você encontre informações específicas com facilidade.
É fundamental ressaltar que antes de abrir um ticket no suporte, é altamente recomendável pesquisar na base de conhecimento. Muitas vezes, as respostas para suas perguntas podem estar lá, economizando seu tempo e agilizando a solução de seus problemas.
Cada menu oferece uma experiência única e valiosa. Na seção "Base de Conhecimento", você terá acesso a uma vasta gama de tutoriais, artigos passo a passo e explicações detalhadas sobre as funcionalidades dos sistemas PRISMAFIVE.
Além disso, em nossa página inicial, você poderá conferir os artigos mais recentes, garantindo que esteja sempre atualizado com as últimas novidades e melhorias em nossos sistemas.
Estamos aqui para guiá-lo em cada etapa e garantir uma experiência excepcional. Sinta-se em casa e aproveite ao máximo tudo o que nossa base de conhecimento tem a oferecer!

---

## 🔴 O objetivo deste artigo é fornecer orientações claras e passo a passo sobre como integrar o PrismaSync com as plataformas de mídia social Facebook e Instagram. Ao destacar os benefícios dessa integração, como centralização do atendimento ao cliente e facilidade de gerenciamento, o texto visa capacitar os usuários a aproveitarem ao máximo essas ferramentas para melhorar sua presença online e aprimorar o relacionamento com os clientes. Além disso, o artigo destaca requisitos importantes e pontos-chave a serem considerados durante o processo de integração, garantindo uma experiência eficiente e sem contratempos para os usuários.Redes Sociais - Facebook e Instagram — 19/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/458224
> Publicado em: 19/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O objetivo deste artigo é fornecer orientações claras e passo a passo sobre como integrar o PrismaSync com as plataformas de mídia social Facebook e Instagram. Ao destacar os benefícios dessa integração, como centralização do atendimento ao cliente e facilidade de gerenciamento, o texto visa capacitar os usuários a aproveitarem ao máximo essas ferramentas para melhorar sua presença online e aprimorar o relacionamento com os clientes. Além disso, o artigo destaca requisitos importantes e pontos-chave a serem considerados durante o processo de integração, garantindo uma experiência eficiente e sem contratempos para os usuários.
Redes Sociais - Facebook e Instagram
Hoje as redes sociais deixaram de ser um lugar apenas para conhecer pessoas. Muitas marcas utilizam elas para promover seu produto e atender ao seus clientes por lá mesmo, facilitando a forma de contato direto entre cliente e empresa.
Dentro do PrismaSync é possível integrar o
Facebook
e o
Instagram
centralizando seu atendimento em um lugar só!
Conectando as páginas
Facebook
Conectado em uma com do tipo
dona (criadora da página no facebook)
no Prisma Sync vá no menu lateral
vá até a opção
Parâmetro
e em seguida na opção
Instagram & Facebook
irá mostrar o status o seu status de conexão, caso não conectado irá apresentar o botão para
Conectar
OBS: contas com atribuição de cargo administrador na página no facebook, não ira conseguir fazer o vinculo com a api do SYNC, é necessário ser a conta do facebook que CRIOU a Página.
OBS 2: como é obrigatório a autenticação de 2 fatores no meta bussines, é necessário cadastrar um número de celular que possa receber o código por SMS, a meta não envia o código por ligação (não recomendamos cadastrar numero de TELEFONE em autenticação de 2 fatores.)
Depois disso clique no botão
Conectar
, abrirá uma janela e basta seguir o passo a passo nela com
uma conta de CRIADORA da página
Se a página for conectada com a do Instagram, aparecerá a opção de vincular ao mesmo tempo
Mantenha
ativas todas as permissões
que o Facebook solicita, pois são importantes para o sincronismo das mensagens. Ao terminar, clique em
Concluir
.
Importante
: Não é possível vincular mais de uma página na mesma conta, selecione apenas
UMA
!
Ao finalizar o passo a passo na tela de login do facebook as páginas disponíveis apareceram para seleção e vínculo no PrismaSync
Instagram
Para conectar o instagram, é necessário que ela esteja
vinculada
ao Facebook Business.
Acesse os
parâmetros
clicando no último ícone no menu lateral esquerdo, em
Instagram & Facebook
, é só clicar no botão
Conectar
e acessar a sua conta do Facebook que está vinculada à sua conta do Instagram;
Selecione a página e Instagram que você deseja conectar ao Prisma Sync e clique em
Avançar
;
Autorize todas as permissões e clique em
Concluir
.
É importante que a conta seja
empresarial
pois sem essa validação o sincronismo das mensagens não acontece!
Pronto! Agora você vinculou o Prisma Sync ao seu Facebook e Instagram.
Pontos
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 A Importância Crítica do Backup no Sistema FARMAFÁCIL: Responsabilidade e Vantagens — 12/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/457037
> Publicado em: 12/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

No universo da gestão de farmácias, a preservação e segurança dos dados são fundamentais para garantir a continuidade das operações e a integridade das informações. No entanto, muitas vezes, a importância do backup do sistema FARMAFÁCIL é negligenciada pelos usuários. Este artigo visa destacar a crítica importância de assegurar que o backup esteja sendo realizado regularmente, reforçando a responsabilidade do cliente e explorando as vantagens de armazenar esses backups na nuvem.
Responsabilidade do Cliente:
É crucial ressaltar que a responsabilidade pelo backup do sistema FARMAFÁCIL recai sobre o cliente. Este procedimento é vital para a preservação dos dados e a manutenção da continuidade das operações. Negligenciar essa tarefa pode resultar em perdas irreparáveis em caso de falhas no sistema, ataques cibernéticos, perda do computador ou outros eventos inesperados.
Consequências da Falta de Backup no FARMAFÁCIL:
1. Perda Irreversível de Dados:
- A ausência de backups pode levar à perda irreversível de dados críticos, como registros de vendas, histórico de clientes e informações de estoque. Isso pode impactar diretamente a eficiência operacional e a tomada de decisões.
2. Interrupção nas Operações:
- Em situações de falha no sistema ou perda de dados, as operações diárias podem ser interrompidas, resultando em prejuízos financeiros, perda de clientes e danos à reputação do negócio.
3. Comprometimento da Segurança:
- Sem backups, a segurança dos dados fica comprometida. Em casos de ransomware ou outros ataques cibernéticos, a recuperação rápida e eficiente se torna impossível, expondo a empresa a riscos significativos.
4. Tempo e Recursos Desperdiçados:
- A recuperação de dados sem backups adequados demanda tempo e recursos consideráveis. Isso pode resultar em custos operacionais elevados e prolongar o tempo de inatividade.
Procedimento para Realizar o Backup no FARMAFÁCIL:
Para garantir que o backup no sistema FARMAFÁCIL seja realizado corretamente, siga o procedimento:
https://prismafive.movidesk.com/kb/pt-br/article/459456/
a-importancia-do-backup-do-banco-de-dados-em-sistemas-de-farmaci
Este guia fornece instruções passo a passo, facilitando a execução do backup de maneira eficaz.
Vantagens de Armazenar Backups na Nuvem:
1. Acessibilidade Remota:
- Os backups na nuvem oferecem acesso remoto a partir de qualquer local, permitindo uma recuperação rápida e eficiente, independentemente da localização física.
2. Segurança Adicional:
- Plataformas de armazenamento em nuvem geralmente oferecem camadas adicionais de segurança, protegendo os dados contra ameaças cibernéticas.
3. Economia de Espaço e Recursos:
- Armazenar backups na nuvem evita a necessidade de hardware adicional, economizando espaço e recursos físicos.
Conclusão:
Investir tempo na realização regular de backups no sistema FARMAFÁCIL é um investimento crucial na proteção do seu negócio. A responsabilidade é do cliente, e as vantagens de armazenar backups na nuvem são inúmeras. Ao compree
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Descrição do Cargo: Analista de Suporte — 04/03/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/455265
> Publicado em: 04/03/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Descrição do Cargo: Analista de Suporte
Identificação:
- Cargo: Analista de Suporte
- Área: Service Desk
Missão:
O Analista de Suporte tem como missão oferecer suporte técnico de alta qualidade aos clientes que utilizam os softwares da PrismaFive. Isso inclui a resolução de problemas, esclarecimento de dúvidas e orientações sobre o uso dos produtos, sempre seguindo as políticas e procedimentos estabelecidos. Além disso, é responsável por identificar e ofertar novos produtos e serviços que atendam às necessidades dos clientes, visando garantir sua satisfação e fidelização, promovendo assim o sucesso da marca PrismaFive.
Organograma:
O Analista de Suporte técnico de software se reporta ao Customer Success, que por sua vez se reporta ao Gestor de Suporte. O profissional também interage com outros membros da equipe de suporte, clientes internos e externos, desenvolvedores de software, vendedores, implantadores e financeiro.
Atribuições e Responsabilidades:
Responsabilidades Principais:
- Assegurar o cumprimento do SLA (Service Level Agreement - Vencimento do ticket) e demais indicadores de atendimento dentro dos níveis aceitáveis para o seu cargo.
- Manter-se informado sobre os produtos da PrismaFive, participando de reuniões, treinamentos e certificações.
- Manter a satisfação do cliente, buscando feedbacks e sugestões de melhoria.
- Apoiar e compartilhar conhecimentos com colegas da equipe.
- Documentar e compartilhar conhecimentos na Central de Ajuda (artigos) mensalmente.
- Observar e criar ações para evitar reincidências de problemas.
- Fornecer informações precisas e completas aos clientes.
- Zelar pela imagem e sigilo da empresa.
- Identificar e ofertar novos produtos e serviços.
- Garantir o sucesso do cliente com os produtos PrismaFive.
- Observar pontos de melhoria e propor soluções.
- Executar treinamentos de clientes nos produtos PrismaFive.
-Estar disponível e atender as ligações do seu ramal seguindo os procedimentos acordados.
Atividades:
- Prestar atendimento e orientação ao cliente via ticket / telefone
- Coletar informações para análise e diagnóstico de problemas.
- Atualizar procedimentos na Central de Ajuda.
- Documentar soluções aplicadas.
- Acompanhar indicadores individuais e da equipe.
- Prestar eventual atendimento externo.
Níveis de Atuação:
- Júnior: Resolver
problemas de baixa complexidade
, manter base de conhecimento atualizada.
- Pleno: Resolver
problemas de média complexidade
de diferentes assuntos/produtos, compartilhar conhecimentos.
- Sênior: Resolver
problemas de alta complexidade
de diferentes assuntos / produtos, assumir provisoriamente atividades de gestão.
Requisitos:
- Grau de Instrução:
- Júnior: Ensino médio completo, desejável cursos em áreas afins (tecnologia, infraestrutura e redes)
- Pleno: Curso técnico completo ou superior incompleto em áreas afins  (tecnologia, infraestrutura e redes)
- Sênior: Ensino superior ou curso técnico em áreas afins  (tecnologia, infraestrutura e redes).
- Experiência Profiss
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Guia de Boas Práticas para Gerenciamento de Tickets de Suporte — 27/02/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/453943
> Publicado em: 27/02/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Bem-vindo ao guia de procedimentos para o gerenciamento eficiente de tickets de suporte utilizando o Movidesk. Este documento oferece diretrizes práticas para garantir um atendimento eficaz e satisfatório aos nossos clientes.
1. Triagem Inicial do Ticket
Ao receber um ticket com o status NOVO, leia o texto revise cuidadosamente, e caso o texto esteja com informações incompleta ou pouco claras,  aplique a macro
3 - Obter Mais Informações - TRIAGEM alterando o status para Aguardando retorno do cliente,
e caso esteja claro já revise SERVIÇO E CATEGORIA e altere o status para
CATEGORIZADO
,  pois essas informações determinam a urgência do atendimento e o prazo de vencimento do ticket.
Não permitam que tickets NOVOS fiquem na fila sem a triagem inicial por mais de 1 dia (revise sua fila no mínimo 3 vezes no dia).
Para os tickets com status Aguardando retorno do cliente, realize tentativas de contato nos números de telefone fornecidos no ticket. Verifique os contatos telefônicos cadastrados, se necessário e revise os telefones no cadastro quando obter o contato.  Após 3 dias com o ticket aguardando retorno e no mínimo 3 tentativas de contato encerre o ticket por falta de retorno.
Notifique a gestão de suporte / cs da equipe se houve troca de proprietário da farmácia, para avaliar a necessidade de encaminhamento ao departamento financeiro para alteração contratual e posterior direcionamento à equipe de onbording (utilizar macro: 10 - Encaminhar Financeiro (FARMÁCIA ADQUIRIDA) - Notificar Cliente.  Normalmente, quando um cliente solicita a alteração do CNPJ ou a substituição do farmacêutico responsável, é um indício de que a farmácia pode ter sido adquirida por um novo proprietário. Portanto, sempre questione se houve mudança de proprietário.
NUNCA FAÇA ALTERAÇÕES NO CNPJ OU NO FARMACÊUTICO SEM ANTES QUESTIONAR.
2. Avaliação de Histórico
- Antes de iniciar o atendimento, verifique os tickets anteriores do cliente dos últimos 3 meses para identificar recorrências ou se já outro ticket aberto do mesmo assunto sendo atendido por outro colega cancele o ultimo ticket aberto com a macro
5 - Cancelamento - Duplicado.
- Resolva a causa raiz do problema para evitar reincidências, porém se não for possível no momento aplique o paliativo e alerte o CS da equipe para que este item seja colocado na lista de
estudo da causa raiz.
Cs deve trazer esta situação para reunião semanal com a gestão para as tomadas de ações.
3. Escalação e Encaminhamento
- Caso identifique necessidade de correção ou melhoria de software, encaminhe adequadamente para a equipe de backservice, porém garanta que a versão do cliente esteja atualizada. Utilize as macros adequadas para notificar o cliente e encaminhar para o backservice (leia artigos de macros).
- Solicite apoio aos colegas da equipe, ao analista de sucesso da sua área se encontrar desafios que não consiga resolver. Consulte nossas base de conhecimento: redmind, central de ajuda, youtube.
- Somente os backservice devem realizar a
po
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Sistema de Pesquisa de Satisfação - PrismaSync — 26/02/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/453523
> Publicado em: 26/02/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Sistema de Pesquisa de Satisfação
A mais recente melhoria implementada em nosso sistema é a inclusão de uma pesquisa de satisfação para cada atendimento realizado dentro da ferramenta. Esta funcionalidade permite aos usuários configurarem até 5 perguntas. Além disso, os usuários podem definir se o disparo da pesquisa é automático ou não, e especificar o texto a ser enviado junto com o link da pesquisa para o cliente.
Configuração das Perguntas:
A farmácia têm a capacidade de configurar até 5 perguntas para a pesquisa de satisfação. Cada pergunta pode ser de um dos seguintes tipos:
Estrela (1 a 5): O cliente pode avaliar o atendimento atribuindo uma pontuação de 1 a 5 estrelas.
Sim ou Não: O cliente pode responder com um simples sim ou não à pergunta.
NPS (Net Promoter Score) de 1 a 10: O cliente pode classificar sua probabilidade de recomendar nosso serviço em uma escala de 1 a 10.
Comentário: O cliente pode fornecer feedback adicional por meio de um campo de texto aberto.
Disparo da Pesquisa:
A farmácia têm a opção de configurar o disparo da pesquisa como automático ou manual. Se configurado como automático, a pesquisa será enviada automaticamente ao cliente após o atendimento de acordo com as regras definidas. Se configurado como manual, os usuários terão a opção de enviar a pesquisa manualmente ao final do atendimento ou quando acharem apropriado.
Relatório de Respostas:
Uma vez que o seu cliente responda à pesquisa de satisfação, as respostas serão registradas e disponibilizadas em um relatório. Este relatório permite aos usuários analisarem o feedback recebido e identificarem áreas de melhoria. As respostas são associadas ao respectivo atendimento, permitindo uma análise específica por caso.
Funcionamento:
Configuração das Perguntas: A farmácia acessa a seção de configurações da pesquisa de satisfação, onde podem definir as perguntas, o tipo de pergunta, o texto a ser enviado e outras opções relacionadas ao disparo da pesquisa.
Atendimento ao Cliente: Após cada atendimento, o sistema verifica se há uma pesquisa de satisfação configurada para aquele tipo de atendimento e, se aplicável, envia automaticamente a pesquisa ao cliente.
Resposta do Cliente: O cliente recebe a pesquisa de satisfação por meio de um link enviado juntamente com o texto configurado. O cliente responde à pesquisa, que é registrada no sistema.
Relatório de Respostas: Os usuários podem acessar o relatório de respostas para visualizar e analisar o feedback fornecido pelos clientes. O relatório fornece insights valiosos para melhorias contínuas no serviço.
Esta melhoria no sistema de pesquisa de satisfação é projetada para aumentar a transparência, promover a comunicação eficaz com os clientes e fornecer uma maneira sistemática de coletar e analisar o feedback do cliente. Estamos confiantes de que esta adição será benéfica para melhorar a qualidade dos serviços da empresa/organização e a satisfação do cliente.

---

## 🔴 Procedimento para Lidar com Clientes Irritados no Atendimento Telefônico — 25/02/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/453501
> Publicado em: 25/02/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Artigo sem tradução para esse idioma
Tente outro idioma ou clique no botão abaixo:
Ir para o idioma padrão

---

## 🔴 Procedimento Atendimento Telefônico — 25/02/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/453500
> Publicado em: 25/02/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Artigo sem tradução para esse idioma
Tente outro idioma ou clique no botão abaixo:
Ir para o idioma padrão

---

## 🔴 Perfil do Profissional de Customer Success da Squad — 05/02/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/449836
> Publicado em: 05/02/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Perfil do Profissional de Customer Success da Squad:
O profissional de Customer Success desempenha um papel crucial no sucesso do cliente e no crescimento sustentável da empresa
PrismaFive.
Seu perfil deve incluir uma combinação de habilidades técnicas, habilidades interpessoais e um profundo entendimento do produto ou serviço oferecido pela empresa. Destacando a importância de ser uma referência de comportamento e boas práticas de atendimento.
Aspectos Importantes do Perfil:
Empatia e Compreensão do Cliente:
Capacidade de compreender as necessidades e desafios dos clientes.
Habilidade em ouvir ativamente para entender as preocupações e expectativas dos clientes.
Empatia para se colocar no lugar do cliente e entender suas perspectivas.
Conhecimento Técnico:
Compreensão aprofundada do produto ou serviço oferecido pela empresa.
Habilidade em explicar recursos e funcionalidades de maneira clara e compreensível para os clientes.
Capacidade de resolver problemas técnicos e oferecer suporte prático.
Comunicação Eficaz:
Habilidades de comunicação escrita e verbal excepcionais.
Capacidade de transmitir informações de forma clara e persuasiva.
Ser capaz de personalizar a comunicação para diferentes públicos e situações.
Orientação para Resultados:
Foco em garantir o sucesso contínuo do cliente e alcançar métricas de retenção e satisfação.
Trabalho proativo na identificação de oportunidades de upsell ou cross-sell.
Atenção aos detalhes para monitorar métricas de desempenho e identificar áreas de melhoria.
Capacidade de Resolução de Problemas:
Habilidade em lidar com desafios e encontrar soluções eficazes.
Pensamento criativo para superar obstáculos e otimizar a experiência do cliente.
Colaboração:
Trabalho em equipe eficaz com outros departamentos, como vendas, marketing e desenvolvimento de produtos.
Compartilhamento de feedback do cliente para contribuir para melhorias contínuas no produto ou serviço.
Proatividade e Autonomia:
Iniciativa para antecipar as necessidades dos clientes e tomar medidas preventivas.
Capacidade de trabalhar de forma autônoma e tomar decisões informadas.
Habilidade de Treinamento:
Capacidade de treinar clientes no uso eficaz do produto ou serviço.
Desenvolvimento de materiais educativos, como tutoriais, para ajudar os clientes a maximizar o valor.
Gerenciamento de Tempo:
Habilidade em priorizar tarefas e gerenciar eficientemente o tempo para atender às necessidades dos clientes.
Referência de Comportamento e Boas Práticas:
Serve como uma referência para a equipe em termos de comportamento exemplar e adoção de boas práticas.
Promove uma cultura de excelência no atendimento ao cliente e busca contínua pela satisfação do cliente.
Em resumo, um profissional de Customer Success precisa equilibrar habilidades técnicas, empatia e uma mentalidade orientada para o cliente, contribuindo assim para o sucesso mútuo da empresa e de seus clientes.
Responsabilidades Principais:
Gestão da Experiência do Cliente:
Desenvolver e manter relacionamen
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Procedimento para Utilização de Macros no Atendimento ao Cliente — 26/01/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/448145
> Publicado em: 26/01/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para garantir um atendimento eficiente e padronizado aos nossos clientes, é essencial que os analistas de suporte estejam familiarizados com as macros disponíveis. As macros são respostas predefinidas que podem ser utilizadas em diferentes situações para agilizar o atendimento e garantir a consistência nas interações. No entanto, é importante ressaltar que o texto da macro deve servir como base e sempre ser adaptado à situação específica do cliente. Abaixo, detalhamos cada macro disponível e quando devem ser aplicadas:
1. Iniciar Atendimento
Quando usar: Utilize esta macro para iniciar o atendimento ao cliente. Lembrese de personalizar a mensagem de acordo com as informações fornecidas pelo cliente e as necessidades específicas do caso.
2. Aguardando Contato Agendado
Quando usar: Use esta macro quando um horário específico foi agendado com o cliente para fornecer atendimento. Certifiquese de criar um evento no ticket para acompanhar o compromisso agendado e adapte a mensagem conforme necessário.
3. Obter Mais Informações  TRIAGEM (Tag SemDetalhe)  Status Aguardando Retorno Cliente
Quando usar: Aplique esta macro quando um novo ticket for recebido sem informações claras para realizar o atendimento. Após aplicar esta macro, faça pelo menos 3 tentativas de contato com o cliente para obter as informações necessárias e ajuste a mensagem conforme a comunicação com o cliente evolui.
4. Cliente Executará uma Ação  Status Aguardando Retorno Cliente
Quando usar: Utilize esta macro quando for necessário aguardar uma ação específica do cliente para continuar o atendimento. Personalize a mensagem de acordo com a ação solicitada e as
instruções fornecidas ao cliente.
5. Mais Informações  Após Análise Técnica  Status Aguardando Retorno Cliente
Quando usar: Se a análise técnica indicar a necessidade de mais informações do cliente e não for possível obter contato, aplique esta macro. Adapte a mensagem conforme a análise técnica realizada e as informações necessárias para prosseguir com o atendimento.
6. Novo Assunto (Abrir Novo Ticket e Solucionar Original com esta macro)
Quando usar: Esta macro deve ser aplicada quando a situação original do ticket for resolvida, mas o cliente reportar uma nova falha relacionada. Abra um novo ticket para o novo assunto e feche o ticket original com esta macro, personalizando a mensagem de acordo com o novo problema relatado pelo cliente.
7. Melhoria Rejeitada (Backservice)
Quando usar: Use esta macro quando uma melhoria proposta tiver sido analisada e rejeitada. Ajuste a mensagem para explicar os motivos da rejeição e oferecer outras soluções, se aplicável.
8. ID  Melhoria  Notificar Cliente Melhoria Aprovada
Quando usar: Esta macro é exclusiva da equipe de backservice. Utilizea para notificar o cliente quando uma melhoria proposta tiver sido analisada e aprovada. Personalize a mensagem para informar sobre a aprovação da melhoria e os próximos passos.
9. Encaminhar Backservice  Notificar Cliente
Quando usar: Utilize esta macro p
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Requisitos Mínimos Infraestrutura e Redes Para Uso Sistemas PrismaFive — 25/01/2024

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/447619
> Publicado em: 25/01/2024
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Este documento serve como guia essencial para aquisição e configuração de equipamentos que
garantam o desempenho ideal ao utilizar o sistema PrismaFive.
Certifique-se de seguir estas orientações durante qualquer negociação com nossa equipe comercial para garantir uma experiência eficiente.
Requisitos Ideais
Servidor até 4 Terminais em Rede
Processador:
Intel Core i5 ou superior
Memória:
8GB ou superior
Rede:
Porta 10/100 Mbps ou superior
Disco Padrão:
500GB SSD ou superior
Sistema Operacional:
Windows 10 x64 ou superior
Nobreak Obrigatório
Servidor entre 5 a 20 Terminais em Rede
Computador com Arquitetura Própria para Servidor (ex.: Dell, HP, IBM)
Processador:
Intel® Xeon® E-2224 (3.4 GHz, 8M cache, 4 núcleos/4 threads) ou superior
Memória:
1 x 8GB DDR4 3200MHz | 16GB para mais de 4 usuários em RDP/WTS/TS*
Rede:
Dual Port Gigabit
Disco Padrão:
1 x 500GB SSD ou superior
Sistema Operacional:
Windows Server 2016* ou superior devidamente licenciado; Windows em 64Bits
Nobreak Obrigatório
*Para integração multilojas (matriz/filial) via RDS/Terminal Server/WTS, ative as calls de acesso remote na versão do Windows adquirida. Este processo deve ser realizado por um engenheiro/técnico da infraestrutura da farmácia. Além disso, é necessário configurar uma VPN para garantir a segurança dos acessos.
Estação
Processador:
Intel i3 ou superior
Memória:
8GB de memória
Rede:
Porta 10/100 Mbps ou superior
Disco Padrão:
1 x 250GB (preferencialmente SSD) ou superior
Sistema Operacional:
Windows 10 ou superior
Impressoras
Rótulos
O sistema é compatível com qualquer impressora no sistema operacional Windows. Recomenda-se o uso de impressoras térmicas para rótulos, como os modelos Argox OS 214 Plus, Zebra GC420 , Elgin L42/
Elgin L42 PRO
e ColorWorks C4000 da Epson.
Gerais (Ordem de Manipulação, Comprovante de Venda e Relatórios)
O sistema pode trabalhar com impressoras laser, matriciais ou jato de tinta, contanto que sejam compatíveis com o sistema operacional Windows.
ECF - Emissor de Cupom Fiscal (Estado de Santa Catarina)
Modelo Homologado:
Bematech MP 4200 TH FI II
Observação:
Caso tenha mais de uma impressora fiscal na farmácia, todas devem ser do mesmo modelo.
Desde 01/11/21 o FarmaFácil possibilita a emissão da NFC-e para SC, converse com seu contador.
SAT (Estado de São Paulo)
Modelos Homologados:
DIMEP, BEMATECH, ELGIN, EPSON, CONTROL ID
Emissão de Documentos Fiscais Eletrônicos (NFC-e, NF-e, NFS-e)
É EXPRESSAMENTE RECOMENDADO O USO DE CERTIFICADO DIGITAL TIPO A1.
Impressoras Térmicas Não Fiscais
Elgin i8/ i9 / USB
Epson TM-T20X Não Fiscal USB
Bematech MP-4200 TH Não Fiscal USB
Bematech Mp-4200 HS Não Fiscal USB
TEF/ PinPad/ Gerenciador Padrão
A legislação prevê que o uso do TEF não é obrigatório, desde que haja comunicação da maquininha com o computador (caixa) e haja um gerenciador instalado que faça a ponte entre o sistema e a maquina de cartão para que as informações possam ser gravadas de acordo com o que o fisco prevê. O sistema Farmafacil é compatível c
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Central Movidesk - Tickets — 14/12/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/440761
> Publicado em: 14/12/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Este guia visa ajudá-lo a abrir e gerenciar tickets de suporte técnico de forma eficaz na plataforma da PrismaFive. Ao seguir estes passos, você garantirá que sua solicitação seja tratada com rapidez e precisão pela nossa equipe de suporte técnico.
Instruções:
1. Acesse a Central de Atendimento:
- Abra o navegador em seu computador ou smartphone e acesse o seguinte link:
https://prismafive.movidesk.com/
- Insira seu login e senha. Se você não tem um login ou esqueceu sua senha, entre em contato com um dos nossos analistas de suporte.
2. Visão Geral da Central:
- Após o login, você verá a tela principal da central de atendimento.
3. Central de Ajuda (Base de Conhecimento):
- Se você tiver dúvidas sobre como usar os produtos da PrismaFive, consulte nossa base de conhecimento. Lá você encontrará artigos explicativos sobre procedimentos e funcionalidades.
- Para buscar um tópico específico entrando opção
BASE DE CONHECIMENTO
e navegando nos tópicos ou  digite uma palavra-chave na barra de pesquisa.
4. Visualizar e Acompanhar os Tickets Abertos
- Caso queira ver um ticket anteriormente resolvido ou acompanhar um em andamento, clique na aba "Meus Tickets".
- Use os filtros disponíveis para ver os diferentes status de atendimento e quem está responsável pelo ticket.
Tickets Pendentes:
Estes tickets estão sendo tratados pelos Analistas de Suporte. Você pode interagir clicando sobre o ticket e deixando uma mensagem para o analista responsável que é imediatamente comunicado.
Tickets Resolvidos Aguardando Minha Aprovação:
Estes são tickets que já foram resolvidos e aguardam seu feedback. Se não houver retorno em 2 dias, o ticket será fechado automaticamente.
Tickets Fechados:
Estes são os tickets que já foram encerrados automaticamente.
Todos os Tickets:
Esta opção oferece uma visão de todos os tickets, incluindo os pendentes, resolvidos e fechados.
5. Abrir um Novo Ticket:
- Para abrir um novo ticket, localize a opção "Criar Ticket" na página principal da central de atendimento.
- Descreva o problema ou dúvida detalhadamente. Quanto mais informações você fornecer, melhor poderemos ajudar.
- Evite usar termos como "URGENTE" ou "AJUDA" sem uma descrição clara do problema.
➡️🚩Dicas Importantes:
a) No campo MENSAGEM, forneça uma descrição detalhada e anexe as evidências necessárias. Se o ticket não possuir uma descrição clara, ele não permanecerá no status "Aguardando retorno do cliente" por 3 dias e será considerado resolvido, sendo necessário abrir um novo ticket.
b)Após abrir o ticket, acompanhe-o através da nossa central de tickets e forneça as informações solicitadas quando necessário.
c)Certifique-se de informar seu telefone e e-mail corretamente, e deixe claro qual é o melhor horário para entrarmos em contato, se necessário. Caso tentemos ligar e você não esteja disponível, o ticket também será alterado para o status "Aguardando retorno do cliente" por 3 dias.
d)
Evite abrir múltiplos tickets para a mesma situação. Acompanhe o seu ticket original e inte
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Novidades da versão 4.7.0 — 24/11/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/435611
> Publicado em: 24/11/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Novidades da versão 4.7.0
1. Integração com Pagina do Facebook e Instagram:
Dentro do PrismaSync agora é possível integrar o
Facebook
e o
Instagram
centralizando o atendimento em um lugar só
Como conectar as paginas ao PrismaSync
2. Iniciar atendimento ao encaminhar mensagem:
Agora é possível iniciar o atendimento ao cliente ao encaminhar uma mensagem pela ferramenta de "Encaminhar Mensagem"
3.
Parâmetro
para usuário não transferir atendimento
:
Agora é possível, caso necessário, bloquear a permissão de transferência de atendimento de um usuário especifico
4. Novo
parâmetro
de atendimento para mensagens agendadas
:
Com o parâmetro marcado a mensagem agendada quando for "disparada", caso a conversa não estiver em atendimento, iniciará o atendimento;

---

## 🔴 Formas de Pagamento — 03/11/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/431853
> Publicado em: 03/11/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

NESSE ARTIGO VOCÊ VERÁ COMO CADASTRAR UMA FORMA DE PAGAMENTO:
No menu Arquivo > Sub menu Venda > Forma Pagamento:
Deve clicar no + para cadastrar uma nova forma de pagamento:
Você deverá incluir a descrição, selecionar o tipo, e selecionar uma das 3 opções a respeito de desconto, as demais informações em tela são opcionais:
Após cadastrar a nova forma de pagamento, ela já estará disponível no caixa, para novos recebimentos.
Em caso de dúvida entre em contato com nosso suporte técnico!

---

## 🔴 Alterar a cápsula na venda — 30/10/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/430775
> Publicado em: 30/10/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Esse artigo irá te mostrar como trocar a cápsula a ser utilizada, dentro da tela da fórmula
Na tela da fórmula, após você ter inserido todos os ativos que irão compor a fórmula, você deve apertar:
Ctrl + F5
para o sistema calcular a quantidade dos ativos e também realizar a sugestão da embalagem conforme o volume, quando a forma farmacêutica for cápsula o sistema irá puxar o tamanho e também a cor conforme especificação de alguns parâmetros, veja exemplo:
Nesse exemplo puxou uma cápsula gelatinosa do tamanho 4 Branca/Branca, porém se você irá utilizar outra especificação de cápsula para essa fórmula, veja como trocar nessa tela, primeiro você irá precisar clicar aqui
Na tela em que abrir você pesquisará então qual a cápsula que você deseja utilizar, conforme exemplo a seguir:
Em caso de dúvida entre em contato com nossa equipe de suporte técnico.

---

## 🔴 Novidades da versão 4.5.0 — 29/09/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/424629
> Publicado em: 29/09/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Novidades da versão 4.5.0
1. Ajustado a visualização de mensagens que são em negrito:
2. Iniciar/pesquisar uma conversa de forma mais prática:
É possível pesquisar por nome ou por telefone (desde que já exista uma conversa), ou ainda, sem precisar digitar o número completo do cliente, para assim, iniciar uma nova conversa de forma mais rápida.
3. Ir para a conversa através de um orçamento
:
É possível ir diretamente para a conversa com o seu cliente através do orçamento.
4. Acesse e envie as mensagens padrões de forma mais ágil
:
É possível localizar as mensagens padrões de forma mais fácil, digitando "/" no início da mensagem. O usuário também pode continuar digitando a descrição da mensagem para localizá-la mais rápida, veja o exemplo:

---

## 🔴 Novidades da versão 4.4.4 — 04/09/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/417366
> Publicado em: 04/09/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Novidade da versão 4.4.4
1. Integração de Reações de Mensagens:
Prepare-se para uma experiência de chat mais interativa! Introduzimos a aguardada função de reagir às mensagens diretamente no sistema. Adicione emoção às suas conversas com emojis personalizados e interaja de forma mais envolvente.
2. Resposta de Mensagens Simplificado:
Agora, vincular mensagens é uma tarefa simples! Com a nossa nova funcionalidade, os operadores podem facilmente relacionar mensagens entre si dentro do sistema. Isso torna a comunicação mais clara e eficiente, permitindo que você mantenha o controle da conversa com facilidade.

---

## 🔴 Análise de Produtos — 09/08/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/410460
> Publicado em: 09/08/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

ANÁLISE DE PRODUTOS
A manipulação personalizada requer atenção especial aos detalhes e aos mais altos padrões de controle de qualidade, garantindo que cada paciente receba um produto sob medida, confiável e seguro, assegurando que os pacientes recebam a dosagem correta do medicamento ou suplemento.
No FarmaFácil, o módulo de análise de produtos é realizado para manipulação que utilizam a forma farmacêutica de cápsulas, e está disponível em PRODUÇÃO > MOVIMENTO > ANÁLISE DE PRODUTO. Para utilizar deste módulo, é necessário que exista uma ordem de produção a ser analisada e que os parâmetros de análise estejam configurados de acordo. Como padrão, o parâmetro é marcado da seguinte forma (permitindo alteração):
O método de análise é referente a Farmacopéia USP (United States Pharmacopeia) ou Nacional (método brasileiro de análise). A Farmacopéia define, além de normas e diretrizes para os ativos, a quantidade e padrão que cada cápsula deve seguir para que o paciente receba a dosagem correta e segura de medicamentos. Neste artigo, iremos utilizar os parâmetros definidos na farmacopéia Brasileira, onde existe a tabela  de critérios de avaliação com os limites de variação do peso médio.
A amostragem é a quantidade de cápsulas padrão que será pesada para avaliar a divisão dos ativos. Pode ser alterado dentro de cada análise. O campo “alterar peso do produto” é utilizado quando a farmácia não tem uma balança configurada diretamente no computador, e a pesagem precisa ser realizada de forma manual, adicionando as informações posteriormente. Os limites descritos no parâmetro são
baseado
s
na farmacopéia brasileira, pela seguinte determinação:
para cápsulas duras e moles (utilizadas pela farmácia) com até 300mg = 0,3g (capacidade máxima), o limite é de +- 10%.
Se a cápsula tiver mais do que 300mg, este limite é alterado para +- 7,5%.
1. CÁLCULO DO PESO MÉDIO
Com uma ordem de produção em mãos, iremos começar a análise daquela manipulação. Na ordem de produção, iremos ter o peso médio das cápsulas. Este peso médio é calculado com base na quantidade de ativos, no peso, na quantidade de cápsulas e no peso das mesmas.
Na ordem acima, podemos verificar que a cápsula sugerida pelo sistema no momento da venda foi a número 4. No cadastro da mesma, temos o peso unitário de 0,04g para esta cápsula. É importante ressaltar que se este peso não estiver preenchido, não será considerado no cálculo do peso médio e no momento da análise exige uma atenção maior do farmacêutico.
Para realizar a análise do produto, o sistema irá realizar os cálculos abaixo, baseados na ordem de produção:
2. ANÁLISE DO PRODUTO
Com o peso médio calculado, iremos iniciar a análise de produtos a partir de uma amostra representativa das cápsulas produzidas. A análise de produtos tem como principal objetivo garantir se as cápsulas contêm a quantidade adequada e correta de princípios ativos, assegurando que a dosagem seja precisa e uniforme em todas as unidades de cápsulas.
Para realizar este procedimen
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Controle de qualidade/quarentena — 21/07/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/405987
> Publicado em: 21/07/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

CONTROLE DE QUALIDADE/QUARENTENA
O controle de qualidade dos produtos é um pilar essencial para a garantia de qualidade dos produtos vendidos e utilizados em uma farmácia de manipulação, contribuindo para a segurança e eficácia do tratamento. No FarmaFácil, o controle de qualidade é realizado a partir da quarentena dos lotes, exigindo da
farmácia uma organização em relação a estoque e datas de validade, visto que precisará ser feita a análise de todos aqueles lotes que estão em uso e, ao cadastrar produtos novos, a análise também precisa ser realizada.
CADASTROS NECESSÁRIOS
Para avaliar se o produto está de acordo com as especificações de uso, podemos realizar a quarentena de lotes. Este módulo do sistema é habilitado se os seguintes parâmetros estão ativos:
As farmacopéias são coleções oficiais de normas e padrões que estabelecem a identidade, pureza, qualidade, eficácia e segurança dos medicamentos, substâncias ativas e preparações farmacêuticas. Para realizar a análise, temos os ensaios padrão para aquela farmacopéia (podem ser cadastrados em ARQUIVO > PARÂMETRO > ENSAIOS) e cadastrar os mesmos no produto, especificamente na parte da “ficha técnica”. Por exemplo, o produto abaixo segue os padrões e ensaios da Farmacopéia Britânica
(
BRITISH Pharmacopoeia 2013. Vol. I London: The Stationery Office, 2013).
Caso o produto não tenha cadastrado nenhum ensaio, você pode fazer o cadastro diretamente pelo lote ao iniciar a análise de qualidade.
1.1.
CONTROLE DE QUALIDADE
Um lote pode estar liberado (quando passou pela análise de produtos) ou bloqueado (quando não está apto para uso ou quando venceu), e apenas lotes liberados podem ser habilitados para uso.
Para liberar o uso de um lote, podemos acessar o controle de qualidade pelo atalho “ctrl + Q”. Ao acessar este módulo, será mostrado em tela os ensaios que estão cadastrados naquele produto, onde iremos escrever o resultado dos testes descritos.
Após completar a análise, será dado a opção de liberar ou bloquear o lote. Caso seja bloqueado, poderá ser feito uma nova análise.
A ficha de análise técnica do produto será emitida para impressão e aprovação do farmacêutico responsável:

---

## 🔴 Cadastrar Convênio — 20/07/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/405752
> Publicado em: 20/07/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Nesse artigo você irá ver como cadastrar um convênio
As formas de chegar a tela de cadastro do convênio são duas
1° Através do comando Ctrl + F, digita a palavra convenio e aperta o enter;
2° Através do menu Arquivo > Sub menu Venda > Convênio
Após abrir a tela de cadastro de convênios, você deve clicar no ícone
para cadastrar um novo convênio;
Na tela que abrir, você deve inserir o nome do convênio, e irá ter disponível em tela diversos campos conforme a sua necessidade, um exemplo você pode inserir um desconto e ou acréscimo padrão para esse convênio, após preencher os dados, você deve clicar no ícone:
para salvar o novo convênio, veja a seguir a tela de exemplo:
Após criar o convênio, você deve associar o mesmo no cadastro do seu cliente conveniado, para saber como fazer esse procedimento você deve acessar o seguinte artigo:
Incluindo convênio no cliente - Prismafive (movidesk.com)
Caso ainda fique em dúvida, entre em contato com nossa equipe de suporte técnico para melhor lhe auxiliar.

---

## 🔴 Conclusão de ordens de produção — 15/06/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/396814
> Publicado em: 15/06/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

CONCLUSÃO DE ORDEM DE PRODUÇÃO
Uma ordem de produção é gerada para cada manipulação que a farmácia realiza, seja ela para uma venda ou para produtos internos, como uma diluição ou base de outros medicamentos. A fim de
manter as quantidades adequadas em nosso inventário e otimizar o uso do sistema FarmaFácil no que se trata ao
gerenciamento
de estoque (para que possamos evitar situações em que a disponibilidade de medicamentos e outros produtos esteja comprometida), é necessário realizar a conclusão destas ordens de produção. Para isso, vamos realizar o seguinte procedimento:
Em PRODUÇÃO > MOVIMENTO > ORDENS DE MANIPULAÇÃO, podemos utilizar os filtros abaixo para visualizar quais são as ordens pendentes, concluídas e em processo de pesagem (quando houver). O relatório (PRODUÇÃO > RELATÓRIO > ORDEM DE MANIPULAÇÃO) também apresenta estas informações.
Para concluir as ordens pendentes, vamos selecionar a opção destacada (ou o atalho F6):
Para realizar a conclusão, temos duas alternativas:
a) Conclusão individual
Para concluir somente uma ordem de manipulação, iremos utilizar o campo "número", na conclusão de ordens, e iremos pesquisar pelo número da ordem de manipulação que queremos concluir.
b) Conclusão por data
Para conclusão de ordem de produção diária, semanal ou mensal, podemos selecionar o filtro abaixo conforme necessidade da farmácia. Utilizando o mesmo, todas as ordens com status "em produção" do período serão trazidas para a tela
Devido ao movimento da farmácia durante o dia a dia, é comum que ao utilizar a conclusão por lote apareça a seguinte mensagem:
No momento que realizamos uma venda, o sistema utiliza a quantidade em estoque do ativo em questão. Quando este lote não é identificado, podem existir alguns motivos:
- Lote vencido na hora da venda
- Quantidade insuficiente na hora da venda
Para informar os lotes no momento da conclusão das ordens, vamos seguir o procedimento abaixo após informar que queremos selecionar os lotes:
Ao selecionar a opção de incluir um lote, será mostrado na tela todos os lotes disponíveis daquele produto, para escolhermos a melhor alternativa:
Após selecionar o lote de todos os produtos, iremos concluir as ordens pelo botão destacado:
A conclusão das ordens de produção desempenha um papel fundamental no controle do estoque e é de extrema importância para garantir uma gestão assertiva e eficiente. Por meio desse procedimento, as quantidades comprometidas dos lotes são adequadamente registradas, permitindo que a farmácia visualize a quantidade real de matérias-primas disponíveis e utilizadas, auxiliando inclusive nas compras a serem realizadas. A seguir, apresentamos os resultados alcançados ao concluir esse importante processo:

---

## 🔴 Zerar estoque — 13/06/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/395936
> Publicado em: 13/06/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

ZERAR ESTOQUE DE PRODUTOS
Um dos principais motivos pelo qual se faz necessário zerar um estoque de produto ou de grupo é a validade expirada dos produtos. Além do descarte correto dos mesmos, precisamos também atualizar nosso estoque para que fique de acordo com a realidade da farmácia.
Para utilizar essa manutenção no FarmaFácil, temos duas regras que precisam ser seguidas:
Não é permitido utilizar a manutenção para grupo ou produtos controlados.
Não é possível zerar o estoque quando temos uma quantidade comprometida no mesmo, ou seja, é preciso concluir todas as ordens de produção pendentes para realizar este procedimento.
Neste artigo, iremos utilizar o grupo 12 como exemplo para o procedimento de zerar o estoque.  Nota-se que antes de começar a manutenção, geramos o relatório de posição de estoque do grupo (disponível em ESTOQUE > RELATÓRIO > POSIÇÃO DE ESTOQUE), que nos mostrou a quantidade de produto em estoque:
IMPORTANTE:
Essa opção não se aplica para os casos onde o lote está com estoque negativo e data de validade vencida.
No FarmaFácil, a opção de zerar o estoque encontra-se em ARQUIVO > UTILITÁRIO > MANUTENÇÃO GERAL:
Para realizar a manutenção, podemos escolher apenas os produtos com estoque negativo ou todos os produtos do grupo, conforme filtros abaixo:
Ao iniciar a manutenção, a seguinte mensagem aparecerá na tela, informando que a manutenção foi iniciada:
Além, caso tenha alguma ordem pendente, irá aparecer uma mensagem de erro solicitando que as mesmas sejam concluídas, conforme regra citada anteriormente:
Após a conclusão da manutenção, validade pela mensagem "MANUTENÇÃO REALIZADA COM SUCESSO", todos os produtos do grupo terão seu estoque zerado, com exceção dos controlados.

---

## 🔴 Unificação de cadastros — 06/06/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/394473
> Publicado em: 06/06/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

UNIFICAÇÃO DE CADASTROS DUPLICADOS
A unificação de cadastros no FarmaFácil tem como objetivo principal consolidar os registros em um único cadastro, contribuindo para a organização e melhoria do sistema, estabelecendo uma confiabilidade nas informações.
A unificação abrange diferentes tipos de cadastros utilizados nas vendas, tais como: CLIENTE, PRODUTO, POSOLOGIA, MÉDICO, CIDADE, CONVÊNIO, BAIRRO e VISITADOR. Ao realizar o processo de unificação, é necessário seguir alguns passos simples no FarmaFácil. Disponível em ARQUIVO > UTILITÁRIO > MANUTENÇÃO GERAL, informaremos qual tipo de cadastro desejamos unificar.
Em seguida, indicaremos o cadastro mais recente como "código atual" e o cadastro mais antigo (ou com mais informações registradas) como "novo código".
Dessa maneira, todas as vendas e ordens de produção registradas no cadastro duplicado do cliente serão transferidas para o cadastro mais antigo correspondente. Essa ação permite consolidar as informações e evitar redundâncias, proporcionando um panorama mais preciso e atualizado sobre as transações realizadas com cada cliente.

---

## 🔴 Fator de correção e Densidade — 06/06/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/394285
> Publicado em: 06/06/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Nesse artigo, irei te mostrar como chegar a tela de lotes, para informar e ou alterar valores como Fator de Correção e Densidade.
1° Passo:
ESTOQUE > MOVIMENTO > LOTE
:
2° Passo, você deve pesquisar
o produto ao qual você deseja validar essas informações, conforme exemplo abaixo:
Após pesquisar e selecionar o produto, confirmando no botão
o sistema irá retornar para a tela anterior, com o produto selecionado, conforme a seguir:
Com o produto selecionado, você deve clicar no ícone de alteração
(ou barra de espaço no teclado), com isso o sistema irá abrir a tela com todos os lotes que existem para aquele produto em questão, conforme a seguir:
Cada lote, possui informações de forma individuais, como fornecedor, nome, data de fabricação e validade, fator de correção (se houver), densidade e outros fatores como UI, UTR, UFC por exemplo, então nessa tela dos lotes do produto, você precisa selecionar o lote desejado e clicar no ícone
para ter acesso aos campos de fatores, para preencher e ou alterar:
Após realizar as alterações desejadas no lote em questão, você deve clicar no ícone
para que seja salvo as alterações feitas.
Detalhe importante, para que o sistema faça o correto cálculo de quantidades que saem na ordem de manipulação, você precisa verificar se o lote ao qual esteja informado o fator de correção e densidade, é o lote que está definido como em uso, na tela de lotes, o lote que estiver definido em uso terá um
você irá visualizar na tela de lotes da seguinte forma:
Caso seja necessário trocar o lote em uso, basta nessa tela você selecionar o lote que deseja deixar como Em uso e realizar o seguinte comando:
Após realizar a alteração, lembrar de clicar em
Caso ainda fique com alguma dúvida entre em contato conosco através da central de tickets.

---

## 🔴 Diluição — 01/06/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/393247
> Publicado em: 01/06/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

DILUIÇÃO E ORDEM DE PRODUÇÃO - VISÃO GERAL
Na farmácia de manipulação, a diluição é um processo essencial que envolve a redução da concentração de uma substância ativa em um medicamento ou fórmula para atingir a dosagem desejada. Ela é realizada adicionando-se um solvente apropriado à substância original, resultando em uma solução final com uma concentração diluída.
O FarmaFácil utiliza a fórmula padrão e a ordem de produção interna para realizar o processo de diluição de ativos, conforme será explicado a seguir:
Cadastro de fórmula de diluição
Para cadastrar uma nova fórmula padrão de diluição, vamos acessar o módulo ARQUIVO > PRODUÇÃO > FÓRMULA PADRÃO
Neste artigo, vamos utilizar como exemplo a diluição de uma Vitamina D3, no padrão 1:100.
Tipo:
O tipo Base/Excipiente/Semi-Acabado serve para produções internas
como a diluição
, onde o produto final será uma outra matéria-prima (base ou excipiente)
.
Forma
: nesse campo deve-se escolher o tipo de Forma Farmacêutica dessa produção. Isso vai influenciar no tipo de cálculo feito pelo sistema.
Validade
: define a validade do produto que será gerado pela Fórmula Padrão. Caso não seja informado, o sistema irá considerar a validade definida na Forma Farmacêutica.
Volume e Unidade
: indica a quantidade a ser produzida. Este campo é habilitado somente se a Forma Farmacêutica for do tipo Volume ou, no caso de ser uma Pré-Venda, também for do tipo Homeopatia e Floral.
Produto final
: neste campo deve ser informado qual é o produto resultante da Fórmula Padrão, ou seja, qual produto a Fórmula Padrão vai produzir. O produto final deve estar cadastrado no grupo adequado, dependendo do tipo de Fórmula Padrão que vai ser criada.
Observação
: campo livre, onde é possível colocar qualquer tipo de informação adicional para a Fórmula Padrão. Pode ser usado para indicar o modo de preparo da fórmula.
O cálculo da diluição é feito da seguinte forma:
Passo 1: quero uma diluição de 1 parte de MP pura e 99 partes de QSP, portanto, 1/100 = 0,01
Passo 2: o sistema faz o cálculo de forma percentual, então multiplicamos a diluição por 100 = 1
Por exemplo, se fossemos utilizar uma diluição 1:1000, o cálculo ficaria:
1 parte de MP pura e 999 partes de QSP, portanto, 1/1000 = 0,001
Multiplicamos a diluição por 0,001 * 100 = 0,1
2.
Ordem de produção interna
Para que possamos utilizar o produto diluído que criamos acima, vamos criar e produzir uma ordem de produção interna, com o intuito de gerar um lote do produto final com quantidade, validade etc.
Para criar a ordem de produção, iremos acessar o módulo PRODUÇÃO > ORDEM DE MANIPULAÇÃO e adicionar uma nova ordem, conforme demonstrado abaixo:
Iremos utilizar a fórmula padrão criada anteriormente:
Para a produção de 100g com a diluição 1:100, o sistema calculou 1g do ativo puro e 99g do QSP.
Concluindo esta ordem de produção interna, vamos gerar um lote com a quantidade de 100g da diluição que será utilizado como produto final nas vendas.
Nota-se também que quando realizamos este 
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Homeopatia - visão geral — 10/05/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/386684
> Publicado em: 10/05/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

HOMEOPATIA - VISÃO GERAL
A homeopatia é uma prática terapêutica que busca tratar os indivíduos com doses altamente diluídas de substâncias que, em doses mais altas, produzem sintomas semelhantes aos da doença que está sendo tratada. Depois que a solução homeopática é preparada, ela é geralmente armazenada em frascos esterilizados e rotulada com informações importantes, como o nome do remédio, a concentração, a data de fabricação e as instruções de uso.
No farmafácil, os módulos de produção homeopática auxiliam na organização,  nos padrões rigorosos de qualidade e segurança, e com técnicas de produção adequadas.
DINAMIZAÇÃO
O processo de dinamização é uma etapa crucial na produção de remédios homeopáticos. Essa técnica consiste em diluir e agitar repetidamente a substância base, e o número de diluições e agitações pode variar de acordo com o tipo de substância e o objetivo do remédio.
Em ESTOQUE > MOVIMENTO > GERAR DINAMIZAÇÃO conseguimos realizar este processo:
Exemplo de dinamização:
1.1.
PRODUTO REFERÊNCIA
A tintura mãe é a base da dinamização homeopática, obtida a partir da extração de uma substância natural e sua diluição em álcool. A partir dessa diluição, são feitas outras diluições sucessivas e agitações vigorosas para produzir as chamadas potências homeopáticas. Recomendamos que, por fins de organização do processo de produção, a tintura mãe seja cadastrada em um grupo de matéria-prima, conforme o utilizado no exemplo.
Também, podemos utilizar um produto já dinamizado como produto referência, desde que a potência inicial seja inferior a dinamização final. Por exemplo, se eu compro uma matéria prima já dinamizada em 1 CH, posso utilizar ela como produto referência para produzir dinamizações a partir de 2 CH.
É necessário apontar um lote para que seja utilizado na produção, mas a dinamização e método não são obrigatórios por se tratar de uma matéria prima.
1.1.
PRODUTO DINAMIZADO
Este é o produto que queremos gerar a dinamização a partir da tintura mãe, o “produto final” deste processo. Selecionamos qual seria a potência homeopática (agitações) e qual seria o método utilizado nesta dinamização, além da validade.
Posteriormente, iremos exemplificar o lote que é gerado no final da dinamização deste produto.
1.1.
VEÍCULO
O veículo padrão é uma substância inerte (semelhante ao QSP, porém em forma líquida), como água ou álcool. É utilizada para diluir as substâncias ativas presentes em medicamentos homeopáticos. Essa opção é disponibilizada para as formas farmacêuticas homeopatia, papel e floral.
A quantidade de “ml” produzido seria o total a ser produzido e  armazenado.
1.1.
DINAMIZAÇÕES GERADAS
Neste ponto, geramos as dinamizações da potência que definimos, sendo desmembrada em ordem crescente. Dependendo da necessidade da farmácia, você pode selecionar mais de uma dinamização para ser gerada e armazenar em seu estoque.
Após salvar a dinamização, será emitido o documento
na impressora definida como padrão, caso não seja possível visualizar é n
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Curva ABC de produtos — 09/05/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/386494
> Publicado em: 09/05/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

A Curva ABC de produtos é uma ferramenta de gestão muito importante para a área de vendas em farmácias, pois permite classificar os produtos em relação à rentabilidade e focar naqueles que são mais importantes para o negócio. O conceito se baseia no Princípio de Pareto
,
que estabelece
:
-
20% dos produtos
vendidos
equivalem a
80%
do faturamento
da farmácia
;
-
30% dos produtos
vendidos
equivalem a
15%
do faturamento
da farmácia
;
-
50% dos produtos
vendidos
equivalem a
5%
do faturamento
da farmácia
;
Com o Farmafácil, o cálculo (que leva em consideração a quantidade de produtos vendidos no período, o valor das vendas realizadas, o lucro total e a participação do lucro de cada produto) é automatizado e os relatórios são facilmente acessíveis, tornando a gestão mais eficiente e eficaz. Para acessar o cálculo, basta ir em ARQUIVO > ESTOQUE > PRODUTO e clicar no ícone destacado.
Os filtros disponíveis permitem gerar a curva por valor, quantidade ou markup dos produtos. É recomendado que o período analisado seja de pelo menos 3 meses para maior precisão nos dados.
Com a curva calculada, é possível verificar relatórios de cada curva no módulo VENDA > RELATÓRIO > CURVA ABC, avaliando individualmente ou de forma geral, de acordo com o filtro selecionado.
No cadastro dos produtos, também é informado a qual curva cada um pertence, sendo essa informação utilizada no módulo de compras
. Para avaliar quando foi a última curva gerada, podemos acessar os parâmetros gerais, conforme destacado abaixo:

---

## 🔴 Mensagem Padrão — 29/03/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/376146
> Publicado em: 29/03/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Você tem nossa ferramenta PrismaSync? se sim nesse artigo vamos te mostrar como chegar até a parte de cadastro de Mensagem padrão, que são as mensagens enviadas por dentro do FarmaFácil, referente ao orçamento de seu cliente.
Existem duas formas de você chegar até a tela de cadastro da Mensagem Padrão:
1° opção:
Apertar: Ctrl + F, digitar mensagens padrão + Enter:
2° opção:
Arquivo > Venda > Mensagens padrão:
A tela de cadastro de mensagens padrão irá aparecer da seguinte forma para você:
Ponto importante referente as mensagens padrão
, devem seguir essa sequência e com essa descrição, pois elas são as etapas dos seus orçamentos do Sync, sendo assim você pode editar cada uma delas, mas
não deve excluir
ou alterar a sequência numérica, pois isso irá ocasionar em mal funcionamento das mensagens, para editar uma das mensagens, basta selecionar na lista qual deseja editar, e clicar no ícone:
(ou barra de espaço) para abrir a tela com a mensagem para edição.
Na tela, você irá então editar o texto conforme desejar e após concluir irá clicar no ícone na parte inferior para salvar a sua alteração. Algumas palavras ficam entre Colchetes [ ], caso você queira editar uma dessas palavras existe um ícone no canto inferior esquerdo
que ao clicar nele irá te exibir um menu com palavras que você pode estar utilizando no seu texto:
Vamos a um exemplo prático, no texto da mensagem está aparecendo a palavra [FORMULAS] ou seja irá aparecer na mensagem de forma resumida para o cliente, não contendo todos os itens lançados naquela fórmula, caso você deseja que sua mensagem saia com todos os itens da fórmula você deve alterar a palavra: [FORMULAS] deixando: [FORMULASCOMPLETA] após realizar a edição da mensagem e salvar a sua alteração, as próximas mensagens já vão aparecer no formato que você deixou para serem enviadas nos orçamentos, na tela do Sync orçamentos.

---

## 🔴 Imagem de receita — 15/03/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/372205
> Publicado em: 15/03/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Você precisa anexar a imagem da receita, dentro da venda lançada no FarmaFácil? sim é possível e tem 3 opções:
No painel de vendas, seleciona venda desejada e aperte a tecla de atalho F8, ou clique no ícone, conforme imagem abaixo:
Na tela em que abrir você deve clicar no ícone para pesquisar e selecionar a imagem, que já deve estar salva no seu computador, após selecionar a imagem em questão, você irá clicar no ícone para salvar a imagem dentro da venda, conforme imagem a seguir:
Após salvar, quando apertar a tecla F8, será exibido a imagem que você salvou dentro da venda, caso haja necessidade você também pode imprimir a imagem:
Além de conseguir pelo painel principal de vendas, você também consegue inserir imagem quando você estiver na tela dentro de uma venda em específico:
E a terceira forma, seria por dentro da tela onde você está montando a fórmula/venda:

---

## 🔴 Pesagem Monitorada - Visão Geral — 06/03/2023

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/369716
> Publicado em: 06/03/2023
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Módulo de Pesagem monitorada
Visão geral
A pesagem monitorada consiste em um sistema acoplado às balanças digitais dos laboratórios que visa monitorar a pesagem de substâncias, evitando falhas do operador na pesagem e escolha da matéria prima através de leitura óptica
de código de barras, evitando assim, erros no processo que é um dos mais importantes na produção de medicamentos.
Desta forma, além de assegurar que as substâncias e as dosagens dos medicamentos presentes na ordem de produção estão corretas, este sistema agiliza a rastreabilidade das formulações através de identificação virtual de lote, validade, fornecedor, operador, etc.
Dentro disso, quando a matéria-prima chega na farmácia é realizado todo o processo de controle de qualidade (algumas farmácias usam a quarentena). Após serem liberados, os lotes das matérias-primas são armazenadas em recipientes/embalagens adequados e recebem uma etiqueta (etiqueta de entrada de estoque)
com suas informações do lote e código de barras.
Tendo os lotes armazenados e identificados, diariamente, o responsável pela pesagem recebe a ficha de produção do paciente que possui todas as informações da fórmula a ser manipulada e também um código de barras que a identifica. Quando o operador lê o código de barras da ordem de produção (Usando leitor de código de barras) essa ordem é lida pelo sistema, onde é listado na tela cada ativo e a dosagem exigida na formulação, nesse momento é feita a pesagem dos ativos que faz com que a quantidade na balança tenha que estar de acordo com o que está na ordem de produção, bem como o lote selecionado para que fique evidenciado que o processo de manipulação está de acordo com o documento e vice e versa. Sendo assim, ao fazer o processo de pesagem é possível atingir ampla segurança na produção eliminando o erro humano em relação a seleção dos ativos e quantidades a serem pesadas, pois caso o operador pegue outro ativo por engano e que não esteja na fórmula, o sistema o avisa em tela, da mesma forma, o sistema só permite continuar a pesagem se a quantidade for exata a calculada na ficha de produção do paciente (não funciona da mesma forma quando se trata de ordem de produção interna.
Por fim, esta função traz agilidade e segurança no procedimento de pesagem da matéria-prima. Neste processo o sistema lê a quantidade aferida na balança e confere com a quantidade requisitada, verificando se a matéria-prima e lote indicados são os mesmos solicitados na ficha de pesagem, conforme citado anteriormente, com isso, o farmacêutico tem a garantia de que o produto pesado no laboratório estará rigorosamente de acordo com as indicações da ordem de produção, ficando tudo registrado no sistema.
Habilitando a pesagem no FarmaFacil
No primeiro momento é importante averiguar se a(s) balança(s) estão instaladas, comunicando corretamente com o computador para que o sistema possa fazer a leitura do peso. Para isso é necessário que a balança esteja cadastrada e que a chave este presente nas 'confi
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Ajustar valor de venda do Produto de forma manual — 07/11/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/340127
> Publicado em: 07/11/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Esse artigo irá te mostrar o caminho para ajustar o valor de venda de um determinado produto, o primeiro passo é acessar a tela de cadastro de produtos através do seguinte caminho:
ARQUIVO > ESTOQUE > PRODUTO
DEPOIS DISSO VOCÊ DEVE LOCALIZAR O PRODUTO QUE DESEJA ALTERAR, PARA ISSO VOCÊ PODE APERTAR O BOTÃO F2 OU O ÍCONE:
APÓS PESQUISAR E SELECIONAR O PRODUTO DESEJADO, ELE IRÁ VOLTAR PARA A TELA DO CADASTRO DE PRODUTOS COM O MESMO SELECIONADO EM AZUL, CONFORME EXEMPLO:
COM O PRODUTO DESEJADO ENTÃO SELECIONADO, VOCÊ PODE APERTAR A TECLA BARRA DE ESPAÇO NO TECLADO OU ENTÃO NO ÍCONE:
PARA ABRIR O CADASTRO DESSE DETERMINADO PRODUTO EM MODO DE ALTERAÇÃO.
NA TELA QUE ABRIR, VOCÊ DEVE ENTÃO INFORMAR O SEU PREÇO DE VENDA PARA AQUELE PRODUTO E ENTÃO APERTAR ENTER PARA SALVAR A ALTERAÇÃO OU ENTÃO CLICAR NO ÍCONE:
VEJA EXEMPLO ABAIXO:
ALÉM DO CAMPO VALOR VENDA, CASO VOCÊ ALTERE O % DO CAMPO MARKUP, ESSA ALTERAÇÃO TEM COMO CONSEQUÊNCIA ALTERAÇÃO NO VALOR DE VENDA TAMBÉM.

---

## 🔴 REPETIÇÃO DE FORMULA COMO FAZER PARA SOMENTE COPIAR — 19/10/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/331201
> Publicado em: 19/10/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O processo de repetição de venda pode ser feito da seguinte forma:
Na tela de vendas clique em + para criar uma nova venda > Clique em Venda/Alt+R para buscar a venda anterior que deseja repetir (a busca pode ser feita por cliente, venda, produto, CPF, etc).
Após encontrar a venda que deseja repetir selecione a formula (uma ou todas) - Mude a opção de 'NÃO' para 'SIM' - Para isso basta pressionar 'S' ou 'N' no teclado do seu computador.
Feito isso o sistema importará o registro selecionado para a tela de vendas e você poderá proceder com a emissão normalmente.
À disposição.

---

## 🔴 NF Importação — 23/09/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/325160
> Publicado em: 23/09/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Após o cadastramento da nota no sistema e com base nos documentos recebidos referente a mercadoria a ser coletada é necessário informar os valores no sistema para calculo dos totais (Produtos, Base de ICMS, Valor do ICMS).
No cadastro do cliente serão informados os campos
bairro, cidade
(código de IBGE nesse caso é igual a 9999999)
e estado = EX
. Os campos de CNPJ e I.E. devem permanecer em branco. Conforme abaixo:
Os itens da nota serão preenchidos de acordo com a nota de compra, bem como o NCM, Alíquota de ICMS e valores unitários.
Após cadastrar a nota contendo as informações da nota de compra, entram em questão as informações referente aos demais custos. Para inserir estes custos na nota sem alterar o valor do item será necessário
somar o total geral - o total dos produto = diferença / pelo total de itens da nota
, nesse caso: R$72,209,273 - R$53.208,21 = R$19.001.52 / 15 = R$1.266,768.
Feito esse calculo, o valor a ser rateado em cada item é de R$1.266,768 e este será inserido no campo
outras despesas
e após será realizado o seguinte cálculo:
Valor do rateio informado em outras despesas + Valor Total do Item = BC ICMS * Alíquota de ICMS = Valor de ICMS
. No caso:
R$1.266,768 + R$7,00 = R$1.273,77 * 18% = R$229,28
Códigos CST, CSOSN
NCM de acordo com o que está informado na nota de compra.
Feito isso para todos os itens os valores totais correspondentes serão exibidos na tela da nota de acordo com a nota de compra.
Feito isso basta cadastrar os dados de importação:
Os campos em destaque sempre usarão essas informações por padrão, que são:
Código Estrangeiro: 0000000
Código Exportador: 0
Adicções com:
Número da Adição = 1
(sempre)
Código do Fabricante = 1
(sempre)
Vlr Desconto = 0,00
(sempre)
Feitos esses passos a nota será emitida com sucesso.

---

## 🔴 Vincular Visitador no cadastro de Médicos — 31/08/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/318651
> Publicado em: 31/08/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

ARQUIVO > SUB-MENU(VENDA) > MÉDICO:
Na tela você irá pesquisar e selecionar o médico, ao qual deseja vincular um Visitador, e clicar na opção de Alterar o cadastro desse médico que é através da barra de espaço do teclado ou do ícone
:
Na tela de cadastro que abrir, você irá clicar na aba Complemento, irá pesquisar o visitador que deseja deixar vinculado e depois irá apertar Enter para salvar a alteração:

---

## 🔴 Configuração NFS-e Simpliss - Piracicaba — 29/07/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/310583
> Publicado em: 29/07/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Versão do sistema:
20.01.57.00
ID do Redmine:
Sem ID
Arquivos relacionados em anexo.
Para configurar Emissão de Nota Fiscal de Serviço / NFS-e com provedor SIMPLISS.
- **Login e senha de acesso ao site da prefeitura para emissão de NFS-e;
-Inscrição Municipal;
**São de extrema importância para esse provedor.
-Copiar do Armazenamento externo
Prisma Drive
os seguintes arquivos:
*Arquivos em anexo nesse artigo.
-
Acbr.rar

---

## 🔴 Sync Orçamento — 28/07/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/310217
> Publicado em: 28/07/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Nesse artigo, você verá um passo a passo, de como gerar um orçamento, do início ao fim, para quem utiliza a ferramenta
PrismaSync
1° Passo
na tela de conversação com o cliente, no canto inferior direito da tela, terá o ícone para gerar seu orçamento, conforme imagem abaixo:
Na tela a seguir, caso o cliente tenha enviado receita por arquivo/imagem é possível você selecionar o arquivo desejado, logo após na parte inferior esquerda irá clicar no
Enviar
, para que nesse momento seja gerado um orçamento dentro do
FarmaFácil
, conforme imagem:
A partir desse momento, você devera seguir pela tela do sistema
FarmaFácil
:
Venda > Movimento > Sync Orçamento
Na tela a seguir você deverá selecionar o orçamento desejado, podendo utilizar qualquer um dos campos disponíveis na tela para filtro, e depois vai clicar em
Filtrar
, conforme imagem:
Após selecionar o orçamento desejado, deve clicar no ícone para ser redirecionado a tela de venda/orçamento do sistema, conforme imagem:
Você deverá então montar de fato o orçamento para o cliente normalmente, salvar, e sair da tela de orçamento, com isso irá voltar para a tela do Sync orçamento com a seguinte pergunta:
Ao clicar em
Não
, o orçamento irá mudar o status de
pendente
para
processando.
Ao clicar em
Sim
, o orçamento irá mudar o status de
pendente
para
calculado
e irá abrir uma telinha com a mensagem do orçamento calculado para ser enviado ao cliente, conforme imagem:
Quando o cliente confirmar que deseja comprar com a sua farmácia, você deverá voltar a tela do Sync Orçamentos no
FarmaFácil
, filtrar por aquele orçamento novamente e então clicar no seguinte ícone
a seguir o sistema irá apresentar a seguinte mensagem:
você deve clicar em
A partir desse momento, você será redirecionado para a tela de venda/orçamento do sistema, você deverá desmarcar o check do orçamento (
) e depois clicar para salvar (
) , transformando assim aquele orçamento em venda:
A partir desse momento, o status do orçamento irá mudar de
calculado
para
confirmado
e você terá a opção de enviar a mensagem para o cliente referente a aprovação da venda:
Outras dicas em relação ao Orçamento entre o PrismaSync e o FarmaFácil:
No
PrismaSync
, na tela de conversação com o cliente, na parte superior direita da tela você terá o seguinte ícone disponível:
Ao clicar no mesmo, você terá acesso visual a todos os orçamentos que já foram criados através do
PrismaSync
para aquele cliente em questão:
Dessa forma, você consegue evitar de gerar orçamento de forma duplicada para um mesmo cliente por exemplo.
No
FarmaFácil
na área de Sync Orçamentos caso tenha criado orçamento de forma duplicada para um cliente, você pode selecionar um deles e efetuar o cancelamento do mesmo clicando no ícone
que fica disponível na parte inferior da tela Sync Orçamentos, dessa forma você terá um orçamento ativo e outro como cancelado.
Demais opções na área do Sync Orçamentos:
Mesmo ícone da tela de venda do sistema, serve para gerar e ou editar um romaneio de entrega daquele o
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Configuração NFS-e IPM Cascavel — 25/07/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/309091
> Publicado em: 25/07/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Versão do sistema:
20.01.55.01 / 60.0
1
ID do Redmine:
#
7654
Arquivos relacionados em anexo.
Para configurar Emissão de Nota Fiscal de Serviço / NFS-e com provedor IPM.
- **Login e senha de acesso ao site da prefeitura para emissão de NFS-e;
-Inscrição Municipal;
**São de extrema importância para esse provedor.
-Copiar do Armazenamento externo
Prisma Drive
os seguintes arquivos:
*Arquivos em anexo nesse artigo.
Na maquina do cliente colocar os arquivos nas seguintes pastas:
-Extrair o arquivo ACBrNFSeXServicos.ini e Prisma5NFSe.dll no diretório: C:\FarmaFacil\exe\
As Pastas Acbr e Schemas devem ser inseridas em seus respectivos locais como a imagem abaixo:
Ir e
Em Parâmetro e configurar conforme Imagens abaixo:
Na configuração do provedor ATENÇÃO ao "Padrão" deve ser "DllPrismaFiveX".
Mesmo não existindo a pasta Schemas 'IPM_110' deve ser informado EXATAMENTE isso no 'Provedor' e no 'Nome da pasta de Schemas'
Justificativas de cancelamento:
[1]-Erro na emissão
[2]-Serviço não prestado
[3]-Erro de assinatura
[4]-Duplicidade de nota
[5]-Erro de processamento
*Caso esteja atualizando para versão 20.01.60.01 repita os passos acima usando os arquivos que estão nesse artigo.
Por fim emitir nota no sistema e validar com cliente.

---

## 🔴 Melhores Praticas de Descrição de Tickets — 20/05/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/291044
> Publicado em: 20/05/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O proposito deste artigo é :
Padronizar o cadastro das iterações do analista;
Centralizar informações sobre o inconsistência ou duvida do cliente;
Orientar a captura de evidencias e anotações para resolução ágil e eficiente;
Orientar analistas para melhores praticas de redação / edição de textos nos Tickets;
Facilitar o entendimento do conteúdo sem a necessidade de outras iterações entre analistas e também com cliente;
Apontar onde ao olhar e identificar no sistema e do que se trata a inconsistência;
Por consequência sanar de forma clara, eficiente e pratica a solução, duvida ou inconsistência pelo cliente identificada.
Assunto:
Esse campo pode ser
alterado pelo analista
quando necessário e identificado que o
assunto não coincide
com a inconsistência identificada pelo cliente, porque:
-Auxilia na primeira visualização do ticket;
-Ajuda a definir categorização e prioridades;
Figura. - Edição de Assunto.
Figura. - Assunto diferente do serviço.
Figura. - Assunto igual ao serviço.
Mensagem:
- Registre o contato e coloque o nome da pessoas que foi efetuado a interação;
Figura - Ausência de Registro.
Figura - Registro Correto.
Figura - Sugestão de Texto.
- Descreva todas os passos/ etapas realizadas para simular o problema com o máximo de detalhes possíveis;
- Anexe imagens ou vídeos que facilitem a compreensão do problema;
- Informe o quando e como a inconsistência começou a ocorrer como por exemplo:
Se ocorreu após alguma data especifica;
Se foi após atualização do sistema;
- Informe os dados de entrada utilizados;
- Filial utilizada pelo usuário;
- Informe o comportamento atual e o esperado;
- Informe ambiente e versão da aplicação;
- Anexe Evidências com marcações e anotações(capturas de tela, logs, etc….);
- Procure inserir o caminho do processo executado pelo usuário com o máximo de detalhes;
Exemplo:
Receber o pagamento de parcelas dessa venda com os seguintes passos:
Caixa>> Movimento >> Caixa >>Botão incluir novo>> Pressionar "F2" >>Aba "A Prazo Pendente" >>Pesquisar pelo cliente>>
Selecionar Todas vendas>>
Exemplo:
Na tela de Caixa inserir valor recebido e duas formas de pagamento;
O total do valor das Vendas é R$280 e o recebimento de R$80 o valor deveria ser R$200 e esta sendo de R$180 conforme imagem:
Importante notar que o sistema efetua os recebimentos de valores normalmente quando não é usado duas formas de pagamento.
- Efetue testes com a versão que o cliente informa que o sistema funcionava, esse informação é importante pois caso seja um erro de versão será possível buscar as alterações efetuadas no sistema;
**Caso não tenha um banco e sistema com as versões necessárias para testes pode solicitar essas informações ao Analista de Infra Diogo ou ao Back Service.
- Informe as etapas realizadas para simular este problema em sua estação de trabalho / computador local:
Acessar a tela de relatório do “Movimento Estoque” (Estoque > Relatório > Movimento);
Preencher os campos com as seguintes informações: classificação analítico, selecionar um
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Configuração e recebimento de vendas a prazo — 13/05/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/287765
> Publicado em: 13/05/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Por que oferecer pagamento parcelado ou ficha aos clientes?
Certamente, atender às preferências dos clientes é uma das principais razões pelas quais a oferta de parcelamento e flexibilidade é tão importante. Ao fazer isso, evita-se perder boas vendas e, consequentemente, eleva a lucratividade e espaço no mercado de atuação. Dentro disso, o sistema permite que seja feita uma análise de perfil do cliente, com base nessa análise de perfil, o cliente poderá ter estipulado um limite de compra e também a possibilidade de comprar a prazo - parcelado e a prazo - ficha.
Qual a diferença entre o prazo - parcelado e o prazo - ficha?
A prazo - parcelado: O pagamento parcelado é aquele cujo valor total de uma compra é dividido em partes menores no momento da cobrança. Na prática, significa que o cliente adquire o item e/ou serviço desejado e não precisa pagar por ele de uma única vez, fará o pagamento em parcelas fixas.
A prazo - ficha: A opção de pagamento a prazo ficha permite que o cliente pague o valor total em partes, porém, de acordo com a sua possibilidade, seria o famoso "paga como pode", muito usado com clientes fidelizados que fazem a compra e pagam o valor total em partes com data e valores indefinidos que variam de acordo com a possibilidade do cliente.
Como configurar um cliente para comprar a prazo?
Acesse o cadastro do cliente para realizar as configurações necessárias:
Arquivo > Venda > Cliente > Selecione cliente > Selecione a Aba Limite de Compra > Clique em editar e marque a opção desejada:
Tendo o cliente configurado, também é necessário cadastrar uma forma de pagamento com o mesmo tipo de configuração, abaixo forma de pagamento tipo 'prazo - parcelamento':
Arquivo > Venda > Forma de pagamento:
Tendo o cadastro do cliente configurado, a forma de pagamento cadastrada, basta gerar as vendas para o cliente e realizar o recebimento no caixa, para isso acesso:
Caixa > Movimento > Caixa > Incluir > Informe a venda > informe a forma de pagamento cadastrada > defina as parcelas e clique para emitir o documento fiscal:
Feito o recebimento no caixa, bem como a definição das parcelas e datas de pagamento será emitido o documento fiscal juntamente com o comprovante de débito para facilitar o controle da farmácia e o status da venda passará a ser 'Parcial', isso porque houve a transação indicando a forma de pagamento (normalmente chamado de primeiro recebimento), porém, as parcelas seguem pendentes até que sejam quitadas.
Antes de realizar a quitação das parcelas, a farmácia pode configurar aplicação de multa, juros diários e prazo de tolerância, com isso, caso ultrapasse a data de vencimento o sistema aplicará a multa e os juros automaticamente, esses custos já serão inseridos no total a receber no caixa juntamente com a (s) parcela(s).
Para realizar as configurações acesse:
Arquivo > Parâmetro > Parâmetro > Geral:
Dando andamento no recebimento da venda, para receber a(s) parcela(s), acesse:
Caixa > Movimento > Caixa > Incluir > Pressione "F2" > Aba 
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Plano de Contas. — 06/05/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/285979
> Publicado em: 06/05/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Plano de contas
O plano de contas é um conjunto de contas que representam os eventos e movimentações econômicas e financeiras que acontecem durante as atividades e operações de uma empresa. Portanto, o objetivo é nortear os trabalhos contábeis de registro das operações.
Por isso a importância de um plano bem estruturado. Afinal, é o plano de contas que vai organizar e categorizar as informações econômico-financeiras da organização, isto é, estabelecer padrões para o registro das operações da empresa.
Para acessar o plano de contas, segue o caminho:
Arquivo >>> Parâmetro >>> Plano de Contas
Para incluir um sub-grupo selecione o anterior e clique no adicionar.
Selecione um plano de conta; selecione um grupo D.R.E; Pressione F3 para realizar o vínculo.
Ao concluir os vínculos, pode clicar em SAIR
.
O plano de contas é utilizado em:
Forma de pagamento;
Entrada de notas;
Contas a pagar;
O uso do relatório “receitas x despesas” depende da configuração adequada do plano de contas.

---

## 🔴 Requisitos para Emissão ou Troca de Provedor de Nota Fiscal de Serviço / NFS-e — 29/04/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/284079
> Publicado em: 29/04/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Orientar cliente que pode haver cobrança caso provedor não esteja integrado ao nosso sistema, solicitar, inserir e anexar as seguintes informações que podem ser obtidas com a Contabilidade:
- Razão Social;
- CNPJ;
- Inscrição Estadual;
*Dados acima podem ser obtidos no moviedesk pressionando o mouse sobre o nome da empresa no ticket irá aparecer os dados.
- Inscrição Municipal;
- ID CNAE (Código Tributação do Município);
- Código de Atividade da Farmácia (Item lista de Serviço);
- CST/ISS;
- A alíquota de ISS;
- Certificado digital
- Login e senha de acesso ao site da Prefeitura;
- Verificar se a empresa esta apta para emitir nota em ambiente de homologação ou produção;
- WebService usado pelo prefeitura, para emissão das notas de serviço;
- Manual de Integração;
Com as informações verificar
lista de cidades e provedores
selecionando o
link
:
Caso não tenha integração colocar informações e arquivos acima no ticket encaminhar para o setor responsável e aguardar análise.

---

## 🔴 Lista Provedores Emissão de Nota Fiscal de Serviço / NFS-e — 26/04/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/283336
> Publicado em: 26/04/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para iniciar o processo de configuração obtenha os dados para configuração conforme processo descrito em:
Requisitos Emissão de Nota Fiscal de Serviço / NFS-e
Cidade
Provedor
Link de Acesso
Manual
Aracaju
WebISS
https://aracajuse.webiss.com.br
Configuração NFS-e WebISS Aracaju
Arraras
SiglSS
https://araras.sigissweb.com
Configuração NFS-e SIGISS Arraras
Bauru
SIL TECN.
https://tributario.bauru.sp.gov.br
Configuração NFS-e SIL Tecn.- Bauru
Cascavel
IPM
https://www.nfs-e.net/fiscalweb.php
Configuração NFS-e IPM Cascavel
Palhoça
IPM
https://nfse-palhoca.atende.net
Configuração NFS-e IPM- Palhoça
Vila Velha
SmarAPDv23
https://tributacao.vilavelha.es.gov.br
Configuração NFS-e SmarAPDv23 - Vila Velha
Balneário Camboriú
Publica
http://nfse1.publica.inf.br/balneariocamboriu_nfse
Configuração NFS-e Publica - Bal. Camboriú
Belém
SIAT
http://siat.belem.pa.gov.br
Configuração NFS-e SIAT -  Belém
Jaraguá do Sul
Betha
https://e-gov.betha.com.br/e-nota/login.faces
Itajaí
Publica
https://nfse.itajai.sc.gov.br
Configuração NFS-e Publica - Itajaí
Indaial
IPM
https://www.nfs-e.net/fiscalweb.php
Canoinhas
Publica
http://nfse2.publica.inf.br/canoinhas_nfse
Configuração NFS-e Publica - Canoinhas
Piracicaba
Simpliss
https://piracicaba.simplissweb.com.br
Configuração NFS-e Simpliss - Piracicaba
Ponta Grossa
Elotech
https://pontagrossa.oxy.elotech.com.br/iss/home
Configuração NFS-e Elotech Ponta Grossa
Ribeirão Preto
ISSNET
https://www.issnetonline.com.br/ribeiraopreto
Rio Grande
SIGISS
https://riogrande.sigiss.com.br/riogrande
Configuração NFS-e SIGISS Rio Grande
São Gonçalo
Simpliss
https://saogoncalo.simplissweb.com.br
Configuração NFS-e Simpliss São Gonçalo
São Paulo
FocusNFe
https://www.nfp.fazenda.sp.gov.br
Configuração NFS-e FocusNFe- São Paulo
Sorocaba
DSF
https://notafiscal.sorocaba.sp.gov.br
Configuração NFS-e DSF Sorocaba
Timbo
IPM
https://timbo.atende.net
Configuração NFS-e IPM Timbó
Blumenau
Simpliss
https://nfse.blumenau.sc.gov.br/contrib/Inicio
Sombrio
Betha
https://e-gov.betha.com.br/e-nota/login.faces
Joinville
ISSJoinville
https://nfem.joinville.sc.gov.br/login.aspx
Configuração NFS-e ISSJoinville Joinville
Matão
GINFES
https://portal.gissonline.com.br/login/index.html

---

## 🔴 Documentação Integração API Alcance — 17/03/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/275035
> Publicado em: 17/03/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Toda documentação do funcionamento da API é gerenciado pela aplicação
swagger
Link da documentação atual:
https://api-alcance.prismafive.com.br/swagger/index.html

---

## 🔴 Documentação Integração API Dashboard — 17/03/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/275007
> Publicado em: 17/03/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Toda documentação do funcionamento da API é gerenciado pela aplicação
swagger
Link da documentação atual:
https://api-dashboard.prismafive.com.br/swagger/index.html?urls.primaryName=API%20Terceiro
Link da documentação Legada:
https://phpstack-525076-2421343.cloudwaysapps.com/drive/s/2xzUusFuz2A6FfoKOE2ADmDFtWSdWl

---

## 🔴 Transferência entre filiais — 14/03/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/274123
> Publicado em: 14/03/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Nesse artigo irá te mostrar, como gerar uma transferência por dentro do sistema.
Acesso através do menu Estoque > Movimento > Transferência:
Nessa parte você irá definir o
Sentido
se é uma entrada ou saída, ou seja se estou na Matriz e quero transferir um determinado
produto
para filial, deve-se marcar o sentido como Saída, no campo Nota fiscal, não é obrigatório, campo
CNPJ
, você irá preencher com o destino, depois de preenchido esses campos, você irá incluir os itens que está transferindo. Se eu gerei uma transferência de saída através da matriz, posteriormente para a entrada de estoque ser feita na filial, eu preciso, ou importar a nota de entrada (se foi gerado uma nota de saída) ou então preciso gerar uma transferência de entrada na filial.
Caso opte por gerar uma nota fiscal da transferência, segue link do artigo:
https://prismafive.movidesk.com/kb/article/35330/emissao-de-nota-de-transferencia?ticketId=&q=transfer

---

## 🔴 Relatório de Produtos e suas respectivas Tributações — 31/01/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/264252
> Publicado em: 31/01/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Com a chegada da Reforma Tributária, torna-se ainda mais importante garantir que as informações fiscais dos produtos estejam corretamente configuradas no sistema.
Pensando nisso, o relatório disponível na tela de Cadastro de Produtos permite a conferência das tributações informadas no momento do cadastro de cada item, auxiliando na validação e prevenção de inconsistências fiscais.
Esse relatório pode ser acessado pelo caminho: Arquivo > Estoque > Produtos.
Clique em "relatório" para visualizar as informações
Na próxima tela exibida, será necessário selecionar, no campo
Classificação
, a opção
“Tributação”
.
Em seguida, na seção de
seleção
, informe os grupos que deseja visualizar no relatório. Caso queira consultar apenas um grupo específico, basta informar o
mesmo código
tanto no campo
Grupo Inicial
quanto no
Grupo Final
Na tela de visualização do relatório será possível imprimir ou até mesmo salvar em PDF:

---

## 🔴 Instalação do FarmaFácil — 25/01/2022

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/262677
> Publicado em: 25/01/2022
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Primeiro passo é compartilhar a pasta FarmaFacil (de uma maquina onde o sistema já está instalado) na rede,
conforme imagens abaixo:
Após isso você acessar o menu de Rede do seu computador, aonde tem acesso aos demais computadores, dar dois cliques no nome do computador e localizar a pasta do sistema que é FarmaFacil, conforme imagem abaixo:
Você dará dois cliques na pasta FarmaFacil, logo após isso, você deverá selecionar 3 pastas para copiar (EXE, PrismaSuporte e PrismaUpdate) conforme imagem a seguir:
Após ter copiado essas 3 pastas, você deve ir até a pasta Meu Computador acessar o disco local C: clicar com o botão direito do mouse, ir na opção Novo > Pasta e renomear para FarmaFacil, após isso você vai acessar a pasta e então colar as 3 pastas que copiou do outro computador.
Se o computador que você acessou não for o servidor, pode ignorar o próximo passo, caso tenha copiado do servidor, será necessário acessar o seguinte arquivo e mudar informações nele: C:\Farmafacil\exe\farmafacil.ini ; Ao abrir o arquivo você precisara mudar o IP informado: 127.0.0.1 no arquivo para o Hostname do  servidor ou o IP caso seja IP fixo, veja exemplo a seguir de antes e depois:
Antes
Depois
Após esse procedimento é necessário rodar o aplicativo de Atualizador do sistema para que o mesmo seja instalado, o arquivo fica em C:\farmafacil\PrismaUpdate\PrismaUpdate.exe
Ao rodar o arquivo, o sistema irá exibir a seguinte mensagem e você deve clicar em SIM:
Logo em seguida será aberta a seguinte tela, e você deve clicar no CONTINUAR:
Após clicar em continuar, o sistema começara a ser instalado nessa mesma tela, após ele chegar a marca de 100% irá habilitar o botão do lado direito "FECHAR" basta clicar em fechar e nesse momento, o sistema irá tentar abrir, porém vai dar uma mensagem de erro, basta clicar em Ok, e então você deverá ir até a pasta EXE novamente e dentro dela na pasta Dlls, para rodar o aplicativo de Registrar as Dlls do sistema, lembrando que deverá rodar em modo Administrador conforme imagem a seguir:
Vai abrir uma tela e você deve clicar em Registrar, após isso irá retornar uma mensagem de que as Dlls foram registradas, basta clicar em OK e então fechar a tela, imagem de exemplo:
Após isso, você pode ir até a área de trabalho do seu computador e tentar abrir o sistema:
Caso o sistema não abra e retorne a seguinte mensagem:
é necessário instalar o vcredist_x86, disponível no seguinte link:
https://aka.ms/vs/17/release/vc_redist.x86.exe
após instalar o mesmo, basta tentar abrir o sistema novamente.
Caso o sistema não abra, e apareça a seguinte mensagem:
Aí será necessário desabilitar o IPV6 do computador.
Para desativar o IPv6 da conexão de rede de seu computador siga está instrução:
1)
Na barra de tarefas do seu Windows localize o ícone de rede.
2)
Clique com botão direito do mouse e vá em
Abrir a Central de Rede e Compartilhamento.
3)
Agora clique em
Alterar as configurações do adaptador.
4)
Clique com o botão direito do mouse no seu ícone de conexão 
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Acerto De Estoque — 22/12/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/255614
> Publicado em: 22/12/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

ACERTO DE ESTOQUE
Menu Estoque > Sub menu Movimento > opção Acerto Estoque
Deve-se informar o sentido do acerto de estoque, de acordo com o sentido irá solicitar para marcar o Tipo Entrada ou Tipo saída, deve-se informar a respectiva quantidade que deseja adicionar ou remover do estoque daquele produto, bem como sua referida unidade de estoque, caso seja um produto que tenha controle de lote, também será necessário informar o lote.
SENTDO:
ENTRADA -
Quando o acerto for voltado para adicionar mais quantidade em estoque do produto;
SAÍDA -
Quando o acerto for voltado para diminuir a quantidade existente no estoque do produto;
TIPO ENTRADA:
SALDO INICIAL:
Essa opção só será utilizada se o acerto de estoque envolver inventário para produtos controlados e ou antimicrobianos;
OUTROS:
Essa opção deverá ser utilizada para todos os produtos, com exceção do que foi mencionado acima;
TIPO SAÍDA:
PERDA:
Essa opção só será utilizada se o acerto de estoque envolver perda para produtos controlados e ou antimicrobianos;
obs: Quando marcar tipo saída por perda, será necessário informar um motivo dessa perda para o SNGPC selecionando o motivo correspondente na grade:
OUTROS:
Essa opção deverá ser utilizada para todos os produtos, com exceção do que foi mencionado acima;
Ao final deve-se clicar no ícone para salvar o item no acerto de estoque:
Necessitando incluir mais itens dentro do mesmo acerto de estoque basta clicar no "+"  caso contrário basta sair da tela dos itens e clicar no ícone para salvar o acerto de estoque em si.
Qualquer dúvida que surgir, entrar em contato com nosso suporte técnico!

---

## 🔴 Mensagens de Ausência e saudação — 11/06/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/209678
> Publicado em: 11/06/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Recentemente atualizamos o PrismaSync e adicionamos uma opção muito pedida pelos cliente, o
Intervalo de Reenvio de Mensagens
. Com ele, você configura o tempo que o robô espera para mandar novamente as mensagem de
Saudação
ou
Ausência
.
Você encontrará a opção no PrismaSync em
Configurações / Parâmetro / Horário de Atendimento
. Aqui terá um novo campo chamado de
Intervalo Reenvio Mensagens (Minutos)
. Esse campo você colocará o intervalo em minutos. Se precisar fazer em horas, basta converter para minutos, por exemplo. se quiser que seja 24 horas, converta em minutos (60 x 24 = 1440), assim como na imagem a seguir.
Caso tenha alguma dúvida sobre a nova opção, basta abrir um chamado na nossa
Central de Tickets
e nosso time de suporte entrará em contato.

---

## 🔴 FAQ - Como funciona PrismaSync — 10/06/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/209602
> Publicado em: 10/06/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Olá, tudo bem? Espero que tenham gostado do nosso Webinar, foi bem legal falarmos um pouco mais sobre a nossa ferramenta PrismaSync. Se você chegou a esse artigo, mas não viu a live, basta
clicar aqui 🎬
.
Conforme prometido durante o Webinar, vamos disponibilizar esse artigo de perguntas e respostas para complementar o conteúdo.
É possível que a mensagem de ausente se repita somente 24 horas depois?
Esta melhoria já estava em desenvolvimento e foi liberada no dia 10/06, onde agora é possível informar o intervalo de tempo para as respostas de ausência.
Como utilizar a ferramenta do PrismaSync E-mail? Recebimento e envio sincronizado com o FarmaFácil, inclusive os orçamentos.
O funcionamento o PrismaSync Mail é semelhante ao do PrimaSync WhatsApp, no painel de Mail, você poderá visualizar os e-mails recebidos do cliente e criar um orçamento a partir deles, o mesmo irá para o FarmaFácil automaticamente, igualzinho o WhatsApp.
Quanto a mensagem programada, no caso de medicamento de uso contínuo, se o cliente encomendar o medicamento antes da mensagem, tem como a gente ser avisado e cancelar?
As mensagens automáticas que o sistema envia no PrismaSync são as agendadas dentro do parâmetro. Com relação a medicamentos de uso contínuo, ele não está associado ao PrismaSync e será apresentada somente na venda dentro do FarmaFácil.
Minha equipe vem tendo algumas dificuldades no uso do PrismaSync com relação ao WhatsApp Web. Uma delas é não poder arquivar as conversas finalizadas. Seria possível implementar essa funcionalidade?
Atualmente todas as mensagens do PrismaSync ficam armazenadas na própria ferramenta, e se há necessidade de deixar as mensagens com um sinalizador que facilite a busca posterior, basta criar uma Etapa com uma etiqueta “Arquivadas” para esse tipo de conversa e marcá-las.
É certo editar o nome do cliente no PrismaSync antes de clicar no carrinho de compra? Percebo na rotina diária, que quando não editamos o nome, lá no FarmaFácil o nome do cliente no orçamento fica diferente.
É sempre bom editar os nomes do cliente já no começo, pois no WhatsApp, não tem uma maneira de conseguirmos o nome dele, sendo assim, caso não coloque um manualmente, o sistema irá procurar um cadastro existente vinculado ao número de celular, caso não encontre, criará um novo cadastro com o número, porém sem nome.
A questão do arquivamento dos orçamentos finalizados é muito importante.
Muito mesmo! Pois facilita a organização e diminui o tempo de procura de um orçamento já realizado.
Outra funcionalidade que sentimos falta é a imagem do contato. A imagem agiliza a identificação do contato e humaniza o atendimento.
Entendemos essa demanda, mas ainda não encontramos uma forma do robô buscar essa imagem no WhatsApp Web, e por enquanto não conseguimos trazer essa foto para o PrismaSync.
Quando o cliente envia a mensagem, mesmo sem iniciarmos a conversa com o mesmo, a mensagem aparece para ele como lida por nós, e isso, às vezes, gera um desconforto parecendo que lemos e
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Drop - Ferramenta para Derrubar Usuários — 10/05/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/197488
> Publicado em: 10/05/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Alguns clientes nos relataram ter problemas relacionados com suas licenças, onde em alguns momentos, determinados usuários abrem várias vezes o FarmaFácil em uma única máquina, fazendo com que suas licenças fiquem "presas", e tem o limite de usuários excedido.
Pensando em uma solução para esse cenário, criamos o
Drop,
uma ferramenta para verificarmos todas as conexões existentes no banco de dados, assim, sendo possível desconectar todos os usuários ou somente o necessário.
Abaixo temos um manual de uso do
Drop:
1 - DOWNLOAD DO DROP
Para download do DROP,
clique aqui 📥
.
2 - ONDE DEVE SER INSTALADO
O Drop deve ser instalado e utilizado, apenas,
no Servidor
, não sendo possível usá-lo em estação.
3 - OPÇÕES DA FERRAMENTA
Ao abrir o
Drop
, essa será a tela inicial.
Nela temos algumas opções de
Verificação
;
Verificar Conexões Abertas no Banco
- Essa opção mostra todas as conexões abertas no seu banco de dados. Não se assuste se aparecerem muitas, o FarmaFácil em média usa 5 conexões, podendo ser mais ou menos (As conexões no banco de dados não influenciam na sua quantidade de acesso e de licenças, não se preocupe).
Verificar Conexões WebKey
- Essa opção mostra todos os acessos da WebKey (chave de acesso virtual) e seus respectivos usuários.
Verificar Conexões HASP
- Essa opção abre o navegador e mostra todos os acessos utilizados no HASP (chave de acesso física).
Outras opções são as de
Derrubar
, onde é possível desconectar os usuários e suas conexões;
Derrubar IP
- Essa opção desconecta todas as conexões do IP inserido.
Derrubar Usuário
- Essa opção desconecta todas as conexões do Usuário inserido.
Derrubar PID
- Essa opção apenas derruba a conexão do PID inserido.
Derrubar Todos
-  Essa opção desconecta todas as conexões do Banco, devendo ser usada com cuidado, pois, caso haja algo não salvo, como ordens, vendas, etc. Tudo será perdido.
4 - USANDO A FERRAMENTA
Agora que todas as opções foram explicadas, darei um exemplo de como derrubar um IP. Na imagem a baixo, temos algumas conexões abertas no banco de dados.
Irei desconectar todas as conexões do IP 192.168.0.72 usando a opção
Derrubar IP.
Podemos ver agora que não há mais conexões desse IP no Banco.
Após o usuário ser desconectado, o FarmaFácil do mesmo irá travar e mostrar a seguinte mensagem;
Caso tenha alguma dúvida sobre a ferramenta, basta abrir um chamado na nossa
Central de Tickets
e nosso time de suporte entrará em contato.

---

## 🔴 Alterar Lote da Ordem de Produção — 15/04/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/192043
> Publicado em: 15/04/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Vá em  Produção
Ordem de manipulação
Pesquise a ordem de produção pela tecla f2 ou pela lupa
Clicar no botão Alterar [Barra de espaço]
Selecionar o produto que deseja alterar o lote e Clicar no botão de alterar
Procurar o lote novo
Clicar no salvar

---

## 🔴 Ferramenta para Acesso Remoto do Suporte — 25/03/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/186819
> Publicado em: 25/03/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Disponibilizamos nesta seção uma  ferramenta de conexão remota, que poderá ser utilizada por um de nossos agentes para lhe auxiliar na solução de uma dúvida, problema ou até mesmo realizar um treinamento.
Após baixar e executar o aplicativo será necessário fazer contato com a nossa equipe de suporte para viabilizar a conexão. Quando for solicitado você deverá enviar os números do campo SUA ID, conforme imagens abaixo:
Baixe aqui o AnyDesk

---

## 🔴 Conciliação Bancária — 25/03/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/186813
> Publicado em: 25/03/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Dentre todas as atribuições inerentes à gestão, certamente o controle financeiro é uma das tarefas mais importantes. Não é à toa que, segundo o Instituto Brasileiro de Geografia e Estatística (IBGE), esse é o motivo que leva quase metade das empresas a fecharem as portas após apenas três anos de funcionamento. Consultores e especialistas geralmente falam sobre a importância dos fluxos de caixa na gestão das finanças, mas poucos se referem à conciliação bancária, ferramenta essencial para essa análise.
O que é conciliação bancária?
Conciliação bancária é conferência das contas bancárias com o controle financeiro interno. A conciliação bancária tem como objetivo verificar se está tudo correto no controle interno ou se há inconsistências de dados. Ela verifica se o saldo bancário do controle interno, os lançamentos e suas datas estão idênticos ao extrato do banco.
Montamos um passo a passo para ajudar a fazer uma conciliação bancária eficiente basta ter em mente o fluxo dos negócios.
Etapa  1: Cadastro de bancos
Lista de bancos Homologados
COD. IBAN
BANCO
SITE
748
Banco Cooperativo Sicredi S.A.
www.sicredi.com.br
085-x
Coperativa Central de Crédito Urbano-CECRED
–
104
Caixa Econômica Federal
www.caixa.gov.br
341
Itaú Unibanco S.A.
www.itau.com.br
Para que se possa utilizar o modulo de conciliação bancária é necessário que se tenha cadastrado no sistema um banco, este banco que posteriormente iremos utilizar para importar o arquivo .ofx. Para isso vá em :
Abrir
ARQUIVO > PARÂMETRO > BANCO
Localizar o banco que ira ser utilizado
Preencher os dados de
AGENCIA
[Caso banco não tenha digito verificador colocar 0 – zero]
Preencher os dados de
CONTA CORRENTE.
Etapa 2: Importando OFX
Nesta etapa o operador financeiro da farmácia deve ir no sistema do banco e efetuar o download do arquivo .ofx do período desejado.
Com o download já realizado na maquina acessamos o seguinte caminho
FINANCEIRO > MOVIMENTO > CONCILIAÇÃO BANCÁRIA
Selecionar o banco a ser utilizado
[Necessita execução da Etapa 1]
Clicar na Seta verde para carregar ou tecla
Enter
Clicar no ícone de importar ou teclas
ALT+I
Localizar o arquivo .ofx salvo anteriormente
Clicar em Abrir
Etapa 2.5: Cadastrando as operações
Sempre que você importar um arquivo OFX o sistema irá identificar se há uma nova transação que ainda não foi importada para o farmafacil.
Neste estágio podemos definir algumas regras
[Tipo]
– Automaticamente o sistema já identifica o tipo da transação {credito ou débito}.
[A conciliar]
– podemos definir se esta transação é obrigatório ou não a conciliação.
[Fornecedor]
+
[Conta]
– Pode-se definir qual o fornecedor e o plano de contas pertencente a esta transação *Utilizado na etapa 4*
Etapa 3 – Conciliando
Para realizar o processo de conciliação basta:
Selecionar a fatura/duplicata do no lado do banco [direito]
Selecionar uma fatura ou mais faturas no lado do farmafacil [esquerdo]
Por fim clicar no botão relacionar fatura
Para confirmar o processo clique no ícone ao lado do botão de s
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Convenio Big / Febrafar — 25/03/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/186786
> Publicado em: 25/03/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

A configuração desse convênios estão documentadas no
PDF
em anexo a este artigo.

---

## 🔴 Impressão de Etiqueta de Estoque e Preço Drogaria — 25/03/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/186784
> Publicado em: 25/03/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

É possível imprimir etiqueta de estoque , etiqueta de preço para drogaria logo a pós a entrada da nota fiscal.
Para isso você precisa ir em
ESTOQUE >  NOTA FISCAL ENTRADA
Em seguida você precia selecionar a nota fiscal que deseja emitir etiqueta e pressionar a tecla
F4
ou clicar no relatório
Em seguida na tela que abrir, você deve digitar a quantidade de etiquetas que deseja imprimir para cada produto, e por último deve clicar na impressora:

---

## 🔴 Como calcular densidade dos lotes — 25/03/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/186781
> Publicado em: 25/03/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Montamos um vídeo demonstrando na pratica como deve ser realizada a densidade dos lotes.
O vídeo abaixo foi gravado dentro de um laboratório real de um cliente nosso.

---

## 🔴 Alteração Tributação Grupos e Produtos — 24/03/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/186465
> Publicado em: 24/03/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Neste artigo você irá encontrar o passo a passo para poder alterar a tributação por grupo. Para isso vá em:
Acessar
ARQUIVO > UTILITÁRIO > MANUTENÇÃO GERAL > ALTERAÇÃO TRIBUTAÇÃO GRUPOS
Definir quais grupos serão alterados
Informar as tributações passadas pelo escritório contábil
Clicar em salvar

---

## 🔴 Cadastro de Produto | Exemplo de telas — 24/03/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/186363
> Publicado em: 24/03/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Artigo sem tradução para esse idioma
Tente outro idioma ou clique no botão abaixo:
Ir para o idioma padrão

---

## 🔴 Formação dos valores de custo/venda — 10/03/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/182412
> Publicado em: 10/03/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Os valores de custo dos itens é formado através da nota fiscal que vem do seu fornecedor conforme valor combinado em cada compra, na qual pode-se conter descontos e custos adicionais por conta das tributações/frete (IPI, DIFAL, Frete e outras despesas)
No sistema Farma fácil conseguimos calcular e controlar esses custos, tanto por entrada via XML quanto entrada realizada manualmente da nota fiscal e também podemos incluir os valores de despesas nos custos dos itens no campo abaixo:
Frete: Valor de frete cobrado para cada item.
Outras despesas: Valor de custo que pode ser incluído pelo fornecedor no ato da geração da nota fiscal.
IPI: É um tributo de competência da União que incide sobre os produtos industrializados no Brasil.
DIFAL: DIFAL é a diferença de alíquota do ICMS que visa tornar essa arrecadação mais justa entre os estados.
OBS.: Esses custos serão calculados com base nos valores informados dentro do item e não o que está no cabeçalho, conforme está na nota fiscal.
Funcionamento do custo na entrada
No sistema, podemos parametrizar para que sempre atualize os custos de forma automática, uma solicitação de confirmação e também para que nunca atualize os custos dos itens
Essa opção fica em "Arquivo -> Parâmetro -> Parâmetro", nas abas "manipulação" e "drogaria" dependendo do tipo de funcionamento da farmácia:
Como estamos com a configuração de "Solicitar confirmação", funcionará da seguinte maneira
Ao salvar a nota fiscal, irá apresentar a seguinte mensagem para cada item que está contido na entrada:
Dependendo da escolha, irá ocorrer a seguinte atualização no cadastro do produto:
Clicando em "Não", sistema irá manter o valor de custo referência e atualizará o valor de custo sempre:
Caso clique em "Sim", irá atualizar o valor de custo referência e ajustará o seu valor de venda:
O valor de venda é calculado da seguinte maneira: Custo referência * (1 + (Markup / 100)). No exemplo acima: 3,975 * (1 + (100/100)) = 7,95
Mas por quê dois campos de custo no cadastro do produto?
Por conta de que caso não queira atualizar o valor de custo para que não atualize o valor de venda, mantenha o real custo que está tendo no ato da venda e nos relatórios e ver o real lucro com base no valor de venda realizado do produto
OBS.: Os valores de venda irá se basear sempre no custo referencia!
Exemplo de funcionamento na venda
No ato da entrada da nota fiscal escolhi não atualizar o valor de custo dos meus item e ficou os seguintes valores
Ao utilizar esses itens dentro de uma fórmula, funcionará da seguinte maneira:
Na tela dos custos os valores serão com base no valor de custo do item, pois segue-se a regra de saber de quanto de custo real estou tendo em uma formula específica por mais que não se tenha atualizado o custo de referência
No campo adicional é apresentado a soma dos valores de venda das embalagens, cápsulas, associação, custo adicional da forma farmacêutica e aplica em conjunto os valores de acréscimo e desconto:
OBS.: A matéria prima é somada direta
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Inventário de estoque por grupo — 02/03/2021

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/180506
> Publicado em: 02/03/2021
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O processo de inventário pode ser realizado com base nos seguintes passos:
1 -
Para iniciar o processo de inventário é importante concluir todas as ordens de manipulação para que não haja nenhuma quantidade comprometida em estoque no momento das conferências e para que as quantidades possam ser ajustadas por completo (principalmente quando o objetivo é zerar o estoque), porém esse processo não é obrigatório pois o sistema possui na tela de inventário uma coluna que exibe a quantidade comprometida atual para o lote. Por outro lado, durante os acertos é necessário parar as movimentações do grupo/produto que será inventariado.
2 -
Abaixo o passo a passo sobre como usar a ferramenta para otimizar o processo de acerto:
Por favor acesse:
Estoque > Movimento > Inventário > Selecione um ou mais grupos e clique confirmar:
Existem filtros específicos, porém esses serão usados somente em casos onde não se deseja inventariar todo o estoque:
Quando o objetivo é inventariar tudo utiliza-se a opção
Filtrar
sem nenhuma outra opção marcada, conforme abaixo:
Após ter feito o processo de filtro do grupo o sistema irá importar todos os produtos e todos os lotes com quantidade existentes para a tela e os exibirá conforme abaixo e na seguinte ordem:
1- Código do grupo;
2 - Código do produto;
3 - Descrição;
4 - Unidade de estoque;
5 - Posição de estoque atual (quantidade total em estoque para o lote informado);
6 - Filial;
7 - Contagem (coluna onde será informada manualmente a quantidade existente no estoque físico caso esta seja diferente da quantidade informada para o lote no sistema);
8 - Comprometida (que é a quantidade comprometida no momento - Ocorre quando existem ordem com status em produção);
9 - Data de validade (do lote);
10 - Fornecedor;
E assim por diante, para ver os demais campos basta arrastar a barra de rolagem inferior para a direita:
(Nesse momento o sistema irá carregar todo o grupo de produto, isso pode travar a tela e demorar alguns minutos, é normal - Dependendo da quantidade de informações/produtos contidos no grupo sugerimos fazer um grupo por vez e cada grupo em uma máquina diferente para evitar conflitos na hora de salvar).
Para demostrar vamos pegar o exemplo do produto de código 13-800.
No momento há uma quantidade de 1,96g em estoque, a quantidade comprometida é igual a 0,00 (zero). Nesse caso, digamos que a quantidade no estoque físico seja 1,00 (um), no momento da conferência e do inventário deverá ser informado na coluna contagem a quantidade do estoque físico. Conforme abaixo:
Após ter feito a conferência de todos os produtos listados na tela e informado na coluna contagem todas as quantidades é o momento de salvar o inventário. Para isso clique em salvar.
Ao informar a quantidade existente no estoque físico e salvar o sistema irá inserir no lote essa quantidade. Exemplo:
Quantidade atual do lote = 1,96
Quantidade do estoque físico = 1,00
Quantidade informada na coluna contagem = 1,00
Resultado: 1g (um)
Após realizar o procedimento par
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Como habilitar operador por caixa — 14/09/2020

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/142808
> Publicado em: 14/09/2020
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Como habilitar operador por caixa.
Abaixo vou deixar o passo a passo para habilitar o mesmo:
Muito importante:  Habilitar esta função, antes da farmácia abrir ou depois da farmácia fechar
Dar um CTRL + F e digitar operador por caixa
Criar os operadores que ficarão habilitados a trabalhar no caixa.
Verificar se o turno 1 está de acordo com o horário de funcionamento da loja [CRTL + F | Turno | Enter]
Habilitar nos parametros o operador por caixa [CRTL + F | Parametro | Enter | Geral >  Geral]
Após isso os
próximos
recebimentos que forem realizados no caixa irão pedir quem é o operador e a senha desse operador [mesma senha de acesso do
usurário
].

---

## 🔴 Compras — 18/05/2020

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/116861
> Publicado em: 18/05/2020
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Sempre pensando em facilitar o dia - a - dia dos usuários do FarmaFácil, o módulo Compras foi criado como uma opção para facilitar a gestão de suas compras.
Com esse novo módulo a gestão de compras ficou muito mais inteligente, fazendo com que você compre apenas os produtos que mais giram,
otimizando custos e tempo, deixando o seu estoque sempre atualizado.
O módulo é acessado pelo menu
Estoque -> Movimento -> Compras
Lista de Compras
Ao acessar o módulo é apresentada a lista de compras, nela ficará registrado todas as compras que você realizou nos últimos meses,
lembrando que é possível fazer uma busca inserindo o período das compras que você deseja encontrar, na parte superior da tela.
Nova Lista de Compras
Primeiramente é preciso escolher o tipo de lista que se deseja obter e preencher os campos relacionados ao tipo conforme abaixo:
Tipo Venda:
Assinalando esta opção o sistema vai sugerir uma listagem de produtos a serem comprados baseado
somente nas informações de Vendas do Período informado, ou seja, se vendi 03 caixas de Neovlar no
período de 1 dia e tenho 2 em estoque o sistema vai sugerir a compra de 1 caixa.
Tipo Demanda:
Neste caso o sistema vai calcular a MÉDIA DE CONSUMO no período informado, considerando o TEMPO DE REPOSIÇÃO, E ESTOQUE MÍNIMO.
O sistema vai fazer o seguinte cálculo:
Cmm = Consumo Médio Mensal: é a soma do consumo de medicamentos utilizados em determinado período de
tempo dividida pelo número de meses da sua utilização. Tr = Tempo de Reposição: é o tempo decorrido entre a solicitação da compra
e a entrega do produto, considerando a disponibilidade para a dispensação do medicamento.
QR = Quantidade reposição.
EMI = Estoque mínimo.
EA = Estoque atual.
QE = (CMM x TR + EMI) – E
Tipo Estoque Mínimo:
Assinalando esta opção sistema vai gerar o relatório considerando todos os produtos
que estão abaixo do estoque mínimo e vai sugerir uma quantidade para ser comprada.
Tipo Consumo:
Assinalando esta opção o sistema vai fazer um calculo rápido da média de consumo, baseado nas
vendas de um período passado, e projetando a quantidade que deve ser comprada para suprir
suas compras para um determinado tempo.
Tipo Faltas/Encomendas:
Assinalando esta opção o sistema vai fazer uma lista de compras baseado somente nas
Faltas/Encomendas, que foram lançadas pelos usuários na tela de vendas.
Feita a escolha do tipo é preciso preencher os campos de filtro de acordo com sua necessidade:
Campos de filtro para lista de compras:
1- Venda de .... Até.....: Neste local você vai inserir o período que você deseja que o sistema calcule, por
exemplo, quero que faça as contas baseado nas vendas do período de 01/07/2020 até
01/08/2020.
2- Curva ABC: Neste opção você pode filtrar pelas curvas que deseja obter a lista, se deseja obter somente
produtos da lista A, da lista B, da lista C ou de todos juntos você escolhe a opção Geral. Lembrando que a
curva ABC é calculada através da tela de produto
3- Considera Encomendas/Faltas: Assinalando esta opção o sis
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Exportação de arquivo para Integração Infomerc - HelloPharma — 21/02/2020

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/101517
> Publicado em: 21/02/2020
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para realizar a exportação dos dados acesse:
Arquivo > Utilitários > Exportação de arquivo > Infomerc
, informe o período e o caminho onde deseja salvar e após clique em exportar:
C
lique em sim para confirmar:
Serão exportados dois arquivos diferentes, o primeiro é o
Detalhe
e o segundo é o M
aster
, após fazer a exportação o arquivo será salvo no local especificado no momento da exportação e posteriormente importado automaticamente para o FTP da Informec (HelloPharma).
Após a conclusão do processo, os arquivos ficarão salvos na pasta especificada e importados automaticamente conforme mencionado acima e podem ser visualizados para conferência se necessário.

---

## 🔴 Orientação para alterar tributação. — 02/12/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/82519
> Publicado em: 02/12/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para efetuar a alteração de tributação em grupos deve ser seguir os passos abaixo:
1-Ir em Arquivo;
2-Utilitário;
3- Manutenção Geral;
4-Selecionar Alterar Tributação de Grupo;
5-Selecionar Grupos;
6-Definir tributações que serão Alteradas e executar o processo no botão Salvar.

---

## 🔴 Sache calculo automático — 29/11/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/81846
> Publicado em: 29/11/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Na versão 18.01.01.33, mudamos a forma de realizar o cálculo do tipo volume X qtd (mg) no sistema, a partir dessa versão é sugerida uma embalagem automaticamente sem a necessidade de informar o volume na tela da formula. O sistema irá selecionar a embalagem mais adequada para a formula conforme a soma da quantidade calculada de todos os ativos. Detalhes abaixo:
Primeiramente, no cadastro das embalagens, informe o volume para que no momento do cálculo o sistema consiga encontrar a melhor opção para calcular a formulação.
Vamos em "Arquivo -> Estoque -> Produto"
Depois, edite a embalagem que irá ser utilizada na formulação, informe o volume e a forma farmacêutica respectivas.
Após isto, no cadastro da forma farmacêutica, acesse "Arquivo -> Produção -> Forma Farmacêutica"
Pode-se editar alguma já existente ou então criar uma nova e selecionar o tipo de cálculo "Volume x Qtd (mg)"
Após ajustar os cadastros, realizamos a formulação, vamos na tela de manipulação (Venda -> Movimento Venda), selecionamos a forma farmacêutica e preenchemos somente a quantidade desejada, no caso abaixo 30 Saches.
Depois, informe os ativos e QSP (base).
Após isto, basta conferir se os valores estão corretos e gerar a ordem de manipulação!
OBS.: Para calcular outras formas farmacêuticas, como por exemplo sublingual, é necessário que a embalagem que é utilizada n produção esteja cadastrada no sistema com o volume, ou seguir o processo a seguir.
Pode-se utilizar um ativo com o cálculo "Percentual" ou trabalhar de maneira anterior é necessário utilizar o outro tipo de cálculo na forma farmacêutica.
Acesse o cadastro da forma farmacêutica e selecione "Volume x Qtd (%)", seja em um cadastro existente ou em um novo.
E realizamos a inserção da fórmula no mesmo processo que foi feito anteriormente, nesse momento é necessário informar o volume da formulação manualmente.
Percentual:

---

## 🔴 PCP (Planejamento e Controle de Produção) — 14/11/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/78252
> Publicado em: 14/11/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O PCP Planejamento e Controle de Produção foi criado para um melhor gerenciamento de todo o processo existente nas farmácias de Manipulação. Este gerenciamento de todo o processo existente nas farmácias de Manipulação. Este módulo torna as informações ainda mais precisas, pois informa em qual estagio da produção se encontra a fórmula dentro da farmácia. A alimentação das informações no PCP, auxilia no gerenciamento da produtividade da farmácia do departamento, e até mesmo dos funcionários, podendo assim criar estratégias, verificar os gargalo, ganhando qualidade e produtividade.
Exemplo: A partir do momento que a balconista inserir a venda, inicia o PCP, sendo que o mesmo é dividido por Etapas, um exemplo simples, a venda é a Etapa de Inclusão, depois vem o processo de Produção, Rotulagem , Análise e Entrega, e todas estas Etapas são configuradas por cada Farmácia de acordo com o seu próprio plano de produção.
1 ° Passo
Primeiramente, devemos realizar os cadastros para o funcionamento do PCP.
Vamos em "Arquivo -> PCP -> Etapa"
e inserimos um novo no botão de "+"
Nos cadastros devemos informar todas as etapas que é realizado na farmácia, por exemplo, Rotulagem, Pesagem, Conferência.
Ao inserir uma etapa você deve preencher os seguintes campos:
Descrição: O nome da etapa.
Sequência: É o número da sequência ao qual se enquadra esta etapa dentro de todo o processo. Vale salientar que é preciso atenção ao inserir o número da sequência, sugerimos que seja colocado inicialmente,10,20,30 e assim por diante, pois caso seu fluxo aumente e seja necessário implantar mais uma etapa, entre as que já existem fica mais fácil de inserir um número 11 entre a 10 e a 20,  por exemplo.
Processo: Ao selecionar uma das opções, você vai estar informando ao sistema que a etapa que esta sendo cadastrada só pode ser concluída se tiver s ido feito o processo no FarmaFácil selecionado, hoje o sistema faz a verificação dos seguintes processos:
Nenhum: Selecionando esta opção não é feita nenhum tipo de verificação.
Imagem vinculada: Verifica se a imagem da receita esta salva no sistema, se não estiver não irá permitir passar para a próxima etapa.
Produção Concluída: Verifica se foi concluída a Ordem de Manipulação, para poder passar para a próxima etapa.
Obrigatória: Se você escolher SIM o sistema vai obrigar e também sugerir que seja realizado o apontamento nesta etapa (de acordo com a sequência cadastrada), se escolher NÃO, o sistema não vai obrigar e nem sugerir para fazer não vai obrigar e nem sugerir para fazer apontamentos nesta Etapa.
Tipo: Aqui você classifica o tipo desta etapa, você determina que ela faz parte do Inicio do processo, intermediária ou final, para posteriores controles e relatórios.
Tempo Máximo: Neste campo você cadastra o tempo máximo que deseja que a formula passe nesta etapa.
Assim como exemplo abaixo após cadastrar todas as etapas:
2° Passo:
Quando os usuários forem inserindo os apontamentos das etapas de produção das Fórmulas, em algum momento, po
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Inventário — 27/08/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/64762
> Publicado em: 27/08/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O módulo inventário serve para ajustar as quantidades dos produtos da farmácia de modo "geral" sem precisar ficar incluindo os produtos manualmente via acerto de estoque trazendo agilidade no processo. Como por exemplo, na finalização de inventário do SNGPC.
1° Passo
Nós vamos em "Estoque -> Movimento -> Inventário"
2° Passo
Escolhemos os grupos que desejamos ajustar
Ou então, selecionamos apenas o produto
3° Passo
Marcamos o filtro que desejamos, e no campo "Contagem" colocamos a quantidade que desejamos que fique, ou seja, o estoque atual
Obs.: As marcações "Mostrar" irá trazer os lotes conforme o que está marcado e irá trazer os outros lotes que não está relacionado ao filtro também
As marcações "Somente" irá trazer apenas o que está marcado.
Como exemplo abaixo, onde o produto tem uma quantidade de 973 g, e na contagem coloquei 0 para que fique zerado.
Após salvar, caso não tenha nenhuma inconsistência, irá trazer a mensagem "inventário realizado com sucesso", onde o sistema irá criar automaticamente um acerto de estoque para deixar a quantidade do produto conforme informado na coluna "Contagem".
Obs.: Para realizar o inventário, os lotes não podem estar comprometidos pois não irá deixar dar baixa dependendo da quantidade que estiver na contagem.
Tela do acerto
Tela do lote do produto após o inventário

---

## 🔴 Bloco X - Funcionamento — 22/08/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/64123
> Publicado em: 22/08/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

1° Passo, vamos em “Arquivo -> Utilitário -> Exportação Arquivo”
2° Passo, marcamos a opção “Situação Bloco X”
3° Passo, ao abrir a janela do bloco X teremos duas “guias” de movimentações, a primeira com o nome “Enviar estoque” e o segundo “Enviar redução Z”
Obs.: O envio de estoque ocorre mensalmente, já o envio de redução Z deve-se ocorrer diariamente, podendo acumular até 10 arquivos (apenas nas reduções Z). Ao chegar nessa quantidade a impressora ficará bloqueada para movimentações, não sendo possível realizar nenhum recebimento.
3.1 Para enviar a movimentação do lote, clicamos em “Atualizar” no campo “Filtros”
O sistema irá trazer todos os arquivos de movimentação com referência a última data de cada mês. Esse arquivo gera automaticamente ao abrir o sistema na qual a impressora fiscal está conectada.
Após selecionar o arquivo, temos a opção de visualizar o arquivo .xml que está sendo enviado clicando na “telinha” antes da transmissão
Para realizar a transmissão, clicamos no “satélite” (caixa marcada abaixo)
Obs.: O sistema realiza o envio automaticamente após a Redução z ou no momento que gera a movimentação do estoque. É necessário ter o certificado instalado no computador que irá transmitir (conforme o pré-requisito).
Após transmitir, o status da movimentação irá sair de “gerar” para “aguardando”
Para verificar se foi aprovado ou não, basta clicar na caixinha do “globo” na qual irá consultar, caso tenha alguma inconsistência, irá mudar o status para “erro” e irá trazer na tela o motivo pela qual foi rejeitado. Caso não ocorra nenhuma inconsistência, irá retornar “sucesso”.
Para cancelar o envio enviado, basta selecionar a movimentação e clicar na caixinha “Cancelar”
A caixinha onde consta uma “Folha rascunho” serve para mostrar os arquivos que foram enviados na movimentação.
3.2 Para enviar a movimentação da redução Z nós vamos na segunda guia e terá o campo “Equipamento”, ali selecionamos a impressora conforme o número de fabricação e clicamos em “Filtrar”. Após isto, irá trazer todas as movimentações de todos os dias, estes arquivos são gerados automaticamente na abertura do sistema onde a impressora fiscal está conectada.
Após listar, basta seguir os mesmos processos que realizamos anteriormente no "Envio estoque".
Obs.: Caso esteja em algum outro computador, por exemplo, e deseja realizar o envio da movimentação e ainda não tem o arquivo gerado (isso para ambas as movimentações), basta clicar no campo “+” na parte inferior que o sistema irá gerar o arquivo automaticamente referente ao mês que está faltando, caso não contenha nenhuma inconsistência.

---

## 🔴 Portaria MJSP 240/19 - Policia Federal - A nível nacional — 10/08/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/61358
> Publicado em: 10/08/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

No dia 14/03/2019, foi publicada a Port. MJSP 240/19 e anexos (DOU nº 50, Seção 1, p. 41-58, de 14 de março de 2019), que estabelece procedimentos para o controle e fiscalização de produtos químicos pela Polícia Federal. As novas regras entram em vigor no dia 01/09/19, data prevista para entrar em produção o Siproquim 2. Ou seja, até o dia 31/08/19, permanecem válidas as regras previstas na Port. MJ 1.274/03.
Em anexo:
Portaria MJSP nº 240/19 sobre controle e fiscalização de produtos químicos pela Polícia Federal.
Em anexo:
Ofício Circular 02-19 CGCSP (orientações referentes à implantação do Siproquim 2).
Em anexo:
Portaria nº 10 - DOU de 16/04/2019 (Portaria de Implantação do Siproquim 2).
Em anexo:
Orientações Gerais e de Transição do Siproquim 1 para o Siproquim 2.
Notas Técnicas:
http://www.pf.gov.br/servicos-pf/produtos-quimicos/arquivos-siproquim2/notas-tecnicas
ATENÇÃO:
Todo o gerenciamento será realizado diretamente no sistema da Polícia Federal (Siproquim 2), sendo assim o Sistema FarmaFacil apenas terá funcionalidades que permitirão a conferência e exportação das informações, informadas abaixo. Todas as informações que giram em torno do cadastro da farmácia e regularização, bem como acesso ao portal da PF e uso do mesmo estão disponíveis detalhadamente no site:
http://www.pf.gov.br/servicos-pf/produtos-quimicos/arquivos-siproquim2
.
O sistema ira dispor de um campo no cadastro de produto para identificar quais fazem parte da portaria;
Estará disponível um relatório de movimentação para que possam ser realizadas as conferências por parte do cliente antes da exportação e envio das informações;
Por fim, a extração das informações será realizada através de uma ferramenta de exportação de arquivo em formato .txt que atende rigorosamente o padrão previsto na Portaria e após a exportação do arquivo o cliente fará a importação no portal da PF.
PS.: Assim que for liberada a versão contendo essas funcionalidades, as telas serão inseridas no manual.

---

## 🔴 Cálculo Forma Farmacêutica Cápsula — 30/07/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/60118
> Publicado em: 30/07/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Cálculo da quantidade
O cálculo dessa forma farmacêutica funciona da seguinte maneira:
Quantidade prescrita / 1000 (para converter em g) = resultado 1
Resultado 1 * fator correção = resultado 2
Resultado 2 * quantidade de capsulas = quantidade a ser utilizada.
Como de exemplo, realizei o seguinte processo com base nos cálculos acima:
100 / 1000 = 0,1
0,1 * 1,02 = 0,102
0,102 * 30 = 3,060.
Conforme os print's abaixo realizado no sistema:
Tela de Lote do produto
Tela de manipulação feita no sistema
Tela da ordem de manipulação
OBSERVAÇÕES IMPORTANTES
1° Caso
Caso o produto tenha sinônimo e no momento da manipulação o produto ser inserido através dele, irá ser utilizado o fator de equivalência do sinônimo + fator de correção do produto
O calculo ficará assim
Quantidade prescrita / 1000 (para converter em g) = resultado 1
(Resultado 1 * Fator equivalência) * fator correção = resultado 2
Resultado 2 * quantidade de capsulas = quantidade a ser utilizada.
Exemplo
100 / 1000 = 0,1
(0,1 * 1,02) *  1,5 = 0,153
0,153 * 30 = 4,59.
Tela do produto
Tela de manipulação e ordem de produção usando o sinônimo
2° Caso
Caso o produto não tenha quantidade de lote suficiente ou está vencido, o sistema irá utilizar os dados (densidade, fator de correção) que está no cadastro do produto.
Tela do produto
Tela do lote sem quantidade
Tela de manipulação
Cálculo do volume da formulação
O sistema utiliza a seguinte formula para realizar o cálculo do volume da formulação:
Quantidade prescrita / 1000 = resultado 1
(Resultado 1 * Fator correção) / densidade = Volume
Obs.: Caso o lote não tenha fator de correção, o valor utilizado é 1.
Cada volume é calculado individualmente e no final é somado
Segue o exemplo abaixo:
Produto 1:
150 / 1000 = 0,15
(0,15 * 1,092) / 0,6 = 0,273
Produto 2:
100 / 1000 = 0,1
(0,1 * 1) / 0,7 = 0,142
Somando os dois volumes finais encontra-se o total de 0,4159 para cada cápsula
Conforme as imagens abaixo:
Produto 1
Produto 2
Tela de Manipulação
Seleção de cápsulas
Após obtermos o volume total da formulação o sistema se baseia na tela "Tipo cápsula" para realizar a seleção do tamanho
Exemplo:
No caso anterior, o volume total da formulação deu um valor de 0,4159
Ao olharmos a tela "Tipo cápsula" veremos o volume interno de cada um.
Como a nossa formulação deu um volume de 0,4159, o sistema irá verificar o volume interno da cápsula que mais se encaixa, por exemplo, o volume do tipo cápsula 4,3 e 2 são menores do que o da nossa formulação, sendo assim não irá puxar essas, logo o tipo 1 já é maior e irá puxar esse
Conforme a imagem abaixo.
Tela de manipulação
Tela de seleção das cápsulas
Seleção de embalagem
Para que o sistema puxe automaticamente a embalagem, é necessário que no cadastro de produto esteja preenchido a capacidade máxima para cada tamanho de cápsula
Sendo assim, o sistema calcula conforme a quantidade que foi utilizada na formulação e seleciona a melhor opção.
Tela do cadastro do produto
Tela de manipulação
Tela de seleção da embalagem
Calcul
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Chave de Acesso — 17/07/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/57473
> Publicado em: 17/07/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

RESTRIÇÕES ATUAIS [17/07/19]
Não liberado para clientes que usam What's, alcance ou tenham integração com filial
Passo 1 - Solicitar Junto ao Financeiro que faça o cadastro do cliente em
http://portal.prismafive.com.br
Passo 2 - Cliente deve estar na versão
18.01.01.23 ou Superior
Passo 3 - Rodar no banco o seguinte script
Update data.parametro set tipochaveseguranca=73
Passo 4 - Instalar Serviço
Farmafacil Chave Service
Passo 5 -
Liberar no firewall a porta 2502
em regras de entrada e saída.
Passo 6 -  Registrar as DLL da pasta
C:\FarmaFacil\EXE\DLLs
Passo 7 - Pegar o código para lançar no portal
.
Passo 8 - Lançar no portal a o codigo.
Executado atualmente apenas pelo Lopes
Passo 4 - Serviço de Chave
Deve-se instalar o serviço de chave apenas no servidor que esteja acessível por todos os terminais que acessem  o sistema FarmaFacil.
Para a instalação do serviço, deve-se acessar a pasta ChaveFarmaFacil, onde estão localizados os arquivos do serviço, e acessar o aplicativo InstaladorServico.exe (Imagem 15).
Imagem 15 - Pasta do Serviço
Selecionar a opção Instalar Serviço (Imagem 16) e aguardar a mensagem de confirmação da instalação (Imagem 17).
Imagem 16 - Instalador Serviço
Imagem 17 - Mensagem Instalador
Para configurar a porta que será utilizada para o serviço de chaves, deve-se abrir o arquivo Service.ini (Imagem 18) e informar a porta necessária (Imagem 19).
Imagem 18 - Configurar Serviço
Imagem 19 - Arquivo Service.ini (
Porta 2502
)
Após instalar e configurar o serviço, deve-se inicializa-lo pelo aplicativo de Serviços do Windows.
Pressione o atalho Win + R para abrir o Executar, digite Services.msc e clique em OK (Imagem 20).
Imagem 20 - Executar
Selecione o serviço FarmaFacil Chave Service na lista de serviços, clique com botão direito e selecione a opção Propriedades (Imagem 21).
Imagem 21 - Serviços do Windows
Na tela de Propriedades do serviço, selecione a aba Recuperação (Imagem 22).
Imagem 22 - Propriedades do Serviço
No campo Primeira Falha, Segunda Falha e Falhas Posteriores, selecione a opção
Reiniciar Serviço e confirme as alterações no botão OK (Imagem 23).
Imagem 23 - Recuperação do Serviço
Selecione novamente o serviço FarmaFacil Chave Service na lista de serviços e clique na opção Iniciar (Imagem 24).
Imagem 24 - Serviços do Windows
Aguarde a conclusão da inicialização e estará concluída a instalação do serviço de chaves (Imagem 25).
Imagem 25 - Inicialização do Serviço de ChavesRegistrar DLL Chave
Passo 6 - Registrar DLL Chave
As DLLs do novo sistema de chave, devem ser registradas no windows para uso do sistema FarmaFacil.
Deve-se abrir a pasta onde estão as novas DLLs criadas e selecionar o aplicativo RegistrarDLLs.exe (Imagem 26).
Imagem 26 - Pasta DLL Chave
Dentro do aplicativo de registro das DLLs, deve-se verificar se o local dos arquivos estão corretos (Imagem 27 - Campo A).
Caso o local não esteja correto, deve-se selecionar o caminho correto (Imagem 27 - Campo B) e confirmar o registro (Imagem 24 - Campo C).
Imagem
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Como Gerar arquivos XML para diferentes Documentos Fiscais — 03/07/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/55989
> Publicado em: 03/07/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Como Gerar Arquivos XML para Diferentes Arquivos Fiscais: Assista ao Vídeo Detalhado
Neste guia, você aprenderá como exportar arquivos XML de diferentes tipos de documentos fiscais eletrônicos, como NF-e (Nota Fiscal Eletrônica), NFC-e (Nota Fiscal de Consumidor Eletrônica), NFS-e (Nota Fiscal de Serviço Eletrônica) e SAT (Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos). Certifique-se de realizar esse processo em uma máquina onde o certificado digital da farmácia esteja instalado.
Assista ao vídeo detalhado para uma demonstração visual do processo descrito neste artigo e deixe um comentário no vídeo se ele foi útil para você. Seu feedback é muito importante para nós e nos ajudará a criar novos vídeos.
Segue detalhamento:
Iniciando a Exportação
1. Acesso ao Menu Principal:
Abra o menu principal do sistema e siga o caminho:
ARQUIVO > UTILITÁRIO > EXPORTAÇÃO ARQUIVO
2. Selecionar Documentos Fiscais:
Clique em DOCUMENTOS FISCAIS para iniciar o processo de exportação.
3. Escolha o Tipo de Arquivo:
Na nova tela, selecione o tipo de arquivo que deseja exportar:
- NF-e (Nota Fiscal Eletrônica)
- NFC-e (Nota Fiscal de Consumidor Eletrônica)
- NFS-e (Nota Fiscal de Serviço Eletrônica)
- SAT (Sistema Autenticador e Transmissor de Cupons Fiscais Eletrônicos)
4. Aplicar Filtros de Exportação:
Escolha um dos métodos de filtro de exportação:
- Por Número de Notas:
Informe o número inicial e final das notas desejadas.
- Por Período (Data):
Defina a data inicial e final do período desejado.
5. Definir Diretório de Exportação:
Crie uma nova pasta no seu computador para salvar os arquivos exportados.
- Selecione a pasta recém-criada ou informe o caminho da pasta onde deseja salvar os arquivos.
6. Concluir Exportação:
Após configurar os filtros e o diretório de exportação, clique em Salvar para iniciar a exportação dos arquivos XML.
Confirmação de Exportação
Ao concluir o processo de exportação, o sistema exibirá uma mensagem indicando:
EXPORTAÇÃO REALIZADA COM SUCESSO
Agora você pode acessar a pasta onde salvou os arquivos para visualizá-los ou utilizá-los conforme necessário.
Dicas Importantes
- Certifique-se de possuir o certificado digital da farmácia instalado na máquina utilizada para realizar a exportação.
- Mantenha seus filtros de exportação atualizados para obter os resultados desejados.
- Utilize esta funcionalidade para manter seus registros fiscais organizados e em conformidade com as regulamentações vigentes.
Se tiver dúvidas adicionais ou necessitar de suporte técnico, entre em contato com nossa equipe de atendimento.

---

## 🔴 Editar relatórios exportados para o Excel em modo protegido — 26/06/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/55377
> Publicado em: 26/06/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Nesse tipo de situação, o arquivo já é gerado e salvo em modo protegido com base nas configurações do próprio Excel. Para desfazer essa configuração siga os passos abaixo:
Clique com botão direito no arquivo e clique em abrir ou simplesmente dois cliques para abrir o mesmo na tela;
Após clique em :
"Não é permitido editar este tipo de arquivo devido as suas configurações de política..."
, conforme abaixo:
Clique em:
"Configurações de bloqueio de arquivo"
, conforme abaixo:
Selecione a opção: "
Abrir tipos de arquivos selecionados no Modo de exibição Protegido e Permitir Edição"
, clique em
OK
e feche o arquivo e abra novamente conforme abaixo:

---

## 🔴 Bloco X - A nível estadual (Somente para SC) — 19/06/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/54870
> Publicado em: 19/06/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

A partir de
01/09/2019
a Secretaria da Fazendo do Estado (Sefaz) passará a exigir informações ainda mais detalhadas das vendas realizadas, isso para empresas que emitem
Cupom Fiscal na Impressora Fiscal
. Ressaltamos que, estas informações serão enviadas automaticamente pelo próprio sistema utilizado por sua empresa (no caso o
FarmaFacil
), onde estão cadastradas as mercadorias e também onde são emitidos os cupons fiscais. Esta nova obrigação fiscal é chamada de BLOCO X.
Mas o que é exatamente este tal de BLOCO X ?
O BLOCO X é uma obrigação fiscal ligada a emissão dos cupons fiscais e se destina à transmissão de informações para a fiscalização fazendária de SC, através de arquivos eletrônicos assinados digitalmente, e enviados pela internet. Ressaltamos que, o referido envio ocorrerá automaticamente, tanto diariamente, quanto mensalmente,
importante
: O arquivo será gerado e enviado AUTOMATICAMENTE pelo sistema emissor dos cupons fiscais da empresa (no caso dos nossos clientes, o FarmaFacil).
DOCUMENTOS E INFORMAÇÕES NECESSÁRIAS:
Para a entrega com sucesso desta obrigatoriedade, listamos alguns pontos que o seu estabelecimento precisa se atentar e adequar caso ainda não possua, são eles:
Possuir um certificado digital válido;
Possui acesso à internet no estabelecimento;
Manter o cadastro de produtos atualizado;
Manter o controle de estoque atualizado no seu sistema emissor de cupons fiscais;
Certificar-se de que as informações que irão gerar as reduções Z e estoque estejam corretas e sejam reais;
Caso sua empresa possua mais de um ponto de venda de uma impressora fiscal instalada, será necessário que cada um delas tenha o certificado digital instalado, para que seja possível a transmissão dos arquivos referente a cada um deles.
Caso ainda não possuam certificado digital,
sugerimos
a aquisição e uso do modelo A1, isso porque o mesmo pode ser instalado e utilizado simultaneamente em todos os computadores da farmácia.
Quando e como os arquivos são enviados para a SEFAZ?
Os arquivos são enviados automaticamente para a fiscalização da fazendária do estado, sempre após a geração da redução Z.
Se não houver conexão com a internet para a transmissão dos arquivos ou houver qualquer rejeição, estes ficarão armazenados para envio no próximo acesso do sistema.
Se a sua empresa possui firewall/proxy é necessário liberar o tráfego para o endereço: ?? . Para isso consulte seu setor de suporte de informática.
O que ocorrerá se o arquivo não for transmitido para a SEFAZ?
IMPORTANTE:
Caso haja 10 transmissões pendentes ou mais, o Programa emissor de cupons fiscais será bloqueado até a transmissão de todos os arquivos.
Ou seja, haverá apenas 20 dias para os ajustes necessários até que o PAF-ECF seja bloqueado.
É importante ficar atento ao prazo e as exigências necessárias para não correr o risco de ficar sem conseguir emitir cupons fiscais e consequentemente em desacordo com a exigência da SEFAZ (Secretaria de Estado da Fazenda).
Por isso, recomendamos que:
Verifiq
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Habilitar Caixa Pós Venda — 06/06/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/53591
> Publicado em: 06/06/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para habilitar o Caixa pós a venda basta seguir os seguintes passos:
Acessar
ARQUIVO > PARAMETRO > PARAMETRO > GERAL > GERAL
e marcar a opção
Caixa após Venda
Feito o passo acima precisamos ativar a função para os terminais que deverão ter esta função, para realizar a ativação precisamos ir em
ARQUIVO > PARAMETRO > CONFIGURAÇÕES PRISMAFIVE
Clicar no botão de mais
Informar os campos
Chave 'CAIXAVENDA'
Valor 'SIM'
Após isso a função já se encontra habilitada para todos o terminal em que foi criado o registro.

---

## 🔴 Sugestões de aparelhos SAT — 05/06/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/53506
> Publicado em: 05/06/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Abaixo os principais modelos de aparelhos SAT, a venda desses equipamentos ocorre somente no estado de São Paulo. As marcas mais comuns, utilizadas pelos nossos clientes são as que estão informadas abaixo, porém no link (
https://portal.fazenda.sp.gov.br/servicos/sat/Paginas/Modelos-SAT.aspx
), disponível no site da Secretaria da Fazenda do Estado de São Paulo estão informadas outras marcas e modelos.
É sempre muito importante consultar e entender a necessidade do cliente para sugerir o equipamento correto.
Marca DIMEP modelo D-SAT;
Marca BEMATECH - Modelos RB-1000 e RB-2000;

---

## 🔴 Sugestões de impressoras NÃO FISCAIS — 05/06/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/53504
> Publicado em: 05/06/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Abaixo os principais modelos de Impressoras NÃO FISCAIS para impressão do cupom SAT, NFCe, comprovante de venda, entre outros documentos.
ATENÇÃO: É sempre muito importante consultar e entender a necessidade do cliente para sugerir o equiparamento correto.
Ficar atento também qual é o estado do cliente e se o mesmo possui impressora fiscal devido ao PAFECF.
Impressora Não Fiscal Bematech MP-4200 TH;
Impressora Não Fiscal Epson TM-T20;
Impressora Não Fiscal Daruma DR-800H;

---

## 🔴 Faltas e Encomendas — 28/05/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/52604
> Publicado em: 28/05/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

É possível registrar no sistema as faltas e encomendas diariamente, de forma simples e rápida. Na tela Principal de Venda ao clicar simultaneamente nas duas teclas
Ctrl + F11
ou clique no ícone
, o sistema vai abrir a tela a seguir
.
Nesta tela são informadas as faltas de produtos que ocorrem nas prateleiras da farmácia ou ainda as encomendas feitas pelos clientes em um determinado período, isso para que posteriormente, quando forem realizadas as compras essas anotações possam ser consideradas. Para realizar uma Falta ou Encomenda é preciso inserir as informações solicitadas nos campos abaixo:
[Vendedor]
– Vendedor responsável pelo cadastro da solicitação;
[Filial]
– Informar a qual filial se destina (Se houver);
[Tipo]
– Assinalar se é uma Falta ou uma Encomenda;
[Previsão de Entrega]
– Preenchido somente em casos onde o tipo é encomenda e representa a data de previsão de entrega para o cliente;
[Cliente]
– Informar o cliente. Obs.: Informar o cadastro do cliente é obrigatório somente para encomendas;
[Telefone]
– Telefone do cliente para posterior contato;
[Observação]
– Caso exista a necessidade de registrar alguma informação relevante, essa deve ser inserida neste campo;
[Produto]
– Informar o produto que está faltando ou que foi encomendado pelo cliente.
Consultar as faltas/encomendas
Para consultar as Faltas e Encomendas que foram registrados no sistema, você deve acessar o
MÓDULO ESTOQUE > MOVIMENTO > FALTAS/ENCOMENDAS.
Nesse tela serão listadas todas as faltas e encomendas, bem como o status e o histórico de cada uma delas.
Sempre que uma falta e/ou uma encomenda for concluída é necessário informar no sistema a conclusão desse processo. Para isso basta clicar em
ou pressionar a tecla
espaço
no teclado. Feito isso o sistema solicitará a confirmação de conclusão, conforme abaixo, e o status do registro será alterado para concluído, com isso a solicitação não aparecerá mais nos filtros de compras quando a opção considerar faltas/encomendas estiver marcada.
Nessa mesma tela também é possível:
[Visualizar]
– Visualizar um determinado registro (F3);
[Inserir]
– Inserir um novo registro;
[Editar/Alterar]
– Editar ou alterar um registro já existente;
[Excluir]
– Excluir um registro existente;
[Relatório]
– Gerar relatório com filtros diversos para facilitar a gestão.
. Conforme abaixo:
Escolha a classificação dentre as disponíveis na tela, informe o período desejado, o tipo e a ordenação, informe também a filial desejada se houver e após clique em visualizar ou imprimir.

---

## 🔴 Configurar Emissão de Cupom SAT — 25/05/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/52227
> Publicado em: 25/05/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

1.Requisitos | Marcas
Marcas de equipamentos que funcionam no FarmaFácil
• TANCA
• DIMEP
• BEMATECH (recomendado)
2. Requisitos Para configurar o SAT no FarmaFácil
"Esses procedimentos devem ser realizados pelo suporte técnico autorizado do SAT."
O equipamento deve estar comunicando com a máquina e/ou rede local.
O equipamento deve estar comunicando como o Sefaz do Estado
O equipamento deve estar ativado.
3. Gerando o código de vinculação do AC
Fazer isso no seu computador, e não no cliente.
1. Acessar o FTP em 1.INSTALADORES\SAT\VINCULAÇÃO-AC. Dentro dele há uma pasta em um zip no qual contém os arquivos necessários para gerar o código, o arquivo a ser aberto é ‘Ger_Cod_Vinc.exe’.
2. Deve ser informado o CNPJ do AC no campo Software House (72216518000178), preencher também os campos do contribuinte.
3. No campo Certificado deve-se procurar e selecionar o certificado digital do ano de 2019.
4. Informar a senha do certificado
5. Clicar em gerar, se tudo der certo o sistema retornará um código de 344 caracteres. (conforme a imagem abaixo)
4. Integrando o equipamento no FarmaFácil
* Esse procedimento só pode ser realizado se a versão do sistema for V.16.01.13.18 ou superior, devido ao layout do XML.
4.1 BEMATECH
1. Na máquina que o SAT está instalado deverá contar com o aplicativo de ativação do equipamento que é fornecido pelo próprio fabricante.
2. A vinculação dos CNPJ’s podem ser realizados tanto no aplicativo de ativação do fornecedor do equipamento quanto pelo sistema Farmafacil. Antes de realizar tal procedimento deve-se seguir os itens abaixo.
3. Dentro da pasta de instalação do ativador você deve procurar e copiar para a pasta EXE do Farmafacil os arquivos
BemaSAT.dll
,
bemasat.xml e o IPAddressControlLib.dll
*
Copiar novamente o BemaSAT.dll e renomear essa segunda cópia para SAT.dll o cfeFimAFim.xml
4. Entrar no FarmaFácil e ir nas chaves do sistema
"Arquivo -> Parâmetro -> Configurações PrismaFive"
, filtrar todas as chaves relacionadas aquele MAC.
5. Incluir uma nova chave de registro chamado "PDV", com o valor de registro ‘001’, e uma outra chave chamado "HABILITASAT", com o valor "SIM"
6.Feito o procedimento anterior podemos configurar o sistema. Para tal vá em
"Arquivo -
>Parâmetro -> Parâmetro"
(caso tenha filial
Arquivo -
>Parâmetro -> Filial
) na aba
Cupom Fiscal/ NFC-e / SAT
, marque a
flag
Habilita SAT.
7.Incluir a chave de ativação do SAT, nos modelos Bematech o padrão é
bema1234
caso não seja essa deverá ser solicitado ao cliente ou ao técnico que fez a instalação do equipamento o código correto.
8.Incluir o código da assinatura de 344 caracteres que foi gerado anteriormente no passo 3.
*I
MPORTANTE* Sempre consultar o SAT detalhadamente no programa do fornecedor do SAT para verificar o layout do mesmo e colocar a mesma informação no sistema.
9. Se tudo ocorreu certo até aqui vá nessa mesma tela e marque a opção ASSOCIAR ASSINATURA. O retorno do Sefaz pode demorar até 30 segundos, caso a mensagem retorne com o Código 1300 é sin
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Convênio Orizon — 25/05/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/52223
> Publicado em: 25/05/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para configurarmos o convênio Orizon no sistema, é necessário que o aplicativo da Orizon esteja instalado e configurado no computador da cliente. A instalação desse aplicativo é realizada pelo suporte da própria Orizon.
Para realizar a configuração no sistema é necessário incluir o caminho para esse aplicativo no parametro.
1° Passo
Vamos em
"Arquivo -> Parâmetro -> Parâmetro"
ou caso tenha filial
"Arquivo -> Parâmetro -> Filial"
Depois vamos nas guias
"Geral -> Cartões/TEF"
e procuramos o campo
"PrevSaúde"
Configuramos o caminho da instalação do convênio que contém a pasta "PSC", no nosso caso estava como "C:\Orizon\PSC", e inserimos essas informações e marcamos o campo "Habilitar"
2° Passo
No cadastro do cliente, é necessário que a mesma esteja vinculada a um convênio do mesmo, caso não esteja, basta criar o convênio em
"Arquivo -> Venda -> Convênios"
.
É importante colocar a informação "Dia recebimento", caso a cliente não saiba, coloque 30 dias
3° Passo
Após de criado, realizamos o vinculo no cadastro do cliente que irá utilizar o convênio, para que no momento do recebimento, a forma de pagamento venha automaticamente no caixa.
Como por exemplo, fiz um cadastro de cliente com o nome "CONVÊNIO ORIZON"
Depois de concluir as configurações e cadastros no sistema, solicite para que a cliente realize uma autorização no site para que possamos realizar o teste.
OBS: é necessário que a cliente finalize a autorização conforme o print abaixo
Deixando nesta tela
4° Passo
Vamos na tela de venda no sistema, inserimos as informações de vendedor, cliente conveniado e clicamos no atalho "Alt + F9" ou então clicamos em "F11" e vamos em "PrevSaúde"
Inserimos o número de autorização que foi gerado no site (Cliente realiza esse processo) e clicamos em "Login"
5° Passo
Após clicar no login, irá puxar automaticamente o produto para a venda com o valor informado no site no momento da geração da autorização (caso isto ocorra, significa que está configurado corretamente), basta salvar a venda e realizar o recebimento.
IMPORTANTE
*Verificar após o recebimento se saiu o vinculo no cupom fiscal.
**Caso a cliente utilize impressora fiscal, é necessário que a forma de pagamento "
CONVENIO
" esteja cadastrada como
Vinculado
, conforme o exemplo abaixo:

---

## 🔴 Controle de qualidade da produto-quarentena — 17/05/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/51019
> Publicado em: 17/05/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O primeiro passo para se realizar o controle de qualidade dos insumos/embalagens é cadastrar no cadastro do produto as especificações. Para isso acesse:
ESTOQUE > LOTE
Localize o produto a ser ficha técnica
Clique em alterar
Após isso selecione o lote e pressione as teclas
CTRL+Q
Se as especificações já estiverem preenchidas o sistema irá permitir com que você faça o preenchimento dos resultados
[pule para etapa 10]
,
caso contrario você deverá clicar em SIM na menagem abaixo.
Com isso irá abrir a tela de cadastro de produto onde você deve ir na aba Ficha Técnica.
Clicar em Importar
Localizar qual farmacopeia deseja importar
Salvar
Após isso você deve informar quais são os resultados das especificações
Aqui você pode salvar sem visualizar
Aqui você pode salvar e visualizar o documento a ser impresso

---

## 🔴 DANFE - Carta de Correção — 04/04/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/45951
> Publicado em: 04/04/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para realizar emissão de carta de correção deve ser realizado em uma maquina que tenha certificado digital.
Com isso basta ir em:
CAIXA > NOTA FISCAL:
Localizar e selecionar a nota fiscal que precisa ser corrigida
Clicar no ícone Carta de correção ou tecla F8
Informar o texto da certa de correção e clicar em Salvar
Caso deseja visualizar ou imprimir a carta de correção deverá ser realizado a consulta e impressão a través do site da SEFAZ a través deste link:
http://www.nfe.fazenda.gov.br/portal/consultaRecaptcha.aspx?tipoConsulta=completa&tipoConteudo=XbSeqxE8pl8=

---

## 🔴 Reinstalação do banco | Troca de servidor — 01/04/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/45591
> Publicado em: 01/04/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Passos.
Baixar o pacote
InstaladorPostgres.zip
Disponível em:
\\192.168.0.240\ArquivosTransfer\PacotePostGreSQL\Instalador Postgres.zip
Extrair os conteúdos do pacote
InstaladorPostgres.zip
para o diretório
C:\FarmaFacil\Instalador Postgres
No diretório
C:\FarmaFacil\Instalador Postgres
executar
InstaladorPGSql.exe
como ADMINISTRADOR
Clicar em Iniciar
Nesta etapa ele irá instalar o postgres no diretório padrão dentro da pasta
C:\FarmaFacil\Database
Caso haja a necessidade é possível alterar o caminho do diretório clicando na engrenagem;
Para restauração de banco de dados é necessário informar o caminho do banco a ser restaurado na aba da engrenagem e depois clicar em Restaurar.
Após isso basta aguardar o processo finalizar.

---

## 🔴 Como gerar Arquivo TDM Daruma — 07/03/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/43058
> Publicado em: 07/03/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Geração de Arquivos TDM com o GAD
Clique aqui para fazer download do GAD
Após o download, extraia o pacote e abra a pasta “GAD_Delphi7exe”.
Execute o “GAD.exe”.
Veja o exemplo:
O GAD reconhecerá automaticamente sua impressora, caso isso não aconteça, verifique se existe outra aplicação aberta que use a impressora fiscal, se existir, feche-a.
No painel “Relatórios”, selecione os arquivos que você deseja gerar da impressora fiscal. Vamos selecionar quase todos,
apenas SPED e SINTEGRA que não
.
Veja como ficou:
No painel “Intervalos”, vamos selecionar a data inicial e data final.
Veja o exemplo:
Agora, vamos definir a pasta onde serão salvos os arquivos gerados, fazemos isso no painel “Geração dos Relatórios”.
Veja o exemplo:
Após os passos acima, clique no botão “GERAR RELATÓRIOS” para iniciar a geração.
Veja o exemplo:
A geração foi iniciada, após o termino você receberá uma mensagem.
Veja o exemplo:
Arquivos gerados! Para visualizar os arquivos, clique no label “Abrir diretório de geração dos arquivos”.
Veja o exemplo:
Após clicar, o diretório com todas as pastas de arquivos será aberto.
Veja o exemplo:
Arquivos gerados e os respectivos nomes:
Espelho da Memória Fita Detalhe – Espelho_MFD.txt
Espelho da Memória Fiscal Completa – Espelho_MF_Completa.txt
Espelho da Memória Fiscal Simplificada – Espelho_MF_Simplificada.txt
Memória Fiscal – ATO_MF_DATA.txt
Memória Fita Detalhe – ATO_MFD_DATA.txt
Nota Fiscal Estadual - DR207190.25D
Nota Fiscal Estadual TDM - DR207190.25D_TDM
VIVANOTA – VIVANOTA.txt
Geração do arquivo SPED
Com o GAD aberto, selecione apenas a opção “SPED” do painel “Relatórios”.
Veja o exemplo:
Vejam que apareceram os campos de “PIS” e “COFINS”. Estes campos não são obrigatórios, use-os apenas se você tiver alíquotas de “PIS” e “COFINS”. Caso não vá usar as alíquotas(PIS/COFINS), deixe os campos em branco, como mostra na imagem acima.
Vamos gerar um arquivo do SPED usando as alíquotas de “PIS” e “CONFINS”, então devemos
preenchê-los.
Veja o exemplo:
No painel “Intervalos”, selecione a data inicial e data final.
Veja como ficou:
Agora, vamos definir a pasta onde serão salvos os arquivos gerados, fazemos isso no painel “Geração dos Relatórios”.
Veja o exemplo:
Após os passos acima, clique no botão “GERAR RELATÓRIOS” para iniciar a geração.
Veja o exemplo:
Quando a geração concluída, você receberá uma mensagem.
Veja o exemplo:
Arquivos do SPED gerados com alíquotas de “PIS” e “COFINS”. Os valores de “PIS” e “COFINS” estão nos registros C410, C425, C460 e C470.
Para visualizar os arquivos, clique no label “Abrir diretório de geração dos arquivos”.
Veja o exemplo:
Após clicar, o diretório com todas as pastas de arquivos será aberto.
Veja o exemplo:
Assista agora o vídeo mostrando passo a passo a geração de arquivos com Gerador de Arquivos Daruma:

---

## 🔴 Declaração de aprovação de programa informatizado liberado pela ANVISA SC — 06/03/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/42865
> Publicado em: 06/03/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Declaração de aprovação de programa informatizado liberado pela AVISA para o estado de Santa Catarina

---

## 🔴 Atualização de preço ABC Farma — 04/03/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/42683
> Publicado em: 04/03/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Acima: Produtos que estão com Valor de Venda da farmácia maior que Valor de Venda da
tabela.
Abaixo: Produtos que estão com Valor de Venda da farmácia menor que o Valor de Venda da
tabela.
Não Cadastrado: Produtos que estão na tabela, mas não possuem cadastro na Farmácia
Atualizado: Produtos que estão com o Valor de Venda da tabela igual ao da Valor de Venda
da Farmácia.
Fração: Fracionamento informado no cadastro do produto
C.Farmácia: Valor de Custo informado no cadastro do produto
P.Farmácia: Valor de Venda informado no cadastro do produto
Fração: Fracionamento do produto na tabela
P.Lab c/ICMS: Valor de Custo do produto com ICMS na tabela
P.Máx c/ICMS: Valor de Venda do produto com ICMS na tabela
P.Lab s/ICMS: Valor de Custo do produto sem ICMS na tabela
P.Máx s/ICMS: Valor de Venda do produto sem ICMS na tabela
Para atualizar os preços, basta selecionar os produtos que deseja atualizar, marcando a caixa
de seleção(1), ou pressionando a tecla(T) para selecionar todos os produtos. E clicar em
confirmar(2)
Os produtos com o Status 'Não Cadastrado'(1) são os produtos que existem na tabela, mas não
possuem cadastro no Farma Fácil, se desejar cadastra-los basta marcar a caixa de seleção(2),
seleciona o Grupo(3) onde serão cadastrados e clicar em confirmar(4)
Após clicar no botão confirmar, aguardar a Atualização.
Após ter importado a tabela, pode acessa-la novamente em
ARQUIVO > ESTOQUE > PRODUTO > ABCFARMA

---

## 🔴 Alterar produto de grupo | Unificação de cadastro de produto — 22/02/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/41997
> Publicado em: 22/02/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

A alteração de produto de grupo ou unificação de cadastros só pode pode ser realizada caso atenda as seguintes regras
1- O grupo final seja o mesmo de origem. Exemplo:
Só posso mudar um produto do grupo de
Drogaria
para outro grupo de
Drogaria.
só posso unificar um produto
Drogaria
com outro
Drogaria
;
2 - Produtos controlados/antibióticos do grupo de matéria prima não podem ser trocados de grupo ou unificados.
Para realizar o processo basta ir em
ARQUIVO > UTILITÁRIO > MANUTENÇÃO GERAL > ALTERAÇÃO CÓDIGO PRODUTO
Agora você deve preencher os dados como a imagem a seguir
Exemplo 1 -
Mudança de grupo
(Código produto automático Marcado)
Exemplo 2
- Unificação de produto
(Código produto automático Desmarcado)

---

## 🔴 Alterar a impressão para outra impressora Jato de tinta ou laser — 22/02/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/41951
> Publicado em: 22/02/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Caso queria efetuar a alteração de impressão por conta própria, você pode seguir o passo a passo abaixo.
ARQUIVO > PARÂMETRO > CONFIGURAÇÕES PRISMAFIVE
1-Clicar no botão de pesquisar
2-Clicar no Ícone de monitor
3- Selecionar qual Chave deseja alterar e clicar no botão de Alteração
4- Copiar o nome da impressora e colar no registro
5- Salvar

---

## 🔴 Compactação de arquivos Xml — 20/02/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/41748
> Publicado em: 20/02/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Após fazer a exportação dos arquivos, os mesmos podem ser compactados para envio a contabilidade, por exemplo. Abaixo informações sobre como fazer a compactação:
É necessário ter  instalado no seu computador um programa próprio para compactação de arquivos como o "Winrar" , tendo o mesmo instalado basta seguir os passos:
1°
Clicar com o botão direto do mouse sobre a pasta onde está os arquivos XML'S e ir em "Adicionar arquivo para" ou "Add to archive"
2° Passo, clicar em "Zip" e depois no "Ok"
3°
passo, só enviar este arquivo por e-mail
Caso não tenha o programa "Winrar" no seu computador.
Basta clicar com o botão direito do mouse e ir em "Enviar para" e depois clicar em "Pasta compactada"
Feito isso basta anexar os arquivos no e-mail ou salvar em um pendrive e fazer o envio.

---

## 🔴 Fator UI, UFC e UTR, MEq — 18/02/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/41508
> Publicado em: 18/02/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Atualmente as informações
UI, UFC e UTR
são informadas dentro dos lotes dos produtos.
O caminho para acessar a tela de Lotes é
ESTOQUE >  LOTE
.
Nele você deve informar quais são os respectivos valores (
em
números
) em um dos campos, conforme o laudo do fornecedor. (Caso não tenha o laudo deverá solicitar ao mesmo)
Fator UI
[Unidade Internacional]
Fator UFC
[Unidade Formadora de Colonias]
Fator UTR
[do inglês: untranslated region]
Feito o preenchimento na tela do lote você pode vender o ativo nas formulações, basta colocar a quantidade solicitada na receitá médica e mudar a unidade para aquela que você preencheu no cadastro do lote conforme imagem abaixo:
Calculo usado:
1
2
3
1 / FLT = X;
X * QM = QF;
QF * FC = QF1
Legenda:
FLT = Fator que foi preenchido no lote
X = Valor temporário do Calculo
QM = Quantidade solicitada na receita Médica
QF = Quantidade Final a ser usada
FC = Caso haja fator de correção deverá ser Multiplicado  pelo mesmo
QF1= Quantidade Final a ser usada com Fator de correção

---

## 🔴 Atualização de versão — 06/02/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/40675
> Publicado em: 06/02/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Em busca de maior agilidade no processo de atualização e com o objetivo de manter nossos clientes sempre atualizados, disponibilizamos abaixo um passo a passo sobre como proceder para atualizar a versão do sistema.
1° passo:
Assim que for disponibilizada uma nova versão, será necessário entrar em contato conosco e solicitar a liberação da versão para o CNPJ em questão. Feito isso o download dos arquivos no servidor ocorrerá de forma automática e assim que estiver concluído, o sistema exibirá a mensagem abaixo no painel principal, essa mensagem será visualizada
apenas através do acesso do usuário administrador
:
2° passo:
Assim que a versão estiver disponível, feche o sistema em todos os computadores, deixando-o aberto somente no servidor ou na máquina onde será executada a atualização;
3° passo:
Clique na mensagem “
Nova versão disponível
” e após clique em SIM na mensagem a seguir para confirmar.
4° passo:
Por questões de segunda o sistema faz uma verificação gerar nas máquinas para confirmar o encerramento do mesmo. Clique em
SIM
para continuar.
5° passo:
O sistema será encerrado na máquina atual e o atualizador será executado automaticamente. Clique em sim para continuar.
6° passo:
Clique em CONTINUAR para iniciar a transferência dos arquivos, conforme abaixo.
7° passo:
Através da barra principal você poderá acompanhar a evolução do processo. Na lateral direita da tela ficará disponível a barra de rolagem, arraste para o final para poder visualizar a mensagem de conclusão da importação. Conforme abaixo:
8° passo:
Quando o processo for concluído a tela será exibida conforme abaixo, clique em fechar para finalizar o processo e abrir o sistema na máquina.
9° passo:
Você já pode iniciar o processo de atualização nos demais computadores, para isso clique duas vezes no atalho de acesso ao sistema, feito isso o atualizador será executado automaticamente, conforme abaixo. Clique em
SIM
para continuar.
10º passo:
Após confirmar o sistema executará o 6º passo e acompanhe a evolução da transferência dos arquivos, conforme os passos 7 e 8.
Feito isso, você poderá visualizar a versão atual conforme imagem abaixo e o sistema estará atualizado, pronto para você usufruir de todas as suas funcionalidades.

---

## 🔴 Convertendo os pontos por prêmios. — 04/01/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/36936
> Publicado em: 04/01/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Basicamente, um cartão fidelidade ou programa de fidelidade permite que o consumidor obtenha benefícios ao comprar com determinada empresa.
Configurando o Cartão Fidelidade e as Pontuações.
1º Passo:
Inicialmente é necessário cadastrar o tipo de cartão, para isso acesse:
Arquivo > venda > Fidelidade
Ao cadastrar o Tipo do Cartão, na Aba Geral, será necessário configurar todas as Pontuações solicitadas. Veja a seguir:
[Descrição]
– Nome do cartão (Ex. Cartão Ouro, Prata, Bronze, etc).
[Pontos Iniciais]
– Quantidade de pontos iniciais que deseja dar ao cliente no momento em que o mesmo fizer o cartão.
[Pontos Primeira Compra]
– Quantos pontos o mesmo receberá na primeira compra.
[Validade Pontos]
– Qual será a validade dos pontos, prazo para que a pontuação expire.
[Avisar Com]
– Quando o cliente atingir uma determinada quantidade de pontos o sistema emitirá um alerta.
[Forma pagamento/Pontos]
– O sistema filtra todas as formas de pagamento cadastradas e permite que seja inserido o valor e a pontuação específica para que o cliente pontue (Ex. para pagamento em dinheiro e compras acima de R$10,00 o cliente ganha 1 ponto, caso alguma das Formas de Pagamento esteja zerada, quando a mesma for utilizada no Caixa, a venda não será pontuada.).
Cadastrando os prêmios
2º Passo:
Na Aba Prêmios serão cadastrados todos os prêmios que farão parte do cartão fidelidade, para isso acesse:
Arquivo > venda > Fidelidade > Prêmios
Ao inserir um Prêmio, é necessário escolher o grupo e o produto, portanto é preciso incluir um Grupo que pode ser chamado de Prêmios Cartão Fidelidade por exemplo, e em seguida cadastrar o prêmio como produto caso ainda não esteja cadastrado, e então inserir a quantidade de pontos que o cliente precisa ter para ganhar este produto.
Pronto, após concluir o cadastro dos Cartões e das pontuações, é possível iniciar  a configuração no cadastro dos clientes.
Configurando o Cadastro do Cliente
3º Passo:
Nessa etapa é feita a ativação do cartão fidelidade no cadastro do(s) cliente(s) para que os mesmos comecem a fazer parte do programa, para isso acesse:
[Fidelidade]
– Selecionar a fidelidade cadastrada no passo 1
[Cartão]
– Neste local será informado o número que corresponde a este cliente no Cartão Fidelidade (Ex. Pode ser usado o código de cliente ou CPF do mesmo), este número deve ser o mesmo que será impresso no Cartão que sua farmácia já possui e entrega para o cliente, ou que ainda será confeccionado em gráfica. Vale salientar que caso a farmácia opte por não ter o cartão físico, ou se seu cliente não querer ou ainda perder o cartão, é possível registrar e controlar a pontuação dele através deste número, este número será colocado na hora de receber a venda no Caixa.
[Cartão Fidelidade Ativo]
– Ativa o cartão fidelidade para o cliente em questão.
Registrando as Pontuações
4º passo:
O registro dos pontos será feito no Caixa quando for o momento de receber a venda, antes de salvar o recebimento pressione as teclas ALT+F9 e o sistema irá exibir 
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Formula padrão de Acabados — 03/01/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/36813
> Publicado em: 03/01/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

1- As formula padrões de produtos acabados é o conceito no qual a farmácia usa suas matérias primas do laboratório para fazer produções de produtos que irão ficar prontos para venda no balcão. Um exemplo simples de um produto acabado é a farmácia usar duas ou mais matérias primas e fazer a manipulação de um SHAMPOO que ficará embalado e rotulado para venda na frente de balcão.
DESCRIÇÃO: É o nome da formula padrão.
FORMA: Forma farmacêutica que será realizada a manipulação
VALIDADE: Validade do produto pronto.
VOLUME: Volume da produção individual, ou seja, é o volume interno de cada embalagem do shampoo.
UNIDADE: Unidade de produção do shampoo.
PRODUTO FINAL: É o nome do produto pronto, e como ele vai ser localizado na tela de venda. Obrigatoriamente para formulas padrão de produtos acabados devem estar em grupos do tipo acabado.
QTDE EMBALAGENS: É o numero de embalagens do shampoo que será produzidas e deixadas expostas para venda nas prateleiras.
EMBALAGEM: É a embalagem que será usada para o shampoo.
POSOLOGIA: É o modo como deverá ser usado o produto pelo cliente final.
ITENS DA FORMULA: São as matérias primas que será usada para produzir o produto e suas dosagens. Essas informações são de responsabilidades da farmácia.
2- APÓS SER CADASTRADO A FORMULA PADRÃO, DEVERA SER GERADA A ORDEM DE PRODUÇÃO DESSAS FORMULA PARA O LABORATÓRIO FAZER A PRODUÇÃO.
MODULO PRODUÇÃO>ORDEM DE PRODUÇÃO>ÍCONE GERAR ORDEM DE MANIPULAÇÃO>ABA FORMULA PADRÃO
Após seguir os passos anteriores, você ira chegar nessa tela que é aonde é gerado a ordem de produção de produções internas da farmácia. Localize a formula padrão desejada e clique em confirmar para ser gerada e impressa a ordem de produção. Nesse exemplo será gerada uma ordem de produção para a produção de 5 Shampoos.
Após confirmar a ordem de produção na tela anterior o sistema ira gerar a ordem de produção que ficará com o status em produção como na imagem acima. Após o laboratório concluir o processo de produção da formula, devera ser realizada a conclusão da ordem de produção. Somente após a conclusão da ordem de produção é que o sistema irá atualizar o estoque do produto final para a quantidade de embalagens solicitadas. Nesse exemplo após a conclusão dessa ordem de produção o sistema irá atualizar o estoque do produto final do shampoo para 5 unidades de 200ml.
Antes dos produtos serem expostos para venda na frente de balcão ou nas prateleiras, deve ser impresso as etiquetas para rotular os produtos prontos. Esse processo é realizado na mesma tela anterior, clicando no ícone de imprimir etiquetas, como mostra à imagem acima.
3-Após os processos anteriores o produto acabado já esta pronto para venda para os clientes finais na tela de venda de produtos acabados\drogaria com seu estoque atualizado.
Obs: O valor de venda pode ser definido pela farmácia, sendo informado manualmente no cadastro do produto final, ou se preferir o sistema mesmo irá sugerir o valor ao concluir a ordem de produção.

---

## 🔴 Como fazer a Inutilização da NF-e/NFC-e: — 03/01/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/36788
> Publicado em: 03/01/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

A inutilização de NF-e/NFC-e é realizada quando o contribuinte precisa comunicar para o fisco que uma faixa de números dentro de uma sequência de notas fiscais não foi utilizada na emissão e portanto, devem ser desconsideradas pela SEFAZ.
Para ficar mais fácil de entender, vamos a um exemplo:
O contribuinte emite uma Nota Número 203
Em seguida uma Nota Número 204
Por uma falha no sistema emissor, a próxima nota emitida é a Nota Número 208
Isso é chamado de quebra de sequência numérica e deve obrigatoriamente sempre ser comunicada ao fisco. Os motivos mais comuns onde ocorrem quebra de sequência numérica são:
Rejeição não tratada pelo sistema emissor, onde não é feita uma nova nota ou a tentativa de autorização daquele mesmo número, deixando passar despercebido.
Erro no sistema emissor de notas na inserção automática do número da nota fiscal que vai ser emitida.
Perda de notas fiscais no processo de autorização, decorrente de instabilidade de conexão de internet, falha no ambiente de recepção ou comunicação com o fisco.
Como fazer a Inutilização da NF-e/NFC-e:
No sistema acesse:
IMPORTANTE:
A inutilização pode ser realizada somente na(s) máquina(s) que possuem o certificado digital instalado, devido a necessidade de envio das informações para a Sefaz.
Arquivo > utilitários > manutenção geral > inutilização de NF-e/NFC-e
Quando o cliente for fazer a inutilização, certamente já terá as informações sobre o que será inutilizado, nesse caso basta preencher os campos.Todos os campos são de preenchimento obrigatório:
[Tipo]
– Permite escolher qual o tipo do documento será inutilizado (NF-e ou NFC-e).
[Ano]
– Ano em que a numeração foi utilizada.
[série]
– Número da série que consta no documento que será inutilizado (1,2, etc).
[Número inicial e final]
– Numero ou intervalo de numeração que será inutilizado(Se for apenas um número, deve ser inserido o mesmo nos dois campos).
[Justificativa]
– Uma breve descrição do motivo pelo qual está sendo realizada a inutilização do(s) número(s).

---

## 🔴 Aumentar ou redução da quantidade de licenças - Chave HASP — 02/01/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/36783
> Publicado em: 02/01/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O aumento ou redução da quantidade de licenças é solicitado pela farmácia e ocorre através de uma negociação com nosso setor comercial e/ou financeiro, o chamado normalmente é aberto pelo setor financeiro após o término das negociações e o setor de suporte executa o processo abaixo para efetivar a alteração no cliente.
1° passo:
Copiar o aplicativo “RUSPrismaFive”, que está na pasta:
\\prismaserver\ftp\1.INSTALADORES\HASP\Formatador
, para a máquina onde se encontra a chave instalada. Conforme a imagem:
2° passo:
Executar o aplicativo dentro pasta onde o mesmo está salvo.
3° passo:
Clicar no botão “Collect Information”, na aba “Collect Key Status Information”, e encontrar a pasta onde esta o aplicativo e salvar o arquivo como o nome da farmácia.
Observação: Será apresentada uma mensagem que o processo foi executado com sucesso.
4° passo:
Copiar o arquivo salvo, colocar no FTP e passar o caminho para o responsável interno pela alteração, gerar a nova chave.
5° passo:
Após o responsável gerar a nova chave, será preciso pegar o arquivo gerado, e coloca-lo na mesma pasta onde está o aplicativo de alteração da chave. Na aba “Apply License Update”, você encontrará o caminho onde esta salvo o novo arquivo e então clicará no botão “Apply Update”.
Observação: Ao final do processo será apresentado uma mensagem informando que a atualização foi gerada com sucesso.
6° passo:
Após esse processo você deve abrir o sistema, e o mesmo irá solicitar a atualização da chave, então você passará o número da nova chave para o responsável e irá atualizar a mesma na tela de manutenção de chave.
7º passo:
Após esse processo, confira a quantidade de licenças acessando o endereço “
http://localhost:1947
” na máquina onde foi feito o processo e observe se a quantidade de licenças informada corresponde ao que está liberado.

---

## 🔴 Cadastro de Natureza de Operação — 02/01/2019

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/36773
> Publicado em: 02/01/2019
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

CFOP
[Código Fiscal de Operações e Prestações] ou
Natureza de Operação
é o código que identifica as entradas e saídas de produto. Mostra também se o produto vai circular dentro do mesmo estado ou em estados diferentes entre origem e destino. O CFOP define também a arrecadação de impostos.Esse código é formado por quatro números. O primeiro define o tipo de operação:
entrada ou saída
. Exemplo:
[
1
xxx] – ENTRADAS OU AQUISIÇÕES DE SERVIÇOS DO ESTADO
[
2
xxx] – ENTRADAS OU AQUISIÇÕES DE SERVIÇOS DE OUTROS ESTADOS
[
3
xxx] – ENTRADAS OU AQUISIÇÕES DE SERVIÇOS DO EXTERIOR
[
5
xxx] – SAÍDAS OU PRESTAÇÕES DE SERVIÇOS PARA O ESTADO
[
6
xxx] – SAÍDAS OU PRESTAÇÕES DE SERVIÇOS PARA OUTROS ESTADOS
[
7
xxx] –  SAÍDAS OU PRESTAÇÕES DE SERVIÇOS PARA O EXTERIOR
Os outros se referem ao tipo e finalidade do produto: se o produto foi produzido pelo seu estabelecimento, se é matéria prima, se vai ser consumido, vendido ou até mesmo se é uma venda simples.
Cadastrando uma CFOP:
Para efetuar o cadastro siga os seguintes passos:
ARQUIVO > PARÂMETRO > NATUREZA DE OPERAÇÃO.
Chaves e campos:
Dentro do cadastro da natureza de operação existem alguns campos que podem ser selecionados:
[Entrada]
– Define o sentido da CFOP, que será do tipo entrada.
[Saída]
– Define o sentido da CFOP, que será do tipo saída.
[Exporta Sintegra]
– Quando habilitado faz com que todas as notas que utilizam essa CFOP saim no arquivo SINTEGRA.
[Exige documento referenciado]
– Quando habilitado indica que esta natureza de operação precisa da chave de referenciada, utilizado em casos de nota de devolução.
[Considerar CFOP no crédito de ICMS]
– Permite a utilização do credito do ICMS na nota fiscal.
[Não incide Pis]
– Define que a CFOP não terá incidência de PIS.
[Não incide Cofins]
– Define que a CFOP não terá incidência de Cofins.
[Contas]
– Define para qual plano de contas será
utilizada/movimentada
a CFOP.

---

## 🔴 Pré requisitos para configurar emissão de NFC-e — 27/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/36154
> Publicado em: 27/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

A NFC-e (Nota Fiscal de Consumidor Eletrônica) é um documento fiscal eletrônico utilizado para registrar operações comerciais de venda de produtos ou prestação de serviços diretamente ao consumidor final. Ela substitui os tradicionais cupons fiscais emitidos no ECF, oferecendo uma alternativa digital mais eficiente, segura e sustentável.
A NFC-e é emitida e armazenada de forma eletrônica, sendo validada pela Secretaria da Fazenda (ou equivalente) do estado onde a operação ocorre. Ela contém informações detalhadas sobre a transação comercial, incluindo dados do estabelecimento, produtos vendidos, valores, impostos incidentes, entre outros.
Os consumidores podem receber a NFC-e por e-mail, mensagem de celular (SMS) ou consultar diretamente no site da Secretaria da Fazenda para obter a sua cópia eletrônica. Essa tecnologia visa facilitar a fiscalização tributária, reduzir custos para as empresas e oferecer mais comodidade aos consumidores, além de contribuir para a diminuição do consumo de papel e a preservação do meio ambiente.
Pré-requisitos para configurar a emissão no sistema FarmaFacil:
Certificado Digital (Modelo A1 ou A3) dentro da data de validade, vinculado e instalado na máquina a ser utilizada para realizar a emissão dos cupons;
Inscrição Estadual regularizada, bem como credenciamento com o SEFAZ estar em dia;
Impressora não fiscal ou laser de acordo com a necessidade da farmácia;
Código CSC/Token da sua Inscrição Estadual; (Para o ambiente de produção e homologação, ambos fornecidos pela contabilidade);
ID token
Informações fiscais para atualização cadastral dos produtos de revenda/acabados, conforme abaixo:
Situação Tributária;
Códido CST;
Código CSOSN;
Código da Natureza de operação (CFOP);
Tabela de NCM atualizada (
https://www.gov.br/receitafederal/pt-br/assuntos/aduana-e-comercio-exterior/classificacao-fiscal-de-mercadorias/download-ncm-nomenclatura-comum-do-mercosul
)
ATENÇÃO!
Quanto a habilitação do ambiente de produção e emissão do CSC/Token, existem padrões diferentes de acordo com cada estado, abaixo alguns estados que possuem particularidades:
Credenciamento em Pernambuco:
Para credenciar o estabelecimento no ambiente de produção é necessário antes realizara emissão de 10 cupons no ambiente de Homologação. Para isso gere uma venda teste contendo um produto com a tributação adequada e receba e cancele a mesma venda 10 vezes consecutivas.
Credenciamento em Mato Grosso do Sul:
Credenciamento:
Acesse o site
http://www.dfe.ms.gov.br/nfce-credenciamento/index.jsf
Clique no botão: "Acessar credenciamento online" .
Clique na
flag:
"Credenciar".
IMPORTANTE:
Se a situação do estabelecimento estiver correta na Sefaz a IE [Inscrição estadual] ficará em verde, conforme imagens abaixo:
Após esse processo deverá ser gerado o CSC e ID Token.
Acesso ao CSC/Token:
Acesse o site:
http://www.dfe.ms.gov.br/csc/
Clique em: "Acessar CSC".
Após clique em NOVO CSC inicialmente para homologação e após faça o mesmo para produção.
ATENÇÃO!
Após ter as in
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Balanço de controlados de Manipulação - BSPO — 19/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/35437
> Publicado em: 19/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Balanço de controlados, também chamado de BSPO ou MAPA de controlados, é toda movimentação trimestral das farmácias com produtos de controle especial. Essa movimentação deve ser apresentada em forma de relatório gerado pelo sistema para a vigilância sanitária até o dia 15 do próximo mês ao encerramento do trimestre.
1º TRIMESTRE:
01/01 A 31/03 (O balanço deve ser entregue até entre o dia 1º de abril a 15 de abril);
2º TRIMESTRE:
01/04 A 30/06 (O balanço deve ser entregue até entre o dia 1º de julho a 15 de julho);
3º TRIMESTRE:
01/07 A 30/09 (O balanço deve ser entregue até entre o dia 1º de outubro a 15 de outubro);
4º TRIMESTRE:
01/10 A 31/12 (O balanço deve ser entregue até entre o dia 1º de janeiro a 15 de janeiro);
BALANÇO ANUAL:
01/01 A 31/12 (O balanço deve ser entregue juntamente com o do 4º trimestre de 01 de janeiro a 15 de janeiro).
ATENÇÃO:
O balanço anual refere-se à movimentação dos controlados de todo o ano da farmácia.
Para gerar o balanço de controlados para manipulação acesse:
Venda > Relatórios > Controlados Manipulação > Opção Balanço Completo > Informe o ano Referência > Selecione o período > Tipo de impressão > Gerar
Ano de referência:
Se refere ao ano em exercício, referente ao período que será entregue o relatório.
Seleção do período:
Se refere ao trimestre que será entregue para o órgão fiscalizador.
Atenção:
Nunca deverá ser entregue o relatório referente ao trimestre atual, ou seja, sempre será entregue o balanço do trimestre anterior ao atual.
TIPO DE IMPRESSÃO:
ATENÇÃO!!
Rascunho:
Essa opção é usada para visualizar o relatório e fazer a conferência (Semelhante ao ambiente de homologação) antes de fazer o envio para a vigilância.
Definitivo:
Opção a ser selecionada quando o balanço está pronto para envio (semelhante ao ambiente de produção). Ao marcar essa opção e gerar o balanço o sistema
fecha o trimestre selecionado
e não é mais possível fazer qualquer tipo de alteração ou movimentação relacionado aos controlados no período referente ao trimestre selecionado, por isso é importante a farmácia emitir o rascunho para conferência e fazer todos os ajustes necessários, caso necessite para somente depois gerar o definitivo.
Ao clicar na opção de visualizar (F3) o sistema ira gerar o balanço em tela para visualização e/ou impressão.
No balanço ira mostrar todas as movimentações de todos os produtos controlados de acordo com padrão que está previsto na legislação.
Estoque inicial:
A quantidade inicial do balanço atual é igual a quantidade final da matéria prima informada no balanço do trimestre anterior.
Aquisição:
É exibido o total de compras lançadas por meio de nota de entrada da matéria prima controlada dentro do período do trimestre selecionado.
Perdas:
É informado o total de acertos de estoque de saída realizado dentro do período do trimestre selecionado.
Fab. não Psicot.:
É exibido o total de vendas manipuladas dos produtos dentro do período do trimestre selecionado.
Estoque Final:
Quantidade final em estoque no trime
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Formula Padrão de Pré-Venda — 19/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/35434
> Publicado em: 19/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Formula padrão de pré-venda é utilizada para todas as formulas da farmácia que são vendidas com muita freqüência ou são formulas complexas, aquelas com muitos itens e muitas dosagens. Ou seja, esse conceito é para agilizar o processo de venda, para que as atendentes não precisem digitar toda vez que é pedido essa a formula, então é realizado o cadastro da formula pré-venda para salvar as informações dos itens e suas dosagens e cálculos, assim facilitando e agilizando a venda.
CADASTRO
Para fazer o cadastro da formula padrão de pré-venda, vá até a tela de formula padrão e insira um novo cadastro do tipo pré-venda:
As demais informações na tela do cadastro são as mesmas que a cliente utilizaria se fosse fazer a vendas pela tela de venda de formulas, essas informações são de responsabilidade da farmácia fazer o preenchimento:
DESCRIÇÃO:
É O NOME DA FORMULAÇÃO, OU SEJA, É O NOME POPULAR QUE A FARMÁCIA CHAMA ESSA FORMULA E PELO QUAL ELA SERÁ PESQUISADA NA TELA DA VENDA.
FORMA:
NOME DA FORMA FARMACÊUTICA QUE SERA REALIZADA (MANIPULADA) FORMULA.
VALIDADE:
VALIDADE DA FORMULA FARMACÊUTICA, ESSA INFORMAÇÃO JÁ VEM AUTOMATICAMENTE DO CADASTRO DA FORMA FARMACÊUTICA, MAS PODE SER ALTERADA PARA OUTRA VALIDADE DEPENDENDO DA NECESSIDADE.
QTDE CÁPSULAS:
QUANTIDADE CÁPSULAS QUE SERÁ REALIZADA A FORMULA, PODENDO SER ALTERADA NO ATO DA VENDA PARA OUTRA QUANTIDADE DEPENDENDO DA NECESSIDADE  DO CLIENTE.
VALOR FORMULA
: NESSE CAMPO A FARMÁCIA JÁ PODE DEIXAR INFORMADO O VALOR QUE ELA DESEJA VENDER ESSA FORMULAÇÃO PARA O CLIENTE. CASO ESSE CAMPO FIQUE EM BRANCO O SISTEMA IRÁ CALCULAR O PREÇO NA HORA DE PUXAR A PRE-VENDA NA VENDA.
EMBALAGEM:
NOME DA EMBALAGEM QUE A FARMÁCIA IRA COLOCAR AS CÁPSULAS MANIPULADAS PARA ENTREGAR PARA O CLIENTE.
CAPSULAS:
NUMERO E COR DA CÁPSULA QUE SERA SERA COLOCADO AS MATÉRIAS PRIMAS DA FORMULA.
POSOLOGIA:
É A INFORMAÇÃO DA FORMA NO QUAL O CLIENTE IRA TOMAR A MEDICAÇÃO
ITENS DA FORMULA:
É AONDE SERA INFORMADO TODAS AS MATÉRIAS PRIMAS QUE SERÃO MANIPULADAS JUNTAMENTE COM SUAS DOSAGENS (QUANTIDADES) E TIPO DE CÁLCULOS UTILIZADOS PARA A FORMA FARMACÊUTICA.
REALIZAÇÃO DA VENDA ATRAVÉS DA OPÇÃO PRE-VENDA-
Vá até a tela da venda, e inseria uma venda nova. Após informar os dados do vendedor e do cliente clique na opção
PESQUISAR VENDA (Alt + R)
, na parte superior e depois em
PRÉ-VENDA.
Depois digite o nome do cadastro da formula padrão pré-venda para localizar, selecione e confirme.
Após a pré-venda será selecionada na tela da venda sem a necessidade do vendedor ter que digitar manualmente todas as informações já cadastradas na pre- venda, assim agilizando o processo.
Caso seja necessário fazer alguma alteração na formula é só clicar no ícone de alterar e realizar as alterações necessárias. Se precisar adicionar mais pré-vendas é só fazer o mesmo processo de inserção pelo ALT + R

---

## 🔴 Cadastro Visitador — 18/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/35334
> Publicado em: 18/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

ARQUIVO > SUB-MENU (VENDA) > VISITADOR:
Clicar no ícone do + ou apertar a tecla Insert do teclado para cadastrar um novo visitador:
Na tela que abrir para preenchimento dos dados, o único campo obrigatório é o nome, o restante é opcional, após preencher basta apertar a tecla Enter para salvar o registro:

---

## 🔴 Cadastro Médico — 18/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/35333
> Publicado em: 18/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O Cadastro de usuário é encontrado no menu
Acesso > Arquivo > Médico
Na janela Médico, clique em
‘Incluir’
Nome e CR são obrigatórios.
CRM
= Conselho Regional de Medicina.
CRMV
= Conselho Regional de Medicina Veterinária.
CRO
= Conselho Regional de Odontologia. Outros podem ser médicos estrangeiros e farmacêuticos.
Na aba complemento pode-se informar o visitador.
Incluir uma Especialidade

---

## 🔴 DANFE - Nota de transferência — 18/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/35330
> Publicado em: 18/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para realizar a emissão dessa nota a farmácia deve realizar antes a transferência de estoque de uma unidade para outra.
Em seguida ir em CAIXA > NOTA FISCAL.
Lá você  incluir uma nova nota fiscal no botão verde de + [conforme imagem abaixo]
Após isso a farmácia precisa informar os dados para emissão da nota sendo eles:
Natureza de operação | Tipo Fatura | Serie | Sub-serie | Numero da nota |
Filial [Se houver]
Dados para quem estará emitindo a nota fiscal | Se tem frete ou não.
Clicar na lupa
Clicar em transferência;
Marcar em SIM  para definir qual é a transferência que deseja incluir na nota fiscal;
Marcar que tipo de valor que deseja levar para a nota fiscal;
Clicar na seta verde
Após isso ele irá transportar os produtos para dentro da sua nota e com isso já se pode clicar no botão de salvar

---

## 🔴 Chave paralela não reconhece — 18/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/35329
> Publicado em: 18/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Após casos de formatação ou instalação nova alguns windows podem não reconhecer a chave para resolver isso basta seguir os passos
Obs: Esta chave não funciona em placas PCI Express somente por comunicação direta via Onboard.
instalar o
Compact drivers
de acordo com a versão [32/64 bits] do windows. [Em anexo]
Colocar a proteq.sys [Em anexo] no seguinte diretório do windows
C:\Windows\System32\drivers
Reiniciar a maquina
Caso a chave não reconheça possíveis soluções
Troque para outra maquina
Chave está queimada

---

## 🔴 Cadastro de Vendedor — 18/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/35306
> Publicado em: 18/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Acessando o cadastro de vendedor
O cadastro de vendedor é encontrado no menu
Arquivo > Venda > Vendedor
Janela de Vendedores clique em 'Incluir'
O Vendedor deve ser  vinculado a um usuário do sistema.
Preencher as informações. Nome e Usuário são obrigatórios
Selecione o usuário e confirme
Para realizar venda de Farmácia Popular, é preciso que o CPF e a senha do vendedor do portal do Farmácia Popular, estejam preenchidos no cadastro do vendedor.

---

## 🔴 Incluindo convênio no cliente — 13/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34956
> Publicado em: 13/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para incluir um convênio no cliente, acesse a janela cliente ( Ctrl + F e digitar Cliente, depois apertar Enter), selecione o cliente, na parte de baixo selecione a aba ‘Convênio’
Clique na aba 'convenio' do cliente selecionado
Clique em pesquisar
Selecione o convênio que deseja inserir e confirme
As opções 'Em uso' e 'Ativo'  precisam estar marcadas para que o convênio apareça na venda.

---

## 🔴 Cadastro de Paciente — 13/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34924
> Publicado em: 13/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para cadastrar um paciente no cliente, acesse a janela cliente, selecione o cliente, na parte de baixo selecione a aba ‘Paciente’
Selecione a aba paciente, clique em incluir
Preencha as informações, o nome é obrigatório, para receitas de produtos controlados, outros campos podem se tornar obrigatórios.

---

## 🔴 Cadastro de Cliente — 13/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34908
> Publicado em: 13/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O cadastro de cliente é encontrado no menu Arquivo > Venda > Cliente
Pela janela de pesquisa pelo nome ‘Cliente’
Janela Cliente
Para incluir novo, clique em incluir
Após preencher os dados clique em Salvar. Para a emissão de nota fiscal eletrônica, outros campos se tornam obrigatórios.
Editando o cadastro de um cliente

---

## 🔴 Politicas de Acesso Usuário — 11/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34640
> Publicado em: 11/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Permissão de Acesso dos Usuários.
O acesso aos módulos e programas é definido pelo grupo de usuário.
O cadastro das funções se encontra em
ACESSO > MOVIMENTO > ACESSO USUÁRIO
Clica em incluir um grupo de acesso, ou editar
Manutenção de acesso usuário
Nessa janela ficam listados todos os acessos do Farma Fácil.
os programas listados no painel da esquerda estão bloqueados, no painel da direita estão liberados.
Altera os programas de painel, utilizando as setas no meio da tela.
Janela de manutenção de acesso
Quando terminar as alterações clique em Salvar

---

## 🔴 Cadastro de Usuário — 11/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34633
> Publicado em: 11/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O Cadastro de usuário é encontrado no menu Acesso > Arquivo > Usuário
Pela janela de pesquisa pelo nome ‘Cliente’
Cadastrando usuário
O Usuário é o login utilizado para entrar no Farma Fácil, e todas as ações realizadas no programa ficam vinculadas ao usuário utilizado para o acesso. O ideal é que cada pessoa que irá utilizar o Farma Fácil tenha seu próprio usuário.
Para cadastrar o usuário, deve seleciona o grupo do usuário, e preencher as informações da janela de cadastro.
Após cadastrar um usuário no primeiro acesso, será solicitado que seja alterada a senha.
Clique no botão incluir para incluir um usuário
Preencher as informações e salvar. Senha de administrador é utilizada para liberar algumas situações no sistema, como exclusões, limite de desconto e troca de vendedor.
No primeiro acesso do novo usuário, será solicitado que troque a senha.

---

## 🔴 Cadastro Grupo de Usuário — 11/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34630
> Publicado em: 11/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O Cadastro de usuário é encontrado no menu Acesso > Arquivo > Grupo Usuário
ou Pela janela de pesquisa pelo nome ‘Grupo Usuário’
Pode-se criar grupos como administradores, vendedores, farmacêutico, etc...
Serve para agrupar os usuários por funções, já que cada grupo possui seu próprio conjunto de acessos configurados.
Clique no botão incluir para incluir um novo grupo
Informe o nome do grupo, e clique em salvar.

---

## 🔴 Cadastro Embalagem — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34549
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para cadastrar embalagem corretamente, é necessário informa o volume, a unidade do volume
e vincular com a Forma Farmacêutica que irá utilizar essa embalagem.
Caso seja uma embalagem para capsulas, também é necessário informar quantas capsulas de determinado tamanho, cabem dentro dela.
Após clicar em incluir Forma Farmacêutica, seleciona a Forma desejada, e salva.
Para informar a Capacidade Embalagem(Cápsulas) seleciona o tipo da capsula e informa a quantidade correspondente.
Cadastro de Composição de Embalagem
Na aba Composição, é possível vincular outras embalagem como parte desse cadastro de embalagem
Selecione ao produto que vai ser vinculado como composição. Pode indicar uma forma Farmacêutica especifica que vai utilizar essa composição
Pode incluir vários produtos como composição.

---

## 🔴 Cadastro Complemento — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34541
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Geral
A aba geral trás os campos, Sinônimo, Incompatibilidade, Excipiente e Associação.
Sinônimos
Sinônimos funcionam como descrições adicionais para o produto, o valor informado no campo fator equivalência, será utilizado para o cálculo de quantidade do produto sempre que o produto for selecionado pelo nome sinônimo.
Incompatibilidade
Utiliza para cadastrar uma incompatibilidade, para não permitir que salve uma formulação em que a substancia estiver sendo utilizada e tentar incluir a substancia informada como incompatível.
Excipiente
Informa um excipiente especifico, quando essa substancia for utilizada em uma formulação o excipiente utilizado será o que estiver informado aqui.
Associação
Informando uma associação, toda vez que a substância for utilizada em uma forma farmacêutica especifica, automaticamente será adicionado a formulação a associação cadastrada. O cálculo da % pode ser em relação:
Somente Ativo
: % em relação a quantidade da substancia utilizada.
Ativo + Excipiente
: % em relação a quantidade da substancia utilizada + a quantidade de excipiente.
Ativo + QSP
: % em relação a quantidade total da formulação.
Especifico
A aba especifico permite cadastrar especifico para esse produto, desconto, validade, capsula e embalagem.
Desconto
Informa uma % desconto para uma forma farmacêutica especifica.
Podendo ser em relação a quantidade em mg (miligramas) ou em quantidade de capsulas utilizadas.
Validade
Informa uma validade em nº de dias, especifica para uma determinada forma farmacêutica.
Cápsula Produto
Informa uma capsula especifica para a substancia, pode ser uma capsula especifica para a quantidade em mg (miligrama) ou especifica pelo tipo de capsula calculado na venda.
Essa opção é muito utilizada por exemplo para definir cores diferentes de capsula para determinadas substancias.
Embalagem Produto
Informar uma embalagem especifica para a formulação que possui essa substancia em uma determinada forma farmacêutica.
Bula
Informa o texto que será impressora na bula do produto.
No estado do Paraná a impressão da bula é obrigatória, e deve seguir modelo padrão, que já está cadastrado no sistema, não sendo necessário informar nenhum texto especifico aqui.
Observação
Permite cadastrar uma mensagem de observação, que será exibida na ordem de manipulação, ou na venda.

---

## 🔴 Cadastro Cápsula — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34537
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

No cadastro da Capsula é necessário informar o tipo da capsula.
Aqui são cadastrados os tipos de capsulas que serão utilizadas na manipulação, os tipos padrão de capsulas de acordo com a capacidade de volume, os tamanhos comuns são 00,0,1,2,3 e 4.
Número:
Informa o número da capsula, se é 0, 00, 1 etc...
Volume Interno:
Informa o volume que comporta dentro da capsula. Esse valor será usado pelo sistema para selecionar a capsula adequada nas formulas de manipulação.
Volume Total:
Informa o volume total da capsula.
Peso:
Informa o peso total do involucro, é utilizado para a correta analise do produto.
Capsula Padrão:
Seleciona qual é a capsula padrão desse tipo.
Tipo Capsula Inativa:
Marcando essa opção o sistema não irá utilizar esse tipo de capsula na manipulação.
Prioridade na Sugestão de Capsulas:
Pode informar capsulas de acordo com a prioridade de uso o sistema irá selecionar na manipulação as capsulas de acordo com prioridade.

---

## 🔴 Calculo Estoque Mínimo — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34535
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Com essa ferramenta é possível atualizar o campo estoque mínimo de todos os produtos com um valor sugerido pelo sistema.
Seleciona o tipo de análise, o período a ser analisado e o tempo de reposição, seria o tempo mínimo que o estoque deve durar.
Demanda:
para produtos acabados e drogaria
Consumo
: para produtos de manipulação
Lembrando que para fazer o cálculo é necessário fazer a conclusão de todas as ordens, isso para que não haja estoque comprometido.
Para realizar o processo acesse:
Arquivo > estoque > produto > Calcular Estoque mínimo (F9).
Preenche as informações seleciona o grupo e clica no botão da calculadora.
O tipo Demanda é para produtos de drogaria, vai exibir o estoque mínimo atual do cadastro, a quantidade vendida no período, o estoque atual e o estoque mínimo calculado. Para gravar a sugestão do sistema clica no Salvar
O tipo Consumo é para produtos de manipulação, para analisar é preciso que tenha concluído todas as ordens de manipulação do período selecionado.
Vai exibir o estoque mínimo atual do cadastro, a quantidade vendida no período, o estoque atual e o estoque mínimo calculado. Para gravar a sugestão do sistema clica no Salvar.

---

## 🔴 Tributação — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34532
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Todos os produtos possuem a aba tributação, onde devem estar especificados os códigos tributários do produto.
Origem Mercadoria:
Seleciona a origem da mercadoria
Situação Tributária:
Seleciona a situação tributaria a que pertence o produto
Alíquota (ICMS):
Informa alíquota ICMS do produto, somente se a situação tributária for ‘
Tributada Integralmente
’ nos demais tipos deixar 0,00%
CST (Código Situação Tributária):
Seleciona o CST adequado para o produto.
CSOSN (Código Situação Optante Simples Nacional):
Seleciona o CSOSN adequado para o produto.
CST Pis Entrada:
Seleciona o CST PIS adequado para a entrada do produto.
CST Pis Saída:
Seleciona o CST PIS adequado para a saída do produto.
CST Cofins Entrada:
Seleciona o CST Cofins adequado para a entrada do produto.
CST Cofins Saída:
Seleciona o CST Cofins adequando para a saída do produto
Alíquota Pis:
Informa a alíquota Pis do produto.
Alíquota Cofins:
Informa a alíquota Cofins do produto.
CFOP (Código Fiscal de Operações e Prestações):
Seleciona o CFOP adequado para o produto.
CEST (Código Especificador da Substituição Tributária):
Seleciona o CEST adequado para o produto.
FCP (Fundo Combate à Pobreza):
Marca se é participante do FCP.

---

## 🔴 Ficha Tecnica — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34531
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

São as definições de qualidade do produto, as especificações técnicas que ele deve apresentar para ser utilizado.
Os ensaios são essas especificações.  No cadastro do produto deve ser indicado quais são esses ensaios, e qual o resultado padrão esperado.
Essa informação é depois utilizada para realizar a aprovação do lote, a liberação dele para o uso.
Os ensaios são vinculados a farmacopeias, que é um conjunto de especificações técnicas, na literatura oficial existem várias especificações que são catalogadas em compêndios, chamados farmacopeia.
Por exemplo a farmacopeia brasileira:
http://portal.anvisa.gov.br/farmacopeia
1 - ARQUIVO > ESTOQUE > PRODUTO > aba 'Ficha Técnica'
Categ. Terapêutica:
deve-se informar a categoria terapêutica do produto.
Conservação:
modo de conservação do produto.
Vincular Farmacopeia:
ao vincular uma farmacopeia será incluído automaticamente todos os ensaios pertencentes a essa farmacopeia.
Incluir Ensaio:
permite incluir um ensaio especifico ao produto.
Solubilidade:
inclui a descrição da solubilidade a um outro produto.
Observação:
Pode preencher uma observação que será impressa na ficha técnica.
Cadastrando Farmacopeia
É permitido o cadastro de somente 5 farmacopeias.
Clicar em incluir.
Preencher o nome, e a observação dessa farmacopeia.
Cadastrando Ensaio
Clicar em Incluir
Preencher o nome do ensaio, e selecionar a farmacopeia a que ele pertence.

---

## 🔴 Curva ABC — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34529
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

A
curva de experiência ABC
, também chamada de
análise de Pareto
ou
regra 80/20
, é um método de categorização de estoques, cujo objetivo é determinar quais são os produtos mais importantes de uma empresa, os mais vendidos.
Para calcular a Curva ABC dentro do sistema será preciso seguir os passos abaixo:
1-
Abrir a tela de cadastro do produto e clicar no botão Calcular Curva ABC, conforme imagem abaixo:
Arquivos > Estoque > Produto
2-
Preencher os campos conforme as instruções abaixo:
Período:
Período que deseja calcular a Curva ABC, informando a data inicial e data final.
Margens:
Curva A, Curva B e Curva C – Informar a porcentagem que deseja que o sistema faça o cálculo.
Após preencher esses dados, clicar no botão Iniciar Calculo.
Então será apresentado mensagem que a Curva ABC foi gerada com sucesso.
3-
Para conferir o relatório com os dados da Curva ABC:
Venda > Relatórios > Curva ABC
Você pode tirar o relatório por Curva ou tirar de todas as classificações, onde será apresentado
os produtos mais rentáveis na Curva A (quem teve maior retorno em valor), intermediário na
Curva B e menos rentáveis na Curva C..
4-
Após o calculo as informações das porcentagens informadas ficarão salvas em:
Arquivo > parametro > parametro > geral > geral > curva ABC

---

## 🔴 Registro MS — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34520
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Registro MS
(Registro do Ministério da Saúde) é o código de identificação de um medicamento no ministério da saúde.
É uma informação obrigatória para medicamentos controlados possui 13 dígitos.
A validade de um registro pode ser consultada através do link:
https://consultas.anvisa.gov.br/#/medicamentos/
O campo registro MS só está habilitado para produtos de drogaria, porque o campo se refere a medicamentos produzidos por laboratórios, que consta na caixa e na bula do medicamento.
1 -
O Campo deve ser preenchido com 13 dígitos
2 -
Exemplo de um Antimicrobiano cadastrado com Registro MS
3 -
Exemplo de um Sujeito a Controle Especial cadastrado com Registro MS

---

## 🔴 Cadastro DCB — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34515
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

DCB -
Denominação Comum Brasileira, é a denominação do fármaco ou princípio farmacologicamente ativo aprovada pelo órgão federal responsável pela vigilância sanitária
(Lei n.º 9.787/1999)
.
Todos os códigos atuais podem ser consultados no site da Anvisa.
http://portal.anvisa.gov.br/denominacao-comum-brasileira
É um código de 5 dígitos, o já vem com os mais comuns cadastrados, bastando apenas digitar o número, ou selecionar da lista. Caso seja necessário incluir um novo, é só clicar no botão incluir e informar o numero e descrição.
1 -
Para incluir um novo, clicar no 'arquivo'
2 -
Para cadastrar um DCB, é preciso apenas informar o código, e a descrição.

---

## 🔴 Classe Terapêutica — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34514
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

As substancias são classificadas em dois tipos.
Antimicrobiano e Sujeito a Controle Especial.
Classe Terapêutica 1 =
antimicrobiano
ou antibiótico.
Classe Terapêutica 2 =
sujeito a controle especial
, são categorizadas em listas de acordo com seu efeito.
1 -
Deve marcar a opção correspondente a classe do produto, essa opção só pode ser alterada caso o produto não possua estoque.
Antimicrobiano:
O produto Antimicrobiano deve conter a marcação da classe e o código DCB
Sujeito a Controle Especial:
Produtos com a classe ‘sujeito a controle especial’ precisam ter a lista a qual pertencem informada.
Lista Controlado
A1 -
ENTORPECENTES
A2 -
ENTORPECENTES, USO PERMITIDO SOMENTE EM CONCENTRAÇÕES ESPECIAIS
A3 -
PSICOTRÓPICAS
B1 -
PSICOTRÓPICAS
B2 -
PSICOTRÓPICAS ANOREXÍGENAS
C1 -
OUTRAS SUBST. SUJEITAS A CONTROLE ESPECIAL
C2 -
RETINÓICAS
C3 -
IMUNOSSUPRESSORAS
C4 -
ANTÍ-RETROVIRAIS
C5 -
ANABOLIZANTES
D1 -
PRECURSORAS DE ENTORPECENTES E/OU PSICOTRÓPICAS
D2 -
INSUMOS E SÍNTESE DE ENVELOPES E/OU PSICOTRÓPICOS
O sistema já possui as comuns cadastradas, bastando apenas selecionar.

---

## 🔴 Produtos Controlados — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34513
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Produtos controlados, são substancias e medicamentos cuja utilização é controlada pela ANVISA (Agência Nacional de Vigilância Sanitária).
Através do Sistema Nacional de Gerenciamento de Produtos Controlados (SNGPC). Essas substancias estão especificadas na portaria 344/98
http://portal.anvisa.gov.br/
A movimentação delas no sistema deve seguir todas as normas dos regulamentos técnicos emitidos pela ANVISA nas RDC (Resolução da Diretoria Colegiada).
Para o funcionamento adequado do controle é imprescindível que todas as informações do cadastro do produto estejam preenchidas corretamente.
A responsabilidade por essas informações, é do RT (Responsável Técnico) da farmácia.
A alteração desses campos no FarmaFácil só é permitida se o produto não possuir nenhuma quantidade em estoque.
1 - Campos no cadastro de produto.

---

## 🔴 Cadastro de Produto — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34511
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

1 -
O cadastro de grupo é encontrado no menu Arquivo > Estoque > Produto
2 -
Na janela produto clique em 'Incluir'
- Filtro da exibição de produtos.
ATIVO
- exibe apenas os produtos Ativos.
INATIVO
– exibe apenas os produtos inativos.
AMBOS
– exibe todos os produtos ativos e inativos.
3 -
Janela de cadastro de produtos, primeiro deve-se selecionar o grupo do produto. Após selecionar o grupo, a janela exibirá somente os campos de cadastro referentes a esse grupo.

---

## 🔴 Cadastro de Matéria Prima — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34506
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

MATÉRIA-PRIMA

---

## 🔴 Grupos de Produtos: Classificação e Funcionalidades no Sistema — 10/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34496
> Publicado em: 10/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Grupos de Produtos: Classificação e Funcionalidades no Sistema
Os grupos são utilizados para categorizar os produtos, determinando quais campos estarão disponíveis no cadastro e como o sistema irá gerenciar a movimentação desses itens.
Tipos de Grupos
O sistema conta com
oito tipos de grupos
, cada um com funções específicas:
Matéria-prima
: Ingredientes básicos, como bases e excipientes, utilizados na produção de outros produtos.
Semi-acabado
: Produtos já produzidos ou adquiridos, que necessitam apenas de um processo final, como embalagem.
Acabado
: Produtos prontos para venda.
Cápsulas
: Utilizadas para armazenar manipulações em volume.
Embalagem
: Materiais para embalar produtos e cápsulas.
Drogaria
: Produtos adquiridos de fornecedores e prontos para venda (medicamentos industrializados, perfumaria e varejo em geral).
Homeopatia
: Itens específicos para homeopatia e dinamização.
Floral
: Produtos destinados à manipulação floral.
Funcionalidades Extras por Grupo
Pesagem Monitorada
Disponível
apenas para grupos do tipo Matéria-prima
. Quando ativada, essa opção faz com que as ordens de produção que contenham produtos desse grupo passem pelo processo de pesagem monitorada.
Ativar Controle de Lotes
Por padrão, o sistema controla lotes para produtos manipulados, como
Matéria-prima, Semi-acabado, Cápsulas, Embalagem, Homeopatia e Floral
.
Para os grupos
Acabado
e
Drogaria
, essa opção precisa ser ativada manualmente.
Atenção
: caso o grupo já esteja em uso, é necessário zerar o estoque antes de ativar essa configuração.
Como Criar um Novo Grupo de Produtos
1- Acesse o menu
ARQUIVO > ESTOQUE > PRODUTO
.
2 - Clique em 'Incluir'
3 - Preencher a Descrição, que é o nome do grupo, selecionar o TIPO e salvar.

---

## 🔴 Gerar o arquivo da Nota Fiscal Gaucha — 07/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34406
> Publicado em: 07/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para gerar a nota Fiscal Gaúcha realize esse procedimento no computador onde fica conectada a impressora fiscal (ECF) do cliente.
1º - Abra o menu fiscal no Farma Fácil (você pode fazer isso pressionando a tecla F12 em qualquer tela do sistema ou seguindo os passos mostrados na tela a baixo).
2º - Selecione a opção ARQ. MFD
3º ) Marque a opção DATA, selecione o modelo da impressora fiscal do cliente em EQUIPAMENTO, e informe o período do arquivo que o cliente deseja, geralmente é o mês anterior ao atual, e clique no ícone de salvar para o sistema começar o processo de gerar o arquivo. Obs:  Após o termino o sistema ira apresentar uma mensagem com o local aonde o arquivo foi salvo, nem sempre o sistema salva esse arquivo no local informado nessa mensagem.

---

## 🔴 Gerar o arquivo Sintegra — 07/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34397
> Publicado em: 07/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para gerar o arquivo SINTEGRA a partir da tela principal do sistema vá até:
ARQUIVO>UTILITARIO>EXPORTAÇÃO DE ARQUIVOS
e após marque a opção Sintegra
Agora siga a sequência das numerações.
1º)
Selecione SINTEGRA
2º)
Informe o período do arquivo
3º)
Marque todos os registros, menos o R74 que é marcado somente no mês de Fevereiro
4º)
Selecione sistema e a impressora que a farmácia possui
5º)
Clique em EXTRAIR DADOS e aguarde o termino da exportação,
6º)
Selecione a pasta para salvar o arquivo, C:\FARMAFACIL\SINTEGRA, ou caso não exista essa pasta, crie uma pasta ou aponte o caminho para qualquer outra que seja fácil para localizar o arquivo gerado.
7º)
Clique em gerar o arquivo.

---

## 🔴 Cadastro Formula Padrão — 07/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34396
> Publicado em: 07/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

O que é uma Fórmula Padrão?
É o documento que especifica as matérias-primas e os materiais de embalagem com as suas respectivas quantidades, juntamente com a descrição dos procedimentos para a produção de um determinado produto. Além disso, fornece instruções sobre o processamento, inclusive sobre os controles em processo. É uma espécie de receita para a produção de um produto final.
A Fórmula Padrão dentro do FarmaFácil tem como função minimizar o trabalho do farmacêutico, e manter um cadastro com todas as fórmulas de uma maneira organizada.
Tipos de Fórmula Padrão
Existem 3 tipos de Fórmula Padrão no FarmaFácil. Os tipos podem ser B
ase/Excipiente/Semi-Acabado
,
Acabado
ou
Pré-Venda
. Dependendo do tipo escolhido, o sistema irá exigir informações diferentes.
Tipo Base/Excipiente/Semi-Acabado
O tipo Base/Excipiente/Semi-Acabado serve para produções internas, onde o produto final será uma outra matéria-prima (base ou excipiente), que será armazenada em estoque e usada na composição de outras formulações, ou um produto final que será feito em grande quantidade e depois será vendido de forma fracionada (semi-acabados). O produto final desse tipo de Fórmula Padrão deve estar em um grupo dos tipos Matéria-prima ou Semi-acabado.
Tipo Acabado
O tipo Acabado gera um produto pronto para a venda, pois não passará por nenhum outro processo. São produtos como, por exemplo, sabonetes e xampus, na mesma forma como são encontrados em lojas e supermercados, já embalados e prontos para a venda. O produto final desse tipo de Fórmula Padrão deve estar necessariamente cadastrado em um grupo dos tipos Acabado.
Tipo Pré-Venda
Não é exatamente uma fórmula padrão. É uma formula de uma venda que fica cadastrada no sistema, evitando que o atendente tenha que informar os itens e quantidades toda vez que alguém compre essa formulação. Tem por finalidade facilitar o trabalho do atendente. É usada geralmente para formulas que tem bastante saída e possuem vários itens em sua formulação, como compostos emagrecedores e compostos de lactobacilos. Este tipo de Fórmula Padrão não gera um produto final.
Tipo Acabado/Pré-Venda
Esta é uma junção dos dois tipos citados anteriormente, possibilitando o cliente utilizar dois tipos em um único cadastro
Incluindo uma Fórmula Padrão
A inclusão da Fórmula Padrão é feito através do seguinte caminho, a partir da tela inicial do FarmaFácil:
ARQUIVO > PRODUÇÃO > FORMULA PADRÃO
Na tela de Fórmula Padrão é possível fazer a inclusão de uma nova fórmula através da opção
Incluir Nova Fórmula Padrão
ou pressionando a tecla
Insert
no teclado, uma nova tela será exibida.
Ela pode ser dividida em duas partes: a primeira parte corresponde as especificações da Fórmula Padrão, enquanto a segunda parte corresponde aos itens que compõe a Fórmula Padrão.
Campos de Especificações da Fórmula Padrão
A tela de cadastro irá habilitar ou desabilitar alguns campos de acordo com o tipo de Fórmula Padrão.
Descrição
: é o nome da Fórmula Padrão. Por ele o farmacêutico v
[... conteúdo truncado para otimizar contexto ...]

---

## 🔴 Impressão de Etiqueta de Estoque e Preço Drogaria — 06/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34262
> Publicado em: 06/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

É possível imprimir etiqueta de estoque, etiqueta de preço para drogaria.
Para imprimir a etiqueta informa a quantidade de cada item e clique em imprimir
Para imprimir a etiqueta de preço drogaria, informe a quantidade de cada item, e clique em imprimir

---

## 🔴 Exclusão da Nota Fiscal de Entrada — 05/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34224
> Publicado em: 05/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Para excluir uma nota fiscal de entrada, é preciso selecionar ela, e clicar no botão excluir.
só é possível excluir notas em que os produtos não possuírem movimentação posterior a entrada a nota, e que não possuam medicamentos controlados om movimentação enviada a Anvisa.
1 - Selecione a nota que deseja excluir, e clique no ícone excluir
2 - Clique em Sim para confirmar, ou Não para cancelar
3 - Caso algum produto possua movimentação, será exibida a mensagem e a nota não será excluída.
4 - Caso a nota possua produto controlado e tenha sido enviado SNGPC, irá exibir a mensagem, e a nota não será excluída.

---

## 🔴 Nota Fiscal de Entrada - Inclusão Manual — 05/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34199
> Publicado em: 05/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Nota fiscal é realizado a entrada dos produtos no estoque e a atualizado os valores de custo das mercadorias.
É Acessado através do menu
ESTOQUE > MOVIMENTO > NOTA FISCAL ENTRADA
1 - Para incluir manualmente a nota fiscal, clique no ícone 'Incluir' nota fiscal
2 -  Preencher todos os campos do cabeçalho de acordo com os dados da nota.
3 - Para incluir os itens, clicar no ícone 'incluir 'produtos +
4 - Preencha com todas as informações do item na nota fiscal. Caso o produto seja de DROGARIA, clicar na aba DROGARIA antes de informar o produto.
5  - Após preencher clicar em salvar.
6 - Para inserir a duplicata clicar no ícone para 'incluir 'duplicata +
7 - Preencha os dados de acordo com a duplicata e salve.
8 - Após preencher todos os campos, e conferir se está correto, clique em salvar para incluir a nota.
9 - Para cada item, a depender da configuração do parâmetro geral, o sistema irá perguntar se deseja atualizar o custo referência. Sim ou Não.

---

## 🔴 Uso Continuo — 04/12/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/34088
> Publicado em: 04/12/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Na inclusão da formula, ao marcar  o campo ‘
uso continuo
’, o sistema vai calcular de acordo com a dose informada na ‘
posologia
’ quantos dias durará a formula, e exibirá no relatório de ‘
vendas uso continuo
’ na data que termina a dose que foi vendida.
Exemplo:
venda de 30 capsulas, dose de 1 capsula por dia. Realizado no dia 29/11/2018 irá constar no relatório de ‘
vendas
uso continuo’
do dia 29/12/2018.
Marca a Opção de Uso continuo
2 - Seleciona a Posologia Adequada
3 - Após Salvar a Venda, Ela irá constar no relatório

---

## 🔴 Adicionando Exceções ao Firewall do Windows — 22/11/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/33256
> Publicado em: 22/11/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Por que realizar este procedimento?
Configurar corretamente o Firewall do Windows é essencial para garantir o funcionamento adequado de serviços como o PostgreSQL e o Webkey, permitindo a comunicação entre sistemas sem comprometer a segurança da rede.
Quando usar este procedimento?
Acesso Remoto ao Banco de Dados PostgreSQL
Quando um aplicativo ou outro servidor precisa se conectar ao PostgreSQL hospedado na máquina local ou em um servidor remoto.
Se um sistema que usa PostgreSQL não está conseguindo acessar o banco devido a bloqueios no firewall.
Funcionamento do Webkey
Quando o serviço da chave WEB (Webkey) precisa ser acessado remotamente, mas está sendo bloqueado pelo firewall.
Se um sistema que depende do Webkey não está funcionando corretamente devido a restrições de rede.
Servidores em Rede Local ou na Nuvem
Quando um servidor Windows está rodando esses serviços e precisa permitir conexões de outros dispositivos na mesma rede ou via internet.
Erros de Conectividade Relacionados ao Firewall
Se aplicações estão reportando erros de conexão ou "timeout" ao tentar acessar o banco de dados ou o Webkey.
Quando há problemas de comunicação entre sistemas após uma atualização ou mudança de configuração de rede.
Essa configuração pode ser realizada em qualquer versão do Windows, seguindo passos muitos similares.
1 -
Abrir o Painel de Controle – Central de Rede – Firewall do Windows ou executando o comando
firewall.cpl
2 -
Selecione a opção Configurações Avançadas
3 -
Seleciona
Regras de Entrada
em seguida clique em
Nova Regra
no painel direito
São 2 exceções que devem ser adicionadas:
PostgresSQL –
adicionar exceção para a porta
5432
(porta que estiver configurado o postgres a
5432
é a porta padrão)
Webkey
– adicionar exceção para a porta
2502
porta padrão do serviço da chave
WEB
.
Realizar o mesmo procedimento para regras de entrada e regras de saida.(TCP/UDP).

---

## 🔴 Entrada de nota por XML — 09/11/2018

> Fonte: https://prismafive.movidesk.com/kb/pt-br/article/31952
> Publicado em: 09/11/2018
>
> ⚠️ **AVISO PARA O ANALISTA:** Este artigo tem mais de 2 anos.
> As informações podem estar desatualizadas. Confirme com a documentação
> atual ou com a equipe antes de aplicar as instruções.

Nota fiscal é realizado a entrada dos produtos no estoque e a atualizado os valores de custo das mercadorias.
Acessar através do menu
ESTOQUE > MOVIMENTO > NOTA FISCAL ENTRADA
1 - Clique no Botão '
importar NFE entrada
' atalho F6.
2 - Clique em procurar, para abrir a janela de seleção de arquivo.
3 - Selecione o arquivo no seu computador, e clique em abrir.
4- Irá carregar as informações do XML e exibir.
5 - Parte superior é exibido o número da nota, a série, a data de emissão, a data de entrada e o valor.
6 - Abas de navegação, é necessário passar por todas elas para salvar corretamente a nota
7 - O sistema vincula automaticamente o fornecedor pelo CNPJ caso não tenha o fornecedor cadastrado, deve cadastra-lo nesse momento.
- Vincular fornecedor
- Cadastrar fornecedor
- Editar fornecedor
8 - Com o fornecedor cadastrado o sistema irá selecionar o fornecedor e exibir o código. Podendo assim passar para a próxima aba '
produtos
'
9 - Os campos GRUPO e PRODUTO é o produto correspondente no sistema, a descrição o código fornecedor Qtde. Unidade e valor, são do XML da nota.
- Conferir XML (F6)
- Vincular Produto (F3)
- Cadastrar Produto
- Alterar Qtde. Produto(F5)
- Desvincular produto(F4)
- Editar Produto
-  Pesquisa Produto (F2)
10 - Produto da nota vinculado a um produto do sistema
11 - Produto da nota que não está vinculado a um do sistema
12 - É necessário vincular todos os produtos da nota com um produto no sistema. Os produtos em vermelho estão sem um correspondente no sistema
13 - Seleciona o produto:
Pressiona F2 para pesquisar no sistema ele vai listar o produto em baixo.
Seleciona o produto correspondente ao da nota.
Pressiona F3 para vincular.
Muita atenção, é preciso ter certeza que está vinculando ao item certo, do contrário o estoque ficará incorreto.
14 - Dados específicos dos produtos.
Sempre conferir com atenção e completar os campos que estiverem em branco, nem sempre vem preenchidos no XML.
15 - Após vincular todos os itens, seleciona a aba 'Unidade'
16 - Alterar a quantidade XML
17 - Utilizar essa opção para ajustar a quantidade e a unidade do produto do XML. É muito comum que na nota fiscal de compra o produto venha com a quantidade da caixa.
Nesses casos é necessário realizar o ajuste da quantidade e da unidade para a correta que utiliza no estoque
18 - Aba Fatura pagar
19 - Aba Totais
Importar ICMS:
utiliza o valor do ICMS para o cálculo do valor de custo do produto.
Importar ICMS ST:
utiliza o valor do ICMS ST para o cálculo do valor de custo do produto.
Importar IPI:
utiliza o valor do IPI para o cálculo do valor de custo do produto.
Calcular ST:
utiliza o valor do ICMS ST para o cálculo do custo referência do produto.
Importar desconto unitário:
importa o valor de desconto unitário no item.
Incide valor frete:
utiliza o valor do frete para o cálculo do valor de custo do produto.
Incide valor outras despesas:
utiliza o valor do campo outras despesas para o cálculo do valor de custo do produto.
Incide valor de IPI:
utiliza o 
[... conteúdo truncado para otimizar contexto ...]

---

## 🟢 Certificado Digital — Caminho Correto no FarmaFácil

> Fonte: Confirmado por analista Rebeca em 17/04/2026

**Caminho correto para configurar o Certificado Digital:**

Parâmetro (ou Filial, caso tenha filiais) → NFe → Certificado

> ATENÇÃO: o caminho NÃO é Arquivo → Configuração → Certificado como pode parecer. É na tela de Parâmetros / NFe.

---

## 🟢 data.notafiscal — Colunas corretas para UPDATE manual

> Fonte: Chat de suporte 17/04/2026

Ao fazer UPDATE manual na tabela `data.notafiscal`:

- Coluna do protocolo: **`protocolonfe`** (não `protocolo`)
- Tipo: `character varying` — deve ser passado entre aspas simples
- Coluna de situação: **`situacaonfe`** — valores válidos: `'AUTORIZADA'`, `'REJEITADA'`, `'CANCELADA'`, `'A ENVIAR'` (não usar `'CONFIRMADA'`)
- Filtro seguro: usar `numeronotafiscal` + `tiponotafiscal`

Exemplo correto:
```sql
UPDATE data.notafiscal 
SET situacaonfe = 'AUTORIZADA', 
    protocolonfe = '135261434424553'
WHERE numeronotafiscal = 365 
AND tiponotafiscal = 2;
```

---

## 🟢 NFS-e TecnoSpeed — Erro "ItemListaServiço obrigatório"

> Fonte: Chat de suporte 17/04/2026

**Erro:** "Campo ItemListaServiço obrigatório"

**Causa:** O campo "Item Lista Serviço" não está preenchido no cadastro do serviço.

**Solução:**
1. Acesse o cadastro do serviço (Arquivo → Cadastros → Serviço)
2. Preencha o campo "ItemListaServiço" com o código da lista de serviços da prefeitura local
3. O código varia por cidade — consultar site da prefeitura ou secretaria de fazenda
4. Exemplos comuns para farmácias: `0108` (Serviços de farmácia), `0101` (Serviços profissionais)
5. Após preencher, tente emitir a NFS-e novamente

Verificar também: certificado digital não vencido e ausência de caracteres especiais no nome do cliente/serviço.

---

## 🟢 Sachê — Cálculo automático Volume x Qtd (mg)

> Fonte: Chat de suporte 17/04/2026

**Pré-requisitos para cálculo automático de sachê:**

1. No cadastro da embalagem (Arquivo → Estoque → Produto): preencher o campo **VOLUME** (ex: `10ml` ou `10g`) e a **FORMA FARMACÊUTICA**
2. No cadastro da forma farmacêutica (Arquivo → Produção → Forma Farmacêutica): selecionar o tipo de cálculo **"Volume x Qtd (mg)"**

**Fluxo de cálculo:**
- Informar apenas a quantidade de sachês (ex: 30)
- Informar os ativos com dosagens em mg por sachê
- Informar o QSP (base do sachê)
- Sistema soma todos os ingredientes e busca automaticamente a embalagem com o volume adequado

**Atenção:** Se a embalagem sachê não tiver volume preenchido, o sistema não consegue sugerir automaticamente. O campo VOLUME é obrigatório para o cálculo automático funcionar.

Alternativa: tipo "Volume x Qtd (%)" para cálculo percentual manual.

---

## 🟢 Ordem de Produção — Fluxo e Status

> Fonte: Chat de suporte 17/04/2026

**Criação:** Gerada automaticamente ao fazer venda de manipulação, ou criada manualmente em PRODUCAO → ORDENS.

**Status da ordem:**
- **Aberta** — criada, ainda não produzida
- **Em produção** — sendo manipulada no laboratório
- **Concluída** — pronta, estoque de matérias-primas já foi baixado
- **Cancelada** — descartada (libera o estoque comprometido)

**Tabelas relacionadas no banco:**
- `data.venda` — venda principal (cliente, vendedor, data, filial, valores)
- `data.itemvenda` — itens da venda (produtos, quantidades, preços)
- `data.formulavenda` — se for fórmula magistral
- `data.itemformulavenda` — ingredientes da fórmula (campos: `quantidade`, `calculoitem`, `fatorconversaoestoque`)
- `data.caixavenda` / `data.caixavendaformapagamento` — recebimento no caixa

**Problema: ficha de pesagem não exibe volume do ingrediente**
- Verificar `siglaunidadeestoque` no cadastro do produto (deve ser mg, g, ml etc.)
- Verificar `fatorconversaoestoque` em `data.itemformulavenda` (não pode ser 0 ou null)
- Verificar `calculoitem` na fórmula (não pode ser null)
- Verificar `aspectofisicoproduto` no cadastro do produto (pó, líquido etc.)

