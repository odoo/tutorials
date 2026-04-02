from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute='_compute_date_deadline', inverse="_inverse_deadline",
    )

    _check_offer_price = models.Constraint(
        'CHECK (price > 0)', 'Offer price must be strictly positive'
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = start_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - start_date).days

    def action_accepted(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == "accepted":
                    raise UserError(
                        "Only 1 offer can be accepted for each property")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
        return True

    def action_refused(self):
        for record in self:
            record.status = "refused"
        return True
