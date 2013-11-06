#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import string
import email
import re
from decimal import Decimal
from email.header import decode_header

import config_sample as config


pop3server = config.pop3server
usernm = config.usernm
passwd = config.passwd


class MngMail:
    def __init__( self, strmsg):
        self.header_from = ''
        self.header_sbrs = 0
        frmMail = email.message_from_string(strmsg)
        for part in frmMail.walk():
            if part.has_key("From"):
                listfrom = []
                fromName = decode_header(part.get("From"))
                for f in fromName:
                    if f[1] != None:
                        try:
                            listfrom.append(f[0].decode(f[1]).encode("utf-8"))
                        except:
                            print sys.exc_info()[0]
                    else:
                        listfrom.append(f[0])
                self.header_from = ''.join(listfrom)
            if part.has_key("X-SBRS"):
                xsbrs = [s[0] for s in decode_header(part.get("X-SBRS"))]
                if xsbrs[0] != 'None':
                    self.header_sbrs = Decimal(xsbrs[0])

        print self.header_from
        print self.header_sbrs


class FilterMail:
    def __init__(self, parent=None):
        self.__parent = parent
    def handle(self, mail):
        result = ''
        if hasattr( self, 'check' ):
            method = getattr( self, 'check')
            result = method(mail)
        if result in ['noop', ''] and self.__parent:
            return self.__parent.handle( mail )
        return result


class FromFilter( FilterMail ):
    def check (self, mail):
        for pattern in config.FROM_REGEXP:
            if re.search(pattern, mail.header_from) != None:
                return 'dele'
                break

        return 'noop'


class SBRSFilter( FilterMail ):
    def check (self, mail):
        # 'X-SBRS' ヘッダが -4.0 以下の場合、spam
        if mail.header_sbrs <= -4.0:
            return 'dele'

        return 'noop'


M = config.pop3connection()
numMsgs = len(M.list()[1])
numFrom = 0
if numMsgs > 50:
    numFrom = numMsgs - 50
deleCount = 0

for i in range(numFrom, numMsgs):
    mailseq = i+1
    strmsg = string.join(M.retr(mailseq)[1], "\n")
    print "-------("+str(i)+")-------"
    result = ''
    mng_mail = MngMail(strmsg)
    from_filter = FromFilter()
    sbrs_filter = SBRSFilter(from_filter)
    result = sbrs_filter.handle(mng_mail)

    # if part.get_content_type() == "text/plain":
    #     print part.get_payload().decode("iso-2022-jp").encode("utf-8")
    print result
    if result == 'dele':
        M.dele(mailseq)
        deleCount += 1

M.quit()
print "delete:" + str(deleCount)
