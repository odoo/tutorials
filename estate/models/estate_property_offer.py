
from odoo import fields, models
from datetime import timedelta


class EstatePropertyTags(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property offer Table"

    price = fields.Float('Price')
    status = fields.Selection([('accepted', 'Accepted') ,('refused', 'refused')],string='Status',copy=False)
    partner_id = fields.Many2one('res.users', string='Partner',required=True)    
    property_id = fields.Many2one('estate.property', string='Property',required=True)    
    validity = fields.Integer('Validity', default=7)    
    date_deadline = fields.Date(compute="_date_deadline",inverse="_inverse_date_deadline",string='Date Deadline')

    def _date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):    
        for record in self:
            record.validity = (fields.Date.today() - record.date_deadline).days    
