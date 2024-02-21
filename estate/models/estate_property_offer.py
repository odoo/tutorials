from odoo import fields, models, api


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for estate."

    price = fields.Float(string="Price")

    status = fields.Selection(
            string="Status",
            copy=False,
            selection=[("accepted", "Accepted"), ("refused", "Refused")],)

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    property_id = fields.Many2one(
            "estate.property", string="Property", required=True)

    validity = fields.Integer(
            default=7,
            string="Validity",
            readonly=False,)

    date_deadline = fields.Date(
            default=fields.Date.today(),
            string="Deadline Date",
            compute="_get_deadline_date",
            inverse="_get_validity_time")

    @api.depends("validity")
    def _get_deadline_date(self):
        for offer in self:
            offer.date_deadline = fields.Date.add(
                    offer.create_date,
                    days=offer.validity)

    @api.onchange("date_deadline")
    def _get_validity_time(self):
        for record in self:
            delta = record.date_deadline - (
                    record.create_date or fields.Date.today())
            record.validity = delta.days

    def accept_offer(self):
        self.status = "accepted"
        return True

    def refuse_offer(self):
        self.status = "refused"
        return True
