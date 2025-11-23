/** @odoo-module **/

import { QuantityButtons } from '@sale/js/quantity_buttons/quantity_buttons';
import { patch } from '@web/core/utils/patch';
import { useService } from "@web/core/utils/hooks";

patch(QuantityButtons.prototype, {
    setup() {
        this.orm = useService("orm");
    },
    async increaseQuantity() {
        if (this.props.product_temp_id) {
            await this.orm.call("product.template", "search_read", [
                [["id", "=", this.props.product_temp_id]],
                ["change_qty"],
            ]).then(product_template => {
                if (product_template[0].hasOwnProperty("change_qty")){
                    this.props.setQuantity(this.props.quantity + product_template[0].change_qty);
                }
                else{
                    this.props.setQuantity(this.props.quantity + 1)
                }
            })
        }
    },
    async decreaseQuantity() {
        if (this.props.product_temp_id) {
        await this.orm.call("product.template", "search_read", [
            [["id", "=", this.props.product_temp_id]],
            ["change_qty"],
        ]).then(product_template => {
            if (product_template[0].hasOwnProperty("change_qty")){
                this.props.setQuantity(this.props.quantity - product_template[0].change_qty);
            }
            else{
                this.props.setQuantity(this.props.quantity - 1)
            }
        })
    }
    }
});
