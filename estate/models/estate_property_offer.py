from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(start_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            start_date = fields.Date.to_date(offer.create_date) or fields.Date.today()
            offer.validity = (offer.date_deadline - start_date).days
