# importing dependencies
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


# User model with required fields
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(Integer, unique=True)
    balance = Column(Float, nullable=False)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'), nullable=False)
    subscription = relationship('Subscription', back_populates='users')
    service_id = Column(Integer, ForeignKey('services.id'), nullable=True)
    service = relationship('Service', back_populates='users')

    def __repr__(self):
        return f'<User {self.id}>'


# Subscription model with required fields
class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    subscription_name = Column(String, nullable=False)
    subscription_price = Column(Integer, nullable=False)
    users = relationship('User', back_populates='subscription')

    def __repr__(self):
        return f'<Subscription {self.subscription_name}>'


# Service model with required fields
class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    service_name = Column(String, index=True, nullable=False)
    service_price = Column(Integer, nullable=False)
    users = relationship('User', back_populates='service')

    class Config:
        orm_mode = True

    def __repr__(self):
        return f'<Service {self.service_name}>'
