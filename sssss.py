from Imap import Imap
import sys
print(sys.platform)

imap = Imap('imap.gmail.com', 993, 'mrtinic489@gmail.com', 'Fcbljhf23Akbynjdyf2323')
print(imap.login())





# print(imap.get_count_of_letters())
