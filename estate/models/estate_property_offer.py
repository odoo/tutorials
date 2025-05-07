from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'
    _order = "price desc"

    _check_positive_offer_price = (models.Constraint("""CHECK (price >= 0)""",
             "The property offer price must be positive."))

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Offer", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", default=fields.Date.add(fields.Date.today(), days=7))
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self.filtered("create_date"):
            record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self.filtered("create_date"):
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        estate_properties = self.env["estate.property"].browse([vals['property_id'] for vals in vals_list if vals['property_id']])
        for vals in vals_list:
            if not vals["property_id"]:
                continue
            estate_property = estate_properties.filtered(lambda ep: ep.id == vals['property_id'])[:1]
            estate_property.state = 'offer_received'
            if vals['price'] < estate_property.best_offer:
                raise UserError("Can't make a smaller offer than the best one currently recorded!")
        return super().create(vals_list)

    def action_btn_accept(self):
        self.ensure_one()
        self.status = "accepted"
        self.property_id.write({
            'buyer_id': self.partner_id.id,
            'selling_price': self.price,
            'state': 'offer_accepted'
        })

    def action_btn_refuse(self):
        self.status = "refused"
        return True
