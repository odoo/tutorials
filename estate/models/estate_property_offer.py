from odoo import api, fields, models

from odoo.exceptions import UserError
from odoo.tools import date_utils


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate property offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        string="Offer Status",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        string="Offer Deadline",
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = date_utils.add(
                    record.create_date, days=record.validity
                )
            else:
                record.date_deadline = date_utils.add(
                    fields.Date.today(), days=record.validity
                )

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = (record.date_deadline - record.create_date).days

    def action_set_offer_accepted(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError(
                    "cannot accept this offer, another offer has been accepted"
                )

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            record.property_id.state = "offer accepted"
        return True

    def action_set_offer_refused(self):
        for record in self:
            record.status = "refused"
        return True
