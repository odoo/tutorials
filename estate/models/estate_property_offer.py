from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'
    _order = 'price desc'
    _sql_constraints = [(
        'offer_price_strictly_positive', 'CHECK(price > 0)',
        'Offer price should be stricly positive.'
    )]

    date_deadline = fields.Date('Deadline',
        compute='_compute_date_deadline', inverse='_inverse_date_deadline',)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    price = fields.Float('Price')
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type',
        string="Type", related='property_id.property_type_id')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),], string='Status', readonly=True)
    validity = fields.Integer('Validity (days)', default=7)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            base_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(base_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    @api.constrains('price')
    def _check_price(self):
        for offer in self:
            if offer.price < offer.property_id.best_price:
                raise exceptions.ValidationError(
                    'The offer´s price must be higher than the current best offer.'
                )

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == 'sold':
                raise exceptions.UserError('You cannot create an offer on a sold property.')
            offer.property_id.state = 'offer_received'
        return offers

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state in ['offer_accepted', 'sold']:
                raise exceptions.UserError('An offer has already been accepted.')
            elif offer.property_id.state in ['canceled']:
                raise exceptions.UserError('This sale has been canceled.')
            elif offer.property_id.state in ['new', 'offer_received']:
                offer.property_id.write({
                    'buyer_id': offer.partner_id,
                    'selling_price': offer.price,
                    'state': 'offer_accepted',
                })
                offer.status = 'accepted'
                for refused_offer in offer.property_id.offer_ids:
                    if refused_offer != offer:
                        refused_offer.status = 'refused'
        return True

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == 'accepted':
                raise exceptions.UserError('You cannot refuse an accepted offer.')
            offer.status = 'refused'
        return True
