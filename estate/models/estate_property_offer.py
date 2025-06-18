from odoo import fields,models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate properties offers"

    price = fields.Float("Price",required=True)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        help="This selection is used to tell whether  buying offer is accepted or refused"
    )
    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("estate.property")