from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from flair.data import Sentence
from flair.models import SequenceTagger

model_ = "ner-ontonotes"
# load the NER tagger
tagger = SequenceTagger.load(model_)

app = FastAPI()

class FLAIR_NER_MODEL(BaseModel):
    text: str



@app.get("/healthcheck")
async def healthcheck():
    return {"Hello": "World"}


@app.post("/ner")
async def getNamedEntities(body:FLAIR_NER_MODEL):
    text = body.text
    sentence = Sentence(text)
    tagger.predict(sentence)
    entities = dict()
    for entity in sentence.get_spans('ner'):
        if entity.tag not in entities.keys(): 
            entities[entity.tag] = [{"text": entity.text, 
                                     "start_position": entity.start_position, 
                                     "end_position": entity.end_position,
                                     "confidence": entity.score}]
        else:
            entities[entity.tag] += [{"text": entity.text, 
                                     "start_position": entity.start_position, 
                                     "end_position": entity.end_position,
                                     "confidence": entity.score}]
    return {"full_text": sentence.text, "entities": entities}



if __name__ == "__main__":
    uvicorn.run("ner_api.__main__:app", host="0.0.0.0", port=5002, log_level="info", reload=True)