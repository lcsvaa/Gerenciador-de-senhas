# 🔐 Vault Moderno - Gerenciador de Senhas

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)
![Offline](https://img.shields.io/badge/🔒-Offline%20Only-purple)

Um gerenciador de senhas moderno, seguro e offline com interface intuitiva. Salva automaticamente seus dados localmente e permite gerenciar todas suas credenciais em um só lugar.

## ✨ Características

- 🎨 **Interface moderna** com tema escuro
- 💾 **Salvamento automático** - nunca perca dados
- ✏️ **Edição completa** de todas as informações
- 🔍 **Busca rápida** em tempo real
- 👁 **Mostrar/ocultar senhas** com um clique
- 📋 **Copiar** usuário, email ou senha individualmente
- 🛡️ **100% offline** - dados apenas no seu computador
- 📤 **Exportação** de backup em JSON
- ⚡ **Atalhos de teclado** para produtividade

## 🚀 Como Usar

### Método 1 - Executável (Recomendado)
1. Baixe o `Meu Gerenciador de Senhas.exe`
2. Execute com duplo clique
3. Pronto! Dados salvos automaticamente

### Método 2 - Código Fonte
```bash
# Instalar dependências
pip install customtkinter pillow

# Executar programa
python gerenciador_senhas.py
📋 Requisitos
Python: 3.8 ou superior

Sistema: Windows 10/11

Dependências: customtkinter, pillow

🎯 Funcionalidades
🔐 Gerenciamento Completo de Senhas
➕ Adicionar novas entradas (site, usuário, email, senha)

✏️ Editar qualquer informação existente

👀 Visualizar senhas em cards organizados

🔍 Buscar/filtrar em tempo real

🗑️ Excluir com confirmação de segurança

🛡️ Segurança e Privacidade
🔒 Senhas ocultas por padrão (••••••••)

👁️ Mostrar/ocultar senha individualmente

📋 Cópia segura para área de transferência

💾 Dados locais salvos em JSON

🌐 Zero conexão com internet

💾 Sistema de Arquivos
⚡ Salvamento automático em minhas_senhas.json

📤 Exportação de backup opcional

🔄 Recuperação automática da sessão anterior

📅 Timestamps de criação e edição

⌨️ Atalhos de Teclado
Atalho	Ação
Ctrl + F	Focar na barra de busca
🎮 Como Usar a Edição
Clique em "✏️ Editar" em qualquer entrada da lista

Os dados aparecem no formulário à esquerda

Altere site, usuário, email, senha ou descrição

Clique em "💾 ATUALIZAR SENHA" para salvar mudanças

Ou "❌ Cancelar Edição" para desistir das alterações

📁 Estrutura do Projeto
text
MeuGerenciadorSenhas/
├── gerenciador_senhas.py      # Aplicação principal
├── Abrir Programa.vbs         # Launcher sem terminal
├── requirements.txt           # Dependências
└── minhas_senhas.json        # Dados (criado automaticamente)
🐛 Solução de Problemas
Programa não abre
bash
# Verificar Python
python --version

# Instalar dependências
pip install customtkinter pillow
Erro de módulo
bash
pip install customtkinter pillow
Interface não carrega
Use Python 3.8+

Verifique dependências instaladas

💾 Formato dos Dados
json
[
  {
    "site": "google.com",
    "usuario": "meu.email@gmail.com",
    "email": "meu.email@gmail.com", 
    "senha": "minha_senha_secreta",
    "descricao": "Conta principal",
    "mostrar_senha": false,
    "data_criacao": "15/01/2024 14:30",
    "data_edicao": "20/01/2024 10:15"
  }
]
🔧 Desenvolvimento
bash
# Executar em desenvolvimento
python gerenciador_senhas.py
O arquivo minhas_senhas.json é criado automaticamente na primeira execução.

✨ Agora você tem um gerenciador de senhas completo e automático!


