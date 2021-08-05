from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from repository import schemas, models
from hashing import Hash
from sqlalchemy.orm import Session
from database import get_db
from typing import List
import oauth2, JWTtoken

user_router = APIRouter(prefix='/user',
                        tags=['Users'])

authentication_router = APIRouter(prefix='/user',
                        tags=['Authentication'])

task_router = APIRouter(
    prefix="/task",
    tags=['Tasks']
)

@user_router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create(request: schemas.User, db:Session = Depends(get_db)):

    try:
        request.password = Hash.bcrypt(request.password)
        new_user = models.User(**request.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
    except:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                            detail=f'some error occured while creating the user')
    return new_user

@user_router.get('/{id}',response_model=schemas.ShowUser, status_code=status.HTTP_302_FOUND)
def show(id: int, db:Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with user ID : {id} not found.')
    db.close()
    return user

@authentication_router.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.name == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = JWTtoken.create_access_token(data={"sub": user.name, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@task_router.get('/', response_model=List[schemas.ShowTask])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    if len(tasks) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No tasks created by current user.")
    db.close()
    return tasks

@task_router.post('/', status_code=status.HTTP_201_CREATED,)
def create(request: schemas.Task,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    request.user_id = current_user.id
    new_task = models.Task(**request.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()
    return new_task

@task_router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id:int,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == id)

    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {id} not found")
    
    if task.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with the id {id} not created by current user.")

    task.delete(synchronize_session=False)
    db.commit()
    db.close()
    return {'message':'deleted'}

@task_router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int,request:schemas.UpdateTask, db: Session = Depends(get_db),
            current_user: schemas.User = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == id)
    # if task.first().user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Task with id {id} not created by current user.")
    if not task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {id} not found")
    if task.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {id} not created by current user.")

    task.update(request)
    db.commit()
    db.close()
    return 'updated'

@task_router.get('/{id}', status_code=200, response_model=schemas.ShowTask)
def show(id:int,db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with the id {id} is not available")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with the id {id} not created by current user.")
    db.close()
    return task