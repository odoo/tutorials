from odoo import api, fields, models, tools

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "an offer made to a specific property"

    price = fields.Float()
    state = fields.Selection([("accepted", "Accepted"), ("refused", "Refused"),], string="Status", copy=False)
    partner_id = fields.Many2one(comodel_name="res.partner", required=True, ondelete="restrict")
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    validity = fields.Integer()
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    
    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.create_date or fields.Date.today() + tools.date_utils.relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = fields.Date.to_date(offer.create_date)
            offer.validity = (offer.date_deadline - create_date).days
