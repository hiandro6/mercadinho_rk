from tkinter import *
import sqlite3

class Mercadinho():
    def __init__(self):
        self.janela = Tk()
        self.janela.geometry("1000x500")
        self.janela.title("MERCADINHO ROBERTO CARLOS")
        self.janela.resizable(0, 0)

        #conteiner esquerdo:
        self.conteinerprodutos = Canvas(self.janela, bg="gray", height=500, width=400, borderwidth=0, highlightthickness=0)
        self.conteinerprodutos.place(x=0, y=0)

        #titulo dele:
        self.tituloprodutos = Label(self.conteinerprodutos, bg="black", fg="white" ,text="PRODUTOS:", justify="center", height=2, width=34, font=("Arial", 16))
        self.tituloprodutos.place(x=0, y=0)

        self.nome_e_preco = {} 

        #conteudo do lado esquerdo(parte branca):
        self.label_nomes = Label(self.conteinerprodutos,bg="blue", fg="white", text="", height=18, width=15, borderwidth=0, highlightthickness=0, font=("Sans-Serif", 12), justify="left")
        self.label_precos = Label(self.conteinerprodutos,bg="blue", fg="white", text="", height=18, width=12, borderwidth=0, highlightthickness=0, font=("Sans-Serif", 12), justify="left")
        
        banco = sqlite3.connect('banco.db')
        con = banco.cursor()

        con.execute("SELECT * FROM mercadinho")
        produtos_precos = con.fetchall()
        print(produtos_precos)

        banco.commit()
        banco.close()

        contador_aux = 0
        while contador_aux < len(produtos_precos):
            self.nome_e_preco[f"{produtos_precos[contador_aux][0]}"] = f"{produtos_precos[contador_aux][1]:.2f}"
            contador_aux += 1

        for chaves, valores in self.nome_e_preco.items():   #porém lembrem de trocar o nome do dicionário nesse for
            self.label_nomes["text"] += f"{chaves}\n"
            self.label_precos["text"] += f"R$ {valores}\n"
        self.label_nomes.place(x=75, y=100)
        self.label_precos.place(x=212, y=100)


        #conteiner direito:
        self.conteinervenda = Canvas(self.janela, bg="blue", height=500, width=600, borderwidth=0, highlightthickness=0)
        self.conteinervenda.place(x=400, y=0)


        #titulo dele
        self.titulovenda = Label(self.conteinervenda, bg="white", fg="black" ,text="ATENDIMENTO:", justify="center", height=2, width=32, font=("Sans Serif", 18))
        self.titulovenda.place(x=80, y=10)


        #imagem que está no titulo:
        self.imagemcarrinho = PhotoImage(file="imagens/carrinho.png").subsample(6)
        self.aux_imgcarrinho = Canvas(self.titulovenda, background="white", height=50, width=60, borderwidth=0, highlightthickness=0)
        self.aux_imgcarrinho.place(x=70, y=0)
        self.aux_imgcarrinho.create_image(30, 25, image=self.imagemcarrinho)
        

        #label e entry referente ao nome do produto:
        self.labelnome = Label(self.conteinervenda, bg="black", fg="white" ,text="PRODUTO:",height=2, width=12, justify="center", font=("Arial", 14))
        self.labelnome.place(x=50, y=90)

        self.entrynome = Entry(self.conteinervenda, bg="white", fg="black" ,justify="center", font=("Arial", 21))
        self.entrynome.place(x=220, y=96)


        #label e entry referente a quantidade do produto:
        self.labelquantidade = Label(self.conteinervenda, bg="black", fg="white" ,text="QUANTIDADE:",height=2, width=12, justify="center", font=("Arial", 14))
        self.labelquantidade.place(x=50, y=160)

        self.entryquantidade = Entry(self.conteinervenda, bg="white", fg="black" ,justify="center", font=("Arial", 21))
        self.entryquantidade.place(x=220, y=166)


        #botao verificar estoque
        self.botao_verificar_estoque = Button(self.conteinervenda, bg="orange", text="verificar estoque", fg="white" ,justify="center", font=("Arial", 14), command=self.verificar_estoque)
        self.botao_verificar_estoque.place(x=200, y=230)


        #label usado para dar avisos ao usuário:
        self.label_avisos = Label(self.conteinervenda, bg="white", fg="black", text="", justify="center", font=("Arial", 11), height=3, width=60)
        self.label_avisos.place(x=30, y=290)


        #botão adicionar, remover do carrinho e finalizar compra:
        self.botao_adicionar = Button(self.conteinervenda, text="adicionar ao carrinho", bg="green", fg="white" ,justify="center", font=("Arial", 12), command=self.adionar_ao_carrinho)
        self.botao_adicionar.place(x=30, y=370)


        self.botao_remover = Button(self.conteinervenda, text="remover do carrinho", bg="red", fg="white" ,justify="center", font=("Arial", 12), command=self.remover_do_carrinho)
        self.botao_remover.place(x=250, y=370)


        self.botao_finalizar = Button(self.conteinervenda, text="finalizar compra", bg="green", fg="white" ,justify="center", font=("Arial", 12), command=self.finalizar_compra)
        self.botao_finalizar.place(x=455, y=370)


        #labels referentes ao valor do carrinho:
        self.label_txtvalor = Label(self.conteinervenda, bg="black", fg="white" ,text="VALOR DO CARRINHO:",height=2, width=20, justify="center", font=("Arial", 12))
        self.label_txtvalor.place(x=100, y=430)

        self.label_valoratual = Label(self.conteinervenda, bg="orange", fg="white" ,text="R$ 0",height=2, width=20, justify="center", font=("Arial", 12))
        self.label_valoratual.place(x=300, y=430)



        self.janela.mainloop()

    
    def verificar_estoque(self):
        produto = self.entrynome.get()  
        quantidade = int(self.entryquantidade.get())  
       
        banco = sqlite3.connect('banco.db')
        con = banco.cursor()

        con.execute("SELECT * FROM mercadinho WHERE produto=?", (produto,))
        resultado = con.fetchone()
        
        if resultado is None:
            self.label_avisos["fg"] = "red"
            self.label_avisos["text"] = "O produto que você procura não é vendido nesse estabelecimento!"
        else:
            estoque_disponivel = resultado[2]  
            if quantidade <= estoque_disponivel:
                self.label_avisos["fg"] = "green"
                self.label_avisos["text"] = "O produto e a quantidade solicitada estão disponíveis!"
            else:
                self.label_avisos["fg"] = "red"
                self.label_avisos["text"] = f"A quantidade que você solicitou não está disponível. \n Só temos {estoque_disponivel} unidades de {produto} restantes."

        banco.close()

    def adionar_ao_carrinho(self):
        produto = self.entrynome.get()
        quantidade = int(self.entryquantidade.get())

        banco = sqlite3.connect('banco.db')
        con = banco.cursor()

        con.execute("SELECT * FROM mercadinho WHERE produto=?", (produto,))
        resultado = con.fetchone()

        if resultado is None:
            self.label_avisos["fg"] = "red"
            self.label_avisos["text"] = "O produto que você procura não é vendido nesse estabelecimento!"
        else:
            estoque_disponivel = resultado[2]
            if quantidade <= estoque_disponivel:
                novo_estoque = estoque_disponivel - quantidade
                con.execute("UPDATE mercadinho SET estoque=? WHERE produto=?", (novo_estoque, produto))
                banco.commit()


                if not hasattr(self, 'carrinho'):
                    self.carrinho = {}

                self.carrinho[produto] = self.carrinho.get(produto, 0) + quantidade

                # Atualizar o valor total do carrinho no label
                total_valor = sum(float(self.nome_e_preco[produto]) * quantidade for produto, quantidade in self.carrinho.items())
                self.label_valoratual["text"] = f"R$ {total_valor:.2f}"
                self.label_avisos["fg"] = "green"
                self.label_avisos["text"] = "Produto adicionado ao carrinho!"

            else:
                self.label_avisos["fg"] = "red"
                self.label_avisos["text"] = f"A quantidade que você solicitou não está disponível. \n Só temos {estoque_disponivel} unidades de {produto} restantes."

        banco.close()


    def remover_do_carrinho(self):
        produto = self.entrynome.get()
        quantidade = int(self.entryquantidade.get())

        if not hasattr(self, 'carrinho') or produto not in self.carrinho or self.carrinho[produto] < quantidade:
            self.label_avisos["fg"] = "red"
            self.label_avisos["text"] = "Produto não encontrado no carrinho ou quantidade inválida."
            return

    
        self.carrinho[produto] -= quantidade

        if self.carrinho[produto] == 0:
            del self.carrinho[produto]

    
        banco = sqlite3.connect('banco.db')
        con = banco.cursor()

        con.execute("SELECT * FROM mercadinho WHERE produto=?", (produto,))
        resultado = con.fetchone()

        if resultado is not None:
            estoque_atual = resultado[2]
            novo_estoque = estoque_atual + quantidade
            con.execute("UPDATE mercadinho SET estoque=? WHERE produto=?", (novo_estoque, produto))
            banco.commit()

            total_valor = sum(float(self.nome_e_preco[produto]) * quantidade for produto, quantidade in self.carrinho.items())
            self.label_valoratual["text"] = f"R$ {total_valor:.2f}"

            self.label_avisos["fg"] = "blue"
            self.label_avisos["text"] = "Produto removido do carrinho."

        banco.close()



    def finalizar_compra(self):
        if not hasattr(self, 'carrinho') or not self.carrinho:
            self.label_avisos["fg"] = "red"
            self.label_avisos["text"] = "Carrinho vazio. Adicione itens antes de finalizar a compra."
            return

        total_valor = 0
        self.label_valoratual["text"] = f"R$ {total_valor:.2f}"
        self.carrinho = {}

        self.label_avisos["fg"] = "green"
        self.label_avisos["text"] = "Compra finalizada. Obrigado pela preferência!"
    










banco = sqlite3.connect('banco.db')
con = banco.cursor()

con.execute("CREATE TABLE  IF NOT EXISTS mercadinho(produto text, valor integer, estoque integer)")
banco.commit()


con.execute("SELECT * FROM mercadinho")
produtos = con.fetchall()


if not produtos:
    con.execute("INSERT INTO mercadinho VALUES('uva',3.56,200)")
    con.execute("INSERT INTO mercadinho VALUES('mamão',8.00,120)")
    con.execute("INSERT INTO mercadinho VALUES('leite',9.30,180)")
    con.execute("INSERT INTO mercadinho VALUES('sabonete',5.00,210)")
    banco.commit()
banco.close()

app = Mercadinho()