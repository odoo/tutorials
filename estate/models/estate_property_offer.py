from dateutil import relativedelta

from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property Offer"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive."),
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + relativedelta.relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - create_date.date()).days

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True

    def action_accept_offer(self):
        for record in self:
            record.status = "accepted"
            record._onchange_status()

        return True

    @api.onchange("status")
    def _onchange_status(self):
        if self.status != "accepted":
            return

        if self.property_id.state in {"accepted", "sold"}:
            self.status = False
            raise exceptions.UserError("An offer as already been accepted.")

        self.property_id.selling_price = self.price
        self.property_id.state = "accepted"
        self.property_id.partner_id = self.partner_id
