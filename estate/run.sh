cd "../../odoo"
kill $(lsof -i:8069)
./odoo-bin --addons-path=addons,../enterprise/,../tutorials/ -d rd-demo -u estate --dev xmlC