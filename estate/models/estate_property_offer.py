from odoo import fields, models
from odoo.orm.fields_selection import Selection


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property offer"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
