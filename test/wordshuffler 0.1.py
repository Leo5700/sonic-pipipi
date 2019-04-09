import random
import time

def wordshuffler(string):
    string1 = ''
    for s in string.split():
        if len(s) > 1:
            smid = s[1:-1]
            s1 = s[0] + ''.join(random.sample(smid,len(smid))) + s[-1]
        else:
            s1 = s
        string1 += s1 + ' '
    return string1

print('-' * 80)

text = 'полагаю чтение текста у которого пляшут буквально все буквы не должно вызывать особых затруднений'
while True:
    print(wordshuffler(text), end="\r", flush=True)
    time.sleep(0.05)
