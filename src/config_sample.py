#!/usr/bin/env python
# -*- coding: utf-8 -*-
import poplib
import imaplib


pop3server = "pop3.server.sample"
imap4server = "imap4.server.sample"
usernm = "info@server.sample"
passwd = "loginpassword"

def pop3connection():
    M = poplib.POP3(pop3server)
    M.user(usernm)
    M.pass_(passwd)
    return M

def imap4connection():
    M = imaplib.IMAP4(imap4server)
    M.login(usernm, passwd)
    return M

FROM_REGEXP = (
    )
