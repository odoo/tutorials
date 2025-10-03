

import { registry } from '@web/core/registry';
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";


export const dashboardService = {
    async start() {
        let stats = reactive({ isLoading: true });
        async function loadStatistics() {
            const data = await rpc("/awesome_dashboard/statistics", {});
            Object.assign(stats, data, { isLoading: false });
        }

        loadStatistics();
        setInterval(async () => await loadStatistics(), 10 * 1000);
        return { stats, loadStatistics };
    }
}

registry.category('services').add('awesome_dashboard.statistics', dashboardService);
