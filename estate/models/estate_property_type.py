from odoo import api, fields, models


class EstatePropertyType(models.Model):
    # ----------------------------------------
    # Private attributes
    # ----------------------------------------
    _name = 'estate.property.type'
    _description = "Different categories or types of properties, such as apartment, house, land, or commercial, used to classify estate properties."
    _sql_constraints = [
        ('check_unique_name', 'UNIQUE (name)', "Type name must be unique."),
    ]
    _order = 'name desc'

    # ----------------------------------------
    # Field declarations
    # ----------------------------------------
    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'type_id', string="Properties"
    )
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )
    offer_count = fields.Integer(
        compute='_compute_offer_count', string="Offers Count"
    )

    # ----------------------------------------
    # Compute, inverse and search methods
    # ----------------------------------------
    @api.depends('property_ids.offer_ids')
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = len(type.property_ids.offer_ids)

    # ----------------------------------------
    # Action methods
    # ----------------------------------------
    def action_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': "Offers",
            'res_model': 'estate.property.offer',
            'view_mode': 'list,form',
            'domain': [('property_id', 'in', self.property_ids.ids)],
            'context': {'default_property_id': self.property_ids.ids},
        }
