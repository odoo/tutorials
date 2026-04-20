from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offers'

    _check_offer_price = models.Constraint(
        'CHECK (price >= 0)',
        'Offer price must be positive',
    )

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
        readonly=True
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', store=True)

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.date_deadline = fields.Date.add(fields.Date.to_date(rec.create_date), days=rec.validity)
            else:
                rec.date_deadline = fields.Date.add(fields.Date.context_today(rec), days=rec.validity)

    @api.onchange('date_deadline')
    def _inverse_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.validity = (rec.date_deadline - fields.Date.to_date(rec.create_date)).days
            else:
                rec.validity = (rec.date_deadline - fields.Date.context_today(rec)).days

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
        return offers

    def action_accept(self):
        if self.property_id.state in ('sold', 'cancelled'):
            raise UserError('You cannot accept an offer in a sold or cancelled property')
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = 'offer_accepted'
        other_offers = self.search([
            ('property_id', '=', self.property_id.id),
            ('id', '!=', self.id)
        ])
        other_offers.write({'status': 'refused'})
        return True

    def action_refuse(self):
        if self.property_id.state in ('sold', 'cancelled'):
            raise UserError('You cannot reject an offer in a sold or cancelled property')
        if self.status == 'accepted':
            self.property_id.selling_price = 0
            self.property_id.buyer_id = False
            self.property_id.state = 'offer_received'
        self.status = 'refused'
        return True
