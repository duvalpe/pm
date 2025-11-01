#!/bin/bash
# Initialize database and run migrations

echo "Creating initial database migration..."
alembic revision --autogenerate -m "Initial schema: users, projects, milestones, schedules, rfi_submittals, audit_logs"

echo "Applying migrations..."
alembic upgrade head

echo "Database initialization complete!"
