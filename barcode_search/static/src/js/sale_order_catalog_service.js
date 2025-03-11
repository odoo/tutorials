/** @odoo-module **/

import { registry } from "@web/core/registry";
import { activeKanbanRecords } from "./kanban_record"; // ✅ Import the Kanban map

export const barcodeScannerService = {
    dependencies: ["barcode", "notification"],

    start(env, { barcode, notification }) {
        console.log("📡 Barcode Scanner Service started. Ready to scan.");

        barcode.bus.addEventListener("barcode_scanned", async (event) => {
            const scannedBarcode = event.detail.barcode;
            console.log("📸 Scanned Barcode:", scannedBarcode);

            if (!window.productData || window.productData.length === 0) {
                console.warn("⚠️ Product data not loaded yet.");
                notification.add("Product data is not available. Please reload the page.", { type: "warning" });
                return;
            }

            const product = window.productData.find((p) => p.barcode === scannedBarcode);

            if (product) {
                console.log("✅ Found Product - ID:", product.id, "Name:", product.name);
                notification.add(`Product: ${product.name} (ID: ${product.id})`, { type: "success" });

                const kanbanRecord = activeKanbanRecords.get(product.id); // ✅ Get the right Kanban record

                if (kanbanRecord) {
                    console.log("🎯 Calling addProductFromBarcode() for Product ID:", product.id);
                    kanbanRecord.addProductFromBarcode();
                } else {
                    console.warn("⚠️ No active Kanban record found for Product ID:", product.id);
                    notification.add("Could not add product. Please try again.", { type: "warning" });
                }
            } else {
                console.warn("⚠️ No matching product found.");
                notification.add("No product found", { type: "warning" });
            }
        });
    },
};

// Register the service
registry.category("services").add("barcode_scanner", barcodeScannerService);
