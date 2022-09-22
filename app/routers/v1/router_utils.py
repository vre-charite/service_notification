# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

from pydantic import BaseModel

from app.models.base_models import APIResponse
from app.models.sql_announcement import Base


def paginate(params: BaseModel, api_response: APIResponse, items: Base):
    total = items.count()
    items = items.limit(params.page_size).offset(params.page * params.page_size)
    items = items.all()
    results = []
    for item in items:
        results.append(item.to_dict())
    api_response.page = params.page
    api_response.num_of_pages = int(int(total) / int(params.page_size))
    api_response.total = total
    api_response.result = results
