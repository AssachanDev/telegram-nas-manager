#!/usr/bin/env bash
set -e

if [ ! -f .env ]; then
    echo "❌ .env file not found. Copy .env.example and fill in your values."
    exit 1
fi

source .env

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ BOT_TOKEN is not set in .env"
    exit 1
fi

if [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "❌ TELEGRAM_CHAT_ID is not set in .env"
    exit 1
fi

if [ -z "$HOST_DATA_DIR" ]; then
    echo "❌ HOST_DATA_DIR is not set in .env"
    exit 1
fi

if [ ! -d "$HOST_DATA_DIR" ]; then
    echo "❌ HOST_DATA_DIR '$HOST_DATA_DIR' does not exist"
    exit 1
fi

if ! command -v docker &>/dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

echo "✅ Config looks good"
echo "   NAS: $HOST_DATA_DIR"
echo ""
docker compose up -d --build
echo ""
echo "✅ Bot is running. Logs: docker compose logs -f"
