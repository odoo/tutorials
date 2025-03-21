/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { stepUtils } from "@web_tour/tour_service/tour_utils";

registry.category("web_tour.tours").add('last_ordered_products_tour', {
    url: "/odoo",
    steps: () => [
        stepUtils.showAppsMenuItem(),
        {
            isActive: ["community"],
            trigger: ".o_app[data-menu-xmlid='sale.sale_menu_root']",
            content: _t("Lets create a beautiful quotation in a few clicks ."),
            tooltipPosition: "right",
            run: "click",
        },
        {
            isActive: ["enterprise"],
            trigger: ".o_app[data-menu-xmlid='sale.sale_menu_root']",
            content: _t("Let’s create a beautiful quotation in a few clicks ."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: "button.o_list_button_add",
            content: _t("Build your first quotation right here!"),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: ".o_field_res_partner_many2one[name='partner_id'] input",
            content: _t("Search a customer name ('Azure Interior'"),
            tooltipPosition: "right",
            run: "edit Azure",
        },
        {
            trigger: ".o-autocomplete--dropdown-item > a:contains('Azure')",
            content: "Select azure interior",
            run: "click",
        },
        {
            trigger: ".o_field_x2many_list_row_add a",
            content: _t("Add a product"),
            tooltipPosition: "bottom",
            run: "click"
        },
        {
            trigger: ".o_field_widget[name='product_id'], .o_field_widget[name='product_template_id']",
            content: _t("Select a product"),
            tooltipPosition: "bottom",
            run: "click"
        },
        {
            trigger: ".o_field_sol_product_many2one[name='product_id'] input, .o_field_sol_product_many2one[name='product_id'] input",
            content: _t("Search a product (Large Cabinet)'"),
            tooltipPosition: "top",
            run: "edit Large Cabinet",
        },
        {
            trigger: ".o-autocomplete--dropdown-item > a:contains('Cabinet')",
            content: _t("Select Large Cabinet"),
            run: "click",
        },
        {
            trigger: ".o_form_button_save",
            content: _t("Save Manually"),
            run: "click",
        },
        {
            trigger: "button[name=action_confirm]",
            content: _t("Confirm Sale Order"),
            tooltipPosition: "bottom",
            run: "click"
        },
        {
            trigger: "#create_invoice_percentage",
            content: _t("Create Invoice"),
            tooltipPosition: "bottom",
            run: "click"
        },
        {
            trigger: "#create_invoice_open",
            content: _t("Create Draft"),
            tooltipPosition: "bottom",
            run: "click"
        },
        {
            content: "Breadcrumb back to Quotations",
            trigger: ".breadcrumb-item:contains('Quotations')",
            run: "click",
        },
        {
            trigger: ".o_list_button_add",
            content: _t("Create New Sale Order"),
            tooltipPosition: "bottom",
            run: "click"
        },
        {
            trigger: ".o_field_res_partner_many2one[name='partner_id'] input",
            content: _t("Search a customer name ('Azure Interior'"),
            tooltipPosition: "right",
            run: "edit Azure",
        },
        {
            trigger: ".o-autocomplete--dropdown-item > a:contains('Azure')",
            content: "Select azure interior",
            run: "click",
        },
        {
            trigger: ".o_field_x2many_list_row_add a",
            content: _t("Add a product"),
            tooltipPosition: "bottom",
            run: "click"
        },
        {
            trigger: ".o_field_widget[name='product_id'], .o_field_widget[name='product_template_id']",
            content: _t("Select a product"),
            tooltipPosition: "bottom",
            run: "click"
        },
        {
            trigger: "div[name='product_id'] .o-autocomplete--dropdown-item > a:contains('[E-COM07]')",
            content: _t("You can see here Product Large Cabinet which is invoiced few time ago to this customer"),
            tooltipPosition: "right",
            run: "click",
        },
    ]
});
