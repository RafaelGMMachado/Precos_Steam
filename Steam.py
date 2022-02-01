#############################################################################
# Nome: Separador de Preços
# Autor: Rafael Machado                                               
# Data: 03/01/2022                                                    
# Resumo: Separar preços de jogos da Steam e salvar o menor preço identificado
#############################################################################
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from unidecode import unidecode

# Função para atualizar ou atualizar automaticamente todos quando abrir? Ou os 2?
# Menu
# Corrigir as partes do código que podem dar erro
# Opções = Ver os preços dos jogos (opções para ver? Alfabética, ordem de prioridade personalizada) 
# / adicionar jogo / excluir jogo / alterar menor preço / sair

def getInfos (): # Abre o arquivo com os jogos e retorna uma lista com cada elemento de cada linha do arquivo
    arquivo = open("jogos.txt", "r")
    conteudo = arquivo.readlines()
    arquivo.close()
    nconteudo = []
    for linha in conteudo:
        linha = linha.split(" / ")
        nconteudo.append(linha)
    return nconteudo
def printar (): # Abre o arquivo com os jogos e coloca todas as linhas dele no programa
    arquivo = open("jogos.txt", "r")
    conteudo = arquivo.readlines()
    arquivo.close()
    games["state"] = NORMAL
    games.delete(1.0, END)
    for linha in conteudo:
        games.insert(END, linha)
    games["state"] = DISABLED
def update (): # Abre o arquivo com os jogos e atualiza o preço de cada um
    nconteudo = getInfos()
    for n in range (1, len(nconteudo)):
        gameid = nconteudo[n][0]
        link = f"https://store.steampowered.com/api/appdetails?appids={gameid}&cc=brl&l=pt"

        html = urlopen(link)
        bs = str(BeautifulSoup(html, 'html.parser'))
        bs = bs.split(",")
        for i in bs:
            if '"final":' in i:
                price = float(i[8:-2] + "." + i[-2::])
        if float(nconteudo[n][3]) > price:
            nconteudo[n][3] = price
        nconteudo[n][2] = price
    arquivo = open("Jogos.txt", "w")
    for n in range (len(nconteudo)):
        arquivo.write("{0} / {1} / {2} / {3} / {4}".format (nconteudo[n][0], nconteudo[n][1], nconteudo[n][2], nconteudo[n][3], nconteudo[n][4]) )
    arquivo.close()
    printar()
# Ver Preços 
def viewPrices ():
    arquivo = open("jogos.txt", "r")
    conteudo = arquivo.read()
    arquivo.close()
    print(conteudo)
# Adicionar Jogo
def addGame ():
    gameid = adicionarEntrada.get()
    link = f"https://store.steampowered.com/api/appdetails?appids={gameid}&cc=brl&l=pt"

    html = urlopen(link)
    bs = str(BeautifulSoup(html, 'html.parser'))
    bs = bs.split(",")
    count = 0
    for i in bs:
        if '"name":' in i and count == 0:
            gamename = i[8:-1]
            print(gamename)
            count += 1
        if '"final":' in i:
            price = float(i[8:-2] + "." + i[-2::])
            lowestprice = price
            print("R$:", price)
        if '"achievements"' in i:
            achievements = i[24::]
            print("Achievements:", i[24::])
    arquivo = open("jogos.txt", "r")
    conteudo = arquivo.readlines()
    arquivo.close()
    exist = False
    for linha in conteudo:
        if gameid in linha:
            exist = True
    if exist == False:
        arquivo = open("Jogos.txt", "a")
        arquivo.write("\n{0} / {1} / {2} / {3} / {4}".format (gameid, gamename, price, lowestprice, achievements) )
        arquivo.close()
    print("Concluido")
    printar()

# Deletar jogo
def delGame ():
    gameid = excluirEntrada.get()
    validate = messagebox.askyesno("Pergunta", "Tem certeza que deseja excluir?")
    if validate == True:
        conteudo = getInfos()
        for n in range (1, len(conteudo)):
            if conteudo[n][0] == gameid:
                del conteudo[n]
                break
        arquivo = open("Jogos.txt", "w")
        for n in range (len(conteudo)):
            arquivo.write("{0} / {1} / {2} / {3} / {4}".format (conteudo[n][0], conteudo[n][1], conteudo[n][2], conteudo[n][3], conteudo[n][4]) )
        arquivo.close()
        printar()
