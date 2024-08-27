from odoo import api, models, fields
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

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
    property_type_id = fields.Many2one(
        "estate.property.type", store=True, related='property_id.property_type_id')

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
        self.property_id.state = 'offer Accepted'

    def action_refused(self):
        self.status = 'refused'
        self.property_id.state = 'canceled'

    _sql_constraints = [
        ('check_price', 'CHECK(price >=0)',
         'offer price must be positive')
    ]

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        price = vals.get('price')
        current_property = self.property_id.browse(property_id)
        current_property.state = 'offer Received'

        existing_offers = current_property.offer_ids
        if existing_offers:
            max_amount = max(existing_offers.mapped('price'))
            if price < max_amount:
                raise UserError(
                    "The offer amount cannot be lower than an existing offer.")
        return super().create(vals)
