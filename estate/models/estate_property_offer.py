from odoo import models, fields, api
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Offer Status",
        selection=[
            ("offer_accepted", "Accepted"),
            ("offer_refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer price must be greater than 0",
    )

    @api.model
    def create(self, vals_list):
        property_id = vals_list[0].get('property_id')
        offer_price = vals_list[0].get('price')
        property_model = self.env['estate.property'].browse(property_id)

        if float_compare(offer_price, property_model.best_price, precision_digits=2) < 0:
            raise ValidationError("New offers cannot have a lower amount than an existing offer")

        property_model.state = 'offer_received'

        return super().create(vals_list)

    # -------------------------------------------------------------------------
    # COMPUTE METHODS
    # -------------------------------------------------------------------------

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else date.today()
            )
            record.date_deadline = start_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else date.today()
            )
            date_diff = record.date_deadline - start_date
            record.validity = date_diff.days

    def action_accept_offer(self):
        for record in self:
            if any(
                offer.status == "offer_accepted"
                for offer in record.property_id.offer_ids
            ):
                raise UserError("Another offer has already been accepted.")
            else:
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
                record.status = "offer_accepted"
                record.property_id.state = "offer_accepted"

    def action_refuse_offer(self):
        for record in self:
            record.status = "offer_refused"
        return True
