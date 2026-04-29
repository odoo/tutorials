import logging

from odoo import api, fields, models


_logger = logging.getLogger(__name__)


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _rec_name = 'type'
    _order = 'type'

    colour = fields.Selection(
        [
            ('red', 'Red'),
            ('green', 'Green'),
            ('yellow', 'Yellow')
        ]
    )
    offer_count = fields.Integer(compute='_compute_offer_count')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id')
    property_ids = fields.One2many(comodel_name='estate.properties', inverse_name='property_type_id')
    type = fields.Char(required=True)

    _check_name = models.Constraint(
        'UNIQUE (type)',
        "Property Type should be unique",
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            # _logger.error(property_type)
            # _logger.error(property_type.offer_ids)
            # _logger.error(property_type.property_ids.offer_ids)
            property_type.offer_count = len(property_type.offer_ids)
