from ast import Break, If
import speech_recognition as sr
from nltk import word_tokenize, corpus
import json

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_FILES = "weather.json"
CAMINHO_CONFIG = "config.json"

def iniciar():
    global reconhecedor
    global palavras_de_parada
    global nome_assistente
    global acoes
    global weather
    
    reconhecedor = sr.Recognizer()
    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))
    
    with open (CAMINHO_FILES, "r", encoding='utf8') as weather_file:
        configuracao = json.load(weather_file)
        weather = configuracao["previsoes"]
        
        weather_file.close()
        
        
    with open (CAMINHO_CONFIG, "r", encoding='utf8') as config_file:
        config = json.load(config_file)

        nome_assistente = config["nome"]
        acoes = config["acoes"]
    
        config_file.close()

def escutar_comando():
    global reconhecedor
    
    comando = None
    
    with sr.Microphone() as fonte_audio:
        reconhecedor.adjust_for_ambient_noise(fonte_audio)
        
        print("Fale alguma coisa...")
        fala = reconhecedor.listen(fonte_audio)
        
        try:
            comando = reconhecedor.recognize_google(fala, language= IDIOMA_FALA)
        except sr.UnknownValueError:
            pass
    
    return comando

def eliminar_palavras_de_parada(tokens):
    global palavras_de_parada
    
    tokens_filtrados = []
    for token in tokens:
        if token.lower() not in palavras_de_parada:
            tokens_filtrados.append(token)

    print(tokens_filtrados)
    
    return tokens_filtrados

def tokenizar_comando(comando):
    global nome_assistente
    
    acao = None
    objeto = None
    
    tokens = word_tokenize(comando, IDIOMA_CORPUS)
    if tokens:
        tokens = eliminar_palavras_de_parada(tokens)

        print('tokens', tokens)
        
        if len (tokens) >= 3:
            if nome_assistente == tokens[0].lower():
                acao = tokens[1].lower()
                objeto = tokens[len(tokens) - 1].lower()  

    print(acao, objeto)          
    
    return acao, objeto

def validar_comando(acao,objeto):
    global acoes
    
    valido = False
    
    if acao and objeto:
        for acaoCadastrada in acoes:
            if acao == acaoCadastrada["nome"]:
                if objeto in acaoCadastrada["objetos"]:
                    valido = True
                    
                Break
    
    return valido

def previsao_momento():
    global weather
    print('Qual a cidade?')
    
    try:
        cidade = escutar_comando()
        previsao = ""
        for clima in weather:
            if clima['cidade'].lower() == cidade.lower():
                for item in clima['agora']:
                    previsao += (item+": "+clima['agora'].get(item)+"\n")
        if previsao == '': 
            print('Não foi possivel encontrar a previsão dessa cidade')
            return None
        
        print (f'A previsão da cidade {cidade} no momento é \n{previsao}')
    except:
        print('ocorreu um erro')
        
        
def previsao_amanha():
    global weather
    print('Qual a cidade?')
    
    try:
        cidade = escutar_comando()
        previsao = ""
        for clima in weather:
            if clima['cidade'].lower() == cidade.lower():
                for item in clima['amanha']:
                    previsao += (item+": "+clima['amanha'].get(item)+"\n")
        if previsao == '': 
            print('Não foi possivel encontrar a previsão dessa cidade')
            return None
        
        print (f'A previsão da cidade {cidade} amanhã é \n{previsao}')
    except:
        print('ocorreu um erro')
        
def porcentagem_chuva():
    global weather
    print('Qual a cidade?')
    
    try:
        cidade = escutar_comando()
        porcentagem = ""
        for clima in weather:
            if clima['cidade'].lower() == cidade.lower():
                for item in clima['porcentagem']:
                    porcentagem += (item+": "+clima['porcentagem'].get(item)+"\n")
        if porcentagem == '': 
            print('Não foi possivel encontrar a porcentagem de chuva do dia dessa cidade')
            return None
        
        print (f'A porcentagem de chuva do dia da cidade {cidade} é \n{porcentagem}')
    except:
        print('ocorreu um erro')
        
    
def executar_comando(acao, objeto):
    print("vou executar o comando:", acao, objeto)
    if acao == 'previsão' and objeto == 'momento':
        previsao_momento()
    if acao == 'previsão' and objeto == 'amanhã':
        previsao_amanha()
    if acao == 'porcentagem' and objeto == 'dia':
        porcentagem_chuva()

if __name__ == '__main__':
    iniciar()
    
    continuar = True
    while continuar:
        try:
            comando = escutar_comando()
            print(f"processando o comando: {comando}")
            
            if comando:
                acao, objeto = tokenizar_comando(comando)
                valido = validar_comando(acao, objeto)
                if valido:
                    executar_comando(acao, objeto)
                else:
                    print("Não entendi o comando. Repita, por favor")           
                    
        except KeyboardInterrupt:
            print("Tchau!")
            
            continuar = False
