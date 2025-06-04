import { expect, test } from "@odoo/hoot";
import { mountView, onRpc, makeMockEnv} from "@web/../tests/web_test_helpers";
import { click, animationFrame } from "@odoo/hoot-dom";
import { defineBarcodeHandlingModels } from "./barcode_handling_test_helpers";

defineBarcodeHandlingModels();

test("Add a new product for so", async () => {
    let env = await makeMockEnv();

    onRpc("product.product","read", () => {
        return {
            length: 1,
            records: [
                { id: 2, name: "iPad", barcode: "987654321",
                    productCatalogData:{
                        price: 200,
                        quantity: 1,
                        productType: "consu",
                        readOnly: false,
                    } 
                },
            ],
        };
    });
    
    onRpc("/product/catalog/order_lines_info", () => {
        return {
            2: {
                price: 200,
                quantity: 1,
                productType: "consu",
                readOnly: false,
            },
        };
    });

    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();
        expect(params.product_id).toBe(1);
        expect(params.quantity).toBe(1);
        expect(params.order_id).toBe(1);
        return {price: 200};
    });

    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            "order_id": 1,
            "orderResModel": "sale.order",
            "active_model": "sale.order.line",
            "product_catalog_order_model": "sale.order",
        },
    });

    await animationFrame();
    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: "123456789" });


});

test("Adding same product increases the quantity for so", async () => {
    let env = await makeMockEnv();

    onRpc("product.product","read", () => {
        return {
            length: 1,
            records: [
                { id: 1, name: "iPhone", barcode: "123456789", 
                    productCatalogData:{
                        price: 100,
                        quantity: 1,
                        productType: "consu",
                        readOnly: false,
                    } 
                },
            ],
        };
    });
    
    onRpc("/product/catalog/order_lines_info", () => {
        return {
            1: {
                price: 100,
                quantity: 1,
                productType: "consu",
                readOnly: false,
            },
        };
    });

    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();
        expect(params.quantity).toBe(2);
        return {price: 200};
    });
    
    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            "order_id": 2,
            "orderResModel": "sale.order",
            "active_model": "sale.order.line",
            "product_catalog_order_model": "sale.order",
        },
    });

    await animationFrame();
    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: "123456789" });

});

test("No product found for so", async () => {
    let env = await makeMockEnv();

    onRpc("product.product","read", () => {
        return {};
    });
    
    onRpc("/product/catalog/order_lines_info", () => {
        return {
            2: {
                price: 200,
                quantity: 1,
                productType: "consu",
                readOnly: false,
            },
        };
    });

    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();
        expect(params.product_id).toBe(1);
        expect(params.quantity).toBe(1);
        expect(params.order_id).toBe(1);
        return {price: 200};
    });

    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            "order_id": 1,
            "orderResModel": "sale.order",
            "active_model": "sale.order.line",
            "product_catalog_order_model": "sale.order",
        },
    });

    await animationFrame();
    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: "12345678" });
    await animationFrame();
    expect(".o_notification_body").toHaveText("No product found with barcode: 12345678");
});


test("Add a new product for po", async () => {
    let env = await makeMockEnv();

    onRpc("product.product","read", () => {
        return {
            length: 1,
            records: [
                { id: 2, name: "iPad", barcode: "987654321",
                    productCatalogData:{
                        price: 200,
                        quantity: 1,
                        productType: "consu",
                        readOnly: false,
                    } 
                },
            ],
        };
    });
    
    onRpc("/product/catalog/order_lines_info", () => {
        return {
            2: {
                price: 200,
                quantity: 1,
                productType: "consu",
                readOnly: false,
                uom: { id: 1, name: "Unit" },
            },
        };
    });

    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();
        expect(params.product_id).toBe(1);
        expect(params.quantity).toBe(1);
        expect(params.order_id).toBe(1);
        return {price: 200};
    });
    
    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            "order_id": 1,
            "orderResModel": "purchase.order",
            "active_model": "purchase.order.line",
            "product_catalog_order_model": "purchase.order",
        },
    });

    await animationFrame();
    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: "123456789" });

});

test("Adding same product increases the quantity for po", async () => {
    let env = await makeMockEnv();

    onRpc("product.product","read", () => {
        return {
            length: 1,
            records: [
                { id: 1, name: "iPhone", barcode: "123456789", 
                    productCatalogData:{
                        price: 100,
                        quantity: 1,
                        productType: "consu",
                        readOnly: false,
                    } 
                },
            ],
        };
    });
    
    onRpc("/product/catalog/order_lines_info", () => {
        return {
            1: {
                price: 100,
                quantity: 1,
                productType: "consu",
                readOnly: false,
                uom: { id: 1, name: "Unit" },
            },
        };
    });

    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();
        expect(params.quantity).toBe(2);
        return {price: 200};
    });
    
    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            "order_id": 2,
            "orderResModel": "purchase.order",
            "active_model": "purchase.order.line",
            "product_catalog_order_model": "purchase.order",
        },
    });

    await animationFrame();
    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: "123456789" });

});

test("No product found for po", async () => {
    let env = await makeMockEnv();

    onRpc("product.product","read", () => {
        return {};
    });
    
    onRpc("/product/catalog/order_lines_info", () => {
        return {
            2: {
                price: 200,
                quantity: 1,
                productType: "consu",
                readOnly: false,
                uom: { id: 1, name: "Unit" },
            },
        };
    });

    onRpc("/product/catalog/update_order_line_info", async (request) => {
        const { params } = await request.json();
        expect(params.product_id).toBe(1);
        expect(params.quantity).toBe(1);
        expect(params.order_id).toBe(1);
        return {price: 200};
    });
    
    await mountView({
        resModel: "product.product",
        type: "kanban",
        context: {
            "order_id": 1,
            "orderResModel": "purchase.order",
            "active_model": "purchase.order.line",
            "product_catalog_order_model": "purchase.order",
        },
    });

    await animationFrame();
    await click(".o_control_panel");
    env.services.barcode.bus.trigger("barcode_scanned", { barcode: "12345678" });
    await animationFrame();
    expect(".o_notification_body").toHaveText("No product found with barcode: 12345678");

});
