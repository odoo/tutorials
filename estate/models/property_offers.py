from odoo import models, fields, api


class EstateOfferModel(models.Model):
    _name = 'estate.property.offer'
    _description = "Real estate offers"
    _order = 'price desc'

    price = fields.Float()
    partner_ids = fields.Many2one('res.partner', string="Partners")
    property_id = fields.Many2one('estate.property', string="Property")
    status = fields.Selection(
        selection=[('refused', 'Refused'), ('accepted', 'Accepted')],
        default='accepted',
        string="Offer",
        copy=False
    )
    validity = fields.Integer(default=5)
    date_deadline = fields.Date(compute='_date_deadline_computed', inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('positive_price', 'CHECK(price >= 0)',
         'Price should be a positive value'),
    ]

    @api.depends('validity')
    def _date_deadline_computed(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date.date() if record.create_date else fields.Date.today(),
                days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_ids.id
        return True

    def action_reject(self):
        self.status = 'refused'
        return True
