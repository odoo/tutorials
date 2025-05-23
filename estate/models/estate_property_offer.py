from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "real esate properties offers"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ('pending', 'Pending')
        ],
        copy=False,
        default='pending',
        required=True
    )
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    property_id = fields.Many2one('estate.property', 'Property', required=True)

    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date('Deadline', compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if not record.validity:
                record.date_deadline = False
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if not record.date_deadline:
                record.validity = 0
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_to_accept(self):
        for record in self:
            property_obj = record.property_id
            if property_obj.state in ["sold", "offer_accepted"]:
                raise UserError(_('Property already accepted an offer.'))
            record.status = 'accepted'
            property_obj.selling_price = record.price
            property_obj.partner_id = record.partner_id
            property_obj.state = 'offer_accepted'

            (property_obj.offer_ids - record).action_to_refuse()
        return True

    def action_to_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    def action_to_undo(self):
        for record in self:
            property_obj = record.property_id

            if record.status == 'accepted':
                property_obj.state = 'offer_received'
                property_obj.partner_id = False
                property_obj.selling_price = 0

            record.status = 'pending'
        return True
