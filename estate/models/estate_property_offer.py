# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions, _
from odoo.tools import relativedelta
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    validity = fields.Integer(string="Offer Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'The price must be strictly positive.')
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline_date(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.to_date(record.create_date) + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        self.ensure_one()

        if self.property_id.offer_ids.filtered(lambda r: r.status == 'accepted'):
            raise exceptions.UserError(_("Another offer is already accepted on this property."))

        self.property_id.accept_offer(self.price, self.partner_id)
        return self.write({'status': 'accepted'})

    def action_refuse(self):
        self.ensure_one()
        return self.write({'status': 'refused'})

    @api.model_create_multi
    def create(self, values):
        best_price = self.env['estate.property'].browse(values[0]['property_id']).best_price
        records = super().create(values)

        for record in records:
            if float_compare(record.price, best_price, 2) == -1:
                raise exceptions.UserError(_("The price of your offer should not be lower than the best offer."))

            record.property_id.state = 'offer_received'

        return records
