import os

from telethon import TelegramClient

import re

class simp_telegram_client():

    def __init__(self, api_id, api_hash, max_error=4):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.client.start()
        self.max_error = max_error

    def send_file_to_multiple_destin(self, contatos, arquivo):
        for contato in contatos:
            try:
                self.client.send_file(contato, arquivo)
            except Exception as e:
                print(e)

    def send_message_to_multiple_destin(self, contatos, texto):
        for contato in contatos:
            try:
                self.client.send_message(contato, texto)
            except Exception as e:
                print(e)

    def list_messages_with(self, contato, texto, limite=20, reverse=False):
        query = self.client.iter_messages(contato, limit=1, reverse=reverse)
        max_id = 0
        min_id = 0
        for i in query:
            if reverse:
                min_id = i.id
                max_id = i.id + 2
            else:
                if limite == "all":
                    limite = i.id
                max_id = i.id
                min_id = i.id - 2
        retorno = []
        while True:
            query = self.client.iter_messages(contato, limit=1, max_id=max_id, min_id=min_id, reverse=reverse)
            total_results = 0
            for i in query:
                total_results += 1
                try:
                    if texto in i.message:
                        retorno.append(i.message)
                        if limite != "" and len(retorno) == limite:
                            return retorno
                        if min_id == 0:
                            return retorno
                    if reverse:
                        min_id = i.id
                        max_id = i.id + 2
                    else:
                        max_id = max_id
                        min_id = max_id - 2
                except:
                    if limite == "":
                        return retorno
                        if reverse:
                            min_id = i.id + 1
                            max_id = i.id + 3
                        else:
                            max_id = max_id - 1
                            min_id = max_id - 3
            if total_results < 1:
                total_error += 1
                if reverse:
                    min_id = i.id + 1
                    max_id = i.id + 3
                else:
                    max_id = max_id - 1
                    min_id = max_id - 3
                print(total_error)
            if total_error == self.max_error:
                print(total_error)
                return retorno

    def search_with_regex(self, contato, regex, limite=20, reverse=False, only_match=False):
        query = self.client.iter_messages(contato, limit=1, reverse=reverse)
        max_id = 0
        min_id = 0
        total_error = 0
        for i in query:
            if reverse:
                min_id = i.id
                max_id = i.id + 2
            else:
                if limite == "all":
                    limite = i.id
                max_id = i.id
                min_id = i.id - 2
        retorno = []
        while True:
            query = self.client.iter_messages(contato, limit=1, max_id=max_id, min_id=min_id, reverse=reverse)
            total_results = 0
            for i in query:
                total_results += 1
                print(i)
                print(str(max_id)+'  '+str(min_id))
                try:
                    if re.search(regex, i.message):

                        if only_match:
                            result = []
                            for resultado in re.findall(regex, i.message)[0]:
                                if resultado != "":
                                    print(resultado)
                                    result.append(resultado)
                            retorno.append(result)
                        else:
                            retorno.append(i.message)
                        if limite != "" and len(retorno) == limite:
                            return retorno
                        if min_id == 0:
                            return retorno
                    if reverse:
                        min_id = min_id + 1
                        max_id = min_id + 3
                    else:
                        max_id = max_id - 1
                        min_id = max_id - 3
                except:
                    if limite == "":
                        return retorno
                    else:
                        if reverse:
                            min_id = min_id + 1
                            max_id = min_id+ 3
                        else:
                            max_id = max_id - 1
                            min_id = max_id - 3
            if total_results < 1:
                total_error += 1
                if reverse:
                    min_id = min_id + 1
                    max_id = min_id + 3
                else:
                    max_id = max_id - 1
                    min_id = max_id - 3
            if total_error == self.max_error:
                return retorno

    def return_message_with_hashtag(self, contato, limite=10, reverse=False, remove_char=","):
        query = self.client.iter_messages(contato, limit=1, reverse=reverse)
        max_id = 0
        min_id = 0
        total_error = 0
        for i in query:
            if reverse:
                min_id = i.id
                max_id = i.id + 2
            else:
                if limite == "all":
                    limite = i.id
                max_id = i.id
                min_id = i.id - 2
        retorno = {}
        while True:
            query = self.client.iter_messages(contato, limit=1, max_id=max_id, min_id=min_id, reverse=reverse)

            total_results = 0
            for i in query:
                total_results += 1
                try:
                    mensagem = i.message
                    mensagem.strip("#")
                    hashtags = []
                    for tag in mensagem.split():
                        if tag.startswith("#"):
                            tag = tag[1:]
                            if tag.endswith(remove_char):
                                tag = tag[:-1]
                            hashtags.append(tag)
                    for hashtag in hashtags:
                        if hashtag not in retorno.keys():
                            retorno[hashtag] = []
                        retorno[hashtag].append(mensagem)
                        if len(retorno[hashtag]) == limite:
                            return retorno
                    if min_id == 0:
                        return retorno
                    if reverse:
                        min_id = i.id
                        max_id = i.id + 2
                    else:
                        max_id = max_id
                        min_id = max_id - 2
                except:
                    if reverse:
                        min_id = i.id + 1
                        max_id = i.id + 3
                    else:
                        max_id = max_id - 1
                        min_id = max_id - 3
            if total_results < 1:
                total_error += 1
                if reverse:
                    min_id = i.id + 1
                    max_id = i.id + 3
                else:
                    max_id = max_id - 1
                    min_id = max_id - 3
            if total_error == self.max_error:
                return retorno
        return retorno
