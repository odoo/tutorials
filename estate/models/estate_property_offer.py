from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    type_id = fields.Many2one("estate.property.type", related="property_id.type_id", store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'An offer price must be strictly positive',
    )

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = [vals.get('property_id') for vals in vals_list]
        properties = self.env['estate.property'].browse(property_ids)
        best_prices = {prop.id: prop.best_price for prop in properties}

        for vals in vals_list:
            best_price = best_prices.get(vals.get('property_id'), 0.0)
            if float_compare(vals.get('price', 0.0), best_price, precision_digits=2) < 0:
                raise UserError(self.env._("A new offer must be higher than the best offer"))
        offers = super().create(vals_list)
        offers.property_id.state = 'offer_received'
        return offers

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.deadline = fields.Date.add(fields.Date.to_date(record.create_date), days=record.validity)
            else:
                record.deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = (record.deadline - fields.Date.today()).days

    def action_confirm_offer(self):
        for record in self:
            if 'accepted' in record.property_id.offer_ids.mapped('status'):
                raise UserError(self.env._("An offer has already been accepted for this property"))
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_cancel_offer(self):
        for record in self:
            record.status = 'refused'
        return True
