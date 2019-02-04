from Imap import Imap

imap = Imap('imap.gmail.com', 993, 'mrtinic489@gmail.com', 'Fcbljhf23Akbynjdyf2323')
print(imap._Socket.get_answer())
imap.login()
print(imap._Socket.get_answer())

imap.select_folder('INBOX')
print(imap._Socket.get_answer())

print(imap.check_folder())

print(imap.search_msg('ALL'))

print(imap.choose_msg(1, 'body'))

imap.close_folder()
print(imap._Socket.get_answer())

imap.logout()
print(imap._Socket.get_answer())