from odoo import fields, models, api # type: ignore

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"
    _sql_constraints = [
        ('check_unique_property_type', 'UNIQUE(name)', 'Property Type already exists')
    ]

#---------------------------------------Basic Fields---------------------------------------#
    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence", default=1)
#---------------------------------------Relational Fields----------------------------------#
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

#---------------------------------------Compute Methods-------------------------------------#
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
