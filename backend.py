from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.note import Note, Base
from fastapi.encoders import jsonable_encoder
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)


def recreate_database():
    Base.metadata.create_all(engine)


recreate_database()

app = FastAPI()


@app.get("/notes")
async def index():
    session = Session()
    notes = session.query(Note).all()
    result = jsonable_encoder({
        "notes": notes
    })
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": result
    })


@app.post("/notes")
async def create_note(title: str, content: str):
    session = Session()
    note = Note(
        title=title,
        content=content
    )
    session.add(note)
    session.commit()
    session.close()
    result = jsonable_encoder({
        "title": title,
        "content": content
    })
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "result": result
    })
