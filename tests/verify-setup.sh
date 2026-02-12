#!/bin/bash

# Verification script for testing infrastructure setup
# This script checks that all test configurations are in place

set -e

echo "=================================="
echo "Test Infrastructure Verification"
echo "=================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check function
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 (missing)"
        return 1
    fi
}

check_directory() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ (missing)"
        return 1
    fi
}

# Backend Tests
echo "Backend Test Infrastructure:"
echo "----------------------------"
check_file "../backend/pytest.ini"
check_file "../backend/requirements.txt"
check_directory "../backend/tests"
check_directory "../backend/tests/unit"
check_directory "../backend/tests/integration"
check_file "../backend/tests/__init__.py"
check_file "../backend/tests/conftest.py"
check_file "../backend/tests/unit/__init__.py"
check_file "../backend/tests/unit/test_security.py"
check_file "../backend/tests/integration/__init__.py"
check_file "../backend/tests/integration/test_algorithms_api.py"
check_file "../backend/tests/integration/test_auth_api.py"
echo ""

# Frontend Tests
echo "Frontend Test Infrastructure:"
echo "-----------------------------"
check_file "../frontend/vitest.config.ts"
check_file "../frontend/src/setupTests.ts"
check_file "../frontend/package.json"
check_directory "../frontend/src/components/__tests__"
check_file "../frontend/src/components/__tests__/AlgorithmCard.test.tsx"
echo ""

# E2E Tests
echo "E2E Test Infrastructure:"
echo "-----------------------"
check_directory "e2e"
check_file "e2e/playwright.config.ts"
check_file "e2e/package.json"
check_directory "e2e/specs"
check_directory "e2e/fixtures"
check_file "e2e/fixtures/test-data.ts"
check_file "e2e/specs/search-and-view.spec.ts"
check_file "e2e/specs/admin-crud.spec.ts"
echo ""

# Documentation
echo "Documentation:"
echo "-------------"
check_file "../docs/testing-strategy.md"
check_file "README.md"
echo ""

# Summary
echo "=================================="
echo "Verification Complete!"
echo "=================================="
echo ""
echo "Next Steps:"
echo "1. Backend: cd ../backend && pip install -r requirements.txt"
echo "2. Frontend: cd ../frontend && npm install"
echo "3. E2E: cd e2e && npm install && npm run install"
echo ""
echo "Run Tests:"
echo "- Backend: cd ../backend && pytest --version"
echo "- Frontend: cd ../frontend && npm test -- --version"
echo "- E2E: cd e2e && npx playwright test --version"
echo ""
