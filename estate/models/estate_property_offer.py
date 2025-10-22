from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "property offer"

    price = fields.Float('price')
    status = fields.Selection(
        string='status',
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", string="partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + relativedelta(days=offer.validity)
            else:
                offer.date_deadline = date.today() + relativedelta(days=offer.validity)

    @api.depends()
    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - date.today()).days
            if offer.validity < 0:
                offer.validity = 0
