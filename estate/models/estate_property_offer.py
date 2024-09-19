from odoo import models, fields, api
from odoo.addons.base.tests.test_uninstall import environment
from odoo.exceptions import UserError
from odoo.tools.translate import _

class EstatePropertyOffer(models.Model):


    _name = "estate.property.offer"
    _description = "Offers of estate.property"
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'The offer price must be positive.')
    ]
    _order = "price desc"


    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False
    )

    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    property_type_id = fields.Many2one(comodel_name="estate.property.type",related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(),days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for offer in self:

            #filtered: return the records in self(input recordset) satisfying param func
            #return self.browse([rec.id for rec in self if func(rec)])
            #self = recordset so here it is the offer_ids of property
            #for each record if func is true then we put its id in a list
            #browse() fetch a new recordset based on the id of the input list
            for other_offer in offer.property_id.offer_ids.filtered(lambda o: o.id != offer.id):
                if other_offer.status == "accepted":
                    raise UserError(_(f"Only one offer can be accepted"))

            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "offer_accepted"
        return True


    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
            offer.property_id.buyer_id = None
            offer.property_id.selling_price = 0.0
            offer.property_id.state = "offer_received"
        return True


    #TODO: What about batch creation ?
    @api.model
    def create(self, vals_list):

        estate_property_record = self.env["estate.property"].browse(vals_list["property_id"])
        estate_property_record.state = "offer_received"
        return super().create(vals_list)


