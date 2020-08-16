# Treinador de Pronúncia Inglês

Programa em python para ajudar no treinamento da pronúncia em inglês.

# Requirements
 - Programa foi testado no python 3.6
 - Tentei usar o python 3.8 mas aparentemente o PyAudio não tem suporte no 3.8.

### Será necessário a instalação de 3 bibliotecas:
  - speech_recognition
  - pyaudio
  - jellyfish

```sh
$ pip install SpeechRecognition
$ pip install PyAudio 
$ pip install jellyfish
```

#### SpeechRecognition
  - Biblioteca para reconhecimento de fala.
  - https://pypi.org/project/SpeechRecognition/
 
#### PyAudio
  - Necessário para o uso do microfone.
  - https://pypi.org/project/PyAudio/
 
#### Jellyfish
  - Responsável pelo cálculo da pontuação utilizando o algoritmo de distância Levenshtein.
  - https://pypi.org/project/jellyfish/
  

# Modos Disponíveis
  - Modo livre.
  - Modo Frase.
  
### Modo Livre

  - Fale o que você quiser.
  - Será feito o reconhecimento da sua fala.
  - Será retornado o que foi dito.
 
### Modo Frases

  - Escolha o tipo de frase. Atualmente disponível Iniciante, frases de efeito e frases de filmes e séries.
  - Escolha a quantidade de frases que queira treinar.
  - Ele irá sortear frases aleatórias e exibirá na tela para você ler.
  - Espere o comando talk e pronuncie a frase.
  - Ao final das frases será exibido sua pontuação para cada frase e sua pontuação final.
  - Será salvo em um arquivo report.txt seu histórico para acompanhar seu progresso.

# Próximas Atualizações
 - Adicionar mais idiomas.
 - Adicionar modo música.
 - Adicionar áudio da frase. (Testei a lib pyttsx3 mas não gostei do resultado)


