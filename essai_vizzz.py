import json
import pandas as pd
import json

with open('/Users/ppx/Desktop/M2\ DS/data_viz/TP/TP_note/liste_json', 'r') as data_file:
    json_data = data_file.read()

data = json.loads(json_data)

with open('/Users/ppx/Desktop/M2\ DS/data_viz/TP/TP_note/votant.textile', 'r') as data_file:
    json_data = data_file.read()

votant = json.loads(json_data)

longueur = len(data)
annee = '15'
data_voulue = []
for x in range(longueur):
    annee_locale = list(data[x]['dateScrutin'])
    annee_locale = annee_locale[2] + annee_locale[3]
    if annee_locale == annee:
        event = data[x]
        event['dateScrutin'] = annee_locale
        data_voulue.append(event)

liste_id = []

acteur = votant['export']['acteurs']['acteur']
longueur_acteur = len(acteur)

for x in range(longueur_acteur):
    liste_id.append(acteur[x]['uid']['#text'])

df = pd.DataFrame(0,index = liste_id, columns = liste_id)


essai_bis = 2
         


def liste_pour_contre_vote(vote):
    liste_pour = []
    liste_contre = []
    groupe = vote['ventilationVotes']['organe']['groupes']['groupe']
    for x in range(0,7):
        pour = groupe[x]['vote']['decompteNominatif']['pours']
        if not pour == None:
            if type(pour['votant']) == list:
                for _votant in pour['votant']:
                    liste_pour.append(_votant['acteurRef'])

            elif type(pour['votant']) == dict:
                liste_pour.append(pour['votant']['acteurRef'])

        contre = groupe[x]['vote']['decompteNominatif']['contres']
        if not contre == None:
            if type(contre['votant']) == list:
                for _votant in contre['votant']:
                    liste_contre.append(_votant['acteurRef'])

            elif type(contre['votant']) == dict:
                liste_contre.append(contre['votant']['acteurRef'])

    return [liste_pour,liste_contre]



k = 0
for vote in data_voulue:
    listes = liste_pour_contre_vote(vote)
    liste_pours = listes[0]
    liste_contres = listes[1]

    for x in liste_pours:
        for y in liste_pours:
            df[x][y] += 1
    for x in liste_contres:
        for y in liste_contres:
            df[x][y] += 1
    k+=1
    print(k)



for x in liste_id:
    if max(df[x]) < 19:
        df = df.drop(x,axis=1)
        df = df.drop(x,axis=0)

df.to_csv('/Users/ppx/Desktop/M2\ DS/data_viz/TP/TP_note/tp_dviz.csv')
df.to_json('/Users/ppx/Desktop/M2\ DS/data_viz/TP/TP_note/tp_dviz.json')


result = dict()

colnames = df.columns
colnames = sorted(colnames)
result['nodes'] = []

groupe = data_voulue[0]['ventilationVotes']['organe']['groupes']['groupe']
liste_groupe = []
for col in colnames:
    allez = sorted(df[col], reverse = True)
    if allez[1] > 20:
        event = dict()
        event['id'] = col
        ok= False
        for x in range(0,7):
            ##print(groupe[x]['vote']['decompteNominatif'])
            for typevote in ['pours', 'contres', 'abstentions', 'nonVotants']:
                if groupe[x]['vote']['decompteNominatif'][typevote] == None:
                    pass
                elif type(groupe[x]['vote']['decompteNominatif'][typevote]) == dict:
                    if type(groupe[x]['vote']['decompteNominatif'][typevote]['votant']) == dict:
                        if groupe[x]['vote']['decompteNominatif'][typevote]['votant']['acteurRef'] == col:
                            liste_groupe.append(x)
                            ok = True
                    else:
                        for votant in groupe[x]['vote']['decompteNominatif'][typevote]['votant']:
                            if votant['acteurRef'] == col:
                                liste_groupe.append(x)
                                ok = True
        if ok == True:
            event['group'] = liste_groupe[-1]
        else:
            event['group'] = 99



        result['nodes'].append(event)
    
result['links'] = []
for col in colnames:
    for coli in colnames:
        if col < coli and df[col][coli] > 20:
            event = dict()
            event['source'] = col
            event['target'] = coli
            event['value'] = str(df[col][coli])
            result['links'].append(event)

j = json.dumps(result)
f = open("/Users/ppx/Desktop/M2\ DS/data_viz/TP/TP_note/allez.json","w")
f.write(j)
f.close()

 
"""
count = 0

longueur_liste_id = len(liste_id)
for i in range(0,longueur_liste_id):
    for j in range(i+1, longueur_liste_id):
        vote0 = meme_vote(data_voulue[0],liste_id[i],liste_id[j])
        if vote0[0]:
            df[liste_id[i]][liste_id[j]] += 1
            count += 1
        for k in range(1,len(data_file)):
            vote0 = meme_vote(data_voulue[k],liste_id[i],liste_id[j],g1 = vote0[1],g2 = vote0[2])
            if vote0[0]:
                df[liste_id[i]][liste_id[j]] += 1
                count += 1
"""