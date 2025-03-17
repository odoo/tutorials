"use_strict";

import { markup } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add("one_time_sale_website_tour", {
    url: "/shop",
    sequence: 252,
    rainbowManMessage: () => markup(
        _t("<b>Congratulations</b>, you have successfully purchase subscription product just for one time.")),
    steps: () => [
        {
            trigger: ".input-group[role='search'] > input",
            content: _t("Search your one time purchase allowed subscription product by name."),
            tooltipPosition: "bottom",
            run: "edit Milk",
        },
        {
            trigger: ".o_search_result_item",
            content: _t("Go ahead and click to see product."),
            tooltipPosition: "right",
            run: "click",
        },
        {
            trigger: ".plan_select[name='plan_id']",
            content: _t("Select the subscription plan if you want to purchase product with subscription."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: "#add_to_cart",
            content: _t("Click to add the product with your selected pricing plan."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: ".o_wsale_my_cart > a",
            content: _t("Let's see the cart if it is perfectly added."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: ".flex-grow-1 > div > a",
            content: _t("Click to remove the product from the cart."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            content: "Wait until the configurator is finished",
            trigger: ".oe_website_sale",
            timeout: 3000,
        },
        {
            trigger: ".nav-link[href='/shop']",
            content: _t("Let's add product for the one time purchase."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: ".input-group[role='search'] > input",
            content: _t("Search your one time purchase allowed subscription product by name."),
            tooltipPosition: "bottom",
            run: "edit Milk",
        },
        {
            trigger: ".o_search_result_item",
            content: _t("Go ahead and click to open product."),
            tooltipPosition: "right",
            run: "click",
        },
        {
            trigger: "#one_time_purchase",
            content: _t("Select option to purchase this subscription product for just one time."),
            tooltipPosition: "left",
            run: "click",
        },
        {
            trigger: "#add_to_cart",
            content: _t("Click to add the product with your selected pricing plan."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: ".o_wsale_my_cart > a",
            content: _t("Let's see the cart if it is perfectly added."),
            tooltipPosition: "bottom",
            run: "click",
        },
        {
            trigger: ".btn-primary[name='website_sale_main_button']",
            content: _t("Click to checkout."),
            tooltipPosition: "left",
            run: "click",
        }
    ]
});
