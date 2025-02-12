from datetime import timedelta, datetime

from odoo import fields, models, api
from odoo.exceptions import UserError

class EstatePropetyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is the offer model, The multiple offer can be assigned to property"
    _order= "price desc"

    #---------------------------------------------------------------------
    # Fields
    #---------------------------------------------------------------------
    price = fields.Float(string = "Price")
    status = fields.Selection(
        string="Status",
        selection = [
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ]
    )
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    #---------------------------------------------------------------------
    # Relations
    #---------------------------------------------------------------------
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type",related="property_id.property_type_id", store=True)


    #---------------------------------------------------------------------
    # Compute fields
    #---------------------------------------------------------------------
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                    record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days


    # --------------------------- Action Methods ---------------------------
    def action_property_offer_accept(self):
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        for offer in self.property_id.offer_ids:
            if offer == self:
                offer.status = "accepted"
            else:
                offer.status = "refused"
        return True


    def action_property_offer_refused(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.partner_id = ""
                record.property_id.selling_price = 0.00
            self.status = 'refused'
        return True


    # --------------------------- Oncreate Methods ---------------------------
    @api.model_create_multi
    def create(self, vals):
        print(vals)
        for val in vals:
            property = self.env['estate.property'].browse(val['property_id'])
            property.status = "offer_received"
            for offer in property.offer_ids:
                if offer.price > val["price"]:
                    raise UserError("The offer must be higher then the existing offer")
        return super().create(vals)
