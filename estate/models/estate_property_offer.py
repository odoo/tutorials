from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted', 'Accepted'),
         ('refused', 'Refused')
        ],
        string="Status", copy=False
    )
    partner_id = fields.Many2one(comodel_name="res.partner")
    property_id = fields.Many2one(comodel_name="estate.property")
