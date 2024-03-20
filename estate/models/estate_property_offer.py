from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    price = fields.Float()
    status = fields.Selection(string="Status", copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    create_date = fields.Date(default=lambda _: fields.Date().today())
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date().add(offer.create_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date).days
