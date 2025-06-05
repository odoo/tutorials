from odoo import api, fields, models


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("cancelled", "Cancelled"),
        ],
        default="accepted",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True
    )
    property_id = fields.Many2one(
        comodel_name="estate.property", string="Property", required=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.validity:
                offer.date_deadline = fields.Date.add(
                    fields.Date.today(), days=offer.validity
                )
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.today()).days
            else:
                offer.validity = 0
