from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import schemas, model
from database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


todo = {

    1: {'task', 'wash toilet'},
    2: {'task', 'prepare for interview'},
    3: {'task', 'upload to github'},
    4: {'task', 'run fastapi'}
}


@app.get("/hello")
def hello():
    return 'Hello world'


@app.get("/")
def getItems():
    return todo


# getting all the task
@app.get("/")
def getList(session: Session = Depends(get_session)):
    items = session.query(model.Item).all()
    return items


# adding a new task
@app.post("/")
def addList(item: schemas.Todo, session=Depends(get_session)):
    item = model.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


# retrieve a single item
@app.get("/{id}")
def getItem(id: int, session: Session = Depends(get_session)):
    item = session.query(model.Item).get(id)
    return item


# updating a new task
@app.put("/{id}")
def updateItem(id: int, item: schemas.Todo, session=Depends(get_session)):
    itemObject = session.query(model.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject


# deleting a new task
@app.delete("/{id}")
def deleteItem(id: int, session=Depends(get_session)):
    itemObject = session.query(model.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted'
