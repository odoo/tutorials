from odoo import api, fields, models


class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float("Offer Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date("Deadline", compute='_compute_date_deadline', inverse="_inverse_date_deadline")

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date.date()).days
