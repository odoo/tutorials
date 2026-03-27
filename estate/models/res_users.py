from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
       comodel_name="estate.property",
        inverse_name="salesman_id",
        string="Sales Properties",
        domain=[('state', 'in', ['new', 'offer_received'])]
    )
