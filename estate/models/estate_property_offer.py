from odoo import models, fields, api

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', required=True, string='Partner')
    property_id = fields.Many2one(comodel_name='estate.property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(fields.Date.to_date(record.create_date), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = fields.Date.subtract(record.date_deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = fields.Date.subtract(record.date_deadline - fields.Date.today()).days

    # def action_property_cancel(self):
    #     for record in self:
