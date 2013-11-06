#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config_sample as config
import re
from decimal import Decimal

msg_set = ''
M = config.imap4connection()
print M.select()
print M.recent()
typ, data = M.search(None, '(HEADER "X-SBRS" "-" UNSEEN)')
prog = re.compile('(?<=X\-SBRS:).+')
for num in data[0].split():
    typ, data = M.fetch(num, '(RFC822.HEADER)')
    m = prog.search(data[0][1])
    if m is not None:
        sbrs = Decimal(m.group(0))
        if sbrs <= Decimal('-4.0'):
            print str(num) + ':' + str(sbrs)
            msg_set += str(num) + ','
            # print 'Message %s\n%s\n' % (num, data[0][1])

if len(msg_set) > 0:
    msg_set = msg_set[:-1]

print msg_set
# print M.list()
M.copy(msg_set, 'INBOX.JunkMail')
M.store(msg_set, '+FLAGS', '\\Deleted')
# M.expunge()

M.close()
M.logout()
