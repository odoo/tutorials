/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { useState, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { ProductCatalogSearchPanel } from "@product/product_catalog/search/search_panel";

patch(ProductCatalogSearchPanel.prototype, {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.checkedCategories = useState(new Set());

        onMounted(() => {
            this.loadCheckedCategories();
        });
    },

    async loadCheckedCategories() {
        if (!this.env.searchModel.globalContext.active_model === "catalog") {
          return;
        }

        const catalogId = this.env.searchModel.globalContext.default_catalog_id || null;

        if (!catalogId) {
            console.warn("No catalog_id found in context.");
            return;
        }

        try {
            const catalogLines = await this.orm.searchRead(
                "catalog.line",
                [["catalog_id", "=", catalogId]],
                ["category_id"]
            );

            this.checkedCategories.clear();
            for (const line of catalogLines) {
                if (line.category_id) {
                    this.checkedCategories.add(line.category_id[0]);
                }
            }

            this.render();
        } catch (error) {
            console.error("Error fetching catalog lines:", error);
        }
    },

    async onCategoryCheckboxClick(ev) {
        if (!this.env.searchModel.globalContext.active_model === "catalog") {
            return;
        }
        const isChecked = ev.target.checked;
        const catalogId = this.env.searchModel.globalContext.default_catalog_id || null;
        const categoryId = parseInt(ev.target.dataset.categoryId, 10);

        if (!catalogId) {
            return;
        }

        try {
            let [catalogLine] = await this.orm.searchRead(
                "catalog.line",
                [["catalog_id", "=", catalogId], ["category_id", "=", categoryId]],
                ["id"]
            );

            if (isChecked) {
                if (!catalogLine) {
                    await this.orm.create("catalog.line", [{
                        catalog_id: catalogId,
                        category_id: categoryId,
                    }]);
                    this.checkedCategories.add(categoryId);
                }
            } else {
                if (catalogLine) {
                    await this.orm.unlink("catalog.line", [catalogLine.id]);
                    this.checkedCategories.delete(categoryId);
                }
            }

            this.render();
        } catch (error) {
            console.error("Error handling catalog line update:", error);
        }
    }
});
