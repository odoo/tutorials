from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, exceptions, tools


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)", "Offered price must be greater than 0."
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()
            start_date = fields.Date.to_date(start_date)
            record.date_deadline = start_date + relativedelta(days=record.validity)

    @api.onchange("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()
            start_date = fields.Date.to_date(start_date)
            if record.date_deadline and start_date:
                diff = record.date_deadline - start_date
                record.validity = diff.days

    def action_set_offer_status_accepted(self):
        for record in self:
            if record.property_id.state == "sold":
                raise exceptions.UserError("Only one offer can be accepted.")
            else:
                record.status = "accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.action_set_state_sold()

        return {"type": "ir.actions.client", "tag": "reload"}

    def action_set_offer_status_refused(self):
        for record in self:
            record.status = "refused"
        return True
