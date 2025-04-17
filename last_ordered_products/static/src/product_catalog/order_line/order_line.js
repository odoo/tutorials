import { ProductCatalogOrderLine } from "@product/product_catalog/order_line/order_line";

export class ProductCatalogLastOrderOrderLine extends ProductCatalogOrderLine {
    static template = "ProductCatalogLastOrderOrderLine";
    static props = {
        ...ProductCatalogLastOrderOrderLine.props,
        sale_uom: { type: Object, optional: true },
        uom: Object,
    };
}
