from odoo import api, fields, models
from odoo.tools import date_utils

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "describes an offer made on a property"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy = False
    )
    partner_id = fields.Many2one("res.partner", required = True)
    property_id = fields.Many2one("estate.property", required = True)
    validity = fields.Integer()
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            if(not offer.create_date): # When creating an offer create_date is not defined yet
                offer.date_deadline = date_utils.add(fields.Date.today(), days=offer.validity)
                continue
            offer.date_deadline = date_utils.add(offer.create_date, days=offer.validity)
    
    #@api.depends("validity")
    def _inverse_date_deadline(self):
        for offer in self:
            if(not offer.create_date): # When creating an offer create_date is not defined yet
                offer.validity = (offer.date_deadline - fields.Date.today()).days
                continue
            offer.validity = (offer.date_deadline - offer.create_date.date()).days
