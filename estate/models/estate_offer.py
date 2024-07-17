from odoo import api, fields, models

class EstateOfferModel(models.Model):
    _name = 'estate.property.offer'
    _description = "Real estate property offers"
    _order = 'price desc'
    _sql_constraints = [('check_price', 'CHECK(price > 0)', "The offer price must be positive.")]

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', required=True)
    status = fields.Selection(selection=[('accepted', "Accepted"),
                                         ('refused', "Refused"),
                                         ],
                              copy=False)
    property_id = fields.Many2one('estate.property')
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(start, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start).days

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer = record.partner_id
            record.property_id.seller = self.env.user
            record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.buyer = None
            record.property_id.seller = None
            record.property_id.selling_price = 0
