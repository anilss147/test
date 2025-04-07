#!/bin/bash

# This script runs necessary tasks before deployment

echo "Running database migrations..."
python manage.py migrate --settings=clothing_store.settings_prod

# Run only if sample data is needed (first deployment)
if [ "$CREATE_SAMPLE_DATA" = "True" ]; then
    echo "Creating sample data..."
    python create_sample_data.py
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=clothing_store.settings_prod

echo "Deployment preparations completed successfully!"