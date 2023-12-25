"""
Copyright 2024 Maner·Fan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging

from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import OperationalError
from starlette.responses import JSONResponse

from utils.errors.base_error import BaseServiceError
from . import auth, system
from ..dependencies.principal import token_verify

log = logging.getLogger()


def register(app: FastAPI):
    """
    注册路由
    :param app:  FastAPI
    """

    app.include_router(system.setup.router, prefix='/api',
                       tags=['init | 初始化'])

    app.include_router(system.system.router, prefix='/api',
                       tags=['info | 系统信息'])

    app.include_router(auth.login.router, prefix='/api',
                       tags=['auth | 认证'])
    app.include_router(auth.users.router, prefix='/api/user',
                       dependencies=[Depends(token_verify)],
                       tags=['user | 用户'])


def exception_handler(app: FastAPI):
    """
    定义全局异常处理
    :param app:  FastAPI
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        """
        参数验证异常
        """
        log.warning('RequestValidationError %s, %s', exc.__class__, str(exc))
        return JSONResponse(exc.errors(), status_code=422)

    @app.exception_handler(BaseServiceError)
    async def service_exception_handler(request, exc: BaseServiceError):
        """
        业务异常
        """
        log.warning('ServiceError %s, %s', exc.__class__, exc.message)
        return JSONResponse({'message': exc.message, 'show_type': exc.show_type, 'target': exc.target}, status_code=exc.status_code)

    @app.exception_handler(OperationalError)
    async def sql_exception_handler(request, exc: OperationalError):
        """
        SQL数据库异常
        """
        log.exception('SQLError 服务异常 %s', str(exc))
        return JSONResponse({'message': '服务异常，请稍候重试'}, status_code=500)

    @app.exception_handler(Exception)
    async def common_exception_handler(request, exc: Exception):
        """
        其他系统异常
        """
        log.exception('ExceptionError 服务异常 %s', str(exc))
        return JSONResponse({'message': '服务异常，请稍候重试'}, status_code=500)
