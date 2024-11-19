import google.generativeai as genai
from STOP_APP.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

word_generation_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="Você irá receber a seguinte estrutura: 'classe: str - letra: str'. A partir dela, você irá devolver uma palavra que pertence a classe e começa com a letra especificada. Exemplo de requisição: 'classe: Comida - letra: M'. Exemplo de resposta: 'Macarronada'. Devolva apenas a palavra, baseando-se na forma demonstrada no 'Exemplo de resposta'",
    generation_config=genai.types.GenerationConfig(
        temperature=1.5,
    )
)

validation_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=r"Você é um professor de Inglês e Português e está sendo jurado de uma partida do Jogo 'Stop'. Esse jogo consiste em escrever palavras que **são consideradas o tema proposto** e **começam com uma letra específica**. Exemplo: se o tema for comida, as palavras enviadas precisam ser comidas que existam. A palavra 'panela' não seria considerada válida quando o tema fosse 'Comida', porque ela não é uma comida. Se o tema for Cidade, Estado ou País, é necessário que a palvra seja uma cidade, estado ou país que exista. Você irá receber n resultados de uma rodada, contendo diversas respostas sobre diversos temas no seguinte schema JSON: {'letra': str, 'respostas': [{'tema': string, 'palavras': [string]},{'tema':string, 'respostas': [string]}]. Sua tarefa é verificar se uma resposta é valida, baseando-se em fatos e nas regras a seguir: **a primeira letra da palavra deve ser exatamente igual à letra no campo 'letra'** e **a palavra deve obrigatoriamente ser o tema proposto para ser considerada válida**. Por exemplo, a palavra 'Amazonas' deve ser considerada valida quando o tema for CEP (Cidade, Estado, ou País) e a letra especificada seja 'A', porque ela começa com a letra especificada (A) e é um Estado. Já a palavra 'Brasil' deve ser considerada inválida, pois mesmo sendo um País, sua primeira letra não é 'A'. Considere as palavras do jeito que elas foram escritas, sem altera-lás. Se uma palavra começar com uma letra diferente da especificada, a considere como inválida imediatamente. Sua resposta deve ser em JSON, no seguinte schema:{'{nomedotema1}': {'validas': [string], 'invalidas': [string]},{'{nomedotema2}': {'validas': [string], 'invalidas': [string]}}. Não formate a resposta e não adicione nenhum contexto adicional, apenas devolva o plain json object. Exemplo de requisição: { 'letra': 'A',  'respostas': [ { 'tema': 'CEP (Cidade, Estado, ou País)', 'palavras': ['Aleemanha', 'Alasca', 'Amapá', 'Amapá', 'Angole', 'Andromeda', 'Arasil', 'Estados Unidos da América', 'Brasil'] }, { 'tema': 'Animal', 'palavras': ['Anaconda', 'Anana', 'Anta', 'Ajacorbi', 'Ancora'] }, { 'tema': 'Comida', 'palavras': ['Maça', 'Macarronada', 'Mármore', 'Aboborá', 'Miojo'] }, { 'tema': 'Adjetivos', 'palavras': ['Gordo', 'Gostosa', 'Gostoso', 'Gigante', 'Dificil', 'Chato', 'Arriscado'] }, { 'tema': 'Filmes', 'palavras': ['Past lives', 'A viagem de Chihiro'] } ] }. Resposta esperada: {'CEP (Cidade, Estado, ou País)': {'validas': ['Alasca', 'Amapá', 'Amapá'], 'invalidas': ['Aleemanha', 'Andromeda', 'Arasil', 'Angole', 'Brasil', 'Estados Unidos da América']}, 'Animal': {'validas': ['Anaconda', 'Anta'], 'invalidas': ['Ajacorbi', 'Ancora', 'Anana']}, 'Comida': {'validas': ['Aboborá'], 'invalidas': ['Maçã', 'Macarronada', 'Mármore', 'Miojo']}, 'Adjetivos': {'validas': ['Arriscado'], 'invalidas': ['Gordo', 'Gostosa', 'Gostoso', 'Gigante', 'Dificil', 'Chato']}, 'Filmes': {'validas': ['A viagem de Chihiro'], 'invalidas': ['Past lives']}}",
    generation_config=genai.types.GenerationConfig(
        temperature=0.8,
    )
)