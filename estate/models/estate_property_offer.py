from odoo import api, fields, models


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    # --------------------------------------- Fields Declaration ----------------------------------
    # Basic
    price = fields.Float("Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default=False,
    )
    # Relational
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    # ---------------------------------------- Compute methods ------------------------------------
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.validity = (offer.date_deadline - date).days
