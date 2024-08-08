from datetime import timedelta
from odoo import api, models, fields


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "estate property offer"

    price = fields.Float(string='Price')
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(compute="_computed_date_deadline",
                                inverse="_inverse_computed_date_deadline")
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True)
    status = fields.Selection(string='Status', copy=False,
                              selection=[
                                  ('accepted', 'Accepted'),
                                  ('refused', 'Refused')
                              ]
                              )
    property_id = fields.Many2one(
        'estate.property', string='Property', required=True)

    @api.depends('create_date', 'validity')
    def _computed_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + \
                    timedelta(days=record.validity)
            else:
                record.date_deadline = fields.datetime.now() + timedelta(days=record.validity)

    @api.depends('create_date', 'date_deadline')
    def _inverse_computed_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline -
                                   record.create_date.date()).days
            else:
                record.validity = (record.date_deadline -
                                   fields.date.today()).days

    def action_accept(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id

    def action_refused(self):
        self.status = 'refused'

    _sql_constraints = [
        ('check_price', 'CHECK(price >=0)',
         'offer price must be positive')
    ]
