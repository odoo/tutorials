import { registry } from '@web/core/registry';
import { rpc } from '@web/core/network/rpc';
import { memoize } from '@web/core/utils/functions';

const dashboardService = {
    start() {
        return {
            loadStatisitcs: memoize(async () => {
                const result = await rpc('/awesome_dashboard/statistics', {});
                return { ...result };
            }),
        }
    }
}

registry.category('services').add('awesome_dashboard.statistics', dashboardService);