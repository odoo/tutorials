from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(string="Deadline Date", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.date_deadline =  relativedelta(days=record.validity) + creation_date

    def _inverse_date_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.to_date(creation_date)).days

    def action_accept(self):
        for record in self:
            if record.property_id.buyer_id:
                raise UserError("Property already accepted")
            else:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'
                record.property_id.buyer_id = record.partner_id

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The price of an offer must be strictly positive.'
    )
