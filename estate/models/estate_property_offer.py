from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models 


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)','The offered price must be positive.')
    ]

    price = fields.Float(string="Offer", required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("accept", "Accepted"), 
            ("refuse", "Refused"), 
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(
        comodel_name='estate.property', string="Property", required=True, 
        ondelete="cascade")
    validity = fields.Integer(string="Validity (Days)", default=7)
    offer_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type', string="Property Type", related="property_id.property_type_id",
        store=True)

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.offer_deadline = date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.offer_deadline-date).days

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if(val["price"] and val["property_id"]):
                prop = self.env["estate.property"].browse(val["property_id"])
                if prop.state in ['sold', 'canceled']:
                    raise exceptions.ValidationError("Cannot create an offer for a sold or canceled property.")
                if(prop.offer_ids):
                    max_offer = max(prop.mapped("offer_ids.price"))
                    if val["price"] < max_offer:
                        raise exceptions.UserError("Price must be higher than %.2f" % prop.best_price)
                else:
                    prop.state = "offer_received"
        return super().create(vals)

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
