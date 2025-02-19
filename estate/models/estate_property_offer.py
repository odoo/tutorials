from dateutil.relativedelta import relativedelta
from odoo import fields
from odoo import api
from odoo import models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _sql_constraints = [
        ('check_offer_price','CHECK(offer_price > 0)','Offer Price must be a positive amount')
    ]
    _order = "offer_price desc"

    #-------------------------------------------Basic Fields-------------------------------------------#
    offer_price = fields.Float(string="Price", required=True)
    state = fields.Selection(string="State", selection=[('offer_received','Offer Received'), ('offer_accepted','Offer Accepted'), ('offer_rejected','Offer Rejected')],
                             copy=False)
    validity = fields.Integer(string="Validity(days)", default=7)
    
    #-------------------------------------------Relational Fields---------------------------------------#
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    
    #-------------------------------------------Computed Fields------------------------------------------#
    deadline_date = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    # ------------------------------------------Compute Methods----------------------------------------#
    @api.depends("create_date", "validity")
    def _compute_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.deadline_date = date + relativedelta(days=offer.validity)

    def _inverse_deadline_date(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.deadline_date - date).days

    # --------------------------------------------Action Methods------------------------------------------------
    def action_offer_accept(self):
        if self.state == "offer_accepted":
            raise UserError('offer is already accepted')
        self.state = "offer_accepted"
        self.property_id.write({
            'selling_price' : self.offer_price,
            'buyer_id' : self.partner_id,
            'state' : "offer_accepted"
        })
        for property in self.property_id.offer_ids:
            if property.id != self.id:
                property.state = "offer_rejected"
        return True
        
    def action_offer_reject(self):
        self.state = "offer_rejected"
        self.property_id.selling_price = 0
        self.property_id.buyer_id = None
        return True

    #-------------------------------------CRUD methods------------------------------------------#
    @api.model_create_multi
    def create(self, vals):
        property = self.env['estate.property'].browse(vals.get('property_id'))
        if property.offer_ids:
            if vals.get('offer_price') < property.best_price:
                raise ValidationError("The offer price should be more than best offer")
        property.state = "offer_received"
        return super().create(vals)
