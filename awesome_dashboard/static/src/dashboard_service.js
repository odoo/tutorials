/** @odoo-module **/

import { memoize } from "@web/core/utils/functions";
import { registry } from "@web/core/registry";

const statisticsService = {
	dependencies: ["rpc"],
	start(env, { rpc }) {
		return {mem_rpc: memoize(rpc)};
	},
};

registry.category("services").add("awesome_dashboard.statistics", statisticsService);
