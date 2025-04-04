FROM registry.wildfireworkspace.com/eop/streamlit-1.0/toolbox-base:latest AS base
WORKDIR /datatoolbox

# Copy utils over
COPY ./src/data_toolbox/utils /datatoolbox/data_toolbox/utils

# Copy the current directory contents into the container at /datatoolbox
COPY ./src/.streamlit/config.toml /datatoolbox/.streamlit/config.toml
COPY ./src/.streamlit/config.toml /usr/local/lib/python3.11/site-packages/streamlit/config.toml

COPY ./src/images /datatoolbox/images
COPY ./src/static /datatoolbox/static
COPY ./src/pages /datatoolbox/pages
COPY ./src/toolbox_logging /datatoolbox/toolbox_logging
COPY ./src/config /datatoolbox/config

# Grab top level python files like main.py tool*.py
COPY ./src/*.py /datatoolbox/
COPY ./src/data_toolbox /datatoolbox/data_toolbox
# ----------------------------------------------------------------
# Run application

# Expose the port that Streamlit will run on (default is 8501)
EXPOSE 8501

# Run your Streamlit app when the container launches
FROM base AS dev
# For Linux hosts
CMD ["streamlit", "run", "main.py", "--logger.level=info", "--server.fileWatcherType", "auto"]
# For Windows hosts
# CMD ["streamlit", "run", "main.py", "--logger.level=info", "--server.fileWatcherType", "poll"]

FROM base AS prod
CMD ["streamlit", "run", "main.py", "--logger.level=info"]

