from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'the offer of the property being sold'

    price = fields.Float()
    status = fields.Selection(selection = [('accepted', 'Accepted'), ('refused', 'Refused')], copy = False)
    partner_id = fields.Many2one('res.partner', string = 'Partner', required = True)
    property_id = fields.Many2one('estate.property', string = 'Property', required = True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_compute_date_deadline', inverse = '_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = fields.Date.from_string(record.create_date)
                deadline_date = fields.Date.from_string(record.date_deadline)
                record.validity = (deadline_date - create_date).days
