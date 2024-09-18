from odoo import models, fields, api

class EstatePropertyOffer(models.Model):


    _name = "estate.property.offer"
    _description = "Offers of estate.property"


    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False
    )

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(),days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    #TODO: validity does not refresh until we refresh the page (it is normal but why ?)
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for offer in self:
            offer.status = "accepted"
            #filtered: return the records in self(input recordset) satisfying param func
            #return self.browse([rec.id for rec in self if func(rec)])
            #self = recordset so here it is the offer_ids of property
            #for each record if func is true then we put its id in a list
            #browse() fetch a new recordset based on the id of the input list
            other_offers = offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id)

            #TODO: investigate the write method to update a recordset instead of a for loop
            #in fields.py def write(self, records, value):
            for other_offer in other_offers:
                other_offer.status = "refused"

            #TODO: is there many2one channel the best way to communicate between model ? investigate model communication
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"
        return True


    def action_refuse(self):
        #TODO: investigate what is the naming convention for this kind of action, seen rec, record does it depend on the context
        for record in self:
            record.status = "refused"
            record.property_id.buyer_id = None
            record.property_id.selling_price = None
            record.property_id.state = "offer_received"
        return True


