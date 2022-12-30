from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import Float


'''
For each database model we create schemas, this will serve
as validator to check whether the sended data is a valid
data type
By specifying Optional we say that this field is not required
'''


class User(BaseModel):
    # id: int
    phone_number: int
    balance: Optional[float] = 0.00

    class Config:
        orm_mode = True


class Subscription(BaseModel):
    # id: int
    subscription_name: str
    subscription_price: float
    user_id: int

    class Config:
        orm_mode = True


class Service(BaseModel):
    # id: int
    service_name: str
    service_price: Optional[float] = Field(default=None)
    user_id: int

    class Config:
        orm_mode = True