from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

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
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _check_price = models.Constraint(
        'CHECK(price > 0.00)',
        "The offer's amount should be strictly positive.",
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = datetime.today()
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = datetime.today()
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        if any(record != self and record.status == 'accepted' for record in self.property_id.offer_ids):
            raise UserError("Only one offer can be accepted")
        self.status = 'accepted'
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer = None
                record.property_id.selling_price = 0.00
            record.status = 'refused'
