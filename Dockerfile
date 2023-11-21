FROM orgoro/dlib-opencv-python:3.7
WORKDIR /app

# RUN conda install -c conda-forge dlib
COPY req.txt /app
COPY .env /app
RUN pip install -r req.txt
RUN pip install mysql-connector
COPY . /app

CMD [ "uvicorn","app:app","--reload","--host","0.0.0.0" ]

# FROM python:3.9 as pystage

# WORKDIR .

# COPY requirements.txt requirements.txt

# RUN pip3 install --no-cache-dir -r requirements.txt

# CMD [ "uvicorn","app:app","--reload","--host 0.0.0.0"]
