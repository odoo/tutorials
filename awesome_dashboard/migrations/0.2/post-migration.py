from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    users = env["res.users"].search([("dashboard_config", "=", False)])
    for user in users:
        user.dashboard_config = {"hidden_items": []}
