from pydantic import BaseModel


class GetFilesResponse(BaseModel):
    files: list[str]
    count: int


class LogsResponse(BaseModel):
    logs: list[str]
    line_count: int


class Message(BaseModel):
    message: str


