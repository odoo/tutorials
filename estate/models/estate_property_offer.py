from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(
            selection=[
                ('accepted', 'Accepted'),
                ('refused', 'Refused')],
            copy=False,
            help="State of the estate property offer")
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
            'Deadline',
            compute='_compute_date_deadline',
            inverse='_onchange_date_deadline',
            help='Deadline defined as date from creation separated by validy dates')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Datetime.now(), days=record.validity)

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

