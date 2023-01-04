from pydantic import BaseModel, Field
from typing import Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Float


'''
For each database model we create schemas, this will serve
as validator to check whether the sended data is a valid
data type
By specifying Optional we say that this field is not required
'''


class User(BaseModel):
    phone_number: int
    balance: float
    subscription_id: int
    service_id: int

    class Config:
        orm_mode = True


class Subscription(BaseModel):
    subscription_name: str
    subscription_price: float

    class Config:
        orm_mode = True


class Service(BaseModel):
    service_name: str
    service_price: float

    class Config:
        orm_mode = True