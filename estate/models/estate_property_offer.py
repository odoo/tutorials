from dateutil.relativedelta import relativedelta

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_date")

    _check_price = models.Constraint(
        "CHECK(price > 0)", "Price of an offer must be positive"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.to_date(base_date)).days

    def action_accept(self):
        if self.property_id.customer:
            raise UserError("Only one offer can be accepted for one property")
        self.status = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        self.property_id.customer = self.partner_id
        other_offers = self.search([
            ('property_id', '=', self.property_id),
            ('status', 'not in', ('refused', 'accepted'))
            ])
        other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.selling_price = 0.00
            record.property_id.customer = None

    @api.model_create_multi
    def create(self, vals_list):
        prop = self.env['estate.property'].browse(vals_list[0]['property_id'])

        for vals in vals_list:
            if vals['price'] < prop.best_price:
                raise UserError(
                    _('An offer with a lower price than an existing one cannot be created.')
                )

        if prop.state == 'new':
            prop.state = 'offer_received'

        return super().create(vals_list)
