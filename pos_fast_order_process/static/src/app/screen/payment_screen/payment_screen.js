/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    setup(){
        super.setup(...arguments);
        this.pos.validateOrderForProductScreen = this.validateOrder.bind(this);
    },

    async addNewPaymentLine(paymentMethod) {
        const result = await super.addNewPaymentLine(paymentMethod);
        if (this.pos.config.pos_fast_order_process && !this.env.isSmall && result) {
               if (typeof this.numberBuffer?.switchComponentStack === 'function' && this.numberBuffer?._currentBufferHolder?.component?.constructor && paymentMethod.type === 'cash') {
                   if (this.numberBuffer?._currentBufferHolder?.component.constructor?.name !== this.constructor?.name) {
                       this.numberBuffer?.switchComponentStack(this.constructor.name);
                   };
                   this.numberBuffer.reset();
               };
        };
    },
    async validateOrder(isForceValidate) {
        if(this.pos.config.pos_fast_order_process  && !this.env.isSmall){
            this.currentOrder.showScreen(false, true);
        };
        return await super.validateOrder(isForceValidate);
    },
    selectNextOrder() {
        if(this.pos.config.pos_fast_order_process  && !this.env.isSmall){
            this.currentOrder.showScreen();
            this.currentOrder.partner_id = null;
        };
        return super.selectNextOrder();
    },
});
