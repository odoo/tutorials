from datetime import timedelta
from odoo import api, fields, models

# estate.property.offer model 
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
    validity = fields.Integer(default=7, string='Validity')
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days
    
    