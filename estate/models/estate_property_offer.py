from datetime import timedelta
from odoo import api, fields, models, tools
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = "price desc"

    price = fields.Float(string="Offer Price", required=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status"
    )
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer('Validity (in days)', default=7)
    date_deadline = fields.Date('Date Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    sequence = fields.Integer('Sequence', help="Used to order offers, first is best")
    property_type_id = fields.Many2one("estate.property.type",string="Property Type",related="property_id.property_type_id",store=True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (record.create_date + timedelta(days=record.validity)).date()
            else:
                record.date_deadline = fields.Date.today()+ timedelta(days=record.validity)
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env["estate.property"].browse([vals.get("property_id")])
            if property_id.state == "sold":
                raise UserError("Offers for sold properties cannot be created.")
            if tools.float_compare(vals.get("price", 0.0), property_id.best_price, precision_digits=2) < 0:
                raise UserError("The offered price cannot be lower than the best price.")
        return super().create(vals_list) 

    def _inverse_date_deadline(self):
        if self.date_deadline:
            self.validity = (self.date_deadline - self.create_date.date()).days

    def action_accept_offer(self):
        if self.property_id.state == 'sold':
            raise UserError("This property is already sold!")
        if self.property_id.buyer_id:
            raise UserError("This property already has a buyer!")

        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'

    def action_refuse_offer(self):
        self.status = 'refused'
        self.property_id.buyer_id = False
        self.property_id.selling_price = False
        self.property_id.state = 'offer_received'

