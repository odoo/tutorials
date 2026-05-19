from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateOffer(models.Model):
    _name = "est.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    _check_price = models.Constraint(
        'CHECK (price >= 0)',
        'The Price should be positive!',
    )


    name = fields.Char("name")
    price = fields.Integer("price",required=True)
    status = fields.Selection(
        string="status", 
        default="waiting",
        selection = [
            ("accepted","Accepted"),
            ("refused","Refused"),
            ("waiting","Waiting"),
        ],
    )
    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("est.property",required=True)

    property_type_id = fields.Many2one("est.property.type", related="property_id.property_type_id", stored=True, compute="_compute_property_type_id") 


    validity_date = fields.Date(compute="_compute_validity_date",inverse="_inverse_validity_duration")
    validity_duration = fields.Integer(default=7)
    
    @api.depends("validity_duration")
    def _compute_validity_date(self):
        for offer in self:
            offer.validity_date = fields.Date.today() + timedelta(days=offer.validity_duration)

    @api.depends("property_id")
    def _compute_property_type_id(self):
        for offer in self:
            if offer.property_id.property_type_id:
                offer.property_type_id = offer.property_id.property_type_id
            else:
                offer.property_type_id = False
    
    def _inverse_validity_duration(self):
        for offer in self:
            offer.validity_duration = (offer.validity_date - fields.Date.today()).days
    
    def action_confirm(self):
        for offer in self:
            if offer.property_id.state == "sold":
                raise UserError(self.env._("Property was already sold!"))
            elif offer.property_id.state == "cancelled":
                raise UserError(self.env._("Property was already cancelled!"))
            elif offer.status == "refused":
                raise UserError(self.env._("Cannot accept a proposal that was already refused!"))
            else:
                offer.status = "accepted"
                offer.property_id.selling_price = offer.price
                offer.property_id.partner_id = offer.partner_id
                offer.property_id.state = "sold"

    def action_reject(self):
        self.status = "refused"

    @api.model
    def create(self,vals_list):
        for vals in vals_list:
            property = self.env['est.property'].browse(vals.get('property_id'))
            
            if property.state == 'new':
                property.state = 'offer_received'

            if property.max_offer > vals.get('price',0):
                raise UserError(self.env._("Cannot create an offer with a lower value than a previous one!"))

        return super().create(vals_list)
