from odoo import api, fields, models

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    # misc
    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')], 
        copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    # computed
    validity = fields.Integer(default=7, string='Validity (days)')
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string='Deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            safe_create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(safe_create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            safe_create_date = record.create_date or fields.Date.today()
            delta = record.date_deadline - fields.Date.to_date(safe_create_date)
            record.validity = delta.days