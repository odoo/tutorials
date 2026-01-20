from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "A real estate property type such as a house, apt..."
    _order = "sequence,name"

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    offer_type_count = fields.Integer(compute="_compute_offer_types")

    # RELATED FIELDS
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="property_type_id",
        string="Properties",
    )

    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_type_id",
        string="Offers",
    )

    # -----------  BUSINESS LOGIC  -------------- #

    @api.depends('property_ids')
    def _compute_offer_types(self):
        for record in self:
            record.offer_type_count = len(record.offer_ids)

    # -----------  MODEL CONSTRAINTS  -------------- #

    sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Type name must be unique'),
    ]
