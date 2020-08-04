import asyncio
import os

from telethon import TelegramClient, sync
import voice_manage

import re


def Find_url(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


class simp_telegram_client():

    def __init__(self, api_id, api_hash, max_error=4, phone="", password="", qr_login=False):
        """
            :param api_id: the telegram api id ,telethon docs related
            :param api_hash: the telegram api hash,telethon docs related
            :param max_error: the maximum amount of times the application will accept an error inside a function before it return all the already retrived answers
            :param phone: the phone number to login
            :param password: the password of two step auth
            :param qr_login: qr code for login into app
            """
        self.client = TelegramClient('session_name', api_id, api_hash, request_retries=max_error)
        if phone == password == "" and not qr_login:
            self.client.start()
        elif qr_login:
            asyncio.get_event_loop().run_until_complete(self.qr_login_func())
        else:
            self.client.start(phone=phone, password=password)
        self.max_error = max_error

    async def qr_login_func(self):
        qr_login_ = await self.client.qr_login()
        qr_login_.url()
        await qr_login_.wait()

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

    def list_messages_with(self, contact, text, limit=20, reverse=False,repeat=False):
        """
        this function list all messages in chat containing the exact text inside of it
        :param contact: reference for access the desired chat,same as telethon
        :param text: the text you want inside the messages
        :param limit: the maximum amount of returns you want in the array
        :param reverse: if true it will search from the first to the last message in the chat,else it will search upsidown
        :return: an string array with the messages text
        """
        id = 0
        total_error = 0
        for i in self.client.iter_messages(contact, limit=1, reverse=reverse):
            id = i.id
            if limit == "all" and not reverse:
                limit = i.id
                break
        for i in self.client.iter_messages(contact, limit=1):
            id_min = i.id
        for i in self.client.iter_messages(contact, limit=1, reverse=True):
            id_max = i.id
        retorno = []
        while True:
            if reverse:
                query = self.client.iter_messages(contact, limit=2, min_id=id, reverse=reverse)
                id += 1
            else:
                query = self.client.iter_messages(contact, limit=2, max_id=id + 1, reverse=reverse)
                id -= 1
            total_results = 0

            for i in query:
                total_results += 1
                id = i.id
                try:
                    if text in i.message:
                        if (i.message not in retorno) or repeat :
                            retorno.append(i.message)
                except:
                    if limit == "":
                        return retorno
            if total_results < 1:
                total_error += 1
            if (total_error == self.max_error) or (id == id_max and not reverse) or (id == id_min and reverse) or (len(retorno) == limit):
                return retorno


    def search_with_regex(self, contact, regex, limit=20, reverse=False, only_match=False,repeat=False):
        """
        this function return the message containing the match for a regex expression or the match resulting from the regex expression applied inside the message
        :param contact: reference for access the desired chat,same as telethon
        :param regex: the regular expression you want to apply
        :param limit: the maximum amount of returns you want in the array
        :param reverse: if true it will search from the first to the last message in the chat,else it will search upsidown
        :param only_match: if true it will return only the matched texts,else will return the complete message
        :return: an arrya of the matching messages,if only_param true instead of the message text will return an array of every non empty match
        """
        id = 0
        total_error = 0
        for i in self.client.iter_messages(contact, limit=1, reverse=reverse):
            id = i.id
            if limit == "all" and not reverse:
                limit = i.id
                break
        for i in self.client.iter_messages(contact, limit=1):
            id_min = i.id
        for i in self.client.iter_messages(contact, limit=1, reverse=True):
            id_max = i.id
        retorno = []
        while True:
            if reverse:
                query = self.client.iter_messages(contact, limit=2, min_id=id, reverse=reverse)
                id += 1
            else:
                query = self.client.iter_messages(contact, limit=2, max_id=id, reverse=reverse)
                id -= 1
            total_results = 0
            for i in query:
                total_results += 1
                id = i.id
                try:
                    if re.search(regex, i.message):
                        if only_match:
                            result = []
                            for resultado in re.findall(regex, i.message)[0]:
                                if resultado != "":
                                    print(resultado)
                                    result.append(resultado)
                            if (result not in retorno) or repeat:
                                retorno.append(result)
                        else:
                            if (i.message not in retorno) or repeat:
                                retorno.append(i.message)
                        if limit != "all" and len(retorno) == limit:
                            return retorno
                except:
                    if limit == "all":
                        return retorno
            if total_results < 1:
                total_error += 1
            if (total_error == self.max_error) or (id == id_max and not reverse) or (id == id_min and reverse) or (
                    len(retorno) == limit):
                return retorno

    def return_message_with_hashtag(self, contact, limit=10, reverse=False, remove_char=",",repeat=False):
        """
        this function search inside a chat for all the messages and categorize them in a dictionary , the keys for the dictionary are the hashtags inside the messages,and the containings are the message texts
        :param contact: reference for access the desired chat,same as telethon
        :param limit: the maximum amount of returns you want in the array,since any key reach this amount the function ends
        :param reverse: if true it will search from the first to the last message in the chat,else it will search upsidown
        :param remove_char: default="," if the hashtag ends with this char(error treating) will remove this character for an more uniform keys distribution
        :return: an dictionary containing every hashtag inside the analizeds messages into the keys,each key represents an array of messages text,if an message have more than one hashtag it will apear in every key corresponding to this hashtag
        """
        id = 0
        total_error = 0
        for i in self.client.iter_messages(contact, limit=1, reverse=reverse):
            id = i.id
            if limit == "all" and not reverse:
                limit = i.id
                break
        for i in self.client.iter_messages(contact, limit=1):
            id_min = i.id
        for i in self.client.iter_messages(contact, limit=1, reverse=True):
            id_max = i.id
        retorno = {}
        while True:
            if reverse:
                query = self.client.iter_messages(contact, limit=2, min_id=id, reverse=reverse)
                id += 1
            else:
                query = self.client.iter_messages(contact, limit=2, max_id=id, reverse=reverse)
                id -= 1
            total_results = 0
            for i in query:
                total_results += 1
                id = i.id
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
                        if (mensagem not in retorno[hashtag]) or repeat:
                            retorno[hashtag].append(mensagem)
                        if len(retorno[hashtag]) == limit:
                            return retorno
                except:
                    if limit == "all":
                        return retorno
            if total_results < 1:
                total_error += 1

            if (total_error == self.max_error) or (id == id_max and not reverse) or (id == id_min and reverse) or (
                    len(retorno) == limit):
                return retorno

    def get_group_id(self, linkgrupo):
        loop = asyncio.get_event_loop()
        retorno = loop.run_until_complete(asyncio.gather(self.get_entity(linkgrupo)))
        return retorno

    async def get_entity(self, link):
        retorno = await self.client.get_entity(link)
        return retorno

    def listar_mensagem(self, contato, limite=20, reverse=False):
        retorno = []
        while True:
            query = self.client.iter_messages(contato, limit=limite, reverse=reverse)
            total_results = 0
            for i in query:
                total_results += 1
                try:
                    retorno.append(i.message)
                    if limite != "all" and len(retorno) == limite:
                        return retorno
                except:
                    if limite == "all":
                        return retorno
