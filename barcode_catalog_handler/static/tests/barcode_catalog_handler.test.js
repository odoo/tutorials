import { expect, test } from "@odoo/hoot";
import { animationFrame, click } from "@odoo/hoot-dom";

import { deepCopy } from "@web/core/utils/objects";
import { makeMockEnv, mountView, onRpc, defineModels} from "@web/../tests/web_test_helpers";

import { defineBarcodeHandlerModels } from "@barcode_catalog_handler/../tests/barcode_catalog_handler_helpers";
import { Product } from "@barcode_catalog_handler/../tests/mock_server/mock_models/product_product";

defineBarcodeHandlerModels();

const saleOrderLineInfo = {
    1: {
        price: 299,
        quantity: 1,
        productType: "consu"
    },
    2: {
        price: 399,
        quantity: 0,
        productType: "consu"
    },
}

test("Add product to sale order on barcode scan", async () => {
    const env = await makeMockEnv();
    const barcode = "987654321";
   
    onRpc("product.product", "web_search_read", () => {
        const products = Product._records._records;
        return { 
            length: products.length,
            records: products
        };
    });
    
    onRpc("/product/catalog/order_lines_info", () => deepCopy(saleOrderLineInfo));
    
    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();
        
        expect.step("update_order_line_info");
        expect(params.product_id).toBe(2);
        expect(params.quantity).toBe(1);
        expect(params.res_model).toBe("sale.order");
        
        saleOrderLineInfo[2].quantity = 1;
        return {}
    });
    
    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            order_id: 1,
            product_catalog_order_model: "sale.order",
            active_model: "sale.order.line",
        }
    })

    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: barcode });
    await animationFrame();

    expect.verifySteps(["update_order_line_info"]);
});

test("Update product quantity in sale order line on scan same barcode again", async () => {
    const env = await makeMockEnv();
    const barcode = "123456789";

    onRpc("product.product", "read", () => {
        const products = Product._records._records.filter((product) => product.barcode === barcode);
        return { 
            length: products.length,
            records: products
        };
    });

    onRpc("/product/catalog/order_lines_info", () => deepCopy(saleOrderLineInfo));

    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();

        expect.step("update_sale_order_line_info");
        expect(params.product_id).toBe(1);
        expect(params.quantity).toBe(2);
        expect(params.res_model).toBe("sale.order");
        
        saleOrderLineInfo[1].quantity = 2;
        return {}
    });

    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            order_id: 1,
            product_catalog_order_model: "sale.order",
            active_model: "sale.order.line",
        }
    })

    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: barcode });
    await animationFrame();
    
    expect.verifySteps(["update_sale_order_line_info"]);
})

test("Prodct Not Found in Sale order", async () => {
    const env = await makeMockEnv();
    const barcode = "1122334455";

    onRpc("product.product", "read", () => {
        const products = Product._records._records.filter((product) => product.barcode === barcode);
        return { 
            length: products.length,
            records: products
        };
    });

    onRpc("/product/catalog/order_lines_info", () => deepCopy(saleOrderLineInfo));

    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            order_id: 1,
            product_catalog_order_model: "sale.order",
            active_model: "sale.order.line",
        }
    })

    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: barcode });
    await animationFrame();
    
    expect(".o_notification_content").toHaveText("Product not found with this barcode!");
});

const purchaseOrderLineInfo = {
    1: {
        price: 299,
        quantity: 0,
        productType: "consu",
        uom: { id: 1, name: "Unit" }},
    2: {
        price: 399,
        quantity: 2,
        productType: "consu",
        uom: { id: 1, name: "Unit" }
    },
}

test("Add product to purchase order on barcode scan", async () => {
    const env = await makeMockEnv();
    const barcode = "123456789";

    onRpc("product.product", "web_search_read", () => {
        const products = Product._records._records;
        return { 
            length: products.length,
            records: products
        };
    });

    onRpc("/product/catalog/order_lines_info", () => deepCopy(purchaseOrderLineInfo));

    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();

        expect.step("update_order_line_info");
        expect(params.product_id).toBe(1);
        expect(params.quantity).toBe(1);
        expect(params.res_model).toBe("purchase.order");

        purchaseOrderLineInfo[1].quantity = 1;
        return {}
    });

    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            order_id: 1,
            product_catalog_order_model: "purchase.order",
            active_model: "purchase.order.line",
        }
    })

    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: barcode });
    await animationFrame();

    expect.verifySteps(["update_order_line_info"]);
});

test("Update product quantity in purchase order line on scan same barcode again", async () => {
    const env = await makeMockEnv();
    const barcode = "987654321";

    onRpc("product.product", "read", () => {
        const products = Product._records._records.filter((product) => product.barcode === barcode);
        return { 
            length: products.length,
            records: products
        };
    });

    onRpc("/product/catalog/order_lines_info", () => deepCopy(purchaseOrderLineInfo));

    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();

        expect.step("update_purchase_order_line_info");
        expect(params.product_id).toBe(2);
        expect(params.quantity).toBe(3);
        expect(params.res_model).toBe("purchase.order");   
        
        purchaseOrderLineInfo[2].quantity = 3;
        return {}
    });

    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            order_id: 1,
            product_catalog_order_model: "purchase.order",
            active_model: "purchase.order.line",
        }
    })

    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: barcode });
    await animationFrame();
    
    expect.verifySteps(["update_purchase_order_line_info"]);
})

test("Prodct Not Found in Purchase order", async () => {
    const env = await makeMockEnv();
    const barcode = "9988776655";

    onRpc("product.product", "read", () => {
        const products = Product._records._records.filter((product) => product.barcode === barcode);
        return { 
            length: products.length,
            records: products
        };
    });

    onRpc("/product/catalog/order_lines_info", () => deepCopy(purchaseOrderLineInfo));

    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            order_id: 1,
            product_catalog_order_model: "purchase.order",
            active_model: "purchase.order.line",
            search_default_available: 1,
        },
    })

    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: barcode });
    await animationFrame();
    
    expect(".o_notification_content").toHaveText("Product not found with this barcode!");
});
