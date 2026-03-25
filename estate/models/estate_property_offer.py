from odoo import api, exceptions, fields, models
from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer made on a property'
    _order = 'price desc'

    price = fields.Float(string='Price')
    _price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one(
        'estate.property', string='Property', required=True, ondelete='cascade'
    )
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    property_type_id = fields.Many2one(
        'estate.property.type', related='property_id.property_type_id', store=True
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                (record.create_date + relativedelta(days=record.validity))
                if record.create_date
                else (fields.Date.today() + relativedelta(days=record.validity))
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = relativedelta(
                record.date_deadline,
                record.create_date if record.create_date else fields.Date.today(),
            ).days

    def action_accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    raise exceptions.UserError(
                        'An offer has already been accepted for this property'
                    )
                else:
                    record.status = 'accepted'
                    record.property_id.state = 'offer_accepted'
                    record.property_id.buyer_id = record.partner_id
                    record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            property_for_offer = self.env['estate.property'].browse(val['property_id'])
            if float_compare(val['price'], property_for_offer.best_price, 2) == -1:
                raise exceptions.UserError(
                    'New offers cannot be lower than existing offers'
                )
            property_for_offer.state = 'offer_received'

        return super().create(vals_list)
