FROM alpine:3.13

# Install Python and pip
RUN apk add --no-cache python3 py3-pip vim curl
RUN pip3 install --no-cache --upgrade pip setuptools

# Set up a virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Pipenv using pip
RUN pip install --upgrade pip && \
    pip install pipenv

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY Pipfile* /app/

# Install dependencies from the Pipfile
# Specify the system's Python interpreter for Pipenv
RUN pipenv install --deploy --ignore-pipfile --python $(which python3)

# Copy the rest of your application's code
COPY . /app

# Expose port 12504
EXPOSE 12504

# Run your application using the virtual environment
#CMD [ "/bin/ls", "-l" ]
CMD ["pipenv", "run", "python3", "/app/proxy.py"]
