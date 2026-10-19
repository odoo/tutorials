from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "It is a estate property offer model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refuse", "Refuse")], copy=False
    )

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_date_validity"
    )
    create_date = fields.Date(default=date.today())
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(
                days=record.validity
            )

    def _inverse_date_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_property_sold(self):
        self.status = "accepted"
        records = self.property_id.offer_ids
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
        self.property_id.state = "offer_accepted"

        for record in records:
            if self.id != record.id:
                record.status = "refuse"

    def action_property_cancel(self):
        self.status = "refuse"

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price of property must be positive",
    )
