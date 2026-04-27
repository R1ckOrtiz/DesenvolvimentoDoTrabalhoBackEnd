# Checklist Definitivo do Trabalho de Back-end

Este arquivo transforma o roteiro em uma lista de execucao objetiva.
Use como guia de producao, revisao e validacao final.

## Regra zero

- Use este arquivo apenas para organizacao do trabalho, estudo, revisao e controle de qualidade.

## Objetivo real do trabalho

Entregar uma API de back-end que:

- rode localmente sem depender de ajustes escondidos;
- tenha persistencia real em banco;
- feche pelo menos 1 fluxo critico ponta a ponta;
- demonstre autenticacao, autorizacao, regras de negocio e padrao de erro;
- esteja coerente com DER, diagramas, README, Swagger e colecao Postman/Insomnia;
- possa ser validada rapidamente pelo corretor.

## Nome do projeto

Nome recomendado para apresentar o sistema:

- `API Raizes do Nordeste`

Padrao recomendado de nomes tecnicos:

- Repositorio: `raizes-do-nordeste-api`
- Projeto da aplicacao: `api-raizes-do-nordeste`
- Titulo no Swagger: `API Raizes do Nordeste`

Nome obrigatorio do PDF final, conforme o roteiro:

- `SEU_RU_Projeto_Back_End.pdf`

Exemplo:

- `4999657_Projeto_Back_End.pdf`

## Como maximizar a nota

Para buscar a faixa mais alta, a entrega precisa ficar forte em 6 blocos:

1. Analise e requisitos: entendimento claro do caso, RF/RNF coerentes, multicanalidade, LGPD, pagamento mock e justificativa do que foi implementado vs. planejado.
2. Modelagem e arquitetura: casos de uso, DER, classes e arquitetura em camadas conectados ao fluxo entregue.
3. Implementacao: API executavel, Swagger real, banco com migrations, fluxo critico completo, `canalPedido`, validacoes e erro padrao.
4. Seguranca e LGPD: hash de senha, token, roles, minimizacao de dados e logs ou auditoria de acoes sensiveis.
5. Testes: minimo de 10 cenarios, com positivos e negativos, todos reproduziveis.
6. Entrega tecnica: PDF organizado, README forte, links publicos funcionando e repositorio limpo.

## Escopo recomendado

### Fluxo recomendado

- Escolher o Fluxo A: `pedido -> pagamento mock -> atualizacao de status`.

Motivo:

- cobre melhor a essencia do estudo de caso;
- facilita demonstrar integracao, regras, status, multicanalidade e validacoes;
- atende melhor os criterios de implementacao.

### O que precisa ser implementado de verdade

- Autenticacao com token
- Pelo menos 1 regra de autorizacao por perfil
- Unidades
- Produtos ou cardapio por unidade
- Criacao de pedido com itens
- Registro de `canalPedido`
- Validacao de disponibilidade basica
- Pagamento mock com sucesso e falha
- Atualizacao de status do pedido
- Persistencia em banco
- Swagger
- README
- Colecao Postman/Insomnia

### O que pode ficar como proposta documentada

- Fidelizacao completa
- Promocoes completas
- Relatorios avancados
- Anonimizacao automatica
- Escalabilidade avancada

Regra:

- tudo que nao for implementado deve aparecer no documento como "proposto" ou "futuro", com justificativa tecnica.

## Checklist de implementacao obrigatoria

### 1. Autenticacao e autorizacao

- [ ] Existe login funcional
- [ ] Senha armazenada com hash
- [ ] A API retorna token
- [ ] Ha pelo menos 1 endpoint protegido por token
- [ ] Ha pelo menos 1 regra de role/perfil
- [ ] Acesso sem token retorna `401`
- [ ] Acesso sem permissao retorna `403`

### 2. Multicanalidade

- [ ] O pedido possui campo `canalPedido`
- [ ] O campo e obrigatorio na criacao do pedido
- [ ] Os valores aceitos estao documentados
- [ ] A API permite filtrar pedidos por `canalPedido`
- [ ] O documento explica por que o canal e um dado de dominio

Valores minimos esperados:

- `APP`
- `TOTEM`
- `BALCAO`
- `PICKUP`
- `WEB`

### 3. Pedido

- [ ] Existe endpoint para criar pedido
- [ ] O pedido aceita itens
- [ ] O pedido calcula ou registra valor total
- [ ] O pedido valida itens invalidos
- [ ] O pedido valida produto ou unidade inexistente
- [ ] O pedido trata estoque indisponivel ou regra equivalente
- [ ] O pedido possui status documentados
- [ ] O pedido pode ser consultado depois da criacao

### 4. Pagamento mock

