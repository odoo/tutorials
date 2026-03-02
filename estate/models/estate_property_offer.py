from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer'

    price = fields.Float(copy=False)
    status = fields.Selection(
        copy=False,
        string="status",
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
    )
    partner_id = fields.Many2one('res.partner', required=True, default=lambda self: self.env.user.partner_id.id)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=0, copy=False)
    deadline = fields.Date(compute='_compute_deadline', store=True, inverse='_inverse_deadline')

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.deadline:
                #record.validity = (record.deadline - fields.Date.today())