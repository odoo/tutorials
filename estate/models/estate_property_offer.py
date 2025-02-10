from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This contains offer related configurations."
    _order = "price desc"


    price = fields.Float(string="Offer", required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("accept", "Accepted"), 
            ("refuse", "Refused"), 
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    offer_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", related="property_id.property_type_id", store=True)
    
    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)',
         'The offered price must be positive.')
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.offer_deadline = date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.offer_deadline-date).days
    
    def action_accept(self):
        for record in self:
            record.status = "accept"
                    # Find other records and set their status to "refused"
            other_records = self.search([('id', '!=', record.id), ('property_id', '=', record.property_id.id)])
            for other_record in other_records:
                other_record.status = 'refuse'
            bought_property = record.property_id
            bought_property.buyer_id = record.partner_id
            bought_property.selling_price = record.price
            bought_property.state = 'offer_accepted'
        return True

    def action_reject(self):
        for record in self:
            record.status = "refuse"
        return True

    @api.model
    def create(self, vals):
        if(vals["price"] and vals["property_id"]):
                prop = self.env["estate.property"].browse(vals["property_id"])
                if(prop.offer_ids):
                    max_offer = max(prop.mapped("offer_ids.price"))
                    if vals["price"] < max_offer:
                        raise exceptions.UserError("Price must be higher than %.2f" % prop.best_price)
                else:
                    prop.state = "offer_received"
        return super().create(vals)
