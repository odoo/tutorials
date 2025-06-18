/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { useState } from "@odoo/owl";
import { KanbanRecord } from "@web/views/kanban/kanban_record";

export class CatalogKanbanRecord extends KanbanRecord {
    static template = "CatalogKanbanRecord";
    static components = {
        ...KanbanRecord.components,
    };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({ removed: false });
        this.fetchRemovedState()
    }

    async fetchRemovedState() {
        try {
            const productId = this.props.record.resId;
            const catalogId = this.props.record.context?.default_catalog_id || null;
            if (!catalogId) return;

            const catalogLines = await this.orm.searchRead("catalog.line", [
                ["catalog_id", "=", catalogId]
            ], ["removed_products"]);

            if (catalogLines.length === 0) return;

            const removedProducts = catalogLines.flatMap(line => line.removed_products || []);
            this.state.removed = removedProducts.includes(productId);
        } catch (error) {
            console.error("Error fetching removed products:", error);
        }
    }

    get isRemoved() {
        return this.state.removed
    }

    async onGlobalClick(ev) {
        const productId = this.props.record.resId;
        const catalogId = this.props.record.context?.default_catalog_id || null;
        const categoryId = this.props.record.data?.categ_id?.[0] || null;

        if (!catalogId) {
            return;
        }

        try {
            let [catalogLine] = await this.orm.searchRead(
                "catalog.line",
                [["catalog_id", "=", catalogId], ["category_id", "=", categoryId]],
                ["id", "removed_products"]
            );

            let catalogLineId;
            let removedProducts = [];

            if (!catalogLine) {
                let createdLines = await this.orm.create("catalog.line", [{
                    catalog_id: catalogId,
                    category_id: categoryId,
                }]);

                catalogLineId = createdLines[0];
            } else {
                catalogLineId = catalogLine.id;
                removedProducts = catalogLine.removed_products || [];
            }

            if (removedProducts.includes(productId)) {
                removedProducts = removedProducts.filter(id => id !== productId);
                this.state.removed = false;

                if (removedProducts.length === 0) {
                    await this.orm.unlink("catalog.line", [catalogLineId]);
                    return;
                }
            } else {
                removedProducts.push(productId);
                this.state.removed = true;
            }

            await this.orm.write("catalog.line", [catalogLineId], {
                removed_products: [[6, 0, removedProducts]],
            });
        } catch (error) {
            console.error("Error updating removed_products:", error);
        }
    }
}
