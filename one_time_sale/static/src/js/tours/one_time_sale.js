"use_strict";

import { markup } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add("one_time_sale_tour", {
    url: "/odoo",
    sequence: 251,
    rainbowManMessage: () => markup(
        _t("<b>Congratulations</b>, you have successfully create subscription product for one time sale.")),
    steps: () => [
        {
            trigger: ".o_app[data-menu-xmlid='sale_subscription.menu_sale_subscription_root']",
            content: _t(
                "Want a one time sale of recurring product through subscription management? \
                Get started by clicking here"),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: ".dropdown-toggle[data-menu-xmlid='sale_subscription.product_menu_catalog']",
            content: _t("Let's go to the catalog to create our first one time purchase allowed subscription product"),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: ".dropdown-item[data-menu-xmlid='sale_subscription.menu_sale_subscription_product']",
            content: _t("Create your first one time purchase allowed subscription product here"),
            tooltipPosition: "right",
            run: "click",
        },
        {
            isActive: ["auto"],
            trigger: ".o_kanban_renderer",
        },
        {
            trigger: ".o-kanban-button-new",
            content: _t("Go ahead and create a new product"),
            tooltipPosition: "right",
            run: "click",
        },
        {
            isActive: ["auto"],
            trigger: ".o_form_editable",
        },
        {
            trigger: "#name_0",
            content: markup(_t("Choose a product name.<br/><i>(e.g. Milk)</i>")),
            tooltipPosition: "right",
            run: "edit Milk",
        },
        {
            isActive: ["auto"],
            trigger: ".o_form_editable",
        },
        {
            trigger: "#radio_field_0_consu",
            content: _t("Select goods(consumable) as product type."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: "#list_price_0",
            content: _t("Enter sales price for your product."),
            tooltipPosition: "right",
            run: "edit 10",
        },
        {
            trigger: ".o_form_button_save",
            content: _t("Save your progress for one-time purchase product creation."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: "a.nav-link[name='sales']",
            content: _t("Let's allow subscription product to be sale/purchase for one time too."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: "#accept_one_time_0",
            content: _t("Go ahead and allow product to sell/purchase for one time too."),
            tooltipPosition: "right",
            run: "click",
        },
        {
            trigger: "a.nav-link[name='subscription_pricing']",
            content: _t("Let's add a pricing with a recurrence"),
            tooltipPosition: "right",
            run: "click",
        },
        {
            trigger: ".o_field_x2many_list_row_add > a",
            content: _t("Add a new rule"),
            run: "click",
        },
        {
            isActive: ["auto"],
            trigger: ".o_form_editable",
        },
        {
            trigger: ".o_list_many2one[name='plan_id']",
            content: _t(
                "Add a recurring plan for this product, or create a new one with the desired recurrence \
                (e.g., Monthly)"),
            run: "edit Monthly",
        },
        {
            isActive: ["auto"],
            trigger: ".ui-autocomplete > li > a:contains('Monthly')",
            run: "click",
        },
        {
            isActive: ["auto"],
            trigger: ".o_form_editable",
        },
        {
            trigger: ".o_field_cell[name='price']",
            content: _t("Let's add price for selected recurrence"),
            run: "edit 8",
        },
        {
            trigger: ".o_form_button_save",
            content: _t("Save your created product."),
            tooltipPosition: "bottom",
            run: "click",
        }
    ]
});
