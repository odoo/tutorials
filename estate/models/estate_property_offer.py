from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "property offer"

    price = fields.Float()
    status = fields.Selection(
        string='status',
        selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')],
        copy=False)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", string="partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + relativedelta(days=offer.validity)
            else:
                offer.date_deadline = date.today() + relativedelta(days=offer.validity)

    @api.depends()
    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - date.today()).days
            if offer.validity < 0:
                offer.validity = 0

    def action_accept(self):
        if (self.property_id.selling_price != 0.0):
            raise UserError("Property already sold")
        else:
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.status = 'Accepted'
        return True

    def action_refuse(self):
        self.status = 'Refused'
        return True

    @api.constrains('price')
    def _check_price_validity(self):
        if (float_is_zero(self.price, 0)):
            raise ValidationError("Offered price must be at least a euro")
        min_amount = self.property_id.expected_price * 0.9
        if (float_compare(self.price, min_amount, 2) < 0):
            raise ValidationError("Offered price must be at least 90% of the expected price")
