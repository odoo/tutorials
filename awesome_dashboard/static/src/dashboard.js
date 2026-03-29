import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
	static template = "awesome_dashboard.AwesomeDashboard";
	static components = { DashboardItem, Layout };

	setup() {
		this.display = {
			controlPanel: {},
		};
		this.action = useService("action");
		this.statistics = {};
		onWillStart(async () => {
			// Fetch data from the controller route
			this.statistics = await rpc("/awesome_dashboard/statistics");
		});
	}

	openCustomersView() {
		this.action.doAction("base.action_partner_form");
	}

	openLeads() {
		this.action.doAction({
			type: "ir.actions.act_window",
			name: "All leads",
			res_model: "crm.lead",
			views: [
				[false, "form"],
				[false, "list"],
			],
		});
	}
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
