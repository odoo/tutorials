from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    _order = "price desc"

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )

    price = fields.Float()

    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )

    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )

    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )

    validity = fields.Integer(
        default=7,
    )

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    property_type_id = fields.Many2one(
        string="estate.property.type",
        related="property_id.property_type_id",
        store=True
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (
                    record.create_date.date() + timedelta(days=record.validity)
            )
            else:
                record.date_deadline = fields.Date.context_today(self)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    def action_accept(self):
        for record in self:
            other_offers = record.property_id.offer_ids - record
            other_offers.write({"status": "refused"})

            record.status = "accepted"

            record.property_id.write({
                "buyer_id": record.partner_id.id,
                "selling_price": record.price,
                "state": "offer_accepted",
            })
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env['estate.property'].browse(vals['property_id'])
            if vals.get('price') < prop.best_price:
                raise UserError(self.env._("The offer must be higher than the current best offer."))
            prop.state = 'offer_received'
        return super().create(vals_list)
