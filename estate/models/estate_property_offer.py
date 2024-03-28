from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)",
         "An offer price must be strictly positive.")
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(copy=False, string="Status", selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one("estate.property.type", related='property_id.type_id', store=True)


    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add((record.create_date or fields.Date.today()), days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date or fields.Date.today())).days

    @api.model
    def create(self, vals):
        best_price = self.env["estate.property"].browse(vals["property_id"]).exists().best_price
        if vals["price"] < best_price:
            raise UserError("The offer must be higher than %s" % best_price)
        self.env["estate.property"].browse(vals["property_id"]).exists().state = "offer_received"
        return super().create(vals)
    
    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == 'offer_accepted' and record.property_id.buyer != record.partner_id:
                raise UserError("This property has other accepted offer")
            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True


    def action_refuse_offer(self):
        for record in self:
            if record.property_id.buyer == record.partner_id:
                record.property_id.buyer = None
                record.property_id.selling_price = 0
                record.property_id.state = 'new'
            record.status = "refused"
        return True
