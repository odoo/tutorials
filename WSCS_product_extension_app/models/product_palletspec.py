from odoo import models, fields, api


class ProductPalletSpec(models.Model):
    _name = "product.palletspec"
    _description = "Product Pallet Specification"

    name = fields.Char(string="Pallet Type")
    product_tmpl_id = fields.Many2one(
        "product.template", string="Product", required=True
    )
    product_uom_id = fields.Many2one("uom.uom", string="Unit of Measure")
    cases_per_layer = fields.Float(string="Cases/Layer", required=True)
    layers_per_pallet = fields.Float(string="Layers/Pallet", required=True)
    qty = fields.Float(
        string="Pallet Quantity", compute="_compute_pallet_quantity", store=True
    )
    width = fields.Integer(string="Pallet Width (m)", required=True)
    length = fields.Integer(string="Pallet Length (m)", required=True)
    height = fields.Integer(string="Pallet Height (m)", required=True)
    weight = fields.Float(string="Pallet Weight (kg)")
    pallet_volume = fields.Float(
        string="Pallet Volume (m³)", compute="_compute_pallet_volume", store=True
    )
    units = fields.Integer(
        string="Pcs/Pallet", compute="_compute_pcs_per_pallet", store=True
    )
    packaging_id = fields.Many2one("product.packaging", string="Packaging")

    @api.depends("cases_per_layer", "layers_per_pallet")
    def _compute_pallet_quantity(self):
        for rec in self:
            if rec.cases_per_layer and rec.layers_per_pallet:
                rec.qty = rec.cases_per_layer * rec.layers_per_pallet
            else:
                rec.qty = 0.0

    @api.depends("width", "length", "height")
    def _compute_pallet_volume(self):
        for rec in self:
            if rec.width and rec.length and rec.height:
                rec.pallet_volume = rec.width * rec.length * rec.height
            else:
                rec.pallet_volume = 0.0

    @api.depends("cases_per_layer", "layers_per_pallet", "packaging_id.qty")
    def _compute_pcs_per_pallet(self):
        for rec in self:
            if rec.cases_per_layer and rec.layers_per_pallet and rec.packaging_id.qty:
                rec.units = int(
                    rec.cases_per_layer * rec.layers_per_pallet * rec.packaging_id.qty
                )
            else:
                rec.units = 0
