from odoo import fields,models,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class estate_property_offer(models.Model):
    # Private attributes
    _name = "estate.property.offer"
    _description = "Estate property offer file"
    _order = "price desc"

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price should be strictly positive.')
    ]

    # Fields declaration
    price = fields.Integer('Price',required=True, default=100000)
    validity = fields.Integer("validity days", default=7)
    date_dateline = fields.Date("Date deadline",compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    status = fields.Selection(
        string="Offer Status",
        selection=[('Accepted','Acccepted'),
            ('In Waiting','In Waiting'),
            ('Refused','Refused')],
        default="In Waiting",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner",required=True)
    property_id = fields.Many2one("estate.property", string="Property",required=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)

    # compute and search fields
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_dateline=fields.Date.context_today(self)+relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_dateline - fields.Date.context_today(self)).days

    # CRUD methods
    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["property_id"])
            if prop.property_offer_ids:
                max_offer = max(prop.property_offer_ids.mapped("price"))
                print(max_offer)
                if vals["price"]<max_offer:
                    raise UserError("offer with better price already exist")
            else:
                prop.estate_state="Offer_Received"
        return super().create(vals)

    #Action methods
    def action_refuse_offer(self):
        for record in self:
            if record.status == "Accepted":
                raise UserError('Unable to refuse offer, please change offer status before continuing.')
            record.status = "Refused"
    
    def action_accept_offer(self):
        for record in self:
            if record.property_id.estate_state=="Cancelled" or record.property_id.estate_state=="Sold":
                raise UserError("Unable to accept offer (estate can't be sold), please change estate status before continuing.")
            if record.status == "Refused":
                raise UserError('Unable to accept offer, please change offer status before continuing.')
            record.status = "Accepted"
            record.property_id.estate_state="Offer_Accepted"
            record.property_id.property_buyer_id = record.partner_id
            record.property_id.selling_price =record.price
