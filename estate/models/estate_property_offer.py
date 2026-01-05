from datetime import timedelta

from odoo import models, fields, api


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property offer for each property.'

    price = fields.Float()
    status = fields.Selection(
        selection=[('Accepted', "Accepted"), ('Refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_deadline', inverse='_inverse_deadline'
    )

    @api.depends('validity')
    def _compute_deadline(self):
        self.date_deadline = self.create_date + timedelta(days=self.validity)

    def _inverse_deadline(self):
        if self.date_deadline:
            self.validity = (
                self.date_deadline - self.create_date.date()
            ).days
