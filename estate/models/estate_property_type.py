from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type'
    _order = "manual_ordering asc, name asc"

    _type_name_uniq = (models.Constraint("""UNIQUE (name)""",
             "The type name must be unique."))

    name = fields.Char('Title', required=True, translate=True)
    line_ids = fields.One2many("estate.property", "property_type_id")
    manual_ordering = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute='_compute_offers')

    @api.depends("offer_ids")
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
