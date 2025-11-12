from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order="name desc"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties")
    sequence = fields.Integer('Sequence', default=7)
    offer_count = fields.Integer(
        string="Number of Offers",
        compute="_compute_offer_count"
    )

    @api.depends('property_ids.offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            offer_count = 0
            for property in property_type.property_ids:
                offer_count += len(property.offer_ids)
            property_type.offer_count = offer_count
    @api.constrains('name')
    def _check_type_name_unique(self):
        for record in self:
            existing_type = self.search([('name', '=', record.name)])
            if existing_type:
                raise ValidationError(f"The property type name '{record.name}' must be unique.")
            
    _check_type_name_unique_ratio = models.Constraint(
        'CHECK(name)',
        'The property name must be unique.'
    )