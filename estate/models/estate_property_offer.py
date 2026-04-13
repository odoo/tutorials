from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real E-state offer"

    price = fields.Float()
    status = fields.Selection(
        string="Offer Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for records in self:
            base_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            records.date_deadline = fields.Date.add(base_date, days=records.validity)

    def _inverse_date_deadline(self):
        for records in self:
            base_date = (
                records.create_date.date()
                if records.create_date
                else fields.Date.today()
            )
            if records.date_deadline:
                records.validity = (records.date_deadline - base_date).days

    def accept_button(self):
        for records in self:
            records.status = "accepted"
            records.property_id.buyer = records.partner_id
            records.property_id.selling_price = records.price
            records.property_id.state = "offer_accepted"

    def reject_button(self):
        for records in self:
            records.status = "refused"
            if records.property_id.buyer == records.partner_id:
                records.property_id.buyer = False
                records.property_id.selling_price = False
                records.property_id.state = "offer_received"
