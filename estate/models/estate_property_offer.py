from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    property_id = fields.Many2one(
        comodel_name='estate.property',
        string='Property',
        required=True,
        index=True,
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        store=True,
        index='btree_not_null',
    )
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            start = offer._get_start_date()
            offer.date_deadline = fields.Date.add(start, days=offer.validity)

    def _inverse_date_deadline(self):
        """Derive the validity in days from the deadline entered by the user."""
        for offer in self.filtered('date_deadline'):
            start = offer._get_start_date()
            offer.validity = (offer.date_deadline - start).days

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = {vals['property_id'] for vals in vals_list if vals.get('property_id')}
        properties = self.env['estate.property'].browse(property_ids)
        best_price_by_property = {prop.id: prop.best_price for prop in properties}
        for vals in vals_list:
            property_id = vals.get('property_id')
            if property_id not in best_price_by_property:
                continue
            price = vals.get('price', 0.0)
            if float_compare(price, best_price_by_property[property_id], precision_digits=2) < 0:
                raise UserError(self.env._(
                    'The offer must be at least %(price)s, the best existing offer.',
                    price=best_price_by_property[property_id],
                ))
            best_price_by_property[property_id] = price
        offers = super().create(vals_list)
        offers.property_id.filtered(lambda prop: prop.state == 'new').state = 'offer_received'
        return offers

    def action_accept(self):
        """Accept the offer: copy its price and partner onto the property and mark it accepted."""
        for offer in self:
            if offer.property_id.state in ('sold', 'cancelled'):
                raise UserError(self.env._('Offers on sold or cancelled properties cannot be accepted.'))
            other_accepted = offer.property_id.offer_ids.filtered(
                lambda o: o.status == 'accepted' and o != offer,
            )
            if other_accepted:
                raise UserError(self.env._('An offer has already been accepted for this property.'))
            offer.status = 'accepted'
            offer.property_id.write({
                'state': 'offer_accepted',
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id,
            })
        return True

    def action_refuse(self):
        if 'accepted' in self.mapped('status'):
            raise UserError(self.env._('Accepted offers cannot be refused.'))
        self.status = 'refused'
        return True

    def _get_start_date(self):
        """Return the creation date, or today while the offer is not saved yet."""
        self.ensure_one()
        return self.create_date.date() if self.create_date else fields.Date.today()
