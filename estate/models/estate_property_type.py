from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "test description 2"
    _order = "name,sequence"

    name = fields.Char(required=True, unique=True)
    property_ids = fields.One2many("estate.property", "id")
    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order stages. Lower is better."
    )
    offer_ids = fields.One2many("estate.property.offer", "id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.constrains("name")
    def _check_unique_name(self):
        for record in self:
            # Check if the name already exists in other records (excluding the current one)
            existing_tag = self.search(
                [("name", "=", record.name), ("id", "!=", record.id)], limit=1
            )
            if existing_tag:
                raise ValidationError(
                    "The type name must be unique. '%s' already exists." % record.name
                )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for offer in self:
            offer.offer_count = len(offer.offer_ids)
