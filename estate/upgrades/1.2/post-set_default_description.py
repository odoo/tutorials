from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    properties_without_description = env['estate.property'].search([("description", "=", False)])
    properties_without_description.description = 'Description is now required as of v1.2'