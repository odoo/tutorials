from odoo import api, fields, models


class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = "A  model where offer for the properties are stored"

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('accepted', "Accepted"),
                              ('refused', "Refused")],
                              required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one(
        'estate.property', required=True)
    validity = fields.Integer(string="Validity", default='7')
    date_deadline = fields.Datetime(
        string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Date.context_today(self)
            rec.date_deadline = fields.Date.add(create_date, days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Date.context_today(self)
            rec.validity = (rec.date_deadline - create_date).days
