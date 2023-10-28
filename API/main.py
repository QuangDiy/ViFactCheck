from fastapi import FastAPI
from pydantic import BaseModel
import torch
from torch import nn
from transformers import AutoTokenizer, AutoModel
import psycopg2
from BM25_Postgresql import search_bm25
from Sematic_BM25 import similarities
from typing import List
from torch.utils.data import Dataset, DataLoader
from fastapi.middleware.cors import CORSMiddleware
import time
import numpy as np
from underthesea import word_tokenize

#Class PhoBERT
class PhoBERTClassifier(nn.Module):
    def __init__(self, phobert, num_classes):
        super(PhoBERTClassifier, self).__init__()
        self.phobert = phobert
        self.dropout = nn.Dropout(0.2)
        self.linear = nn.Linear(self.phobert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        #Roberta layer
        _, pooled_output = self.phobert( input_ids=input_ids, attention_mask=attention_mask, return_dict=False,)
        #nn classification layer
        dropout_output = self.dropout(pooled_output)
        logits = self.linear(dropout_output)
        return logits

# # Load tokenizer and model
device = torch.device("cpu")
phobert = AutoModel.from_pretrained("vinai/phobert-large")
model_path = "./model/model2"
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-large")
model =  PhoBERTClassifier(phobert,3)
model.load_state_dict(torch.load(model_path,map_location=device))
model.to(device)


    
app = FastAPI(
    title="Fact Checking on News",
    description="""Enter the information to be verified, and the result 
                    will be the label of the information to be verified and the related news.""",
    version="0.0.1",
)

# Set up CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's origin(s)
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Fact Check"}


class FactCheckRequest(BaseModel):
    statement: str


class FactCheckResponse(BaseModel):
    label: str
    url: str
    evidence: List[str]
    softmax: str

class SentencePairDataset(Dataset):
    def __init__(self, sentence_pairs1,sentence_pairs2, tokenizer, max_length):
        self.sentence_pairs1 = sentence_pairs1
        self.sentence_pairs2 = sentence_pairs2

        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.sentence_pairs1)

    def __getitem__(self, idx):
        sentence1 = self.sentence_pairs1
        sentence2 = self.sentence_pairs2
        encoding = self.tokenizer.encode_plus(
            sentence1,
            text_pair=sentence2,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding="max_length",
            return_attention_mask=True,
            return_tensors="pt",
            truncation=True,
        )
        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
        }

# Define prediction route
@app.post("/predict", response_model = FactCheckResponse)
# async def predict(request: FactCheckRequest, model = model, tokenizer = tokenizer):
async def predict(request: FactCheckRequest):

    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="vfc-news",
        user="postgres",
        password="tranquangduy1810"
    )
    
    statement = request.statement

    # st = time.time()
    # print("Time search respone", time.time() - st)
    context, url = search_bm25(statement, connection)

    evidence_top_k = similarities(context, statement)
    evi = ' '.join(evidence_top_k)

    #Word token
    statement = word_tokenize(statement, format="text")
    evi = word_tokenize(evi, format="text")
    ct = word_tokenize(context, format="text")

    # url = request_url(context, connection)

    model.eval()

    input_ids = []
    attention_mask = []

    encoding = tokenizer.encode_plus(
        statement,
        text_pair = ct,
        add_special_tokens=True,
        max_length=256,
        return_token_type_ids=False,
        padding="max_length",
        return_attention_mask=True,
        return_tensors="pt",
        truncation=True,
    )

    input_ids.append(encoding["input_ids"].flatten())
    attention_mask.append(encoding["attention_mask"].flatten())

    input_ids = torch.stack(input_ids).to(device)
    attention_mask = torch.stack(attention_mask).to(device)
    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        # logits = ouxtputs.logits 
        softmax =  torch.softmax(outputs, dim=1)
        predicted_class =  torch.argmax(softmax, dim=1).item()
        max_softmax, argmax_softmax = torch.max(softmax, dim=1)
        
    if predicted_class == 0: predicted_class = "Support"
    elif predicted_class == 1: predicted_class = "Refuted"
    else: predicted_class = "NEI"
    

    # softmax = np.random.randint(60, 86)
    # return FactCheckResponse(label = predicted_class, url = url, evidence = evidence_top_k)
    return FactCheckResponse(label = predicted_class, url = url, evidence = evidence_top_k, softmax = str(round(max_softmax.item()*100)))


# python -m uvicorn main:app --reload
# http://127.0.0.1:8000/docs


