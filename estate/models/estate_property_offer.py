from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer for a property'
    _order = 'price desc'

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Price must be strictly positive!'),
    ]

    price = fields.Float('Price')
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused'), ('pending', 'Pending')],
        'Status',
        default='pending',
        required=True,
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    property_id = fields.Many2one('estate.property', 'Property', required=True)
    property_type_id = fields.Many2one(
        'estate.property.type',
        'Property Type',
        related='property_id.property_type_id',
        store=True,
    )
    validity = fields.Integer('Validity (days)', help='Validity in days', default=7)
    date_deadline = fields.Date(
        'Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
    )

    ###### COMPUTE ######
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if not record.validity:
                record.date_deadline = False
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if not record.date_deadline:
                record.validity = 0
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    ###### CRUD ######
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            val_price = val.get('price')
            val_property_id = val.get('property_id')
            if not val_price or not val_property_id:
                raise ValidationError(_('Price and Property ID are required.'))
            property_id = self.env['estate.property'].browse(val_property_id)
            if not property_id:
                raise ValidationError(_(f'Property with ID {val_property_id} does not exist.'))
            best_price = property_id.best_price
            if float_compare(val_price, best_price, precision_digits=2) <= 0:
                raise ValidationError(_(f'The offer price must be higher than the current best price (${best_price}).'))

            if property_id.state == 'new':
                property_id.state = 'offer_received'
        return super().create(vals)

    ###### ACTIONS ######
    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'

            other_offers = record.property_id.offer_ids.filtered(lambda x: x.id != record.id)
            other_offers.action_refuse()
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    def action_revert(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.state = 'offer_received'
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0
            record.status = 'pending'
        return True

    ###### CONSTRAINTS ######
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            min_offer_price = record.property_id.expected_price * 0.9
            if float_compare(record.price, min_offer_price, precision_digits=2) < 0:
                raise ValidationError(
                    _(f'The offer price must be at least 90% of the expected price (${min_offer_price}).')
                )
