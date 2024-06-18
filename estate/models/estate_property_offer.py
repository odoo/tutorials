from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer to buy a real estate property"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            try:
                offer.date_deadline = fields.Date.add(offer.create_date, days=offer.validity)
            except:
                offer.date_deadline = fields.Date.add(fields.Date.today(), days=offer.validity)

    @api.depends('create_date', 'date_deadline')
    def _compute_validity(self):
        for offer in self:
            try:
                offer.validity = (offer.date_deadline - fields.Date().to_date(offer.create_date)).days
            except:
                offer.validity = (offer.date_deadline - fields.Date().today()).days

    def _inverse_deadline(self):
        for offer in self:
            offer.date_deadline = offer.date_deadline

    def _inverse_validity(self):
        for offer in self:
            offer.validity = offer.validity

    validity = fields.Integer(default=7, compute=_compute_validity, inverse=_inverse_validity)
    date_deadline = fields.Date(compute=_compute_deadline, inverse=_inverse_deadline)
