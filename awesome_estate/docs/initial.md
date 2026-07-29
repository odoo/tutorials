# Notes

## Start Odoo command

`odoo-bin -d <db_name> --addons-path=<paths...>`

### Breakdown

- `odoo-bin` starts the Odoo server.
- `-d <db_name>` selects which PostgreSQL database to use.
- `--addons-path=<paths...>` is a comma-separated list of addon folders that Odoo scans.

### It does

- Loads already-installed modules.
- Starts the UI and backend services.

## Upgrade a module

### Command

`odoo-bin -d <db_name> -u <module_name> --addons-path=<paths...>`

### Meaning

`-u <module_name>` reloads the module and applies its model and data changes.

### It does

- After changing Python models (ORM), upgrade the module so database schema changes happen.
- After adding security or ACLs, upgrade the module so access rules apply.

### For me

`odoo-bin --addons-path=addons,../enterprise/,../tutorials/ -d patja -u awesome_estate`

## Install a module for the first time

### Command

`odoo-bin -d <db_name> -i <module_name> --addons-path=<paths...>`

### Meaning

`-i <module_name>` installs the module for the first time in that database.
