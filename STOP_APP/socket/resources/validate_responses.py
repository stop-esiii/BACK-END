from STOP_APP.socket.models.gemini_model import word_generation_model, validation_model
from STOP_APP.socket.models.storage_stop import storage_stop
import json

def handle_validate_responses(socketio, data):
    lobby = data["code_lobby"]
    letra = data["letra"]
    users = storage_stop[lobby]

    temas_palavras = get_temas_palavras(users, letra)

    request_payload = generate_request_payload(temas_palavras, letra)

    response = validation_model.generate_content(request_payload)

    not_repeated_words = get_not_repeated_words(users)

    formated_response = json.loads(response.text)

    response_payload = generate_response_payload(formated_response)

    socketio.emit("retrieve_validate_responses", response_payload, to=lobby)

    update_users_scores(users, formated_response, not_repeated_words)
        
    storage_stop[lobby] = users

def get_temas_palavras(users, letra):
    temas_palavras = {}

    for userPayload in users:
        for tema in userPayload["receive_payload"]:
            if temas_palavras.get(tema) == None:
                temas_palavras[tema] = []
            
            palavra = userPayload["receive_payload"].get(tema)

            if palavra == "" and userPayload["autocomplete"]:
                word_request = f"classe: {tema} - letra: {letra}"
                response = word_generation_model.generate_content(word_request)
                palavra = response.text.replace("\n", "").split(' ')[0]
                userPayload["receive_payload"][tema] = palavra
                userPayload["autocomplete"] = False

            if palavra != "" and palavra not in temas_palavras[tema]:
                temas_palavras[tema].append(palavra)
    
    return temas_palavras

def generate_request_payload(temas_palavras, letra):
    request = {"letra": letra, "respostas": []}

    for tema in temas_palavras:
        request_obj = {"tema": tema, "palavras": temas_palavras[tema]}
        request["respostas"].append(request_obj)

    request_payload = json.dumps(request)

    return request_payload

def get_not_repeated_words(users):
    not_repeated_words = {}
    repeated_words = {}

    for userPayload in users:
        for tema in userPayload["receive_payload"]:
            if not_repeated_words.get(tema) == None:
                not_repeated_words[tema] = []
                repeated_words[tema] = []

            palavra = userPayload["receive_payload"].get(tema)
        
            if palavra in not_repeated_words[tema]:
                not_repeated_words[tema].remove(palavra)
                repeated_words[tema].append(palavra)

            if palavra not in repeated_words[tema]:
                not_repeated_words[tema].append(palavra)
    
    return not_repeated_words

def generate_response_payload(formated_response):
    response_payload = []

    for obj in formated_response:
        palavras_validas = formated_response[obj].get('validas')
        palavras_invalidas = formated_response[obj].get('invalidas')

        payload_obj = {"tema": obj, "palavras_validas": palavras_validas, "palavras_invalidas": palavras_invalidas}
        response_payload.append(payload_obj)
    
    return response_payload

def update_users_scores(users, formated_response, not_repeated_words):
    for user_info in users:
        round_payload = user_info['receive_payload']
        round_points = 0
        for tema in round_payload:
            if round_payload[tema] in formated_response[tema].get("validas"):
                if round_payload[tema] in not_repeated_words[tema]:
                    round_points += 10
                else:
                    round_points += 5
        
        if user_info['double_points']:
            user_info['score'] += round_points * 2
            user_info['double_points'] = False
        else:
            user_info['score'] += round_points
        
        user_info['receive_payload'] = {}