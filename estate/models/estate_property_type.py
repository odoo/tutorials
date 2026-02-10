from odoo import api, fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Types of Property"
    _order = "name"
    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many("estate.estate.property", "property_type_id")

    # Stat button fields
    offer_ids = fields.One2many("estate.property.offer", "property_type_ids")
    offer_count = fields.Integer(compute="_compute_offer_count")

    ## Constraints Section ##
    _check_name = models.Constraint(
        'UNIQUE(name)',
        'The type of a property should be unique'
    )

    ## Computed fields ##
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        return True
