from typing import List

from fastapi import Depends, HTTPException
from freenit.api.router import route
from freenit.decorators import description
from freenit.models.user import User
from freenit.permissions import user_perms

from ..models.mailbox import EMail, Mailbox

tags = ["mail"]


@route("/folders", tags=tags)
class MailboxListAPI:
    @staticmethod
    @description("Get mail folders")
    async def get(user: User = Depends(user_perms)) -> List[Mailbox]:
        return await Mailbox.all(user)

    @staticmethod
    @description("Create mail folder")
    async def post(mailbox: Mailbox) -> Mailbox:
        await mailbox.create(user)
        return mailbox


@route("/folders/{folder}", tags=tags)
class MailboxDetailAPI:
    @staticmethod
    @description("Get all emails from folder")
    async def get(folder, user: User = Depends(user_perms)) -> List[EMail]:
        mailbox = await Mailbox.get(user, folder)
        emails = await mailbox.emails(user)
        return emails

    @staticmethod
    @description("Delete folder")
    async def delete(folder, user: User = Depends(user_perms)) -> Mailbox:
        mailboxes = await Mailbox.all(user)
        for mailbox in mailboxes:
            if mailbox.name == folder:
                await mailbox.delete(user)
                return mailbox
        raise HTTPException(status_code=409, detail="No such folder")


@route("/folders/{folder}/{id}", tags=tags)
class MailboxDetailAPI:
    @staticmethod
    @description("Get all emails from folder")
    async def get(folder, id: int, user: User = Depends(user_perms)) -> EMail:
        mailbox = await Mailbox.get(user, folder)
        email = await mailbox.email(user, id)
        return email
