from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate property offers"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    property_type_id = fields.Many2one(
        'estate.property.type', related='property_id.property_type', store=True
    )
    date_deadline = fields.Date(
        compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )
    _chek_offer_price = models.Constraint(
        "CHECK(price > 0)", "offer price of property should be positive"
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            if record.property_id.selling_price:
                raise UserError("One offer is already Accepted")
            else:
                record.status = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = False
            record.status = 'refused'
        return True
