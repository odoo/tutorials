from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.date_utils import date, relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for a real estate property"
    _order = "price desc"

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The price of the offer must be strictly positive'),
    ]

    price = fields.Float()
    status = fields.Selection(
            string="Status",
            selection=[('refused', 'Refused'), ('accepted', 'Accepted')]
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, copy=False)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date or date.today()) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            if record.search([("id", "!=", self.id), ("property_id", "=", self.property_id.id), ("status", "=", "accepted")]):
                raise UserError("Another offer has already been accepted")

            record.status = "accepted"
            record.property_id.selling_price = self.price

        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
            record.property_id.selling_price = 0
        return True
