import { ProductProduct } from "@point_of_sale/app/models/product_product";
import { patch } from "@web/core/utils/patch";


patch(ProductProduct.prototype, {
    get_price(pricelist, quantity, price_extra = 0, recurring = false, list_price = false) {
        if(this.custom_price && this.custom_price > 0){
            return this.custom_price
        }
        return super.get_price(pricelist, quantity, price_extra, recurring, list_price);
    }
});
