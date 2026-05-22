#!/usr/bin/env bash
set -e

COMPOSE_FILE="infrastructure/docker/docker-compose.local.yml"

case "$1" in

  up)
    echo "🚀 Starting local development environment..."
    docker-compose -f $COMPOSE_FILE up --build
    ;;

  down)
    echo "🛑 Stopping local development environment..."
    docker-compose -f $COMPOSE_FILE down
    ;;

  logs)
    echo "📜 Showing container logs..."
    docker-compose -f $COMPOSE_FILE logs -f
    ;;

  restart)
    echo "🔄 Restarting local development environment..."
    docker-compose -f $COMPOSE_FILE down
    docker-compose -f $COMPOSE_FILE up --build
    ;;

  ps)
    echo "📦 Running containers..."
    docker-compose -f $COMPOSE_FILE ps
    ;;

  *)
    echo "❌ Invalid command."

    echo ""
    echo "Usage:"
    echo "./scripts/dev.sh up"
    echo "./scripts/dev.sh down"
    echo "./scripts/dev.sh logs"
    echo "./scripts/dev.sh restart"
    echo "./scripts/dev.sh ps"
    echo ""

    exit 1
    ;;

esac