import { _t } from "@web/core/l10n/translation";
import { reactive } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export const statistics = {
    start() {
        this.data = reactive({ });
        return {
            loadStatistics: this.loadStatistics.bind(this)
        };
    },
    async rpcCall() {
        const result = await rpc("/awesome_dashboard/statistics");
        for (const [key, value] of Object.entries(result)) {
            this.data[key] = value;
            /* Adds action to the chart for onclick callback */
            if (key === "orders_by_size") {
                Object.keys(this.data[key]).forEach(stat => {
                    this.data[key][stat] = {
                        value: this.data[key][stat],
                        action: {
                            name: _t("Corresponding Orders"),
                            type: "ir.actions.act_window",
                            res_model: "sale.order",
                            views: [
                                [false, "list"]
                            ],
                            domain: [
                                [ "state", "not in", [ "draft", "sent", "cancel" ] ],
                                [ "order_line.product_id.product_template_attribute_value_ids.name", "=", stat ]
                            ]
                        }
                    }
                });
            }
        }
    },
    loadStatistics() {
        if (!this.interval) {
            this.rpcCall();
            clearInterval(this.interval);
            this.interval = setInterval(this.rpcCall.bind(this), 10000);
        }
        return this.data;
    }
};

registry.category("services").add("awesome_dashboard.statistics", statistics);
