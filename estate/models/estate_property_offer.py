from odoo import fields, models, api
from datetime import timedelta, date
from odoo.exceptions import UserError


class EstatePropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([('ACCEPTED', 'Accepted'), ('REFUSED', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse='_inverse_deadline', string='Deadline')

    @api.depends("validity", 'create_date')
    def _compute_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Datetime.now()
            record.date_deadline = creation_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days

    def action_accept_offer(self):
        for record in self:
            if record.status == "ACCEPTED":
                raise UserError('Offer is already accepted')
            record.property_id.refuse_all()
            record.status = "ACCEPTED"
            record.property_id.update_on_accept(record.price, record.partner_id)

    def action_refuse_offer(self):
        for record in self:
            if record.status == "ACCEPTED":
                record.property_id.update_on_refuse_accepted()
            else:
                raise UserError('Offer is already refused')
            record.status = "REFUSED"
        return True

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive.'),
    ]
