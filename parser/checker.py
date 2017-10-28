from autocorrect import spell

def spellings(query):
    sent=" "
    for w in (query.strip()).split(" "):
        sent=sent+spell(w)+ " "
    return sent.strip()