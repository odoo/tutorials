from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import add


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    _sql_constraints = [
        ('check_positive_price', 'CHECK (price > 0)', 'The price of an offer should be strictly positive')
    ]

    # Model Fields
    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])

    # Relational Fields
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # Computed Fields
    validity = fields.Integer(default="7")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    # Computation methods
    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.to_date(add(record.create_date, days=record.validity))
            else:
                record.date_deadline = fields.Date.to_date(add(fields.Date.today(), days=record.validity))

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = int((record.date_deadline - fields.Date.to_date(record.create_date)).days)

    # Buttons methods
    def action_validate(self):
        for record in self:
            record.property_id.action_refuse_all_offer()
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = "offer_accepted"
            record.status = "accepted"

    def action_cancel(self):
        for record in self:
            record.status = "refused"

    @api.model
    def create(self, vals):
        if self.env['estate.property.offer'].search([
            ('property_id', '=', vals['property_id']),
            ('price', '>', vals['price'])
        ], limit=1):
            raise UserError("You're trying to create an offer with a lower price than an existing offer")

        property_record = self.env["estate.property"].browse([vals['property_id']])
        property_record.state = "offer_received"

        return super().create(vals)
