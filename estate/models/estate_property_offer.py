from odoo import fields, models, api, exceptions


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for estate."

    price = fields.Float(string="Price")

    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        readonly=True)

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
        compute="_compute_deadline_date",
        inverse="_compute_validity_time")

    @api.depends("validity")
    def _compute_deadline_date(self):
        for offer in self:
            offer.date_deadline = fields.Date.add(
                offer.create_date or fields.Date.today(),
                days=offer.validity)

    @api.onchange("date_deadline")
    def _compute_validity_time(self):
        for offer in self:
            delta = offer.date_deadline - fields.Date.to_date(
                offer.create_date or fields.Date.today())
            offer.validity = delta.days

    def _set_offer_status(self):
        for offer in self.env["estate.property.offer"].search([("property_id", "=", self.property_id.id)]):
            if offer.id != self.id:
                offer.status = "refused"

    def accept_offer(self):
        self.status = "accepted"
        id = self.property_id
        self.env["estate.property"].search(
            [("id", "=", id.id)]).buyer_id = self.partner_id
        self.env["estate.property"].search(
            [("id", "=", id.id)]).selling_price = self.price
        self._set_offer_status()
        return True

    def refuse_offer(self):
        self.status = "refused"
        return True
