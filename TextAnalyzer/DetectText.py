import spacy 
from spacy.lang.en.stop_words import STOP_WORDS


class DetectText:


    def detectTextIn(self,Text):
        classFromText=[]
        #Text=Text.lower()
        nlp = spacy.load('en_core_web_sm')
        # Adding Custom stop words 
        STOP_WORDS.add("picture")
        STOP_WORDS.add("image")
        STOP_WORDS.add("images")
        STOP_WORDS.add("pics")
        STOP_WORDS.add("portrait")
        for word in STOP_WORDS:
            lexeme = nlp.vocab[word]
            lexeme.is_stop = True
        
        uni_string=str(Text)
        doc = nlp(uni_string)
        for ent in doc.ents:
            print("====",ent.label_)
            classFromText.append(ent.label_)

        Text=Text.lower()
        uni_string=str(Text)
        doc = nlp(uni_string)
        
        for token in doc:
            # """token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            #       token.shape_, token.is_alpha, token.is_stop"""
                if not token.is_stop:
                    print(token.text,token.lemma_)
                    classFromText.append(token.lemma_)
                    classFromText.append(token.text)
                     
        classFromText=[a.lower() for a in classFromText]
        classFromText=set(classFromText)
        return classFromText
             


                


