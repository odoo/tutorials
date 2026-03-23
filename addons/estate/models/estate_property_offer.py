from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string='Status',
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner', string='Partner', required=True
    )
    property_id = fields.Many2one(
        'estate.property', string='Property', required=True, ondelete='cascade'
    )

    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        string='Property Type',
        store=True,
    )

    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)', 'Offered price must be greater than 0.'
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()
            start_date = fields.Date.to_date(start_date)
            record.date_deadline = start_date + relativedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()
            start_date = fields.Date.to_date(start_date)
            if record.date_deadline and start_date:
                diff = record.date_deadline - start_date
                record.validity = diff.days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env['estate.property'].browse(
                vals['property_id']
            )
            if vals.get('price') <= property_record.best_price:
                raise exceptions.UserError(
                    'New offer must be higher than existing offers.'
                )

        offers = super().create(vals_list)

        for record in offers:
            if record.property_id.state == 'new':
                record.property_id.state = 'offer_received'

        return offers

    def action_set_offer_status_accepted(self):
        for record in self:
            if record.property_id.state == 'offer_accepted':
                raise exceptions.UserError('Only one offer can be accepted.')
            else:
                record.status = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'

        return True

    def action_set_offer_status_refused(self):
        for record in self:
            record.status = 'refused'
        return True
