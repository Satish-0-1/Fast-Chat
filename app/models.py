import uuid
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import UUID,ForeignKey
from app.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import func

class Guest(Base):
    __tablename__ = 'guest'

    id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    name = Column(String,nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True),default=func.now(),nullable=True)
    updated_at = Column(DateTime(timezone=True),onupdate=func.now(),nullable=True)
    profile = relationship("Message", back_populates="user",cascade="all, delete-orphan")

    class config:
        orm_mode = True

class Message(Base):
    __tablename__ = 'messages'

    id = Column(UUID(as_uuid=True),primary_key=True, index=True,default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True),ForeignKey('guest.id'),nullable=False)
    chat = Column(String,nullable=True)
    send_at = Column(DateTime(timezone=True),default=func.now(),nullable=True)

    user = relationship("Guest", back_populates="profile")

    class config:
        orm_mode = True