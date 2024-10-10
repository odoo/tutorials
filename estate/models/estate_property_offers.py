from odoo import fields, models # type: ignore

class EstatePropertyOffers(models.Model):

    _name = "estate.property.offers"
    _description = "Estate Property Offers Model"
    
    price = fields.Float(string='Offer Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
       )
    partner_id = fields.Many2one('res.partner', required=True) # type: ignore
    property_id = fields.Many2one('estate.property', required=True)



