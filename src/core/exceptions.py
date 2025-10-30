from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback

class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            error_detail = {
                "error": str(e),
                "path": request.url.path,
                "trace": traceback.format_exc().splitlines()[-3:]  # last few lines for debug
            }
            return JSONResponse(status_code=500, content=error_detail)
