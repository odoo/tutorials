from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    has_bom = fields.Boolean(string="Has Bills of Materials", compute='_compute_has_bom', store=True)

    @api.model
    def _get_buy_route(self):
        buy_route = self.env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        if not buy_route:
            buy_route = self.env['stock.route'].search([('name', '=', 'Buy')], limit=1)
        return buy_route

    @api.model
    def _get_manufacture_route(self):
        manufacture_route = self.env.ref('mrp.route_warehouse0_manufacture', raise_if_not_found=False)
        if not manufacture_route:
            manufacture_route = self.env['stock.route'].search([('name', '=', 'Manufacture')], limit=1)
        return manufacture_route

    @api.model
    def _get_subcontract_route(self):
        subcontract_route = self.env.ref('mrp_subcontracting.route_resupply_subcontractor_mto', raise_if_not_found=False)
        if not subcontract_route:
            subcontract_route = self.env['stock.route'].search(
                [('name', '=', 'Resupply Subcontractor on Order')], limit=1
            )
        return subcontract_route

    @api.model
    def _get_dropship_route(self):
        dropship_route = self.env.ref('purchase_stock.route_warehouse0_dropship', raise_if_not_found=False)
        if not dropship_route:
            dropship_route = self.env['stock.route'].search([('name', '=', 'Dropship')], limit=1)
        return dropship_route

    @api.model
    def _get_dropship_subcontractor_route(self):
        dropship_subcontractor_route = self.env.ref('mrp_subcontracting_dropshipping.route_subcontracting_dropshipping', raise_if_not_found=False)
        if not dropship_subcontractor_route:
            dropship_subcontractor_route = self.env['stock.route'].search(
                [('name', '=', 'Dropship Subcontractor on Order')], limit=1
            )
        return dropship_subcontractor_route

    @api.depends('bom_ids')
    def _compute_has_bom(self):
        for product in self:
            product.has_bom = bool(product.bom_ids)

    @api.onchange('purchase_ok')
    def _onchange_purchase_ok(self):
        """Automatically handle buy route when purchase option changes"""
        buy_route = self._get_buy_route()
        if not buy_route:
            return

        if self.purchase_ok:
            # Only add if not already in the routes
            if buy_route.id not in self.route_ids.ids:
                self.route_ids = [(4, buy_route.id, 0)]
        else:
            # Remove from routes
            if buy_route.id in self.route_ids.ids:
                self.route_ids = [(3, buy_route.id, 0)]

    @api.model
    def create(self, vals):
        """Override create to automatically manage routes"""
        product = super(ProductTemplate, self).create(vals)
        product._update_routes_based_on_config()
        return product

    def write(self, vals):
        """Override write to automatically manage routes"""
        result = super(ProductTemplate, self).write(vals)
        if any(field in vals for field in ['purchase_ok', 'route_ids']):
            self._update_routes_based_on_config()
        return result

    def _is_subcontract_component(self):
        """check if product is used as a component in any subcontracting BOM"""
        self.ensure_one()
        boms = self.env['mrp.bom'].search([('type', '=', 'subcontract')])
        for bom in boms:
            if bom.bom_line_ids.filtered(lambda bom_line: bom_line.product_id.product_tmpl_id.id == self.id):
                return True
        return False

    def _handle_dropship_routes(self):
        """Handle dropship routes based on product context

        This method manages both regular dropship and dropship subcontractor routes:
        - If product is a component in a subcontracting BOM and dropship is enabled,
          apply the dropship subcontractor route
        - Otherwise, apply the regular dropship route if enabled
        """
        self.ensure_one()

        dropship_route = self._get_dropship_route()
        dropship_subcontractor_route = self._get_dropship_subcontractor_route()

        if not dropship_route or not dropship_subcontractor_route:
            return []

        route_commands = []
        is_subcontract_component = self._is_subcontract_component()

        # Check if regular dropship is enabled
        dropship_enabled = dropship_route.id in self.route_ids.ids

        # Handle dropship subcontractor route for components in subcontracting BOMs
        if is_subcontract_component and dropship_enabled:
            # Add dropship subcontractor route if not already present
            if dropship_subcontractor_route.id not in self.route_ids.ids:
                route_commands.append((4, dropship_subcontractor_route.id, 0))
        elif dropship_subcontractor_route.id in self.route_ids.ids:
            # Remove dropship subcontractor route if not needed
            route_commands.append((3, dropship_subcontractor_route.id, 0))

        return route_commands

    def _update_routes_based_on_config(self):
        """Update routes based on product configuration

        This method ensures that routes are correctly assigned based on:
        - Purchase configuration (Buy route)
        - Manufacturing configuration (Manufacture route)
        - Subcontracting usage (Subcontract route)

        It will add or remove routes as needed without user intervention.
        """
        buy_route = self._get_buy_route()
        manufacture_route = self._get_manufacture_route()
        subcontract_route = self._get_subcontract_route()

        for product in self:
            route_commands = []
            
            # Handle Buy route
            if product.purchase_ok and buy_route and buy_route.id not in product.route_ids.ids:
                route_commands.append((4, buy_route.id, 0))
            elif not product.purchase_ok and buy_route and buy_route.id in product.route_ids.ids:
                route_commands.append((3, buy_route.id, 0))
            
            # Handle Manufacture route
            if product.has_bom and manufacture_route and manufacture_route.id not in product.route_ids.ids:
                route_commands.append((4, manufacture_route.id, 0))
            elif not product.has_bom and manufacture_route and manufacture_route.id in product.route_ids.ids:
                route_commands.append((3, manufacture_route.id, 0))
            
            # Handle Subcontract route (components used in subcontracting BoMs)  
            is_subcontract_component = False
            if subcontract_route:
                is_subcontract_component = self._is_subcontract_component()
            
            if is_subcontract_component and subcontract_route.id not in product.route_ids.ids:
                route_commands.append((4, subcontract_route.id, 0))
            elif not is_subcontract_component and subcontract_route.id in product.route_ids.ids:
                route_commands.append((3, subcontract_route.id, 0))
            
            # Handle Dropship routes
            dropship_commands = product._handle_dropship_routes()
            if dropship_commands:
                route_commands.extend(dropship_commands)

            if route_commands:
                product.write({'route_ids': route_commands})
