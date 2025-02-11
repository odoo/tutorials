from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type table"
    # _order="name asc"

    name = fields.Char(string="Property Type", required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", readonly=True)
    sequence = fields.Integer(string='Sequence', default=1,
                              help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers"
    )
    offer_count = fields.Integer(
        string="Offer Count", compute="_compute_offers", store=True)

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)',
         'The property type name must be unique.'),
    ]

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_open_offers(self):
        return {
            "name": "Offers",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id},
        }
