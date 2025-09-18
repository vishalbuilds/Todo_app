from enum import Enum
from typing import Any, Optional, TypeVar, Generic

T = TypeVar("T")


class ResultType(str, Enum):
    """
    Enumeration for all possible result statuses.
    """
    # Success
    SUCCESS = "success"
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"

    # Warnings
    WARNING = "warning"
    PARTIAL_SUCCESS = "partial_success"

    # Errors
    ERROR = "error"
    NOT_FOUND = "not_found"
    ALREADY_EXISTS = "already_exists"
    VALIDATION_FAILED = "validation_failed"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    INTERNAL_ERROR = "internal_error"
    CONFLICT = "conflict"


class Result(Generic[T]):
    """
    Represents the result of an operation.
    """

    def __init__(self, status: ResultType, data: Optional[T] = None, message: Optional[str] = None):
        self.status = status
        self.data = data
        self.message = message or f"{status.value.replace('_', ' ').capitalize()}"

    def __str__(self) -> str:
        return f"Status: {self.status.value}, Data: {self.data}, Message: {self.message}"

    # ---- Explicit factory methods ----
    @classmethod
    def success(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.SUCCESS, data=data, message=message)

    @classmethod
    def created(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.CREATED, data=data, message=message)

    @classmethod
    def updated(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.UPDATED, data=data, message=message)

    @classmethod
    def deleted(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.DELETED, data=data, message=message)

    @classmethod
    def warning(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.WARNING, data=data, message=message)

    @classmethod
    def partial_success(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.PARTIAL_SUCCESS, data=data, message=message)

    @classmethod
    def error(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.ERROR, data=data, message=message)

    @classmethod
    def not_found(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.NOT_FOUND, data=data, message=message)

    @classmethod
    def already_exists(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.ALREADY_EXISTS, data=data, message=message)

    @classmethod
    def validation_failed(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.VALIDATION_FAILED, data=data, message=message)

    @classmethod
    def unauthorized(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.UNAUTHORIZED, data=data, message=message)

    @classmethod
    def forbidden(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.FORBIDDEN, data=data, message=message)

    @classmethod
    def internal_error(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.INTERNAL_ERROR, data=data, message=message)

    @classmethod
    def conflict(cls, data: Optional[T] = None, message: Optional[str] = None) -> "Result[T]":
        return cls(ResultType.CONFLICT, data=data, message=message)
