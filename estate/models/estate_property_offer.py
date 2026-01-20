from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for estate property"
    _order = "price desc"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline",
    )
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False,
    )
    property_type_id = fields.Many2one(
        'estate.property.type', related='property_id.property_type_id', string="Property Type", store=True
    )

    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price > 0)",
            "Offer price must be strictly positive.",
        ),
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.context_today(record)
            record.date_deadline = fields.Date.add(start_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.context_today(record)
            if record.date_deadline:
                delta = record.date_deadline - start_date.date()
                record.validity = delta.days
            else:
                record.validity = 0

    def action_on_accepted(self):
        for offer in self:
            accepted_offers = offer.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted"
            )
            if accepted_offers:
                raise UserError("An offer has already been accepted for this property.")

            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"
        return True

    def action_on_refused(self):
        for offer in self:
            offer.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env['estate.property'].browse(vals.get('property_id'))

            if prop.offer_ids:
                max_prop = max(prop.offer_ids.mapped('price'))
                if vals['price'] < max_prop:
                    raise UserError(f"The offer price must be higher than the current best offer of {max_prop}.")

            prop.state = 'offer_received'

        return super().create(vals_list)
