import streamlit as st
import pandas as pd
import pke
from pke.unsupervised import MultipartiteRank, PositionRank

#データの読み込み
data = pd.read_csv("data.csv")

#テキスト化する
data_title = ""

for i in range(5):
    title = data.iloc[i, 2]
    data_title = data_title + title.replace(u"\xa0", u" ").replace("\n", "")


#position rank する
extractor_for_posi = pke.unsupervised.PositionRank()
extractor_for_posi.load_document(input=data_title, language='en')
extractor_for_posi.candidate_selection()
extractor_for_posi.candidate_weighting()
keyphrases_posi = extractor_for_posi.get_n_best(n=15)

posi_list = []

#空白ごとに切り分ける
for keyphrase in keyphrases_posi:

    try: 
        keyphrase_splits = keyphrase[0].split(" ")
        for keyphrase_split in keyphrase_splits:
            organnised_keyphrase = keyphrase_split.replace("、", "").replace("。", "").replace("「", "").replace("」", "").replace("？", "").replace("！", "")
            
            if organnised_keyphrase != "":
                posi_list.append(organnised_keyphrase)
    except:
        organnised_keyphrase = keyphrase[0].replace("、", "").replace("。", "").replace("「", "").replace("」", "").replace("？", "").replace("！", "")
        posi_list.append(organnised_keyphrase)

#以下見えるところ
###########################################################################

st.header("Keyphrase query in Japanese")

st.write("")
st.write("")
st.write("")


selected_keyphrases = st.multiselect("Select keyphrases", posi_list, default=None)


for selected_keyphrase in selected_keyphrases:
    st.write("Keyphrase: " + selected_keyphrase)
    data[data[" Title"].str.contains(selected_keyphrase)]
