###############################################
# Base Image
###############################################

ARG BASE_IMAGE=registry.gitlab.com/acceso/dive.tech/platform/base-images/python-poetry-image
ARG BASE_TAG=0.8.0

FROM ${BASE_IMAGE}:${BASE_TAG}

LABEL maintainer="Dive <it@dive.tech>"

ARG DIVE_PYPI_TOKEN

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential \
    jq

# copy project requirement files here to ensure they will be cached.
COPY poetry.lock pyproject.toml ./

RUN poetry config http-basic.dive-pypi DIVE_TECH_PYPI_TOKEN ${DIVE_PYPI_TOKEN}

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry config virtualenvs.create false \
    && poetry install

# Add app
WORKDIR /usr/src/app
COPY . .

# Apply migrations
ENTRYPOINT [ "poetry", "run", "alembic", "upgrade", "head"]
