from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    property_type_id = fields.Many2one(
        related="property_id.type_id", 
        string="Property Type", 
        store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    _check_price = models.Constraint(
    'CHECK(price > 0)',
    'The offer price should be > 0',
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                (fields.Date.to_date(record.create_date) or fields.Date.today()),
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                record.date_deadline - (fields.Date.to_date(record.create_date) or fields.Date.today())
            ).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise exceptions.UserError("Prob is already sold")
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.status = 'accepted'

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == 'new':
                offer.property_id.state = 'offer_received'
                
        return offers
