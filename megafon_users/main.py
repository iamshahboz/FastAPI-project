# import dependencies
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI(
    title="Megafon project API",
    description="You will find all available API here")

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD for Subscription model
# api to get all subscriptions
@app.get('/subscriptions', status_code=status.HTTP_200_OK, tags=['subscriptions'])
async def all_subscriptions(db: Session = Depends(get_db)):
    subscriptions = db.query(models.Subscription).all()
    return subscriptions


# api to get the subscription by id
@app.get('/subscription/{id}', status_code=status.HTTP_200_OK, tags=['subscriptions'])
async def get_subscription(id, response: Response, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(models.Subscription.id == id).first()
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Subscription with an id {id} is not available')
    return subscription


# api to create a subscription
@app.post('/subscription', status_code=status.HTTP_201_CREATED, tags=['subscriptions'])
async def create_subscription(request: schemas.Subscription, db: Session = Depends(get_db)):
    new_subscription = models.Subscription(subscription_name=request.subscription_name,
                                           subscription_price=request.subscription_price)
# if we don't add and commit the query to the db it will not be added
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription


# this endpoint is for updating the specific subscription
@app.put('/subscription/{id}', status_code=status.HTTP_200_OK, tags=['subscriptions'])
async def update_subscription(id, request: schemas.Subscription, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(models.Subscription.id == id)
    if not subscription.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Subscription with id {id} not found')
    subscription.update(request.dict())
    db.commit()
    return "the subscription updated sucessfully"


# this is for deleting
@app.delete('/subscription/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['subscriptions'])
async def delete_subscription(id, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(models.Subscription.id == id)
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Subscription with id {id} not found')
    subscription.delete(synchronize_session=False)
    db.commit()
    return f'subscription with id {id} deleted sucessfully'


# CRUD for Service model
@app.get('/services', status_code=status.HTTP_200_OK, tags=['services'])
async def all_services(db: Session = Depends(get_db)):
    services = db.query(models.Service).all()
    return services


# get specific service by id
@app.get('/service/{id}', status_code=status.HTTP_200_OK, tags=['services'])
async def get_service(id, response: Response, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Service with an id {id} is not available')
    return service


# create a new service
@app.post('/service', status_code=status.HTTP_201_CREATED, tags=['services'])
async def create_service(request: schemas.Service, db: Session = Depends(get_db)):
    new_service = models.Service(service_name=request.service_name,
                                 service_price=request.service_price)
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


# update the existing service
@app.put('/service/{id}', status_code=status.HTTP_200_OK, tags=['services'])
async def update_service(id, request: schemas.Service, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Service with id {id} not found')
    service.update(request.dict())
    db.commit()
    return "the service updated sucessfully"


# delete the service
@app.delete('/service/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['services'])
async def delete_service(id, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Service with id {id} not found')
    service.delete(synchronize_session=False)
    db.commit()
    return f'Service with id {id} deleted sucessfully'


# CRUD for User model
# to get all users
@app.get('/users', status_code=status.HTTP_200_OK, tags=['users'])
async def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


# get specific user by id
@app.get('/user/{id}', status_code=status.HTTP_200_OK, tags=['users'])
async def get_user(id, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with an id {id} is not available')
    return user


# create a new user
@app.post('/user', status_code=status.HTTP_201_CREATED, tags=['users'])
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    subscription = db.query(models.Subscription).filter(models.Subscription.id == request.subscription_id).first()
    if request.balance >= subscription.subscription_price:
        new_balance = request.balance - subscription.subscription_price
        new_user = models.User(phone_number=request.phone_number,
                               balance=new_balance,
                               subscription_id=request.subscription_id,
                               service_id=request.service_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,
                            detail=f'{"You dont have enough balance"}')


# update user
@app.put('/user/{id}', status_code=status.HTTP_200_OK, tags=['users'])
async def update_user(id, request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found')
    user.update(request.dict())
    db.commit()
    return "the user updated sucessfully"


# delete the user
@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
async def delete_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id {id} not found')
    user.delete(synchronize_session=False)
    db.commit()
    return f'User with id {id} deleted sucessfully'