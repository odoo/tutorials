import {registry} from '@web/core/registry';
import * as tourUtils from '@website_sale/js/tours/tour_utils';

registry.category('web_tour.tours').add('shop_update_cart', {
    url: "/shop/checkout",
    test: true,
    steps: () => [
        ...tourUtils.searchProduct("conference chair"),
        {
            content: "select conference chair",
            trigger: '.oe_product_cart:first a:contains("Conference Chair")',
            run: "click",
        },
        {
            trigger: "#product_detail",
        },
        {
            content: "select Conference Chair Aluminium",
            trigger: 'label:contains(Aluminium) input',
            run: "click",
        },
        {
            trigger: "#product_detail",
        },
        {
            content: "select Conference Chair Steel",
            trigger: 'label:contains(Steel) input',
            run: "click",
        },
        {
            trigger: "label:contains(Steel) input:checked",
        },
        {
            content: "click on add to cart",
            trigger: '#product_detail form[action^="/shop/cart/update"] #add_to_cart',
            run: "click",
        },
        tourUtils.goToCart(),
        tourUtils.goToCheckout(),
        {
            content: "Edit Address",
            trigger: '#delivery_and_billing a:contains("Edit")',
            run: "click",
        },
        {
            content: "Enable Tax Credit",
            trigger: 'input#want_tax_credit',
            run: "click",
        },
        {
            content: "Tax Credit row is visible",
            trigger: '#tax_credit_container:not(.d-none)',
            run: () => {},
        },
        {
            content: "Enter VAT number",
            trigger: "#o_vat",
            run: "123456789",
        },
        {
            content: "Company name will be auto-filled based on vat",
            trigger: "#o_company_name[value!='']",
            run: () => {},
        },
    ]
});
