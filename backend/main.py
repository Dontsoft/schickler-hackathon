from joblib import load

from fastapi import FastAPI
from sklearn.svm import LinearSVC
from pydantic import BaseModel
from typing import Union
import pandas as pd

app = FastAPI()

svm = load("LocalModel.joblib")

# Calculate text complexity using rounded ARI
def ARI(text):
    score = 0.0 
    len1, len2, len3 = len(text), len(text.split()), len(text.split('.'))
    if len(text) > 0 and len2 > 0 and len3 > 0:
        score = round(4.71 * (len1 / len2 ) +  0.5 * ( len2 / len3) - 21.43)
    return score if score > 0 else 0


class RequestItem(BaseModel):
    is_plus_article: Union[bool, None] = False
    is_dpa: Union[bool, None] = False
    pad_pleasure: Union[float, None] = 0.3
    pad_arousal: Union[float, None] = -0.16
    pad_dominance: Union[float, None] = -0.09
    preview_pad_pleasure: Union[float, None] = 0.3
    preview_pad_arousal: Union[float, None] = -0.2
    preview_pad_dominance: Union[float, None] = -0.02
    emo_aerger: Union[float, None] = 0.13
    emo_erwarten: Union[float, None] = 0.0
    emo_ekel: Union[float, None] = -0.014
    emo_furcht: Union[float, None] = 0.035
    emo_freude: Union[float, None] = 0.166
    emo_traurigkeit: Union[float, None] = -0.179
    emo_ueberraschung: Union[float, None] = -0.019
    emo_vertrauen: Union[float, None] = -0.02
    preview_emo_aerger: Union[float, None] = 0.0
    preview_emo_erwarten: Union[float, None] = 0.0
    preview_emo_ekel: Union[float, None] = -0.022
    preview_emo_furcht: Union[float, None] = 0.0
    preview_emo_freude: Union[float, None] = 0.24733
    preview_emo_traurigkeit: Union[float, None] = -0.09
    preview_emo_ueberraschung: Union[float, None] = -0.0188
    preview_emo_vertrauen: Union[float, None] = 0.0
    article_header_contains_quote: Union[bool, None] = False
    article_header_contains_question: Union[bool, None] = False
    article_header_contains_doppelpunkt: Union[bool, None] = False
    article_header_contains_pronoun_writer: Union[bool, None] = False
    article_header_contains_pronoun_reader: Union[bool, None] = False
    article_preview_contains_quote: Union[bool, None] = False
    article_preview_contains_question: Union[bool, None] = False
    article_preview_contains_doppelpunkt: Union[bool, None] = True
    article_preview_contains_pronoun_writer: Union[bool, None] = True
    article_preview_contains_pronoun_reader: Union[bool, None] = False
    topic: str
    locality : str
    newstype :str
    genre: str
    full_text: str
    portal_id: str


# portal_id ['portal_1' 'portal_31' 'portal_17' 'portal_3' 'portal_2']
# topic: ['Vermischtes: Gesundheit' 'Justiz/Kriminalität' 'Vermischtes: Religion'
#  'Vermischtes: Soziales' 'Verkehr/Infrastruktur' '' 'Kultur'
#  'Vermischtes: Sonstiges' 'Vermischtes: Leute' 'Wirtschaft: Unternehmen'
#  'Vermischtes: Freizeit/Hobbys' 'Sport: Fußball' 'Politik'
#  'Katastrophe/Unglück' 'Sport: Nicht-Fußball' 'Vermischtes: Wissenschaft'
#  'Bildung/Erziehung' 'Wirtschaft: Verbraucher']
# locality: ['National' 'Lokal (Lokalausgabe)' 'Regional (Verbreitungsgebiet)' ''
#  'International']
# newstype: ['News to Know' 'News to Entertain' '' 'News to Use']
# genre: ['Nachrichten/Bericht' 'Meinung' 'Ratgeber/Service' ''
#  'Reportage/Storytelling' 'Kurzmeldung' 'Porträt' 'Interview'
#  'Newsblog/Ticker']

PORTAL_VALUES = ['portal_1', 'portal_31', 'portal_17', 'portal_3', 'portal_2']
PORTAL_PREFIX = 'portal_id_'
PORTAL_COL = lambda x : f"{PORTAL_PREFIX}{x}"
TOPIC_VALUES = ['Vermischtes: Gesundheit', 'Justiz/Kriminalität','Vermischtes: Religion', 'Vermischtes: Soziales', 'Verkehr/Infrastruktur', '',  'Kultur', 'Vermischtes: Sonstiges', 'Vermischtes: Leute', 'Wirtschaft: Unternehmen', 'Vermischtes: Freizeit/Hobbys','Sport: Fußball','Politik', 'Katastrophe/Unglück', 'Sport: Nicht-Fußball', 'Vermischtes: Wissenschaft', 'Bildung/Erziehung', 'Wirtschaft: Verbraucher']
TOPIC_PREFIX = 'topic_'
TOPIC_COL = lambda x : f"{TOPIC_PREFIX}{x}"
LOCALITY_VALUES = ['National', 'Lokal (Lokalausgabe)', 'Regional (Verbreitungsgebiet)', '', 'International']
LOCALITY_PREFIX = 'locality_'
LOCALITY_COL = lambda x : f"{LOCALITY_PREFIX}{x}"
NEWS_TYPE_VALUE = ['News to Know', 'News to Entertain', '', 'News to Use']
NEWS_TYPE_PREFIX = 'newstype_'
NEWS_TYPE_COL = lambda x : f"{NEWS_TYPE_PREFIX}{x}"
GENRE_VALUE = ['Nachrichten/Bericht', 'Meinung', 'Ratgeber/Service', '', 'Reportage/Storytelling', 'Kurzmeldung', 'Porträt', 'Interview', 'Newsblog/Ticker']
GENRE_PREFIX = 'genre_'
GENRE_COL = lambda x : f"{GENRE_PREFIX}{x}"

@app.post("/")
async def root(data : RequestItem):
    
    _ari = ARI(data.full_text)
    _dict = data.dict()
    print(_dict)
    df = pd.DataFrame(_dict, index=[0])
    df["ARI"] = _ari
    for v in TOPIC_VALUES:
        df[TOPIC_COL(v)] = v == data.topic
    for v in LOCALITY_VALUES:
        df[LOCALITY_COL(v)] = v == data.locality
    for v in NEWS_TYPE_VALUE:
        df[NEWS_TYPE_COL(v)] = v == data.newstype
    for v in GENRE_VALUE:
        df[GENRE_COL(v)] = v == data.genre
    for v in PORTAL_VALUES:
        df[PORTAL_COL(v)] = v == data.portal_id
    df = df.drop(columns=["topic", "locality", "newstype", "genre", "full_text", "portal_id"])
    print(df.columns)

    prediction = svm.predict(df)
    print(prediction)
    return {
        "value": int(prediction[0])
    }
