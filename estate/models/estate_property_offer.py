from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers for real state properties'

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    property_id = fields.Many2one(comodel_name='estate.property')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Buyer')

