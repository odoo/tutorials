from odoo import api, models, fields
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")
    property_state = fields.Selection(
        related="property_id.state",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True,
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)', 'The offer price must be strictly positive.'
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(
                    offer.create_date.date(), days=offer.validity)
            else:
                offer.date_deadline = fields.Date.add(
                    fields.Date.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                delta = (offer.date_deadline - offer.create_date.date()).days
                offer.validity = delta
            elif offer.date_deadline:
                delta = (offer.date_deadline - fields.Date.today()).days
                offer.validity = delta

    @api.model
    def create(self, vals):
        for val in vals:
            property_obj = self.env['estate.property'].browse(
                val.get('property_id'))
            property_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', property_obj.id),
            ])
            if property_offers:
                lowest_offer = min(property_offers.mapped('price'))
                if val.get('price', 0) <= lowest_offer:
                    raise ValidationError(
                        "The offer price must be higher than existing offers."
                    )
            property_obj.state = 'offer_received'
        return super().create(vals)

    def action_accept_offer(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"

            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id),
                ('status', '!=', 'refused')
            ])
            other_offers.action_refuse_offer()

        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"

        return True
