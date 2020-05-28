import os

from telethon import TelegramClient

import re

class simp_telegram_client():

    def __init__(self, api_id, api_hash, max_error=4):
        """

        :param api_id: the telegram api id ,telethon docs related
        :param api_hash: the telegram api hash,telethon docs related
        :param max_error: the maximum amount of times the application will accept an error inside a function before it return all the already retrived answers
        """
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.client.start()
        self.max_error = max_error

    def send_file_to_multiple_destin(self, contacts, file):
        """
        this function send an file to multiple telegram chats
        :param contacts: reference for access the desired chat,same as telethon
        :param file: file you want to send
        :return:
        """
        for contact in contacts:
            try:
                self.client.send_file(contact, file)
            except Exception as e:
                print(e)

    def send_message_to_multiple_destin(self, contacts, text):
        """
        this function send an text to multiple chats
        :param contacts: reference for access the desired chat,same as telethon
        :param text: text you want to send
        :return:
        """
        for contact in contacts:
            try:
                self.client.send_message(contact, text)
            except Exception as e:
                print(e)

    def list_messages_with(self, contact, text, limit=20, reverse=False):
        """
        this function list all messages in chat containing the exact text inside of it
        :param contact: reference for access the desired chat,same as telethon
        :param text: the text you want inside the messages
        :param limit: the maximum amount of returns you want in the array
        :param reverse: if true it will search from the first to the last message in the chat,else it will search upsidown
        :return: an string array with the messages text
        """
        query = self.client.iter_messages(contact, limit=1, reverse=reverse)
        max_id = 0
        min_id = 0
        for i in query:
            if reverse:
                min_id = i.id
                max_id = i.id + 2
            else:
                if limit == "all":
                    limit = i.id
                max_id = i.id
                min_id = i.id - 2
        retorno = []
        while True:
            query = self.client.iter_messages(contact, limit=1, max_id=max_id, min_id=min_id, reverse=reverse)
            total_results = 0
            for i in query:
                total_results += 1
                try:
                    if text in i.message:
                        retorno.append(i.message)
                        if limit != "" and len(retorno) == limit:
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
                    if limit == "":
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

    def search_with_regex(self, contact, regex, limit=20, reverse=False, only_match=False):
        """
        this function return the message containing the match for a regex expression or the match resulting from the regex expression applied inside the message
        :param contact: reference for access the desired chat,same as telethon
        :param regex: the regular expression you want to apply
        :param limit: the maximum amount of returns you want in the array
        :param reverse: if true it will search from the first to the last message in the chat,else it will search upsidown
        :param only_match: if true it will return only the matched texts,else will return the complete message
        :return: an arrya of the matching messages,if only_param true instead of the message text will return an array of every non empty match
        """
        query = self.client.iter_messages(contact, limit=1, reverse=reverse)
        max_id = 0
        min_id = 0
        total_error = 0
        for i in query:
            if reverse:
                min_id = i.id
                max_id = i.id + 2
            else:
                if limit == "all":
                    limit = i.id
                max_id = i.id
                min_id = i.id - 2
        retorno = []
        while True:
            query = self.client.iter_messages(contact, limit=1, max_id=max_id, min_id=min_id, reverse=reverse)
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
                        if limit != "" and len(retorno) == limit:
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
                    if limit == "":
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

    def return_message_with_hashtag(self, contact, limit=10, reverse=False, remove_char=","):
        """
        this function search inside a chat for all the messages and categorize them in a dictionary , the keys for the dictionary are the hashtags inside the messages,and the containings are the message texts
        :param contact: reference for access the desired chat,same as telethon
        :param limit: the maximum amount of returns you want in the array,since any key reach this amount the function ends
        :param reverse: if true it will search from the first to the last message in the chat,else it will search upsidown
        :param remove_char: default="," if the hashtag ends with this char(error treating) will remove this character for an more uniform keys distribution
        :return: an dictionary containing every hashtag inside the analizeds messages into the keys,each key represents an array of messages text,if an message have more than one hashtag it will apear in every key corresponding to this hashtag
        """
        query = self.client.iter_messages(contact, limit=1, reverse=reverse)
        max_id = 0
        min_id = 0
        total_error = 0
        for i in query:
            if reverse:
                min_id = i.id
                max_id = i.id + 2
            else:
                if limit == "all":
                    limit = i.id
                max_id = i.id
                min_id = i.id - 2
        retorno = {}
        while True:
            query = self.client.iter_messages(contact, limit=1, max_id=max_id, min_id=min_id, reverse=reverse)

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
                        if len(retorno[hashtag]) == limit:
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
