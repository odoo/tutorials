import { mailModels } from "@mail/../tests/mail_test_helpers";

import { defineModels } from "@web/../tests/web_test_helpers";

import { Product } from "./mock_server/mock_models/product_product";
import { SaleOrder } from "./mock_server/mock_models/sale_order";
import { SaleOrderLine } from "./mock_server/mock_models/sale_order_line";
import { PurchaseOrder } from "./mock_server/mock_models/purchase_order";
import { PurchaseOrderLine } from "./mock_server/mock_models/purchase_order_line";


export function defineBarcodeHandlerModels() {
    return defineModels(barcodeHandlerModels);
}

export const barcodeHandlerModels = {
    ...mailModels,
    Product,
    SaleOrder,
    SaleOrderLine,
    PurchaseOrder,
    PurchaseOrderLine
};
