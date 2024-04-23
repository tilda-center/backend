import email
import email.header
from imaplib import IMAP4_SSL, IMAP4
from typing import List

from fastapi import HTTPException
from freenit.config import getConfig
from pydantic import BaseModel, Field

config = getConfig()


def decode_mailbox(mailbox):
    m = mailbox.decode()
    start = m.find(")")
    separator = m[start + 1 : start + 6]
    data = m.split(separator)
    flags = data[0].replace("\\", "").replace("(", "").replace(")", "").split()
    name = data[1].replace('"', "")
    return name, flags, separator[2]


def create_and_insert(folders, paths, flags, separator):
    if len(paths) == 1:
        name = paths[0]
        m = Mailbox(name=name, flags=flags, separator=separator)
        folders.append(m)
    elif len(paths) > 1:
        name = paths[0]
        for folder in folders:
            if folder.name == name:
                create_and_insert(folder.children, paths[1:], flags, separator)
                return


def get_header(data, name):
    h = data[name]
    if h is None:
        return ""
    head = email.header.decode_header(data[name])
    res = ""
    for header, enc in head:
        if enc is not None:
            res += header.decode(enc)
        elif type(header) == bytes:
            res += header.decode()
        else:
            res += header
    return res


class EMail(BaseModel):
    id: int = Field(0, description="ID")
    msgid: str = Field("", description="Message-ID")
    from_addr: str = Field("", description="EMail sender")
    to: str = Field("", description="Recepient of email")
    subject: str = Field("", description="EMail subject")
    body: str = Field("", description="EMail body")
    date: str = Field("", description="Date of EMail")


class Mailbox(BaseModel):
    name: str = Field("", description="Mailbox name")
    flags: List[str] = Field([], description="Mailbox flags")
    separator: str = Field(".", description="Mailbox name separator")
    children: List = Field([], description="Submailboxes")

    @classmethod
    async def get(cls, user, folder):
        with IMAP4_SSL(config.mail.server) as M:
            try:
                M.login(
                    f"{user.email}*{config.mail.master_user}", config.mail.master_pw
                )
            except IMAP4.error:
                raise HTTPException(status_code=403, detail="Failed to login to mail server")
            status, _ = M.select(folder)
            if status == "OK":
                return cls(name=folder)
        raise HTTPException(status_code=409, detail="No such folder")

    @classmethod
    async def all(cls, user):
        ret = []
        with IMAP4_SSL(config.mail.server) as M:
            try:
                M.login(
                    f"{user.email}*{config.mail.master_user}", config.mail.master_pw
                )
            except IMAP4.error:
                raise HTTPException(status_code=403, detail="Failed to login to mail server")
            res = M.list()
            if len(res) < 2:
                raise HTTPException(
                    status_code=409, detail="Invalid data from mail server"
                )
            mailboxes = res[1]
            for mailbox in mailboxes:
                name, flags, separator = decode_mailbox(mailbox)
                create_and_insert(ret, name.split(separator), flags, separator)
        return ret

    async def create(self, user):
        with IMAP4_SSL(config.mail.server) as M:
            try:
                M.login(
                    f"{user.email}*{config.mail.master_user}", config.mail.master_pw
                )
            except IMAP4.error:
                raise HTTPException(status_code=403, detail="Failed to login to mail server")
            M.create(self.name)

    async def delete(self, user):
        with IMAP4_SSL(config.mail.server) as M:
            try:
                M.login(
                    f"{user.email}*{config.mail.master_user}", config.mail.master_pw
                )
            except IMAP4.error:
                raise HTTPException(status_code=403, detail="Failed to login to mail server")
            M.delete(self.name)

    async def emails(self, user):
        result = []
        with IMAP4_SSL(config.mail.server) as M:
            try:
                M.login(
                    f"{user.email}*{config.mail.master_user}", config.mail.master_pw
                )
            except IMAP4.error:
                raise HTTPException(status_code=403, detail="Failed to login to mail server")
            status, nmess = M.select(self.name)
            if status != "OK":
                raise HTTPException(status_code=409, detail="Error selecting folder")
            if nmess[0] is None:
                raise HTTPException(
                    status_code=409, detail="Invalid data from mail server"
                )
            try:
                endindex = int(nmess[0])
            except:
                raise HTTPException(
                    status_code=409, detail="Invalid data from mail server"
                )
            msgset = f"1:{endindex}"
            status, msgs = M.fetch(msgset, "(RFC822)")
            if status != "OK":
                raise HTTPException(
                    status_code=409, detail=f"Error fetching from {self.name}"
                )
            i = 0
            for msg in msgs:
                if type(msg) != tuple:
                    continue
                i += 1
                mail = email.message_from_bytes(msg[1])
                e = EMail(
                    id=i,
                    msgid=str(mail["message-id"]),
                    date=str(mail["date"]),
                    subject=get_header(mail, "subject"),
                    from_addr=get_header(mail, "from"),
                    to=get_header(mail, "to"),
                )
                result.append(e)
        return result
