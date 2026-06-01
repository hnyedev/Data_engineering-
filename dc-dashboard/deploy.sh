#!/usr/bin/env bash
# deploy.sh — Build Docker image locally, copy to EC2, run it.
# Usage:  ./deploy.sh <EC2_PUBLIC_IP>  (or set DC_HOST env var)
# Example: ./deploy.sh 54.123.45.67

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
DC_HOST="${1:-${DC_HOST:-}}"
SSH_KEY="${SSH_KEY:-~/.ssh/id_rsa}"
EC2_USER="ec2-user"
IMAGE_NAME="dc-dashboard"
CONTAINER_NAME="dc-dashboard"
STREAMLIT_PORT="8501"

# ── Validate ──────────────────────────────────────────────────────────────────
if [[ -z "$DC_HOST" ]]; then
  echo "❌  Usage: ./deploy.sh <EC2_PUBLIC_IP>"
  echo "   Or:    DC_HOST=<ip> ./deploy.sh"
  exit 1
fi

SSH_CMD="ssh -i $SSH_KEY -o StrictHostKeyChecking=no $EC2_USER@$DC_HOST"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  DC Dashboard Deploy → $DC_HOST"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. Build image locally ────────────────────────────────────────────────────
echo "▶ [1/4] Building Docker image..."
docker build -t "$IMAGE_NAME" .

# ── 2. Save image and stream to EC2 ──────────────────────────────────────────
echo "▶ [2/4] Transferring image to EC2 (this takes ~30–60s first time)..."
docker save "$IMAGE_NAME" | \
  ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no \
  "$EC2_USER@$DC_HOST" "docker load"

# ── 3. Stop old container if running ─────────────────────────────────────────
echo "▶ [3/4] Replacing existing container..."
$SSH_CMD "
  docker stop $CONTAINER_NAME 2>/dev/null || true
  docker rm   $CONTAINER_NAME 2>/dev/null || true
"

# ── 4. Run new container ──────────────────────────────────────────────────────
echo "▶ [4/4] Starting container..."
$SSH_CMD "
  docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    -p $STREAMLIT_PORT:$STREAMLIT_PORT \
    $IMAGE_NAME
"

echo ""
echo "✅  Deployed successfully!"
echo "🌐  Dashboard: http://$DC_HOST:$STREAMLIT_PORT"
