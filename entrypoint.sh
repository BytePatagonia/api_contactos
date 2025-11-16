#!/bin/bash
set -e

echo "🔍 Esperando a PostgreSQL..."

# Esperar a que PostgreSQL esté listo
until pg_isready -h db -p 5432 -U ${POSTGRES_USER:-contactsuser} > /dev/null 2>&1; do
  echo "⏳ PostgreSQL no está listo - esperando..."
  sleep 2
done

echo "✅ PostgreSQL está listo!"
echo "🚀 Iniciando API..."

# Iniciar la aplicación
exec uvicorn app.main:app --host 0.0.0.0 --port 8000