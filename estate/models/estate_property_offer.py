from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class estate_property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'property offer'

    price = fields.Float(string = 'price')
    status = fields.Selection([('accepted', 'Accepted'),
            ('refused', 'Refused')], string = 'status')
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default = 7, string = "Validity (days)")
    date_deadline = fields.Date(string = "Deadline", copmute = 'compute_date_deadline', store= True)

    @api.depends('validity')
    def compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)
