FROM python:3.11

EXPOSE 8501
ENV DEBIAN_FRONTEND=noninteractive

COPY . /app

RUN apt update && \
    apt install ffmpeg rsync fonts-wqy-zenhei fonts-wqy-microhei -y && \
    apt clean && \
    addgroup --gid 1000 chenymeaavt && \
    adduser --uid 1000 --ingroup chenymeaavt --disabled-password chenymeaavt && \
    pip cache purge && \
    chown 1000:1000 /app -R && \
    chmod +x /app/entry.sh

USER chenymeaavt
WORKDIR /app

RUN python -m venv . && \
    . ./bin/activate && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 && \
    pip install -r /app/requirements.txt && \
    pip cache purge && \
    mv config _config && \
    mv cache _cache && \
    mv model _model && \
    mkdir config cache model

ENTRYPOINT ["./entry.sh"]
