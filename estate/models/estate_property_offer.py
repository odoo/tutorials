from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'All offers'
    _order = 'price desc'

    price = fields.Float(required=True)
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
    )
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price of an offer should be strictly positive.',
    )

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            created_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(
                created_date, days=record.validity,
            )

    @api.model
    def create(self, val_lists):
        for vals in val_lists:
            linked_property = self.env['estate.property'].browse(vals['property_id'])
            if vals['price'] < linked_property.best_price:
                raise UserError('Offer price cannot be lower than existing offers')

            linked_property.state = 'offer_received'
        return super().create(val_lists)

    def _inverse_deadline(self):
        for record in self:
            created_date = record.create_date.date() or fields.Date.today()
            record.validity = (record.date_deadline - created_date).days

    def action_mark_as_accepted(self):
        for record in self:
            if (
                record.property_id.state != 'new'
                and record.property_id.state != 'offer_received'
            ):
                raise UserError('Cannot accept offer in this state')

            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'

    def action_mark_as_refused(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.state = 'offer_received'
                record.property_id.selling_price = None
                record.property_id.buyer_id = None
            record.status = 'refused'
