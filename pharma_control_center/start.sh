#!/bin/bash
set -e

# Default values for environment variables
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-odoo}
DB_PASSWORD=${DB_PASSWORD:-odoo}
DB_NAME=${DB_NAME:-odoo}
ADMIN_PASSWD=${ADMIN_PASSWD:-admin}

# Generate Odoo config file with environment variables
cat > /tmp/odoo.conf << EOF
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
xmlrpc_port = 8069
db_host = $DB_HOST
db_port = $DB_PORT
db_user = $DB_USER
db_password = $DB_PASSWORD
db_name = $DB_NAME
admin_passwd = $ADMIN_PASSWD
without_demo = False
EOF

# Run Odoo server with initialization of base and pharma_control_center modules
exec odoo server --config /tmp/odoo.conf --init=base,pharma_control_center
