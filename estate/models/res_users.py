from odoo import fields, models


class InheritedResUser(models.Model):
    _inherit = "res.users"
    _description = "Inherited User For Estate Module"

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="seller_id",
        domain=[('status', 'in', ['new', 'offer_received'])],
    )
