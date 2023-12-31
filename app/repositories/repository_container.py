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

from dependency_injector import containers, providers

from . import data, oss, vector


class RepositoryContainer(containers.DeclarativeContainer):
    """
    数据容器
    """

    config = providers.Configuration()

    # data
    data_container: data.DataContainer = providers.Container(
        data.DataContainer,
        config=config,
    )

    # oss
    oss_container: oss.OssContainer = providers.Container(
        oss.OssContainer,
        config=config,
    )

    # vector
    vector_container: vector.VectorContainer = providers.Container(
        vector.VectorContainer,
        config=config,
    )
