import { registry } from "@web/core/registry";
import * as tourUtils from "@website_sale/js/tours/tour_utils";

registry.category("web_tour.tours").add("tax_credit_checkbox_test", {
    test: true,
    url: "/shop",
    steps: () => [
        ...tourUtils.addToCart({ productName: "Office Chair Black TEST" }),
        tourUtils.goToCart({ quantity: 1 }),
        tourUtils.goToCheckout(),
        {
            content: "Click Edit button",
            trigger: 'a[href="/shop/checkout"].float-end.no-decoration',
            run: 'click'
        },
        {
            content: "Click 'Want Tax Credit' checkbox",
            trigger: "input#want_tax_credit_checkbox",
            run: "click",
        },
        {
            content: "Check VAT and Company fields are visible",
            trigger: '#vat_number:visible, #company_name:visible',
        },
    ],
});
