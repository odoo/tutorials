from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price"

    price = fields.Float(required=True)
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    property_id = fields.Many2one("estate.property", "Property", required=True, ondelete='cascade')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _check_price = models.Constraint(
        'CHECK (price > 0)',
        'Offer price must be strictly positive'
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if not record.create:
                record.date_deadline = fields.Datetime.add(record.create_date.date(), days=record.validity)
            else:
                record.date_deadline = fields.Datetime.add(fields.Datetime.today(), days=record.validity)

    @api.depends("date_deadline")
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def accept_offer(self):
        for record in self:
            if record.status == "accepted" or record.property_id.stage in ("cancelled", "sold", "offer accepted"):
                raise UserError(self.env._("Property not available"))
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.stage = "offer accepted"
        return True

    def refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            if "price" in vals and property.best_price > vals.get("price", 0):
                raise UserError(self.env._("Cannot create an offer bellow the current offer (%d€)", property.best_price))
            property.set_stage("offer received")

        return super().create(vals_list)