# Mudar o menor preço
def chngPrice ():
    gameid = atualizarPrecoEntrada.get()
    lowestprice = PrecoEntrada.get()
    conteudo = getInfos()
    for n in range (1, len(conteudo)):
        if conteudo[n][0] == gameid:
            if float(conteudo[n][3]) > float(lowestprice):
                conteudo[n][3] = lowestprice
    arquivo = open("Jogos.txt", "w")
    for n in range (len(conteudo)):
        arquivo.write("{0} / {1} / {2} / {3} / {4}".format (conteudo[n][0], conteudo[n][1], conteudo[n][2], conteudo[n][3], conteudo[n][4]) )
    arquivo.close()
    printar()
    
# Transformar essa parte em função
"""arquivo = open("Jogos.txt", "w")
for n in range (len(conteudo)):
    arquivo.write("{0} / {1} / {2} / {3} / {4}".format (conteudo[n][0], conteudo[n][1], conteudo[n][2], conteudo[n][3], conteudo[n][4]) )
arquivo.close()"""
# Colocar para alterar o , por . caso digitar errado (Corrigir pra não dar erro quando não colocar float)

# Janela
window = Tk()
window.title("Algoritimos")
window.geometry("1366x768")

# Lista dos Jogos
games = scrolledtext.ScrolledText(window, width = 60, height = 27, state = DISABLED, font = ("Arial", 16))
games.place(relx = 0.02, rely = 0.085)
# Labels
titulo = Label(window, text = "JOGOS", font = ("Arial", 20))
titulo.place (relx = 0.25, rely = 0.02)

adicionar = Label(window, text = "Adicionar Jogo", font = ("Arial", 18))
adicionar.place(relx = 0.775, rely = 0.12, anchor = CENTER)

excluir = Label(window, text = "Excluir Jogo", font = ("Arial", 18))
excluir.place(relx = 0.775, rely = 0.35, anchor = CENTER)

atualizarPreco = Label(window, text = "Atualizar Menor Preço", font = ("Arial", 18))
atualizarPreco.place(relx = 0.775, rely = 0.58, anchor = CENTER)
##################################################################
# Entrada Adicionar Jogo
adicionarEntrada = Entry(window, width = 15, font = ("Arial", 14), justify = CENTER)
adicionarEntrada.place(relx = 0.81, rely = 0.19, anchor = E)

adicionarEnviar = Button(window, text = "Enviar", command = addGame, font = ("Arial", 14))
adicionarEnviar.place(relx = 0.815, rely = 0.19, anchor = W)

# Entrada Excluir Jogo
excluirEntrada = Entry(window, width = 15, font = ("Arial", 14), justify = CENTER)
excluirEntrada.place(relx = 0.81, rely = 0.42, anchor = E)

excluirEnviar = Button(window, text = "Enviar", command = delGame, font = ("Arial", 14))
excluirEnviar.place(relx = 0.815, rely = 0.42, anchor = W)

# Entrada Atualizar Preço
atualizarPrecoEntrada = Entry(window, width = 15, font = ("Arial", 14), justify = CENTER)
atualizarPrecoEntrada.place(relx = 0.81, rely = 0.65, anchor = E)

PrecoEntrada = Entry(window, width = 10, font = ("Arial", 14), justify = CENTER)
PrecoEntrada.place(relx = 0.795, rely = 0.69, anchor = E)

atualizarPrecoEnviar = Button(window, text = "Enviar", command = chngPrice, font = ("Arial", 14))
atualizarPrecoEnviar.place(relx = 0.815, rely = 0.67, anchor = W)

# Botão Atualizar
atualizar = Button(window, text = "Atualizar", command = update, font = ("Arial", 20), width = 20)
atualizar.place(relx = 0.655, rely = 0.85)
# Loop da Janela
update()
window.mainloop()