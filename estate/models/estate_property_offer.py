from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='price', required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'),
        ('refused', 'Refused')],
        string="Status",
        copy=False,
        default='accepted',
    )

    validity = fields.Integer(string='Validity(days)', default=7)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', store=True)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                create_date = offer.create_date.date()
            else:
                create_date = fields.Date.today()
                offer.date_deadline = create_date + relativedelta(days=offer.validity)

    def action_accept(self):
        for offer in self:
            if offer.state != 'Refused':
                offer.state = 'Accepted'
            else:
                raise UserError("A refused offer cannot be accepted.")
        return True

    def action_refuse(self):
        for offer in self:
            if offer.state != 'Accepted':
                offer.state = 'Refused'
            else:
                raise UserError("An accepted offer cannot be refused.")
        return True