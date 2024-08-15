import logging
from odoo import fields, models, api
import datetime

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate property offer"
    price = fields.Float('Price')
    status = fields.Selection(string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy = False)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required = True)
    property_id = fields.Many2one(comodel_name="estate.property", string="Property", required = True)
    validity = fields.Integer('Validity', default = 7)
    date_deadline = fields.Date(string='Deadline', compute='_deadline_compute', inverse = '_inverse_validity')

    @api.depends("validity", "create_date")
    def _deadline_compute(self):
        for record in self:
            if record.create_date:
                create_date = fields.Date.from_string(record.create_date)
                record.date_deadline = create_date + datetime.timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.context_today(record) + datetime.timedelta(days=record.validity)
    
    
    @api.onchange('date_deadline')
    def _inverse_validity(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date = fields.Date.from_string(record.create_date)
                deadline_date = fields.Date.from_string(record.date_deadline)
                record.validity = (deadline_date - create_date).days
            else:
                record.validity = 0
            