from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "ch7 exercise tutorial"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        string='Offer Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")
    create_date = fields.Date(default=fields.Date.today) 
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The Price offered for an estate should be positive.'),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_offer_accept(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("A offer has already been accepted.")
            record.status = 'accepted'
            for id in record.property_id:
                id.selling_price = record.price
                id.buyer = record.partner_id
                id.state = 'offer_accepted'
        return True

    def action_offer_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("You cannot refuse an accepted offer.")
            record.status = 'refused'
        return True
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            price = vals.get('price')
            estate_property = self.env['estate.property'].browse(vals.get('property_id'))
            if estate_property.best_price and price <= estate_property.best_price:
                raise UserError(f"The selling must be higher than {estate_property.best_price:.2f}")
            estate_property.best_price = price
        return super().create(vals_list)

