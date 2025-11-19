from odoo import fields, models


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "property offer"

    price = fields.Float(string='Price')
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate.property', required=True, string='Property')
    status = fields.Selection(
        string='Status',
        copy=False, 
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')]
        )
