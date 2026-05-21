import uuid
from sqlalchemy import (
    Column, String, Numeric, Boolean, Integer,
    Text, TIMESTAMP, ForeignKey, Float, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.repository.database import Base


class ErrorLogSchema(Base):
    __tablename__ = "error_logs"

    error_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(Text, nullable=True)
    function_name = Column(Text, nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    created_by = Column(String(100), nullable=False, default="SYSTEM")
    updated_by = Column(String(100), nullable=True)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)