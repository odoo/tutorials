import { registry } from "@web/core/registry";
import {
    SaleOrderLineListRenderer,
    SaleOrderLineOne2Many,
} from "@sale/js/sale_order_line_field/sale_order_line_field";


export class ProductKitSaleOrderLineListRenderer extends SaleOrderLineListRenderer {

    isKitChild(record) {
        return !!record.data.is_kit_child;
    }

    isKitParent(record){
        return !!record.data.is_kit;
    }

    isCellReadonly(column, record) {
        return super.isCellReadonly(column, record) || (
            this.isKitChild(record)
        ) || (
            this.isKitParent(record)
        );
    }

    displayDeleteIcon(record) {
        return super.displayDeleteIcon(record)
            && !this.isKitChild(record);
    }
}

export class ProductKitSaleOrderLineOne2Many extends SaleOrderLineOne2Many {
    static components = {
        ...SaleOrderLineOne2Many.components,
        ListRenderer: ProductKitSaleOrderLineListRenderer,
    };
}

export const productKitSaleOrderLineOne2Many = {
    ...registry.category("fields").get("sol_o2m"),
    component: ProductKitSaleOrderLineOne2Many,
};

registry.category("fields").add(
    "product_kit_sol_o2m",
    productKitSaleOrderLineOne2Many
);
