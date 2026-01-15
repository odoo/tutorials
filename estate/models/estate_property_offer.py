from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is the table of offer that is received for property"
    _order = "price desc"

    price = fields.Float('price')
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    _check_offer_price = models.Constraint(
        "check(price > 0)",
        "Offer price must be positive",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create = record.create_date or fields.Date.today()
            record.date_deadline = (create + relativedelta(days=record.validity))

    def _inverse_date_deadline(self):
        for record in self:
            create = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.today(create)).days

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.customer_id:
                raise UserError(_("Only one offer can be accepted."))
            offer.property_id.customer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "sold"
            offer.status = "accepted"
        other_offer = offer.property_id.offer_ids.filtered(
            lambda s: s.status != offer.status
        )
        other_offer.status = "refused"

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True
