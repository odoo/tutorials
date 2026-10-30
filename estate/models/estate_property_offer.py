from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused'), ('ongoing', 'Ongoing')], required=True, copy=False, default='ongoing', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(
        'Validity (in days)',
        default=5,
    )
    date_deadline = fields.Date(
        'Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id')

    _offer_price_must_be_positive = models.Constraint(
        "CHECK(price > 0.0)",
        "The offer price must be greater than 0",
    )

    @api.depends("date_deadline", "create_date")
    def _inverse_date_deadline(self):
        for record in self:
            created_d = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - created_d).days

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            created_d = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(created_d, days=record.validity)

    # This method checks if there is already an offer larger or equal to the new one. If so, the new offer cannot be added to the property object
    @api.model
    def create(self, vals):
        for value in vals:
            highest_offer = self.env['estate.property'].browse(value.get('property_id')).best_offer
            if highest_offer >= value.get('price'):
                raise exceptions.UserError(f"Cannot create an offer lesser or equal to {highest_offer}")
        return super().create(vals)

    def action_accept_offer(self):
        if any(offer.status == 'accepted' for offer in self.property_id.offer_ids):
            raise exceptions.UserError("Only one offer can be accepted at a time. If you want to accept another offer, refuse the one accepted first and then accept the one you want.")
        self.status = 'accepted'
        self.property_id.state = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def action_refuse_offer(self):
        # If the refused offer was the one accepted, this means that the property state is 'Offer accepted'. We must change its state to 'received' (a property could have received offers even if they all refused) .
        if self.status == 'accepted':
            self.property_id.state = 'received'
        self.status = 'refused'
        return True
