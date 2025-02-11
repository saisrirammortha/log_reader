from fastapi import APIRouter, Response, status
import os
from app.config import LOG_DIRECTORY
from app.models import GetFilesResponse, Message

router = APIRouter()


@router.get("", responses={200: {"model":GetFilesResponse}, 500: {"model":Message}},
            description="This endpoint returns list of files in the log directory. "
                        "We can use search to filter the files. Right now the filter only supports substring matching")
async def get_files(response: Response, search: str = None):
    try:
        if not search:
            search = ""
        files = []

        for root, _, filenames in os.walk(LOG_DIRECTORY):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if search in filepath:
                    files.append(filepath)
        response.status_code = status.HTTP_200_OK
        return GetFilesResponse(
            files=files,
            count=len(files)
        )
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Message(message=str(e))


