from odoo import fields, models, api

class estate_property_offer(models.Model):
    _name = "estate.property.offer"  
    _description = "real estate property offers"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one("res.partner", required = True)
    property_id = fields.Many2one("estate.property", required = True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The Offer price should be greater than equal to zero.')
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (fields.Date.add(fields.Date.today(), days=+record.validity))

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = fields.Date.add(fields.Date.today(), days=+record.validity)

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True