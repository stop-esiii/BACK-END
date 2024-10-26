from math import ceil
from STOP_APP.socket.models.validations import validations
from STOP_APP.socket.models.storage_stop import storage_stop

def handle_receive_validate(socketio, data):
    lobby = data["code_lobby"]
    usersValidations = validations[lobby]
    minimalApproval = ceil(len(usersValidations) / 2)

    wordsCount = get_words_count(usersValidations)

    validWords = get_valid_words(wordsCount, minimalApproval)

    lobbyUsers = storage_stop[lobby]

    notRepeatedWords = get_notRepeatedWords(lobbyUsers)
            
    usersScores = get_users_scores(lobbyUsers, validWords, notRepeatedWords)

    storage_stop[lobby] = lobbyUsers
    validations[lobby].clear()
    
    socketio.emit("trigger_stop", usersScores, to=lobby)


def get_words_count(usersValidations):
    wordsCount = {}

    for validation in usersValidations:
        for category in validation:
            if wordsCount.get(category) == None:
                 wordsCount[category] = {}
            for word in validation[category]:
                if wordsCount.get(category).get(word) == None:
                    wordsCount[category][word] = 1
                else:
                    wordsCount[category][word] += 1

    return wordsCount

def get_valid_words(wordsCount, minimalApproval):
    validWords = {}

    for category in wordsCount:
        validWords[category] = []
        for word in wordsCount[category]:
            if wordsCount[category][word] >= minimalApproval:
                validWords[category].append(word)

    return validWords


def get_notRepeatedWords(lobbyUsers):
    notRepeatedWords = {}
    repeatedWords = {}

    for user_info in lobbyUsers:
        round_payload = user_info['receive_payload']
        for category in round_payload:
            if notRepeatedWords.get(category) == None:
                notRepeatedWords[category] = []
                repeatedWords[category] = []

            if round_payload[category] in notRepeatedWords[category]:
                notRepeatedWords[category].remove(round_payload[category])
                repeatedWords[category].append(round_payload[category])

            if round_payload[category] not in repeatedWords[category]:
                notRepeatedWords[category].append(round_payload[category])

    return notRepeatedWords


def get_users_scores(lobbyUsers, validWords, notRepeatedWords):
    usersScores = []

    for user_info in lobbyUsers:
        round_payload = user_info['receive_payload']
        for category in round_payload:
            if round_payload[category] in validWords[category]:
                if round_payload[category] in notRepeatedWords[category]:
                    user_info['score'] += 10
                else:
                    user_info['score'] += 5

        usersScores.append({'username': user_info['username'], 'score': user_info['score']})

    usersScores.sort(key = lambda x: x['score'], reverse=True)

    return usersScores
