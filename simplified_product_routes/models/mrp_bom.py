from odoo import api, fields, models


class MrpBom(models.Model):
    """Extends mrp.bom to automatically update routes on product templates

    This extension ensures that whenever BOMs are created, modified, or deleted,
    the routes on associated products are automatically updated to maintain
    consistency with the manufacturing configuration.
    """
    _inherit = 'mrp.bom'
    
    @api.model
    def create(self, vals):
        """Override create to update routes on associated products"""
        bom = super(MrpBom, self).create(vals)
        # Update routes for the product
        if bom.product_tmpl_id:
            bom.product_tmpl_id._update_routes_based_on_config()
        
        # Update routes for components in case of subcontract BoM
        if bom.type == 'subcontract':
            component_templates = bom.bom_line_ids.mapped('product_id.product_tmpl_id')
            if component_templates:
                component_templates._update_routes_based_on_config()
        
        return bom
    
    def write(self, vals):
        """Override write to update routes on associated products"""
        old_type = {bom.id: bom.type for bom in self}
        old_lines = {}
        if 'bom_line_ids' in vals or 'type' in vals:
            for bom in self:
                old_lines[bom.id] = bom.bom_line_ids.mapped('product_id.product_tmpl_id')
        
        result = super(MrpBom, self).write(vals)
        
        # Update routes if type changed or lines changed
        if 'bom_line_ids' in vals or 'type' in vals:
            product_templates = self.mapped('product_tmpl_id')
            product_templates.read(['route_ids'])
            for bom in self:
                # Update product routes
                if bom.product_tmpl_id:
                    bom.product_tmpl_id._update_routes_based_on_config()
                
                # If this is or was a subcontract BoM, update component routes
                if bom.type == 'subcontract' or old_type.get(bom.id) == 'subcontract':
                    # Get all affected components (old and new)
                    component_templates = set()
                    if bom.id in old_lines:
                        component_templates.update(old_lines[bom.id].ids)
                    component_templates.update(bom.bom_line_ids.mapped('product_id.product_tmpl_id').ids)
                    
                    # Update routes for all affected components
                    for template_id in component_templates:
                        template = self.env['product.template'].browse(template_id)
                        template._update_routes_based_on_config()
        
        return result
    
    def unlink(self):
        """Override unlink to update routes on associated products"""
        # Store products and component products before deletion
        products_to_update = self.mapped('product_tmpl_id')
        subcontract_components = self.env['product.template']
        
        for bom in self:
            if bom.type == 'subcontract':
                subcontract_components |= bom.bom_line_ids.mapped('product_id.product_tmpl_id')
        
        result = super(MrpBom, self).unlink()
        
        # Update routes for affected products
        for product in products_to_update:
            product._update_routes_based_on_config()
        
        for component in subcontract_components:
            component._update_routes_based_on_config()
        
        return result
