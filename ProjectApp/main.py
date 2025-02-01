from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from model import *
from model import stvari
from model.cache import region
import logging

print("Im running")

app = FastAPI()

Base.metadata.bind = engine
Base.metadata.create_all(bind=engine)

class StvariBase(BaseModel):
    ime: str
    opis: str

    class Config:
        from_attributes = True

logging.basicConfig(level=logging.DEBUG)
# Get all items
@app.get("/")
async def read_items():
    db_stvari = session.query(stvari.Stvari).all()
    return db_stvari

@app.delete("/stvari/{id_stvari}")
async def remove_item(id_stvari: int):
    db_stvar = session.query(stvari.Stvari).get(id_stvari)
    if db_stvar:
        session.delete(db_stvar)
        session.commit()
        return JSONResponse(content={'message': f'Stvar sa ID {id_stvari} je izbrisana.'}, status_code=200)
    else:
        return JSONResponse(content={'message': f'Nema stvari s ID {id_stvari}.'}, status_code=404)

@app.get("/stvari/{id_stvari}")
async def read_item(id_stvari: int):
    db_stvar = region.get_or_create(
        f'Stvar:{id_stvari}',
            creator=lambda: session.query(stvari.Stvari).get(id_stvari),
            expiration_time=60
        )

    if db_stvar:
        return db_stvar
    else:
        return JSONResponse(content={'message': f'Nema stvari s ID {id_stvari}.'}, status_code=404)

@app.put("/stvari/{id_stvari}")
async def modify_item(id_stvari: int, stvar: StvariBase):
    db_stvar = session.query(stvari.Stvari).get(id_stvari)

    if db_stvar:
        db_stvar.ime = stvar.ime
        db_stvar.opis = stvar.opis
        session.commit()
        session.refresh(db_stvar)
        return db_stvar
    else:
        return JSONResponse(content={'message': f'Nema stvari s ID {id_stvari}.'}, status_code=404)


@app.post("/stvari/")
async def create_item(stvar: StvariBase):
    db_stvar = stvari.Stvari(**stvar.dict())
    session.add(db_stvar)
    session.commit()
    session.refresh(db_stvar)
    return JSONResponse(content={"message": "Dodana nova stvar u bazu."}, status_code=201)



