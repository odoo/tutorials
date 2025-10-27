from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = 'price desc'

    _check_expected_price = models.Constraint(
        'CHECK(price >= 0)',
        'An offer price must be strictly positive',
    )
    _check_validity = models.Constraint(
        'CHECK(validity >= 0)',
        'Validity must be positive',
    )

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused'), ('pending', 'Pending')],
        default='pending',
    )

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(related='property_id.type_id', string="Property Type", store=True)
    property_state = fields.Selection(related='property_id.state', string="Property State")
    property_expected_price = fields.Float(related='property_id.expected_price', string="Expected Price")

    create_date = fields.Datetime(readonly=True, default=fields.Datetime.now)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_deadline',
        inverse='_inverse_deadline',
        string="Deadline")

    @api.model_create_multi
    def create(self, vals_list):
        properties = self.env['estate.property'].search([
            ('id', 'in', [vals['property_id'] for vals in vals_list]),
            ('state', 'not in', ('sold', 'cancelled')),
        ])

        for values in vals_list:
            property_reference = properties.filtered(lambda r: r.id == values['property_id'])

            if len(property_reference) != 1:
                return UserError("Cannot create an offer on a sold or cancelled property")

            if values['price'] <= property_reference.best_price:
                raise UserError(f"The offer needs to be higher than {property_reference.best_price}")

            property_reference.write({'state': 'offer_received'})
        return super().create(vals_list)

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Datetime.now()) + relativedelta(days=offer.validity)

    @api.depends('validity', 'create_date')
    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_confirm(self):
        for offer in self:
            offer.status = 'accepted'
            offer.property_id.write(
                {'selling_price': offer.price, 'buyer_id': offer.partner_id, 'state': 'offer_accepted'})

    def action_cancel(self):
        for offer in self:
            offer.status = 'refused'
