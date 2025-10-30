#!/bin/bash
# test_frontend.sh
# simple health check for frontend nginx
# just makes sure the container is serving correctly

set -e

# colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

FRONTEND_URL="${FRONTEND_URL:-http://localhost:8080}"

echo "testing frontend at $FRONTEND_URL"
echo ""

# test health endpoint
echo -n "checking /health... "
if curl -f -s "$FRONTEND_URL/health" | grep -q "healthy"; then
    echo -e "${GREEN}✓ passed${NC}"
else
    echo -e "${RED}✗ failed${NC}"
    exit 1
fi

# test that index.html is served
echo -n "checking index.html... "
if curl -f -s "$FRONTEND_URL/" | grep -q "<!doctype html>"; then
    echo -e "${GREEN}✓ passed${NC}"
else
    echo -e "${RED}✗ failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}frontend tests passed${NC}"