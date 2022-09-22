<!--
 Copyright 2022 Indoc Research
 
 Licensed under the EUPL, Version 1.2 or – as soon they
 will be approved by the European Commission - subsequent
 versions of the EUPL (the "Licence");
 You may not use this work except in compliance with the
 Licence.
 You may obtain a copy of the Licence at:
 
 https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
 
 Unless required by applicable law or agreed to in
 writing, software distributed under the Licence is
 distributed on an "AS IS" basis,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 express or implied.
 See the Licence for the specific language governing
 permissions and limitations under the Licence.
 
-->

# service_notification

## About
Manages emails and system maintenance notifications.
### Built With
- Python
- FastAPI
## Getting Started

### Prerequisites
- [Poetry](https://python-poetry.org/) dependency manager.
- Vault connection credentials or custom-set environment variables.

### Installation
#### Using Docker
1. Run Docker compose with environment variables.

       PIP_USERNAME=[...] PIP_PASSWORD=[...] docker-compose up

2. Find service locally at `http://localhost:5065/`.

#### Without Docker
1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Configure access to internal package registry.

       poetry config http-basic.pilot ${PIP_USERNAME} ${PIP_PASSWORD}

3. Install dependencies.

       poetry install

4. Add environment variables into `.env`.
5. Run application.

       poetry run python run.py

6. Find service locally at `http://localhost:5065/`.

Example:

```
poetry install
poetry run python run.py
CONFIG_CENTER_ENABLED=true VAULT_URL=[...] VAULT_CRT=[...] VAULT_TOKEN=[...] poetry run python run.py
```

## Usage
Swagger API documentation can be found locally at `http://localhost:5065/v1/api-doc`.

