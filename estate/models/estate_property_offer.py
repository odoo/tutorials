from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for a property"

    price = fields.Float()
    status = fields.Selection([
        ('refused', 'Refused'),
        ('accepted', 'Accepted')
    ], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Datetime(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if (offer.create_date):
                offer.date_deadline = fields.Datetime.add(offer.create_date, days=offer.validity)
            else:
                offer.date_deadline = fields.Datetime.add(fields.Datetime.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if (offer.create_date):
                offer.validity = (offer.date_deadline - offer.create_date).days
            else:
                offer.validity = (offer.date_deadline - fields.Datetime.today()).days
