from odoo import models, fields


class ResUsersInherited(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="salesperson_id",
        string="Properties",
        domain="[('state', 'in', ['new', 'offer_received'])]",
    )
