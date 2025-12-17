import { ProductCatalogSaleOrderLine } from "@sale_stock/product_catalog/sale_order_line/sale_order_line";
import { patch } from "@web/core/utils/patch";

patch(ProductCatalogSaleOrderLine, {
    template: "ProductCatalogLastOrderOrderLine",
    props: {
        ...ProductCatalogSaleOrderLine.props,
        deliveredQty: Number,
        sale_uom: { type: Object, optional: true },
        uom: Object,
    }
});
