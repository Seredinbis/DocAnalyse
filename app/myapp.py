import os
import config_data.descriptions as des

from fastapi import FastAPI, UploadFile
from sql.psql import connect, Document, DocumentText
from datetime import datetime as dt
from config_data.config import load_config
from celery_module.tasks import doc_analyse
from loguru import logger

app = FastAPI(title='api for upload and analyse docs')

abspath = os.path.abspath('../.env')

logger.add("./logs/myapp.log", format="{time} {level} {message}", level="INFO")


@app.post("/upload_doc", description=des.Upload.description, summary=des.Upload.summary)
def upload_doc(file: UploadFile):
    logger.info("Попытка загрузки документа")
    file_path = load_config(abspath).doc_path.path + file.filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        f.close()
    with connect() as ses:
        ses.add(Document(psth=file_path, date=dt.now().date()))
        ses.commit()
    logger.info("Документ успешно загружен")
    return {"message": "Документы успешно скачены"}


@app.delete("/doc_delete", description=des.Delete.description, summary=des.Delete.summary)
def delete_doc(doc_id: int):
    with connect() as ses:
        doc = ses.query(Document).filter(Document.id == doc_id).one_or_none()
        if doc is not None:
            path = doc.psth
            ses.delete(doc)
            ses.commit()
        else:
            return {"message": "Таких документов не существует"}
    if os.path.exists(path):
        os.remove(path)
    return {"message": "Документы успешно удалены"}


@app.patch("/doc_analyse", description=des.Analyse.description, summary=des.Analyse.summary)
def analyse_doc(doc_id: str):
    doc_analyse.delay(doc_id)
    return {"message": "OK"}


@app.get('/get_text', description=des.Text.description, summary=des.Text.summary)
async def get_text(doc_id: int):
    with connect() as session:
        text = session.query(DocumentText.text).filter(DocumentText.id_doc == doc_id).scalar()
        if text is None:
            return {'message': "Document not found, please use /doc_analyse"}
        return {'Text': text}
