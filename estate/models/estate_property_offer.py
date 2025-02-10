from odoo import api,models, fields
from datetime import timedelta  

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property offer'
    _order = "price desc"
    
    price = fields.Float(string='Price', required=True)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", default=lambda self: self.env.user)
    property_id = fields.Many2one('estate.property', string="Offer")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline",inverse="_inverse_date_deadline")
    validity = fields.Integer(string="Validity (days)", default=7)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)
   
    
    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days if record.date_deadline else 7

    def property_action_accept(self):
        for record in self:
            if not any(rec.status == "accepted" for rec in self):
                record.status = 'accepted'
                record.property_id.state = 'offer_accepted'
                record.property_id.partner_id = record.partner_id
                record.property_id.selling_price = record.price

    def property_action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.state = 'new'
            
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive.')
    ]