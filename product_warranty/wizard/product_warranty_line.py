from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ProductWarrantyLine(models.TransientModel):
    _name = "product.warranty.line"
    _description = "Warranty Line"
    
    # fields
    wizard_id = fields.Many2one(comodel_name="add.product.warranty")
    warranty_configuration_id = fields.Many2one(comodel_name="product.warranty.configuration")
    sale_order_line_id = fields.Many2one(comodel_name="sale.order.line")
    
    # related fields
    warranty_name = fields.Char(related="warranty_configuration_id.name")
    warranty_percentage = fields.Float(related="warranty_configuration_id.percentage")
    warranty_duration = fields.Integer(related="warranty_configuration_id.duration")
    warranty_end_date = fields.Date(compute="_compute_warranty_end_date")
    
    @api.depends("warranty_configuration_id.duration")
    def _compute_warranty_end_date(self):
        for record in self:
            if record.warranty_configuration_id:
                record.warranty_end_date = fields.Date.today() + relativedelta(years=record.warranty_configuration_id.duration)
            else:
                record.warranty_end_date = fields.Date.today()
