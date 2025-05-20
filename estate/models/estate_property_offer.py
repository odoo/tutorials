from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An Offer on a property"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )

    # Relations
    property_id = fields.Many2one(comodel_name="estate.property", string="Property")
    partner_id = fields.Many2one("res.partner", string="Partner", copy=False)
