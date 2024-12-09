from odoo import fields, models, api
from odoo.exceptions import UserError


class estate_property_offer(models.Model):
    _name = "estate.property.offer"  
    _description = "real estate property offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", required = True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(comodel_name="estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The Offer price should be greater than equal to zero.')
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 0

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
    

    @api.model
    def create(self, vals):
        property_record = self.env['estate.property'].browse(vals['property_id'])
        
        if property_record.offer_ids.filtered(lambda o: o.price >= vals['price']):
            raise UserError("You cannot create an offer lower than an existing offer.")
        
        property_record.state = 'Offer Received'
        
        return super(estate_property_offer, self).create(vals)