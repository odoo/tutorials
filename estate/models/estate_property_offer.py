from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date if offer.create_date else fields.Datetime.now()
            offer.date_deadline = fields.Date.add(date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
