from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    # Order attributes
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    validity = fields.Integer(default=7,)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    partner_id = fields.Many2one("res.partner", required=True,)
    property_id = fields.Many2one("estate.property", required=True,)
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    # -------------------------------------------------------------------------
    # CONSTRAINTS
    # -------------------------------------------------------------------------
    _check_price = models.Constraint(
        'CHECK(price > 0)', 
        'An offer price must be strictly positive.',
    )

    @api.depends("create_date", "validity",)
    def _compute_date_deadline(self,):
        for offer in self:
            base_date = (offer.create_date or fields.Datetime.now()).date()
            offer.date_deadline = base_date + timedelta(days=offer.validity,)

    def _inverse_date_deadline(self,):
        for offer in self:
            base_date = (offer.create_date or fields.Datetime.now()).date()
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - base_date).days

    # -------------------------------------------------------------------------
    # CRUD methods
    # -------------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list,):
        for vals in vals_list:
            property_record = self.env['estate.property'].browse(vals['property_id'])
            
            if property_record.offer_ids:
                best_price = max(property_record.offer_ids.mapped('price'))
                if vals.get('price', 0) < best_price:
                    raise UserError(self.env._("You cannot create an offer with a price lower than the current best offer."))
            
            property_record.state = 'offer_received'
            
        return super().create(vals_list)

    # -------------------------------------------------------------------------
    # ACTIONS
    # -------------------------------------------------------------------------
    def action_accept(self,):
        for offer in self:
            if offer.property_id.state in ('sold', 'canceled',):
                raise UserError(self.env._("You cannot accept an offer on a sold or canceled property."))
            
            if offer.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise UserError(self.env._("An offer has already been accepted for this property."))
            
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            
            other_offers = offer.property_id.offer_ids - offer
            other_offers.status = 'refused'
            
        return True
            
    def action_refuse(self,):
        for offer in self:
            if offer.property_id.state in ('sold', 'canceled',):
                raise UserError(self.env._("You cannot refuse an offer on a sold or canceled property."))
                
        self.status = 'refused'
        
        return True
