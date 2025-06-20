/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen, {
    components: {
        ...ProductScreen.components,
        PaymentScreen,
    },
    props: {
        ...ProductScreen.props,
        others: {type: Boolean, optional: true},
        orderUuid: {type: String, optional: true},
    },
});
