#!/usr/bin/env pythonw
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VaultAutomatico(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração da janela
        self.title("🔐 Meu Gerenciador de Senhas")
        self.geometry("1100x650")
        self.minsize(900, 550)
        
        # ⚡ DADOS SALVOS AUTOMATICAMENTE - Substitui o bloco de notas
        self.data_file = "minhas_senhas.json"  # Arquivo FIXO na pasta do programa
        self.entries = []
        self.filtered_entries = []
        self.editando_index = None  # Para controlar se está editando
        
        # Carregar dados automaticamente ao iniciar
        self.carregar_dados_automaticamente()
        
        # Configurar interface
        self.setup_ui()
        
        # Atalhos de teclado
        self.bind_all("<Control-f>", lambda e: self.focus_search())
        
    def carregar_dados_automaticamente(self):
        """Carrega os dados automaticamente ao abrir o programa"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.entries = json.load(f)
                print(f"✅ {len(self.entries)} senhas carregadas automaticamente")
            else:
                # Criar arquivo vazio se não existir
                self.salvar_dados_automaticamente()
                print("📁 Arquivo criado: minhas_senhas.json")
        except Exception as e:
            print(f"❌ Erro ao carregar: {e}")
            self.entries = []
        
        self.filtered_entries = self.entries.copy()
    
    def salvar_dados_automaticamente(self):
        """Salva os dados automaticamente SEMPRE que houver mudança"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)
            print("💾 Dados salvos automaticamente")
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
    
    def setup_ui(self):
        """Configura toda a interface do usuário"""
        # Frame principal
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Header
        self.create_header()
        
        # Barra de pesquisa
        self.create_search_bar()
        
        # Corpo principal
        self.create_main_content()
        
        # Footer
        self.create_footer()
        
        # Atualizar lista inicial
        self.refresh_entries_list()
    
    def create_header(self):
        """Cria o cabeçalho"""
        header_frame = ctk.CTkFrame(self.main_container, height=50)
        header_frame.pack(fill="x", pady=(0, 8))
        header_frame.pack_propagate(False)
        
        # Título
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left", fill="y", padx=8)
        
        ctk.CTkLabel(title_frame, text="🔐 Minhas Senhas", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        
        # Contador
        self.contador_label = ctk.CTkLabel(title_frame, text=f"{len(self.entries)} salvas",
                                          text_color="gray", font=ctk.CTkFont(size=12))
        self.contador_label.pack(side="left", padx=(10, 0))
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=8)
        
        ctk.CTkButton(btn_frame, text="📤 Exportar", 
                     command=self.exportar_backup, width=80, height=28).pack(side="left", padx=3)
        ctk.CTkButton(btn_frame, text="🔄 Recarregar", 
                     command=self.recarregar_dados, width=80, height=28).pack(side="left", padx=3)
    
    def create_search_bar(self):
        """Cria a barra de pesquisa"""
        search_frame = ctk.CTkFrame(self.main_container)
        search_frame.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(search_frame, text="🔍", 
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=(10, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, 
                                       textvariable=self.search_var,
                                       placeholder_text="Buscar site, usuário, email...",
                                       height=32)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=6)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_entries())
    
    def create_main_content(self):
        """Cria o conteúdo principal"""
        content_frame = ctk.CTkFrame(self.main_container)
        content_frame.pack(fill="both", expand=True, pady=5)
        
        # Formulário à esquerda
        self.create_form_panel(content_frame)
        
        # Lista à direita
        self.create_list_panel(content_frame)
    
    def create_form_panel(self, parent):
        """Cria o painel do formulário"""
        form_frame = ctk.CTkFrame(parent, width=300)
        form_frame.pack(side="left", fill="y", padx=(0, 8))
        form_frame.pack_propagate(False)
        
        # Título do formulário (muda entre Adicionar/Editar)
        self.form_title = ctk.CTkLabel(form_frame, text="Adicionar Nova Senha",
                                      font=ctk.CTkFont(size=14, weight="bold"))
        self.form_title.pack(pady=12)
        
        # Campos do formulário
        form_content = ctk.CTkScrollableFrame(form_frame)
        form_content.pack(fill="both", expand=True, padx=8, pady=5)
        
        # Variáveis do formulário
        self.site_var = tk.StringVar()
        self.user_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.pass_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        
        # Campos
        fields = [
            ("🌐 Site/App", self.site_var),
            ("👤 Usuário", self.user_var),
            ("📧 Email", self.email_var),
            ("🔒 Senha", self.pass_var),
            ("📝 Descrição (opcional)", self.desc_var)
        ]
        
        for label, var in fields:
            ctk.CTkLabel(form_content, text=label, 
                        font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(10, 3))
            
            if label == "🔒 Senha":
                pass_frame = ctk.CTkFrame(form_content, fg_color="transparent")
                pass_frame.pack(fill="x", pady=(0, 8))
                
                entry = ctk.CTkEntry(pass_frame, textvariable=var, show="•", height=32)
                entry.pack(side="left", fill="x", expand=True)
                
                ctk.CTkButton(pass_frame, text="👁", width=35, height=32,
                             command=lambda e=entry: self.toggle_password_visibility(e)).pack(side="left", padx=(3, 0))
            else:
                entry = ctk.CTkEntry(form_content, textvariable=var, height=32)
                entry.pack(fill="x", pady=(0, 8))
        
        # Botão de salvar/atualizar
        btn_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        
        self.salvar_btn = ctk.CTkButton(btn_frame, text="💾 SALVAR SENHA", height=36,
                                       command=self.adicionar_ou_editar_senha,
                                       fg_color="green", hover_color="dark green",
                                       font=ctk.CTkFont(weight="bold"))
        self.salvar_btn.pack(fill="x", pady=2)
        
        ctk.CTkButton(btn_frame, text="🔄 Limpar Campos", height=32,
                     command=self.limpar_formulario).pack(fill="x", pady=2)
        
        # Botão cancelar edição (inicialmente escondido)
        self.cancelar_btn = ctk.CTkButton(btn_frame, text="❌ Cancelar Edição", height=32,
                                        command=self.cancelar_edicao,
                                        fg_color="gray", hover_color="dark gray")
        # Inicialmente escondido
    
    def create_list_panel(self, parent):
        """Cria o painel da lista de senhas"""
        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(side="left", fill="both", expand=True)
        
        # Título da lista
        ctk.CTkLabel(list_frame, text="Todas as Minhas Senhas",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=12)
        
        # Lista scrollable
        self.list_container = ctk.CTkScrollableFrame(list_frame)
        self.list_container.pack(fill="both", expand=True, padx=8, pady=8)
    
    def create_footer(self):
        """Cria o rodapé"""
        footer_frame = ctk.CTkFrame(self.main_container, height=25)
        footer_frame.pack(fill="x", pady=(8, 0))
        footer_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(footer_frame, 
                                        text=f"🔒 {len(self.entries)} senhas salvas automaticamente • Seus dados estão seguros",
                                        font=ctk.CTkFont(size=11))
        self.status_label.pack(side="left", padx=8)
    
    # ⚡ MÉTODOS PRINCIPAIS - SALVAMENTO AUTOMÁTICO
    
    def adicionar_ou_editar_senha(self):
        """Adiciona nova senha ou atualiza uma existente"""
        site = self.site_var.get().strip()
        usuario = self.user_var.get().strip()
        email = self.email_var.get().strip()
        senha = self.pass_var.get().strip()
        descricao = self.desc_var.get().strip()
        
        # Validação
        if not site:
            self.mostrar_status("⚠️ Digite o site/app", 3000)
            return
        
        if not senha:
            self.mostrar_status("⚠️ Digite a senha", 3000)
            return
        
        if self.editando_index is not None:
            # 🔄 MODO EDIÇÃO - Atualizar entrada existente
            entrada_editada = {
                "site": site,
                "usuario": usuario,
                "email": email,
                "senha": senha,
                "descricao": descricao,
                "mostrar_senha": False,
                "data_criacao": self.entries[self.editando_index]["data_criacao"],
                "data_edicao": self.obter_data_atual()
            }
            
            # Substituir a entrada original
            self.entries[self.editando_index] = entrada_editada
            
            # 🔥 SALVAR AUTOMATICAMENTE
            self.salvar_dados_automaticamente()
            
            # Limpar e atualizar
            self.limpar_formulario()
            self.sair_modo_edicao()
            self.filter_entries()
            
            self.mostrar_status(f"✏️ '{site}' atualizado com sucesso!", 3000)
            
        else:
            # ➕ MODO ADIÇÃO - Criar nova entrada
            nova_entrada = {
                "site": site,
                "usuario": usuario,
                "email": email,
                "senha": senha,
                "descricao": descricao,
                "mostrar_senha": False,
                "data_criacao": self.obter_data_atual()
            }
            
            # Adicionar no início da lista
            self.entries.insert(0, nova_entrada)
            
            # 🔥 SALVAR AUTOMATICAMENTE
            self.salvar_dados_automaticamente()
            
            # Limpar e atualizar
            self.limpar_formulario()
            self.filter_entries()
            
            self.mostrar_status(f"✅ '{site}' salvo automaticamente!", 3000)
        
        self.atualizar_contador()
    
    def entrar_modo_edicao(self, index):
        """Preenche o formulário com dados para edição"""
        entrada = self.filtered_entries[index]
        
        # Encontrar índice na lista principal
        self.editando_index = self.entries.index(entrada)
        
        # Preencher formulário
        self.site_var.set(entrada.get("site", ""))
        self.user_var.set(entrada.get("usuario", ""))
        self.email_var.set(entrada.get("email", ""))
        self.pass_var.set(entrada.get("senha", ""))
        self.desc_var.set(entrada.get("descricao", ""))
        
        # Atualizar interface para modo edição
        self.form_title.configure(text="✏️ Editar Senha")
        self.salvar_btn.configure(text="💾 ATUALIZAR SENHA", fg_color="#e67e22", hover_color="#d35400")
        self.cancelar_btn.pack(fill="x", pady=2)  # Mostrar botão cancelar
        
        self.mostrar_status("✏️ Editando entrada - altere os campos e clique em ATUALIZAR", 3000)
    
    def sair_modo_edicao(self):
        """Sai do modo de edição e volta ao modo normal"""
        self.editando_index = None
        self.form_title.configure(text="Adicionar Nova Senha")
        self.salvar_btn.configure(text="💾 SALVAR SENHA", fg_color="green", hover_color="dark green")
        self.cancelar_btn.pack_forget()  # Esconder botão cancelar
    
    def cancelar_edicao(self):
        """Cancela a edição atual"""
        self.limpar_formulario()
        self.sair_modo_edicao()
        self.mostrar_status("Edição cancelada", 2000)
    
    def limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.site_var.set("")
        self.user_var.set("")
        self.email_var.set("")
        self.pass_var.set("")
        self.desc_var.set("")
    
    def filter_entries(self):
        """Filtra as entradas"""
        termo = self.search_var.get().lower()
        if not termo:
            self.filtered_entries = self.entries.copy()
        else:
            self.filtered_entries = [
                e for e in self.entries 
                if (termo in e.get("site", "").lower() or
                    termo in e.get("usuario", "").lower() or
                    termo in e.get("email", "").lower() or
                    termo in e.get("descricao", "").lower())
            ]
        self.refresh_entries_list()
    
    def refresh_entries_list(self):
        """Atualiza a lista na tela"""
        # Limpar lista atual
        for widget in self.list_container.winfo_children():
            widget.destroy()
        
        if not self.filtered_entries:
            ctk.CTkLabel(self.list_container, 
                        text="Nenhuma senha encontrada\nAdicione sua primeira senha usando o formulário 👈",
                        text_color="gray", font=ctk.CTkFont(size=12)).pack(expand=True, pady=40)
            return
        
        # Mostrar cada entrada
        for i, entrada in enumerate(self.filtered_entries):
            self.criar_card_senha(i, entrada)
    
    def criar_card_senha(self, index, entrada):
        """Cria um card para cada senha"""
        card = ctk.CTkFrame(self.list_container, corner_radius=10, height=160)
        card.pack(fill="x", pady=3, padx=2)
        card.pack_propagate(False)
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=8)
        
        # Linha superior: Site e botões
        top_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 8))
        
        # Site
        site_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        site_frame.pack(side="left", fill="x", expand=True)
        
        site_text = entrada.get("site", "Sem nome")
        ctk.CTkLabel(site_frame, text=site_text,
                    font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        
        # Data de criação/edição (se disponível)
        if entrada.get("data_edicao"):
            data_info = f"Editado: {entrada['data_edicao']}"
        else:
            data_info = f"Criado: {entrada.get('data_criacao', '')}"
        
        ctk.CTkLabel(site_frame, text=data_info, 
                    text_color="gray", font=ctk.CTkFont(size=10)).pack(side="left", padx=(10, 0))
        
        # Botões de ação
        action_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        action_frame.pack(side="right")
        
        # Botão Editar
        ctk.CTkButton(action_frame, text="✏️ Editar", width=70, height=28,
                     command=lambda idx=index: self.entrar_modo_edicao(idx),
                     fg_color="#e67e22", hover_color="#d35400").pack(side="left", padx=2)
        
        # Botão Mostrar/Ocultar Senha
        texto_botao = "👁 Mostrar" if not entrada.get("mostrar_senha") else "👁 Ocultar"
        ctk.CTkButton(action_frame, text=texto_botao, width=80, height=28,
                     command=lambda idx=index: self.alternar_visibilidade_senha(idx)).pack(side="left", padx=2)
        
        # Botão Excluir
        ctk.CTkButton(action_frame, text="🗑 Excluir", width=60, height=28,
                     command=lambda idx=index: self.excluir_senha(idx),
                     fg_color="#c44", hover_color="#a33").pack(side="left", padx=2)
        
        # Detalhes - COM BOTÕES PERFEITAMENTE ALINHADOS E MESMO TAMANHO
        details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_frame.pack(fill="x")
        
        # LARGURA PADRÃO PARA TODOS OS BOTÕES DE COPIAR
        BOTAO_COPIAR_LARGURA = 110
        BOTAO_COPIAR_ALTURA = 28
        
        # Usuário com botão copiar alinhado
        if entrada.get("usuario"):
            user_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            user_frame.pack(fill="x", pady=2)
            user_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(user_frame, text="👤", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w", padx=(0, 5))
            ctk.CTkLabel(user_frame, text=entrada["usuario"], 
                        font=ctk.CTkFont(size=12)).grid(row=0, column=1, sticky="w", padx=(0, 10))
            
            # BOTÃO COM MESMA LARGURA
            ctk.CTkButton(user_frame, text="📋 Copiar Usuário", 
                         width=BOTAO_COPIAR_LARGURA, height=BOTAO_COPIAR_ALTURA,
                         command=lambda: self.copiar_texto(entrada["usuario"], "Usuário")).grid(row=0, column=2, sticky="e")
        
        # Email com botão copiar alinhado
        if entrada.get("email"):
            email_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            email_frame.pack(fill="x", pady=2)
            email_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(email_frame, text="📧", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w", padx=(0, 5))
            ctk.CTkLabel(email_frame, text=entrada["email"], 
                        font=ctk.CTkFont(size=12)).grid(row=0, column=1, sticky="w", padx=(0, 10))
            
            # BOTÃO COM MESMA LARGURA
            ctk.CTkButton(email_frame, text="📋 Copiar Email", 
                         width=BOTAO_COPIAR_LARGURA, height=BOTAO_COPIAR_ALTURA,
                         command=lambda: self.copiar_texto(entrada["email"], "Email")).grid(row=0, column=2, sticky="e")
        
        # Senha com botão copiar alinhado
        senha_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
        senha_frame.pack(fill="x", pady=2)
        senha_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(senha_frame, text="🔒", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        senha_display = entrada["senha"] if entrada.get("mostrar_senha") else "•" * 12
        ctk.CTkLabel(senha_frame, text=senha_display, 
                    font=ctk.CTkFont(size=12)).grid(row=0, column=1, sticky="w", padx=(0, 10))
        
        # BOTÃO COM MESMA LARGURA
        ctk.CTkButton(senha_frame, text="📋 Copiar Senha", 
                     width=BOTAO_COPIAR_LARGURA, height=BOTAO_COPIAR_ALTURA,
                     command=lambda: self.copiar_senha(entrada["senha"])).grid(row=0, column=2, sticky="e")
        
        # Descrição
        if entrada.get("descricao"):
            desc_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            desc_frame.pack(fill="x", pady=2)
            ctk.CTkLabel(desc_frame, text="📝", font=ctk.CTkFont(size=11)).pack(side="left")
            ctk.CTkLabel(desc_frame, text=entrada["descricao"], 
                        text_color="gray", font=ctk.CTkFont(size=11)).pack(side="left", padx=5)
    
    def alternar_visibilidade_senha(self, index):
        """Mostra ou oculta a senha"""
        entrada = self.filtered_entries[index]
        entrada["mostrar_senha"] = not entrada.get("mostrar_senha", False)
        
        # Atualizar na lista principal também
        original_index = self.entries.index(entrada)
        self.entries[original_index]["mostrar_senha"] = entrada["mostrar_senha"]
        
        # 🔥 SALVAR AUTOMATICAMENTE quando alterar visibilidade
        self.salvar_dados_automaticamente()
        
        self.refresh_entries_list()
    
    def excluir_senha(self, index):
        """Exclui uma senha"""
        entrada = self.filtered_entries[index]
        site = entrada.get("site", "Sem nome")
        
        if messagebox.askyesno("Confirmar Exclusão", 
                             f"Tem certeza que deseja excluir a senha de:\n\n{site}?"):
            # Remover da lista principal
            original_index = self.entries.index(entrada)
            self.entries.pop(original_index)
            
            # Se estava editando esta entrada, cancelar edição
            if self.editando_index == original_index:
                self.cancelar_edicao()
            
            # 🔥 SALVAR AUTOMATICAMENTE após exclusão
            self.salvar_dados_automaticamente()
            
            self.filter_entries()
            self.atualizar_contador()
            self.mostrar_status(f"🗑 '{site}' excluído", 3000)
    
    def copiar_senha(self, senha):
        """Copia a senha para área de transferência"""
        self.clipboard_clear()
        self.clipboard_append(senha)
        self.mostrar_status("🔒 Senha copiada!", 1500)
    
    def copiar_texto(self, texto, tipo):
        """Copia qualquer texto para área de transferência"""
        self.clipboard_clear()
        self.clipboard_append(texto)
        self.mostrar_status(f"📋 {tipo} copiado!", 1500)
    
    def toggle_password_visibility(self, entry):
        """Alterna visibilidade no campo de formulário"""
        current_show = entry.cget("show")
        entry.configure(show="" if current_show == "•" else "•")
    
    def focus_search(self):
        """Foca na barra de pesquisa"""
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)
    
    def mostrar_status(self, mensagem, duracao=3000):
        """Mostra mensagem de status"""
        self.status_label.configure(text=mensagem)
        if duracao > 0:
            self.after(duracao, lambda: self.status_label.configure(
                text=f"🔒 {len(self.entries)} senhas salvas automaticamente • Seus dados estão seguros"))
    
    def atualizar_contador(self):
        """Atualiza o contador no header"""
        self.contador_label.configure(text=f"{len(self.entries)} salvas")
    
    def exportar_backup(self):
        """Exporta backup dos dados"""
        path = filedialog.asksaveasfilename(
            title="Exportar Backup",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(self.entries, f, ensure_ascii=False, indent=2)
                self.mostrar_status("📤 Backup exportado com sucesso!", 3000)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
    
    def recarregar_dados(self):
        """Recarrega os dados do arquivo"""
        self.carregar_dados_automaticamente()
        self.filter_entries()
        self.atualizar_contador()
        self.mostrar_status("🔄 Dados recarregados!", 2000)
    
    def obter_data_atual(self):
        """Retorna data atual formatada"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def on_closing(self):
        """Executado ao fechar o programa"""
        # Salva uma última vez antes de fechar
        self.salvar_dados_automaticamente()
        self.destroy()

if __name__ == "__main__":
    app = VaultAutomatico()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()