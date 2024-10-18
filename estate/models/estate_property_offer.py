from odoo import models, fields, api # type: ignore
from datetime import timedelta, datetime

class estatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "This is offer table"

    price = fields.Float(required=True)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        ondelete='set null'
    )
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_compute_validity', string="Date Deadline")
    sum = fields.Integer(compute='_compute_sum', string="Sum")
    sum2 = fields.Integer(compute='_compute_sum2', string="Sum2")

    _sql_constraints = [
            ('check_offer_price','CHECK(price > 0)','A property offer price must be strictly positive.')
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(record.validity)
            else:
                record.date_deadline = datetime.today() + timedelta(record.validity)

    @api.depends('date_deadline') 
    def _compute_validity(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - datetime.today()).days

    @api.depends('validity')
    def _compute_sum(self):
        for record in self:
            record.sum = 7 + record.validity

    @api.depends('sum')
    def _compute_sum2(self):
        for record in self:
            record.sum2 = 7 + record.sum

    def action_accept(self):
            self.status = 'accepted'
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price

    def action_refuse(self):
            if(self.status == 'accepted'):
                self.status = 'refused'
                self.property_id.buyer_id = False
                self.property_id.selling_price = False
            else: 
                self.status = 'refused'
    