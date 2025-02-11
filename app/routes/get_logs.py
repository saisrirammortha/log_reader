import os
from fastapi import APIRouter, Response, status

from app.config import LOG_DIRECTORY
from app.models import LogsResponse, Message

router = APIRouter()


@router.get("", responses={500: {"model": Message}, 400: {"model": Message},
                           404: {"model": Message}, 200: {"model": LogsResponse}},
            description="This endpoint returns the logs for a file."
                        "We can use entries to specify the number of latest log lines to return. "
                        "We can use chunk_size to specify the number of bytes to read at a time. "
                        "We can use prefix to filter the logs.Rightnow the filter only supports substring matching. "
            )
async def get_logs(file_name: str, response: Response, entries: int = 10, prefix: str = None, chunk_size: int = 1024):
    try:
        if not file_name.startswith(LOG_DIRECTORY):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Message(message=f"File name doesn't start with {LOG_DIRECTORY}")
        if prefix is None:
            prefix = ""
        if not os.path.exists(file_name):
            response.status_code = status.HTTP_404_NOT_FOUND
            return Message(message=f"File {file_name} doesn't exist")
        with open(file_name, "rb") as f:
            f.seek(0, 2)  # Move to the end of the file
            size = int(f.tell())
            buffer = bytearray()
            lines = []
            while size > 0 and len(lines) <= entries:
                size = max(0, size - chunk_size)
                f.seek(size)
                buffer[:0] = f.read(1024)
                lines = buffer.split(b"\n")[-entries:]
            logs = [line.decode() for line in lines]
            logs = [log for log in logs if prefix in log]
            return LogsResponse(
                logs=logs,
                line_count=len(logs)
            )
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Message(message=str(e))
        # return Message(message=str(traceback.format_exc()))