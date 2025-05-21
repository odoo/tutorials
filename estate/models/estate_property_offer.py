from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "ch7 exercise tutorial"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        string='Offer Status',
        selection= [('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
