import { reactive } from '@odoo/owl';
import { rpc } from '@web/core/network/rpc';
import { registry } from '@web/core/registry';

const statisticsService = {
  start(env) {
    async function fetchStatistics() {
      const result = await rpc('/awesome_dashboard/statistics');
      return result;
    }

    async function updateData() {
      const results = await fetchStatistics();

      for (const key in data) {
        delete data[key];
      }

      Object.assign(data, results);
    }

    const data = reactive({});

    updateData();
    setInterval(updateData, 10000);

    return {
      loadStatistics() {
        return data;
      },
    };
  },
};

registry.category('services').add('statistics_service', statisticsService);
