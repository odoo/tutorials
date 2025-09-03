
from odoo import models, fields


class resUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        "estate.property",
        "salesperson",
        string='Property Associated with Users',
        domain=[('state', '!=', 'sold'), ('state', '!=', 'cancel')]
    )