- [ ] Existe simulacao de pagamento desacoplada do pedido
- [ ] O pagamento mock registra sucesso
- [ ] O pagamento mock registra falha
- [ ] O retorno do mock fica persistido
- [ ] O pedido muda de status apos o pagamento
- [ ] O documento explica que nao ha gateway real, apenas fluxo simulado

### 5. Status e regras de negocio

- [ ] O fluxo de status esta definido e documentado
- [ ] Transicoes invalidas sao tratadas
- [ ] Cancelamento segue regra coerente
- [ ] Erros de negocio retornam codigo coerente

### 6. Persistencia

- [ ] Banco real configurado
- [ ] Entities/tabelas coerentes com o DER
- [ ] Migrations existem e funcionam
- [ ] Seed existe se for necessario facilitar teste
- [ ] Nada critico depende apenas de memoria

### 7. Swagger/OpenAPI

- [ ] Swagger abre localmente
- [ ] Os endpoints exibidos sao os reais
- [ ] Cada endpoint importante tem request e response
- [ ] Codigos de status aparecem na documentacao
- [ ] Endpoints protegidos indicam autenticacao

### 8. Padrao de qualidade da API

- [ ] URLs no plural
- [ ] IDs no path
- [ ] Query params para filtros e paginacao quando fizer sentido
- [ ] Validacao de entrada consistente
- [ ] Status codes coerentes
- [ ] Erro padronizado em JSON

Codigos esperados no minimo:

- `200` para leitura ou sucesso comum
- `201` para criacao
- `204` para operacao sem corpo
- `400` ou `422` para validacao
- `401` para nao autenticado
- `403` para sem permissao
- `404` para nao encontrado
- `409` para conflito ou regra de negocio

## Padrao de erro minimo

Defina 1 formato unico e use em toda a API.

O formato precisa ter, no minimo:

- identificacao do erro;
- mensagem legivel;
- status code;
- detalhes de validacao quando aplicavel.

Regra:

- nao misturar formatos diferentes entre endpoints.

## Modelagem minima esperada

### Entidades candidatas para o fluxo recomendado

- [ ] Usuario
- [ ] Role ou Perfil
- [ ] Unidade
- [ ] Produto
- [ ] CardapioUnidade ou relacao equivalente
- [ ] Estoque
- [ ] Pedido
- [ ] ItemPedido
- [ ] Pagamento
- [ ] ConsentimentoLGPD ou campo equivalente
- [ ] AuditoriaLog ou tabela equivalente

### No DER precisa aparecer

- [ ] PK e FK
- [ ] Cardinalidades
- [ ] Restricoes relevantes
- [ ] Relacao entre unidade e estoque
- [ ] Relacao entre pedido e itens
- [ ] Relacao entre pedido e pagamento
- [ ] Compatibilidade com o que esta implementado

### Na arquitetura precisa ficar claro

- [ ] Camada de dominio
- [ ] Camada de aplicacao
- [ ] Camada de infraestrutura
- [ ] Camada de API
- [ ] Separacao de responsabilidades

## Seguranca, LGPD e auditoria

### Minimo obrigatorio

- [ ] Senha com hash
- [ ] Token de autenticacao
- [ ] Roles ou perfis
- [ ] Respostas sem expor senha ou dado sensivel
- [ ] Finalidade dos dados explicada no documento
- [ ] Minimizacao de dados aplicada
- [ ] Consentimento mencionado no contexto de fidelizacao, quando usado
- [ ] Registro de pelo menos 1 acao sensivel

### Acoes sensiveis boas para auditar

- [ ] Criacao de pedido
- [ ] Cancelamento de pedido
- [ ] Mudanca de status
- [ ] Resultado de pagamento mock

Se auditoria nao for implementada:

- [ ] declarar explicitamente no documento que nao foi implementada;
- [ ] justificar a priorizacao;
- [ ] aceitar que isso reduz nota, mas evita incoerencia.

## Endpoints minimos recomendados

Use este bloco como referencia de cobertura minima, nao como resposta final obrigatoria.

- [ ] `POST /auth/login`
- [ ] `GET /unidades`
- [ ] `GET /unidades/{id}/cardapio` ou rota equivalente
- [ ] `POST /pedidos`
- [ ] `GET /pedidos/{id}`
- [ ] `GET /pedidos?canalPedido=APP`
- [ ] `PATCH /pedidos/{id}/status` ou equivalente
- [ ] `POST /pagamentos/mock` ou rota equivalente ao fluxo escolhido

Boa pratica:

- prefira poucos endpoints bem fechados a muitos endpoints incompletos.

## Plano de testes obrigatorio

Precisa haver no minimo 10 cenarios:

- [ ] 6 positivos
- [ ] 4 negativos

Cada cenario precisa ter:

- [ ] ID do teste
- [ ] endpoint e metodo
- [ ] pre-condicao
- [ ] entrada
- [ ] saida esperada
- [ ] status code esperado
- [ ] trecho relevante da resposta
- [ ] referencia da evidencia na colecao

