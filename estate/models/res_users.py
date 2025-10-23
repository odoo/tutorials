from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    # Add a domain to the field so it only lists the available properties.
    property_ids = fields.One2many(
        comodel_name="estate.property", inverse_name="salesperson_id",
        domain=[('state', 'in', ['new', 'offer_received']),
                ('active', '=', True)],
    )
