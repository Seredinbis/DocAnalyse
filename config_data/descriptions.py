from dataclasses import dataclass


@dataclass()
class Root:
    description: str = 'корень проекта сделан просто так'
    summary: str = 'Корень'


@dataclass()
class Upload:
    description: str = 'Апи принимает картинку в формате ,сохраняет ее на диск в папку DOCUMENTS и добавляет в базу' \
                       ' данных запись в таблицу Documents.'
    summary: str = 'Загрузка документов'


@dataclass()
class Upload:
    description: str = 'Апи принимает картинку в формате ,сохраняет ее на диск в папку DOCUMENTS и добавляет в базу' \
                       ' данных запись в таблицу Documents.'
    summary: str = 'Загрузка документов'


@dataclass()
class Delete:
    description: str = 'Апи принимает id документа и удаляет его из базы данных и с диска.'
    summary: str = 'Удаление документов'


@dataclass()
class Analyse:
    description: str = 'Апи принимает id документа и используя брокер сообщений Rabbitmq вызывает функцию очереди задач' \
                       ' celery для выполнения в фоновом режиме. В методе celery использует tesseract для получения' \
                       ' текста и записывает результат в таблицу Documents_text базы данных fastdoc.'
    summary: str = 'Анализ документов'


@dataclass()
class Text:
    description: str = 'Апи принимает id документа и возвращает текст из таблицы Document_text.'
    summary: str = 'Получение текста документов'
