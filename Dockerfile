# Gáttagægir í skýinu — sjá verkfaeri/gattagaegir/README.md („Í skýinu").
#
# Skráin er í rót safnsins af því að þjónninn les snidmat/ (gullna sniðið og
# dæmin) beint úr safninu. Byggt með:  docker build -t gattagaegir .
FROM python:3.12-slim

# Ekkert pip: tólið er hreint stdlib. Aðeins skrárnar sem þjónninn þarf.
WORKDIR /app
COPY verkfaeri/gattagaegir/ verkfaeri/gattagaegir/
COPY snidmat/ snidmat/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GATTAGAEGIR_OPINN=1 \
    PORT=8080
EXPOSE 8080

# Keyrt sem venjulegur notandi, ekki root.
RUN useradd --system --no-create-home gaegir
USER gaegir

# PORT og GATTAGAEGIR_OPINN eru lesin úr umhverfinu (sjá __main__.lesa_rok).
CMD ["python", "-m", "verkfaeri.gattagaegir"]
