from odoo import fields, models

# estate.property.type model 
class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer database table"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted','Accepted'), 
            ('refused','Refused'), 
            ],
        help="Status of the offer")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property ID", required=True)
