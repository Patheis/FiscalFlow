import logging
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
import mysql.connector
from mysql.connector import Error
import hashlib

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,  # Define o nível de log (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",  # Salva os logs em um arquivo chamado 'app.log'
    filemode="a"         # Modo de escrita, "a" para append
)

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.add_background_image()
        self.create_login_frame()

    def setup_window(self):
        """Configura as propriedades da janela principal."""
        self.root.title("FiscalFLOW")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Centraliza a janela na tela
        window_width, window_height = 800, 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    def add_background_image(self):
        """Adiciona uma imagem de fundo com efeito de blur."""
        try:
            bg_image = Image.open("C:/Users/User/Desktop/FISCALFLOW/img/background.jpg")
            bg_image = bg_image.filter(ImageFilter.GaussianBlur(10))
            bg_photo = ImageTk.PhotoImage(bg_image)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Imagem de fundo não encontrada!")
            logging.error("Imagem de fundo não encontrada.")
            return
        
        bg_label = tk.Label(self.root, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_login_frame(self):
        """Cria o frame central para login."""
        frame = tk.Frame(self.root, bg="white", width=400, height=450, relief="solid", bd=1)
        frame.pack_propagate(False)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        self.add_user_icon(frame)
        self.add_login_fields(frame)
        self.add_login_button(frame)

    def add_user_icon(self, frame):
        """Adiciona o ícone do usuário no frame."""
        try:
            icon_image = Image.open("C:/Users/User/Desktop/FISCALFLOW/img/iconlogin.png")
            icon_image = icon_image.resize((100, 100), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Ícone de login não encontrado!")
            logging.error("Ícone de login não encontrado.")
            return

        user_icon = tk.Label(frame, image=icon_photo, bg="white")
        user_icon.image = icon_photo
        user_icon.pack(pady=20)

        instruction_label = tk.Label(frame, text="Por favor informe seus dados.", font=("Arial", 12, "italic"), bg="white", fg="#555555")
        instruction_label.pack(pady=10)

    def add_login_fields(self, frame):
        """Adiciona os campos de entrada para usuário e senha."""
        # Campo de entrada para usuário
        username_container = tk.Frame(frame, bg="white")
        username_container.pack(pady=(10, 0))

        tk.Label(username_container, text="Usuário:", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(anchor="center")
        self.username_entry = tk.Entry(username_container, font=("Arial", 12), width=25, relief="flat", highlightbackground="#cccccc", highlightthickness=1)
        self.username_entry.pack(pady=(5, 10), anchor="center")

        # Campo de entrada para senha
        password_container = tk.Frame(frame, bg="white")
        password_container.pack(pady=(10, 0))

        tk.Label(password_container, text="Senha:", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(anchor="center")
        self.password_entry = tk.Entry(password_container, font=("Arial", 12), width=25, relief="flat", show="*", highlightbackground="#cccccc", highlightthickness=1)
        self.password_entry.pack(pady=(5, 10), anchor="center")

        # Checkbox para mostrar senha
        self.show_password_var = tk.BooleanVar()
        show_password_checkbox = tk.Checkbutton(password_container, text="Mostrar senha", font=("Arial", 10), bg="white", fg="#333333", variable=self.show_password_var, command=self.toggle_password_visibility)
        show_password_checkbox.pack(anchor="center")

    def add_login_button(self, frame):
        """Adiciona o botão de login."""
        login_button = tk.Button(frame, text="ACESSAR", font=("Arial", 14, "bold"), bg="#002855", fg="white", relief="flat", command=self.login)
        login_button.pack(pady=15, ipadx=10, ipady=5)
        login_button.bind("<Enter>", lambda e: login_button.config(bg="#004080"))
        login_button.bind("<Leave>", lambda e: login_button.config(bg="#002855"))

    def toggle_password_visibility(self):
        """Alterna a visibilidade da senha."""
        self.password_entry.config(show="" if self.show_password_var.get() else "*")

    def login(self):
        """Realiza a validação do login."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Atenção", "Os campos de usuário e senha não podem estar vazios.")
            logging.warning("Tentativa de login com campos vazios.")
            return

        # Gera o hash MD5 da senha fornecida
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        try:
            # Conecta ao banco de dados MySQL
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root842",
                database="sistemanf"
            )

            if connection.is_connected():
                logging.info("Conexão com o banco de dados bem-sucedida.")
                cursor = connection.cursor()
                query = "SELECT * FROM Usuario WHERE nome_usuario = %s AND senha_usuario = %s"
                cursor.execute(query, (username, hashed_password))
                result = cursor.fetchone()

                if result:
                    messagebox.showinfo("Login", "Acesso permitido!")
                    logging.info(f"Login bem-sucedido para o usuário: {username}")
                else:
                    messagebox.showerror("Login", "Usuário ou senha inválidos.")
                    logging.warning(f"Falha no login para o usuário: {username}")
        except Error as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados.\nErro: {e}")
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                logging.info("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
