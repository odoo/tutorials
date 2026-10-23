from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    # Inverse of the field referencing the salesperson in estate.property
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="seller_id",
        string="Assigned Properties",
        domain=[('state', 'in', ['new', 'received'])]
    )
