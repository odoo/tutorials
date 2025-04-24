from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "property offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate_property", string="Property", required=True)
    validity = fields.Integer(compute="_compute_validity", inverse="_inverse_validty")
    date_deadline = fields.Date(string="Deadline", required=True)
    property_type_id = fields.Many2one(related="property_id.estate_property_type", string="Property Type", store=True)

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'The price should be higher than 0'),
    ]

    @api.depends("date_deadline")
    def _compute_validity(self):
        today = fields.Datetime.today().date()
        for record in self:
            deadline = record.date_deadline
            if deadline:
                start_date = record.create_date.date() if record.create_date else today
                delta = deadline - start_date
                record.validity = delta.days
            else:
                record.validity = 0

    def _inverse_validty(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Datetime.add(record.create_date, days=record.validity)

    def action_confirm(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("You can't validate an offer for a sold property")
            else:
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.status = 'accepted'
                record.property_id.mark_as_sold()

    def action_close(self):
        for record in self:
            record.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            property = offer.property_id
            if any(offer.price < existing_price for existing_price in property.offer_ids.mapped('price')):
                raise UserError("You can't create offer with a lower price than existing offer")
            else:
                property.state = 'offer_received'
        return offers
