import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers to estate properties"

    price = fields.Float("Price")
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused")
    ], "Status", required=False, copy=False)
    property_id = fields.Many2one("estate.property", "Property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Date deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    def init(self):
        self.env.cr.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS estate_property_offer_single_accepted_status
            ON %s (property_id)
            WHERE status = 'accepted'
        """ % self._table)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            starting_date = record.create_date or datetime.date.today()
            timedelta = datetime.timedelta(days=record.validity)
            record.date_deadline = starting_date + timedelta

    @api.constrains('date_deadline')
    def _check_date_deadline(self):
        for record in self:
            if record.date_deadline < fields.Date.today():
                raise ValidationError("The end date cannot be set in the past")

    def _inverse_date_deadline(self):
        for record in self:
            starting_date = record.create_date.date() or datetime.date.today()
            timedelta = record.date_deadline - starting_date
            record.validity = timedelta.days

    @api.constrains('status', 'price')
    def _check_sale_price_above_minimum(self):
        for record in self:
            if (
                    record.status == 'accepted'
                    and
                    float_compare(record.price, record.property_id.minimum_sale_price, 5) < 0
            ):
                raise ValidationError(
                    "The selling price of a property cannot be less than 90% of the expected sale price"
                )

    def accept_offer(self):
        self.status = 'accepted'

    def refuse_offer(self):
        self.status = 'refused'
