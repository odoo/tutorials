# Notes


## Start odoo command:

`./odoo-bin -d <db_name> --addons-path=<paths...>`

### Breakdown:

`./odoo-bin` : starts the Odoo server
`-d <db_name>` : which PostgreSQL database to use (for me: patja)
`--addons-path=<paths...>` : comma-separated addon folders that Odoo will scan
  
### it does:
- loads already-installed modules
- starts the UI and backend services


## Upgrade a module (Chapter - 3)

### Command:

`./odoo-bin -d <db_name> -u <module_name> --addons-path=<paths...>`

### Meaning:
`- -u <module_name>` : reload it and apply its model/data changes

### it does:

- after changing Python models (ORM), upgrade so database schema updates happen`
- after adding security/ACL, upgrade so access rules apply`

### for me:

`./odoo-bin --addons-path=addons,../enterprise/,../tutorials/ -d patja -u awesome_estate`


## Install a module (first time)

### Command:
`./odoo-bin -d <db_name> -i <module_name> --addons-path=<paths...>`

### Meaning:
`- -i <module_name> `: install the module for the first time in that database
