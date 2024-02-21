from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer model"


    price = fields.Float()
    status = fields.Selection(
        copy=False,
        string = 'Status',
        selection = [
            ('accepted', 'Accepted'), 
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

