from odoo import fields, models, api


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer for Estate Property"

    price = fields.Float("Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        "Deadline",
        compute="_compute_date_deadline",
        inverse="_compute_inverse_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(
                fields.Date.to_date(create_date), days=offer.validity
            )

    def _compute_inverse_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.validity = (
                offer.date_deadline - fields.Date.to_date(create_date)
            ).days
