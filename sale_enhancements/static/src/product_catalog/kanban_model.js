import { ProductCatalogKanbanModel } from "@product/product_catalog/kanban_model";
import { patch } from "@web/core/utils/patch";
import { rpc } from "@web/core/network/rpc";

patch(ProductCatalogKanbanModel.prototype, {

    async _loadData(params) {
        const result = await super._loadData(...arguments);
        if (!result.records?.length) {
            return result;
        }
        this.records = [...result.records];
        let orderType = params.context.product_catalog_order_model === "purchase.order" ? "purchase" : "sale";
        let partnerIds = await this._fetchPartnerIds(params);
        if (!partnerIds) {
            return result;
        }
        let partnerProdData = await this._fetchPartnerProdData(orderType, partnerIds);
        const productInvoiceDate = {};
        partnerProdData.forEach((line) => {
            const productIds = line.product_id[0];
            const invoiceDates = line.move_id && line.create_date;
            if (invoiceDates) {
                if (!productInvoiceDate[productIds] || new Date(invoiceDates).getTime() > [productIds]) {
                    productInvoiceDate[productIds] = new Date(invoiceDates).getTime();
                }
            }
        });
        this.records.forEach((p) => {
            p.invoice_time = productInvoiceDate[p.id] || 0; 
        });
        this.records.sort((a, b) => b.invoice_time - a.invoice_time);
        return { ...result, records: this.records };
    },

    async _fetchPartnerIds(params) {
        if (!params.context.order_id) return null;
        try {
            const orderData = await rpc("/web/dataset/call_kw", {
                model: params.context.product_catalog_order_model,
                method: "read",
                args: [[params.context.order_id], ["partner_id"]],
                kwargs: { context: params.context },
            });
            return orderData?.[0]?.partner_id?.[0] || null;
        } catch (error) {
            return null;
        }
    },

    async _fetchPartnerProdData(orderType, partnerIds) {
        try {
            return await rpc("/web/dataset/call_kw", {
                model: "account.move.line",
                method: "search_read",
                args: [
                    [["move_id.partner_id", "=", partnerIds], ["move_id.move_type", "=", orderType === "sale" ? "out_invoice" : "in_invoice"]]
                ],
                kwargs: {
                    fields: ["product_id", "move_id", "invoice_date", "create_date"],
                    order: "create_date desc",
                    limit: 100,
                },
            });
        } catch (error) {
            console.error("Failed to fetch partner product data:", error);
            return [];
        }
    }
});
