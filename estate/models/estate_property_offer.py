# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate offers tag info"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    validity = fields.Integer(string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    _check_price = models.Constraint(
        "CHECK(price >= 0)",
    )

    @api.depends("validity", "property_id.date_availability")
    def _compute_date_deadline(self):
        for record in self:
            if record.validity and record.property_id.date_availability:
                record.date_deadline = fields.Date.add(record.property_id.date_availability, days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.property_id.date_availability:
                record.validity = fields.Date.subtract(record.date_deadline, record.property_id.date_availability).day

    def action_set_property_offer_status_to_accepted(self):
        for record in self:
            if record.property_id.state in ["sold", "cancelled", "offer_accepted"]:
                raise exceptions.UserError("An offer was already accepted or the sale was cancelled !")
            else:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id.name = record.partner_id.name
                record.property_id.state = "offer_accepted"
        return True

    def action_set_property_offer_status_to_refused(self):
        for record in self:
            record.status = "refused"
        return True
