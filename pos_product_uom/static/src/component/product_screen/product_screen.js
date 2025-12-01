/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        this.handleNewAddProduct = new Set();
        this.addProductToOrder = this.addProductToOrder.bind(this);
    },

    /** override **/
    async addProductToOrder(product) {
        const addProductId = product.id
        const orderList = this.pos.get_order().lines
        if (!this.handleNewAddProduct.has(addProductId) && product.is_use_second_uom) {
            const factorInv = product.uom_id?.factor_inv || 1;
            let firstUom = await this.pos.models['uom.uom'].getAll().find(rec => rec.id == product._raw.uom_id)
            product.lst_price = (factorInv === 1) 
                ? product.lst_price / firstUom.factor_inv
                : product.lst_price * factorInv;
            this.handleNewAddProduct.add(addProductId);                 
        }
        return super.addProductToOrder(product);
    }
});
