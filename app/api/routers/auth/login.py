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

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app_container import AppContainer
from services import AccountService

router = APIRouter()


@router.post('/login')
@inject
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        account_service: AccountService = Depends(
            Provide[AppContainer.service_container.account_service]
        ),
):
    """
    登录
    :param form_data: 登录提交的参数
    :param account_service: 账号服务
    :return:
    """
    return account_service.authenticate(form_data.username, form_data.password)


@router.get('/logout')
def logout():
    return