### Cobertura minima que precisa aparecer

- [ ] Login valido
- [ ] Acesso sem token
- [ ] Acesso com perfil sem permissao
- [ ] Campo obrigatorio ausente
- [ ] Formato ou dado invalido
- [ ] Pedido valido criado com sucesso
- [ ] Produto ou unidade inexistente
- [ ] Estoque insuficiente ou regra equivalente
- [ ] Pagamento mock aprovado
- [ ] Pagamento mock recusado

## README obrigatorio

O README precisa permitir que outra pessoa rode tudo sem adivinhacao.

- [ ] Tecnologias e versoes
- [ ] Requisitos para rodar
- [ ] Como configurar `.env`
- [ ] Arquivo `.env.example`
- [ ] Como instalar dependencias
- [ ] Como criar banco
- [ ] Como rodar migrations
- [ ] Como rodar seed
- [ ] Como iniciar a API
- [ ] URL e rota do Swagger
- [ ] Como executar a colecao de testes
- [ ] Ordem sugerida de chamadas, se necessario

## Colecao Postman/Insomnia

- [ ] Arquivo `.json` no repositorio
- [ ] Requisicoes organizadas por pasta
- [ ] Pasta de autenticacao
- [ ] Pasta do fluxo principal
- [ ] Pasta de cenarios de erro
- [ ] Variaveis de ambiente explicadas
- [ ] Nomes das requisicoes claros

## PDF final

O PDF academico precisa conter:

- [ ] capa
- [ ] sumario
- [ ] introducao e objetivos
- [ ] analise e requisitos
- [ ] diagramas
- [ ] arquitetura
- [ ] endpoints da API
- [ ] LGPD, privacidade e seguranca
- [ ] entrega tecnica
- [ ] plano de testes
- [ ] conclusao
- [ ] referencias, se usadas

### Regras do texto

- [ ] explicar o que foi implementado
- [ ] explicar o que ficou como proposta
- [ ] justificar prioridades
- [ ] conectar DER, classes, casos de uso e endpoints
- [ ] mostrar como o pagamento mock foi tratado
- [ ] mostrar validacoes e erros padronizados
- [ ] mostrar cuidados com seguranca e LGPD
- [ ] mostrar como os testes evidenciam o funcionamento

## Historico de commits

- [ ] Repositorio publico
- [ ] Historico com evolucao do trabalho
- [ ] Minimo recomendado de 5 commits
- [ ] Commits com mensagens claras

## Riscos que derrubam nota

- [ ] Link quebrado
- [ ] README incompleto
- [ ] Swagger nao abre
- [ ] Colecao nao executa
- [ ] API nao fecha o fluxo minimo
- [ ] Falta de persistencia real
- [ ] `canalPedido` ausente
- [ ] Sem autenticacao
- [ ] Sem regra de autorizacao
- [ ] Diagramas desconectados do codigo
- [ ] Entrega com coisas citadas, mas nao implementadas nem justificadas

## Risco critico de nota zero no criterio de entrega tecnica

Se o corretor nao conseguir acessar ou validar:

- [ ] repositorio publico;
- [ ] Swagger;
- [ ] colecao Postman/Insomnia.

## Ordem de execucao recomendada

1. Definir stack, banco e escopo exato do MVP.
2. Modelar entidades e fazer o DER.
3. Montar arquitetura em camadas.
4. Implementar autenticacao e autorizacao.
5. Implementar unidades, produtos e base do pedido.
6. Implementar `canalPedido` e filtros.
7. Implementar pagamento mock e mudanca de status.
8. Padronizar validacoes e erros.
9. Gerar Swagger coerente com a API real.
10. Criar seed e preparar dados de teste.
11. Montar colecao Postman/Insomnia com os 10 cenarios.
12. Escrever README.
13. Escrever o PDF final.
14. Validar links, execucao e reproduzibilidade do zero.

## Definicao de pronto

O trabalho so esta pronto quando todas estas respostas forem "sim":

- [ ] A API sobe em ambiente limpo seguindo apenas o README.
- [ ] O banco e criado e populado sem gambiarras.
- [ ] O fluxo critico fecha do inicio ao fim.
- [ ] O Swagger mostra os endpoints reais.
- [ ] A colecao executa os cenarios principais e os de erro.
- [ ] O DER bate com o banco e com o codigo.
- [ ] O PDF descreve exatamente o que foi entregue.
- [ ] Nao ha links quebrados.
- [ ] Nao ha parte importante dependendo de explicacao oral.

## Regra de ouro para nao errar

- entregue menos coisas, mas entregue tudo coerente, executavel e testavel;
- nao invente modulo extra se o fluxo principal ainda nao estiver fechado;
- o corretor precisa entender, rodar e validar rapido;
- consistencia vale mais do que quantidade.
