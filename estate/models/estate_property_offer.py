from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Offer"
    _order = "price desc"
    _check_price = models.Constraint("CHECK (price > 0)",
                                    "The price of an offer needs to be strictly positive")

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    create_date = fields.Date(default=fields.Date.today())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = 0

    @api.model
    def create(self, vals):
        # Group all current offers by property_id, and extract the minimum price of its offers
        min_price_by_property_id = {
            property.id: min(group_orders.mapped('price'))
            for property, group_orders in self.env['estate.property.offer'].search([('property_id', 'in', [offer['property_id'] for offer in vals])]).grouped('property_id').items()
        }

        for offer in vals:
            min_curr_price = min_price_by_property_id.get(offer['property_id'], 0)
            if offer['price'] < min_curr_price:
                raise UserError("A new offer can't be lower in price than an existing offer!")

        self.env['estate.property'].search([('id', 'in', [offer['property_id'] for offer in vals])]).state = 'received'
        return super().create(vals)

    def action_accept_offer(self):
        for record in self:
            # All of the offers we accepted previously are reverted to refused
            record.property_id.offer_ids.filtered(lambda o: o.status == "accepted").status = "refused"

            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
