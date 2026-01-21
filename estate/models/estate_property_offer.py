from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )

    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_deadline',
        inverse="_compute_validity"
    )

    property_id = fields.Many2one('estate.property', string='Property', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(creation_date, days=record.validity)

    def _compute_validity(self):
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - creation_date.date()).days
