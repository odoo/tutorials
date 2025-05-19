from odoo import fields, models

class property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Model to modelize Offer for Properties"

    price = fields.Float()
    status= fields.Selection(
        string='Status',
        selection=[('accepted','Accepted'), ('refused','Refused')],
        help="The Status of the offer"
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)