from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

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

    def action_accept_offer(self):
        if not any(offer.status == 'accepted' for offer in self.property_id.offer_ids):
            self.status = 'accepted'
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price
            return True
        else:
            raise exceptions.UserError("Only one offer can be accepted at a time. If you want to accept another offer, refuse this first and then accept the one you want.")

    def action_refuse_offer(self):
        self.status = 'refused'
        if not any(offer.status == 'accepted' for offer in self.property_id.offer_ids):
            self.property_id.buyer_id = None
            self.property_id.selling_price = 0
        return True
