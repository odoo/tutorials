/** @odoo-module **/

import { registry } from '@web/core/registry';

registry.category("web_tour.tours").add("stock_bulk_return_sale_tour", {
    url: "/odoo",
    steps: () => [
        {
            "trigger": ".o_app[data-menu-xmlid='sale\\.sale_menu_root']",
            "run": "click"
        },
        {
            "trigger": ".o_list_button_add",
            "run": "click"
        },
        {
            "trigger": ".o_field_widget[name='partner_id'] .o-autocomplete--input",
            "run": "click"
        },
        {
            "trigger": ".o-autocomplete--dropdown-item:nth-child(1) > a",
            "run": "click"
        },
        {
            "trigger": ".o_field_x2many_list_row_add > a:nth-child(1)",
            "run": "click"
        },
        {
            "trigger": ".o_field_product_label_section_and_note_cell .o-autocomplete--input",
            "run": "click"
        },
        {
            "trigger": ".o-autocomplete--dropdown-item:nth-child(3) > a",
            "run": "click"
        },
        {
            "trigger": ".o_field_widget[name='product_uom_qty'] > .o_input",
            "run": "edit 2"
        },
        {
            "trigger": ".o_statusbar_buttons > button[name='action_confirm']",
            "run": "click"
        },
        {
            "trigger": ".o_stat_text",
            "run": "click"
        },
        {
            "trigger": ".o_statusbar_buttons > button[name='button_validate']",
            "run": "click"
        },
        {
            "trigger": ".o_back_button > a",
            "run": "click"
        },
        {
            "trigger": ".o_statusbar_buttons > button[name='\\33 68']",
            "run": "click"
        },
        {
            "trigger": ".o_technical_modal button[name='create_invoices']",
            "run": "click"
        },
        {
            "trigger": ".o_statusbar_buttons > button[name='action_post']",
            "run": "click"
        },
        {
            "trigger": ".o_back_button > a",
            "run": "click"
        },
        {
            "trigger": ".o_menu_brand",
            "run": "click"
        },
        {
            "trigger": ".o_app[data-menu-xmlid='stock\\.menu_stock_root']",
            "run": "click"
        },
        {
            "trigger": ".o-dropdown[data-menu-xmlid='stock\\.menu_stock_warehouse_mgmt']",
            "run": "click"
        },
        {
            "trigger": ".o-dropdown-item[data-menu-xmlid='stock_bulk_return\\.menu_stock_bulk_return']",
            "run": "click"
        },
        {
            "trigger": ".o-autocomplete--input",
            "run": "click"
        },
        {
            "trigger": ".o-autocomplete--dropdown-item:nth-child(1) > a",
            "run": "click"
        },
        {
            "trigger": ".o_field_widget[name='partner_id'] .o-autocomplete--input",
            "run": "edit de"
        },
        {
            "trigger": ".o-autocomplete--dropdown-item:nth-child(1) > a",
            "run": "click"
        },
        {
            "trigger": ".o_field_x2many_list_row_add > a",
            "run": "click"
        },
        {
            "trigger": ".o_field_widget[name='product_id'] .o-autocomplete--input",
            "run": "click"
        },
        {
            "trigger": ".o-autocomplete--dropdown-item:nth-child(9) > a",
            "run": "click"
        },
        {
            "trigger": ".o_data_row:nth-child(13) > .o_data_cell[name='name']",
            "run": "click"
        },
        {
            "trigger": ".o_field_widget[name='picking_id'] .o-autocomplete--input",
            "run": "click"
        },
        {
            "trigger": ".o-autocomplete--dropdown-item:nth-child(9) > a",
            "run": "click"
        },
        {
            "trigger": ".o_data_row:nth-child(26) > .o_data_cell[name='location_id']",
            "run": "click"
        },
        {
            "trigger": ".o_field_widget[name='picking_id'] .o-autocomplete--input",
            "run": "click"
        },
        {
            "trigger": ".o-autocomplete--dropdown-item:nth-child(9) > a",
            "run": "click"
        },
        {
            "trigger": ".o_content > .o_list_renderer .o_column_sortable:nth-child(2) > .o_resize",
            "run": "click"
        },
        {
            "trigger": ".o_data_row:nth-child(24) > .o_data_cell[name='name']",
            "run": "click"
        },
        {
            "trigger": ".o_group",
            "run": "click"
        },
        {
            "trigger": ".o_data_cell[name='lot_id']",
            "run": "click"
        },
        {
            "trigger": ".o_field_widget[name='lot_id'] .o-autocomplete--input",
            "run": "click"
        },
        {
            "trigger": ".o_technical_modal button[name='action_confirm']",
            "run": "click"
        },
        {
            "trigger": ".o_statusbar_buttons > button[name='button_validate']",
            "run": "click"
        },
        {
            "trigger": ".o_statusbar_buttons > button[name='action_create_credit_note']",
            "run": "click"
        },
        {
            "trigger": ".oe_stat_button[name='action_view_credit_note']",
            "run": "click"
        },
        {
            "trigger": ".o_menu_brand",
            "run": "click"
        },
        {
            "trigger": ".o_app[data-menu-xmlid='sale\\.sale_menu_root']",
            "run": "click"
        },
        {
            "trigger": ".o_data_row:nth-child(1) > .o_data_cell[name='name']",
            "run": "click"
        }
    ]
})