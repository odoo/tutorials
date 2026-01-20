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
            content: "Click 'Want Tax Credit' checkbox",
            trigger: "input#want_tax_credit_checkbox",
            run: "click",
        },
        {
            content: "Check VAT and Company fields are visible",
            trigger: '#vat_number:visible, #company_name:visible',
        },
        {
            content: "Click Confirm button",
            trigger: "#confirm_btn",
            run: "click",
        },
        {
            content: "Error should show: please enter correct Vat Number",
            trigger: "#errors:contains('Please enter VAT number')",
        },
        {
            content: "Uncheck 'Want Tax Credit' checkbox",
            trigger: "input#want_tax_credit_checkbox:checked",
            run: "click",
        },
        {
            content: "Click Confirm button",
            trigger: "#confirm_btn",
            run: "click",
        },
        {
            content: "Check delivery and billing are same",
            trigger: "#delivery_and_billing",
            run: () => {
                const address_card = document.querySelector("#delivery_and_billing");
                const address_text = address_card.innerText;
                if (!address_text.includes("Delivery & Billing")) {
                    throw new Error("addresses are not the same");
                }
            }
        },
        {
            content: "Click Edit button on payment page",
            trigger: "#delivery_and_billing a[href='/shop/checkout']",
            run: "click"
        },
        {
            content: "Verify Want Tax Credit checkbox is unchecked",
            trigger: "#want_tax_credit_checkbox:not(:checked)",
        },
        {
            content: "Verify tax credit container is hidden",
            trigger: "#tax_credit_container:not(:visible)",
        },
    ],
});
