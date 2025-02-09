from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "These are Estate Module Property Offer"

    price = fields.Float(string="price")
    state = fields.Selection(
        string="Status", 
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False
    )
    estate_property_id = fields.Many2one(comodel_name="estate.property", string="Property", required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True)
