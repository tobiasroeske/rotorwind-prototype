#!/usr/bin/env bash
set -euo pipefail

CONTAINER="kafka"                               # container_name aus deiner compose
BROKER="kafka:9092"
CLI="/opt/bitnami/kafka/bin/kafka-topics.sh"

# Sanity-Check: läuft der Container?
if ! docker inspect -f '{{.State.Running}}' "$CONTAINER" >/dev/null 2>&1; then
  echo "Kafka container '$CONTAINER' not running. Start the stack first (make up)."
  exit 1
fi

# Topics: name:partitions:replication
topics=(
  "rotorwind.telemetry.v1:3:1"
  "rotorwind.telemetry.enriched.v1:3:1"
)

for t in "${topics[@]}"; do
  name="${t%%:*}"; rest="${t#*:}"; parts="${rest%%:*}"; rf="${rest##*:}"
  echo "Creating topic $name (partitions=$parts, rf=$rf)"
  docker exec -i "$CONTAINER" bash -lc \
    "$CLI --create --if-not-exists \
      --topic '$name' \
      --bootstrap-server $BROKER \
      --partitions $parts \
      --replication-factor $rf"
done

echo "Done."
