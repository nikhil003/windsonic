FROM waggle/plugin-base:1.1.1-ml
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app/
WORKDIR /app
ENTRYPOINT ["--device", "/dev/ttyUSB5", "python3", "/app/main.py"]