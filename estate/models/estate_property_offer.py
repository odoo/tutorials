from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offers'

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', store=True)

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.date_deadline = fields.Date.add(fields.Date.to_date(rec.create_date), days=rec.validity)
            else:
                rec.date_deadline = fields.Date.add(fields.Date.context_today(rec), days=rec.validity)

    @api.depends('create_date', 'validity')
    @api.onchange('date_deadline')
    def _inverse_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.validity = (rec.date_deadline - fields.Date.to_date(rec.create_date)).days
            else:
                rec.validity = (rec.date_deadline - fields.Date.context_today(rec)).days
