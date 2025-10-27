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
    buttons_invisibility = fields.Boolean(
        compute="_compute_buttons_invisibility",
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)', 'The offer price must be strictly positive.'
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.add((
                offer.create_date.date() if offer.create_date else fields.Date.today()), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - (offer.create_date.date()
                              if offer.create_date else fields.Date.today())).days

    @api.depends('property_state', 'status')
    def _compute_buttons_invisibility(self):
        for offer in self:
            offer.buttons_invisibility = (
                offer.property_state not in [
                    'new', 'offer_received'] or offer.status
            )

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', val.get('property_id')),
            ])
            if property_offers and val.get('price') <= min(property_offers.mapped('price')):
                raise ValidationError(
                    "The offer price must be higher than existing offers."
                )
        offers = super().create(vals)
        offers.property_id.state = "offer_received"
        return offers

    def action_accept_offer(self):
        self.status = "accepted"
        self.property_id.state = "offer_accepted"

        self.env['estate.property.offer'].search([
            ('property_id', 'in', self.property_id.ids),
            ('id', '!=', self.id),
        ]).action_refuse_offer()

        return True

    def action_refuse_offer(self):
        self.status = "refused"
        return True
