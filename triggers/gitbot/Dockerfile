# --------------------------------------------------------------------------------------------------------
FROM python:3.9.6-slim-buster as build

COPY dev-requirements.txt .
COPY requirements.txt .

# install dependencies to the user install directory (typically ~/.local/)
RUN pip install --user -r dev-requirements.txt

# --------------------------------------------------------------------------------------------------------

FROM python:3.9.6-slim-buster as base

WORKDIR /triggers/gitbot

# Copy dependencies installation to this image
COPY --from=build /root/.local /root/.local

# Copy code
COPY . .

# update PATH environment variabl
ENV PATH=/root/.local/bin:$PATH

# --------------------------------------------------------------------------------------------------------

FROM base as continuous-integration
# Lint

# vunerabilities
# yet to be decided what to use

# Unit tests
RUN pytest tests/unit/

# Integration tests
# python -m pytest tests/integration/