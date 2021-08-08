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

#RUN set -o allexport; source <(cat eva-cicd_env | sed -e '/^#/d;/^\s*$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g"); set +o allexport

#RUN (cat eva-cicd_env | sed -e '/^#/d;/^\s*$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g") >> /etc/environment

#RUN sed -e '/^#/d;/^\s*$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g" -e 's/^/export /' -i eva-cicd_env

#CMD ["bash"]

# Lint
# pylint, flake8, bandit
RUN pylint bot
RUN pylint tests
RUN flake8 --append-config=.flake8 bot
RUN flake8 --append-config=.flake8 tests
RUN bandit -c .bandit -r bot
RUN bandit -c .bandit -r tests

# vulnerabilities
# yet to be decided what to use


SHELL ["/bin/bash", "-c"]
# Unit tests
RUN source eva-cicd_env; pytest tests/unit/
SHELL ["/bin/sh", "-c"]

# Integration tests
# python -m pytest tests/integration/

CMD ["echo", "Finished"]