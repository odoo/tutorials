/** @odoo-module **/

import { registry } from "@web/core/registry";

export const saleOrderLoggerService = {
    dependencies: ["barcode", "notification", "orm"],
    start(env, { barcode, notification, orm }) {
        console.log("📡 Sale Order Logger Service started. Barcode Scanner Active.");

        barcode.bus.addEventListener("barcode_scanned", async (event) => {
            const scannedBarcode = event.detail.barcode;
            console.log("📸 Scanned Barcode:", scannedBarcode);

            try {
                // Fetch product with matching barcode using ORM
                const products = await orm.call("product.template", "search_read", [
                    [["barcode", "=", scannedBarcode]], ["id", "name"]
                ], { limit: 1 });

                console.log("📦 All Products:", all_products);

                if (products.length > 0) {
                    const productName = products[0].name;
                    console.log("✅ Product found:", productName);

                    // Start looking for the product in pagination
                    await findAndClickProduct(productName);
                } else {
                    console.warn("⚠️ No matching product found.");
                    notification.add("No product found", { type: "warning" });
                }
            } catch (error) {
                console.error("❌ Error fetching product:", error);
                notification.add("Error fetching product", { type: "danger" });
            }
        });

        async function findAndClickProduct(productName) {
            let productFound = false;
            let pageCounter = 1; // Track page numbers

            while (!productFound) {
                console.log(`🔄 Checking Page ${pageCounter}...`);

                // Find all product cards on the current page
                let productCards = document.querySelectorAll(".o_kanban_record");
                productCards.forEach((card) => {
                    let nameElement = card.querySelector("span.fw-bolder.fs-4.text-reset.mb-1");

                    if (nameElement && nameElement.textContent.trim() === productName) {
                        console.log("🔍 Found matching product card:", productName);

                        if (card.classList.contains("o_product_added")) {
                            console.log("➕ Product already added. Clicking + button...");
                            let plusButton = card.querySelector("button:nth-child(3)");
                            if (plusButton) {
                                plusButton.click();
                            }
                        } else {
                            console.log("🛒 Product not added yet. Clicking Add button...");
                            let addButton = card.querySelector("button.btn-secondary");
                            if (addButton) {
                                addButton.click();
                            }
                        }
                        productFound = true;
                    }
                });

                if (productFound) {
                    return;
                }

                // Get pagination details
                let pagerValue = document.querySelector("span.o_pager_value");
                let totalProducts = document.querySelector("span.o_pager_limit")?.textContent || "0";

                if (!pagerValue || !totalProducts) {
                    console.warn("⚠️ Pagination elements not found.");
                    break;
                }

                let [currentStart, currentEnd] = pagerValue.textContent.split(" ")[0].split("-").map(Number);
                let totalProductCount = Number(totalProducts);

                console.log(`📄 Current Page Range: ${currentStart}-${currentEnd} / ${totalProductCount}`);

                if (currentEnd >= totalProductCount) {
                    console.warn("⚠️ Product not found, and no more pages left.");
                    notification.add("Product found, but could not update quantity", { type: "warning" });
                    break;
                }

                // Click the next page button
                let nextPageButton = document.querySelector(".o_pager_next");
                if (nextPageButton) {
                    console.log("➡️ Moving to the next page...");
                    nextPageButton.click();
                    await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for page load
                    pageCounter++;
                } else {
                    console.warn("⚠️ No Next Page button found.");
                    break;
                }
            }
        }
    },
};

// Register the service
registry.category("services").add("sale_order_logger", saleOrderLoggerService);
