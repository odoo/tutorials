from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "test description 4"
    _order ="price desc"

    price = fields.Float(allow_negative=False)
    status = fields.Selection(
        copy=False, selection=[("refused", "Refused"), ("accepted", "Accepted")]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, store=True)
    date_deadline = fields.Date(
        compute="_compute_date", inverse="_inverse_date", store=True
    )
    create_date = fields.Date(default=date.today(), readonly=True, store=True)

    @api.depends("validity")
    def _compute_date(self):
        for dates in self:
            if dates.validity:
                dates.date_deadline = dates.create_date + relativedelta(
                    days=dates.validity
                )

    def _inverse_date(self):
        for dates in self:
            if dates.date_deadline:
                dates.validity = (dates.date_deadline - dates.create_date).days

    def offer_accept(self):
        if self.property_id.buyer:
            raise UserError(
                "This property already has an offer that has been accepted!"
            )
        else:
            if self.price >= (0.9) * self.property_id.expected_price:
                self.property_id.selling_price = self.price
                self.property_id.buyer = self.partner_id
                self.status = "accepted"
                self.property_id.state = "offer accepted"
            else:
                raise ValidationError(
                    "The acceptance offer should be atleast 90 percent of the expected price"
                )

    def offer_refuse(self):
        self.status = "refused"
        if self.partner_id == self.property_id.buyer:
            self.property_id.buyer = None
            self.property_id.selling_price = 0
            

    @api.constrains("price")
    def _check_price_positive(self):
        for record in self:
            if record.price < 0:
                raise ValidationError("Price cannot be negative!")
