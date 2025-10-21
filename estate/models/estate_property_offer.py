from odoo import api, models, fields


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(
                    offer.create_date.date(), days=offer.validity)
            else:
                offer.date_deadline = fields.Date.add(
                    fields.Date.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                delta = (offer.date_deadline - offer.create_date.date()).days
                offer.validity = delta
            elif offer.date_deadline:
                delta = (offer.date_deadline - fields.Date.today()).days
                offer.validity = delta
