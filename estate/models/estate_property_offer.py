from odoo import fields, models, api ,_
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer'
    _check_positive_offer_price = models.Constraint(
        'CHECK (price >= 0)', 'price should be positive'
    )
    _order = 'price desc'

    price = fields.Float(copy=False)
    status = fields.Selection(
        copy=False,
        string='status',
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
    )
    partner_id = fields.Many2one(
        'res.partner', required=True, default=lambda self: self.env.user.partner_id.id
    )
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, copy=False)
    deadline = fields.Date(
        compute='_compute_deadline', store=True, inverse='_inverse_deadline'
    )

    property_type_id = fields.Many2one(
        'estate.property.type', related='property_id.property_type_id', store=True
    )

    @api.depends('validity', 'deadline')
    def _compute_deadline(self):
        for record in self:
            record.deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            today_date = fields.Date.today()
            record.validity = (record.deadline - today_date).days

    def action_accept_offer(self):
        for offer in self:
            for offer.property_id in offer.property_id:
                if (
                    offer.property_id.state == 'offer accepted'
                    or offer.property_id.state == 'sold'
                ):
                    raise UserError(
                        'An offer has already been accepted for this property.'
                    )
                else:
                    offer.status = 'accepted'
                    offer.property_id.state = 'offer accepted'
                    offer.property_id.buyer_id = offer.partner_id
                    offer.property_id.selling_price = offer.price
        for offers in self.property_id.offer_ids:
            if offers != self:
                offers.status = 'refused'

    def action_reject_offer(self):
        for offer in self:
            if offer.status == 'accepted':
                if offer.property_id.state == 'sold':
                    raise UserError(
                        'the property is sold. CANT REJECT THE OFFER - THANK YOU'
                    )
                else:
                    offer.status = 'refused'
                    offer.property_id.state = 'offer received'
                    offer.property_id.buyer_id = False
                    offer.property_id.selling_price = 0
            elif offer.status == 'refused':
                raise UserError('This offer has already been refused.')
            else:
                offer.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals.get('property_id'))
            if property_id.offer_ids:
                max_offer_price = max(property_id.offer_ids.mapped('price'))
                if vals.get('price', 0) <= max_offer_price:
                    raise UserError(_("The offer price must be higher than the current highest offer (%s).") % max_offer_price)
            property_id.state = "offer received"
        return super(EstatePropertyOffer, self).create(vals_list)
