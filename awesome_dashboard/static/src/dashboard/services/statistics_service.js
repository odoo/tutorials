import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { reactive } from "@odoo/owl";

const statisticsService = {
	async start() {
		const data = reactive({ isReady: false });
		const intervalId = setInterval(() => {
			loadStatistics
		}, 10 * 60 * 1000); // run 10 minutes

		const loadStatistics = async function () {
			try {
				const statistics = await rpc("/awesome_dashboard/statistics");
				Object.assign(data, statistics, { isReady: true });
			} catch (error) {
				clearInterval(intervalId);
			}
		};
		loadStatistics();
		return data;
	},
};

registry
	.category("services")
	.add("awesome_dashboard.statistics", statisticsService);
