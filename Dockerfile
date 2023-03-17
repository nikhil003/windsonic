FROM waggle/plugin-base:1.1.1-ml
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY . .
ENTRYPOINT ["--device", "/dev/ttyUSB5", "python3", "main.py"]
