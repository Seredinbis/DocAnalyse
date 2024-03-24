import pytesseract
import logging

from celery_module.celery_setup import app
from sql.psql import connect, DocumentText, Document
from PIL import Image

# получение пользовательского логгера и установка уровня логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# настройка обработчика и форматировщика
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)


@app.task
def doc_analyse(doc_id):
    try:
        logger.info('вошли в таску')
        with connect() as session:
            doc_path = session.query(Document.psth).filter(Document.id == int(doc_id)).scalar()
            if doc_path is not None:
                doc_text = session.query(DocumentText).filter(DocumentText.id_doc == int(doc_id)).one_or_none()
                if doc_text is None:
                    image = Image.open(doc_path)
                    text = pytesseract.image_to_string(image, lang='eng+rus')
                    session.add(DocumentText(id_doc=int(doc_id), text=text))
                    session.commit()
                    return 'Task completed'
                return 'Document in database'
            return 'File with this id not found'
    except BaseException as ex:
        logger.exception(f'{ex} не прошли')
