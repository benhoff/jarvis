import os 
import poplib
from email import parser
pop_connection = poplib.POP3_SSL('pop.gmail.com')
recent_account =  'recent:jarvis.ai.para.ben@gmail.com'
# normal_email = 'jarvis.ai.para.ben@gmail.com'
pop_connection.user(recent_account)
pop_connection.pass_(os.getenv('JAR_EMAIL_PASS'))

messages = [pop_connection.retr(i) for i in range(1, len(pop_connection.list()[1]) + 1)]
print(messages)    
for index, mssg in enumerate(messages):
    information = mssg[1]
    result = []
    for item in information:
        item = item.decode('utf-8')
        print(item)
        result.append(item)
    #messages[index] = "\n".join(result)
    messages[index] = result
    print(messages[index])
"""
messages = [parser.Parser().parsestr(mssg) for mssg in messages]
for message in messages:
    print(message['subject'])

"""
for message in messages:
    sender = message[5]
    sender = sender[14:len(sender)-1]

    msg = message[-4]
    print(sender, msg)
pop_connection.quit()
