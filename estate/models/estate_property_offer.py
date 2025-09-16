from datetime import date, timedelta
from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float("Price", required=True)
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @property
    def _create_date(self) -> date:
        if self.create_date is not None:
            return self.create_date.date()
        else:
            return fields.Date.today()

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self) -> None:
        for offer in self:
            offer.date_deadline = offer._create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer._create_date).days
