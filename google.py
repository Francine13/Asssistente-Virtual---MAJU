import speech_recognition as sr

def interpretar_microfone():
    reconhecedor = sr.Recognizer()
    
    with sr.Microphone() as fonte_audio:
        reconhecedor.adjust_for_ambient_noise(fonte_audio)
        
        print("Fale alguma coisa....")
        fala = reconhecedor.listen(fonte_audio)
        
        try:
            texto = reconhecedor.recognize_google(fala, language="pt-BR")
            print("Você disse:", texto)
        except sr.UnknownValueError:
            print("Não entendi o que você disse:")
            
if __name__ == '__main__':
    interpretar_microfone()