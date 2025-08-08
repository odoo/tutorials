import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

const statistics_service = {
    start() {
        const statistics = reactive({ isAvailable: false });

        async function fetchStatistics() {
            try {
                const update_data = await rpc("/awesome_dashboard/statistics");
                Object.assign(statistics, update_data, { isAvailable: true });
            } catch (error) {
                console.error(_t("Error fetching statistics: "), error);
            }
        }

        return {
            statistics,
            fetchStatistics
        };
    },
};

registry.category("services").add("awesome_dashboard.statistics", statistics_service);
