import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    /**
     * Set the sales agent for the current order
     * @param {Number} sales_agent - The ID of the sales agent
     */
    set_sales_agent(sales_agent) {
        this.update({ sales_agent_id: sales_agent });
    },
    
    /**
     * Get the current sales agent ID
     * @returns {Number|null} The sales agent ID or null if not set
     */
    get_sales_agent() {
        return this.sales_agent_id || null;
    },
    
    /**
     * Export the order data including the sales agent
     * @override
     */
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (this.sales_agent_id) {
            json.sales_agent_id = this.sales_agent_id;
        }
        return json;
    },
});
