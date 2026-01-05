from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"

    price = fields.Integer()
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        "Deadline", compute='_compute_validity', inverse='_inverse_validity'
    )

    @api.depends('validity', 'create_date')
    def _compute_validity(self):
        start_date = (
            self.create_date.date() if self.create_date else fields.Date.today()
        )
        self.date_deadline = start_date + relativedelta(days=self.validity)

    def _inverse_validity(self):
        start_date = (
            self.create_date.date() if self.create_date else fields.Date.today()
        )
        self.validity = (self.date_deadline - start_date).days
