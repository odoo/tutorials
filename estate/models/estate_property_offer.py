from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price"

    price = fields.Float("Price", required=True)
    state = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        default=False,
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(
        "Validity (days)", default=7
    )
    date_deadline = fields.Date(
        "Deadline", compute="_compute_date_deadline", store=True
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer._origin.validity:
                offer.date_deadline = fields.Date.add(
                    offer.create_date.date(), days=offer.validity
                )
            else:
                offer.date_deadline = False
