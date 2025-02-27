import { registry } from '@web/core/registry';
import { rpc } from '@web/core/network/rpc';
import { reactive } from '@odoo/owl';

const dashboardService = {
    start() {
        let stats = reactive({
            isReady: false,
        });

        async function loadData() {
            const result = await rpc('/awesome_dashboard/statistics');
            Object.assign(stats, result, { isReady: true });
            setTimeout(() => {
                loadData();
            }, 1000 * 10);
        }

        loadData();

        return stats;
    },
};

registry
    .category('services')
    .add('awesome_dashboard.statistics', dashboardService);
