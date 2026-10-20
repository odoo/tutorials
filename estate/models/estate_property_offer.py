from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for the properties of the estate module"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help='Current status of the offer (Accepted or Refused).'
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Properties")
