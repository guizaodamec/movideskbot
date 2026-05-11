# Instalação da Extensão — FarmaFacil Assistente

## Chrome ou Edge

1. Abra `chrome://extensions` (ou `edge://extensions`)
2. Ative o **Modo do desenvolvedor** (canto superior direito)
3. Clique em **Carregar sem compactação**
4. Selecione esta pasta (`extensao/`)
5. A extensão aparece na barra com o ícone ⚕

## Primeiro uso

1. Clique no ícone ⚕ na barra de extensões
2. Faça login com seu usuário e senha do FarmaFacil Assistente
3. Abra qualquer chamado em `prismafive.movidesk.com`
4. Clique no botão azul ⚕ que aparece na borda direita da tela

## O que aparece no painel

- **Status e analista** do chamado atual
- **Versão do cliente** no Avalon — com indicador de quantas versões está atrasado
- **Últimos 5 chamados** do mesmo cliente (do cache local)
- **Bugs abertos no Jira** que podem ser relevantes

## Servidor

O assistente precisa estar rodando em `192.168.0.118:5000`.
Se o IP mudar, edite `background.js` linha 1: `const SERVER = 'http://...'`
