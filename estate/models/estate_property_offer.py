from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real estate property offer"

    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    price = fields.Float()
    status = fields.Selection(selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    validity = fields.Integer()
    date_deadline = fields.Date(compute='_compute_date_deadline_from_validity',
                                inverse='_compute_validity_from_deadline')

    def _compute_validity_from_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days if record.date_deadline else 0.0

    @api.depends('validity')
    def _compute_date_deadline_from_validity(self):
        for record in self:
            record.date_deadline = (record.create_date if record.create_date else fields.Date.today()) + relativedelta(
                days=record.validity)

    def accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

            if len(record.property_id.offer_ids.filtered(lambda r: r.status == 'accepted')) > 1:
                raise UserError("You can't Accept more than one offer")

        return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
