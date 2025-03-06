from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import date

class RealEstatePropertyOffer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'This models if for offer'

    price = fields.Float(string = 'Price')
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string = 'Status'
    )
    validity = fields.Integer(string = "Validity (days)", default = 7)
    date_deadline = fields.Date(string = "Deadline", default = fields.Datetime.now() + relativedelta(days = 7), inverse = "_inverse_validity", compute = "_compute_deadline")
   
    partner_id = fields.Many2one('res.partner', required = True, string = 'Partners')
    property_id = fields.Many2one('real.estate.property', required = True, string = 'Property name')

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date.today() + relativedelta(days=record.validity)
    
    def _inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days




