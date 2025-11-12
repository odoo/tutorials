/** @odoo-module **/

import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import { patch } from "@web/core/utils/patch";

patch(ActionpadWidget.prototype, {
    async onValidateClick() {
        if (this.pos.validateOrderForProductScreen) {
            await this.pos.validateOrderForProductScreen({ isForceValidate: true });
        } else {
            this.pos.showScreen('ProductScreen');
        }
    },
});
