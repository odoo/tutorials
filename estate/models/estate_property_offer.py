from odoo import models,fields,api
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="status",
        selection=[
            ('accepted','Accepted'),
            ('rejected','Rejected')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id',string='Property Type',store=True)
    validity = fields.Integer(string='Validity(days)',default=7)
    date_deadline = fields.Date(string='Date Deadline',inverse='_date_deadline',compute='_set_deadline')
    create_date = fields.Date(default = fields.date.today(),readonly=True)

    @api.depends('validity')
    def _set_deadline(self):
        for record in self:
            if record.create_date == False:
                record.date_deadline = fields.date.today() + relativedelta(days = record.validity)
            else:
                record.date_deadline = record.create_date + relativedelta(days = record.validity)

    def _date_deadline(self):
        for record in self:
            if record.create_date == False:
                record.validity = record.date_deadline.day - fields.Date.today().day
            else:
                record.validity = record.date_deadline.day - record.create_date.day

    def action_status_accept(self):
        for record in self:
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'

    def action_status_reject(self):
        for record in self:
            record.status = 'rejected'
    
    _sql_constraints = [
        ('check_positive_integer', 'CHECK(price > 0)', 'Price must be greater than 0.')
    ]
