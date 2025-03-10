import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { formatCurrency } from "@point_of_sale/app/models/utils/currency";
import { patch } from "@web/core/utils/patch";


patch(PosOrderline.prototype, {

    _compute_price_with_tax(basePrice, quantity = 1, applyDiscount = true) {
        let price = basePrice * quantity;
        if (applyDiscount && this.discount > 0) {
            price = price * (1 - this.discount / 100);
        }

        const taxes = this.product_id.taxes_id;
        const taxDetails = this.get_tax_details();

        let accPrice = price;
        if (taxes && taxes.length > 0) {
            for (let i = 0; i < taxes.length; i++) {
                const tax = taxes[i];
                if (taxDetails) {
                    const taxData = taxDetails[tax.id];
                    if (!taxData) {
                        continue;
                    }
                    if (tax.price_include) {
                        continue;
                    } else {
                        accPrice = accPrice + (accPrice * tax.amount) / 100;
                    }
                }
            }
        }
        return accPrice;
    },

    get_standard_price_with_tax() {
        const quantity = this.get_quantity()
        return this._compute_price_with_tax(this.product_id.lst_price, quantity, false);
    },

    getProductBarcode() {
        const product = this.get_product();
        if (product) {
            return product.barcode;
        }
    },

    showStrikedPrice(){
        const product = this.get_product()
        if((product && product.custom_price > 0) && this.get_all_prices(this.get_quantity()).priceWithTax < this.get_standard_price_with_tax()){
            return true
        }
        return false
    },

    getDisplayData() {
        const data = super.getDisplayData();
        const barcode = this.getProductBarcode()
        const standardPrice = formatCurrency(this.get_standard_price_with_tax(), this.currency).toString()
        const showStrikedPrice = this.showStrikedPrice()
        if (barcode){
            data.barcode = barcode
        }
        data.standardPrice = standardPrice
        data.showStrikedPrice = showStrikedPrice
        return data;
    },
});
