from odoo import models, fields, api


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "sequence,name"

    name = fields.Char("Property Type Name", required=True)
    sequence = fields.Integer(default=1, help="Used to order stages. Lower is ranked higher.")
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="type_id")
    offer_ids = fields.One2many(related="property_ids.offer_ids", inverse_name="property_type_id")

    offer_count = fields.Integer(compute="_compute_offer_count")

    _name_uniq = models.Constraint(
        'unique(name)',
        'A property type with the same name already exists.',
    )

    @api.depends("property_ids.offer_ids")
    def _compute_offer_count(self):
        for type in self:
            type.offer_count = self.env['estate.property.offer'].search_count([('property_id', 'in', type.property_ids.ids)])
