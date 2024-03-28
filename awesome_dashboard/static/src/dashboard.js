/** @odoo-module **/

import { Component, onWillStart, useState, xml } from "@odoo/owl";

import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { memoize } from "@web/core/utils/functions";
import { _t } from  "@web/core/l10n/translation";

import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";

class AwesomeDashboard extends Component {
	static template = "awesome_dashboard.AwesomeDashboard";
	static components = { Layout, DashboardItem, PieChart };

	setup() {
// 		this.state = useState({data: {}});
		this.state = useState( useService("awesome_dashboard.statistics") );
		this.action = useService("action");
// 		this.mem_rpc = useService("awesome_dashboard.statistics").mem_rpc;
// 		onWillStart(async () => {
// 			this.state.data = await this.mem_rpc("awesome_dashboard/statistics");
// 			console.log(this.state.data);
// 		});
		onWillStart( () => {
			console.log(this.state);
		});
	}

	customersView() {
		this.action.doAction("base.action_partner_form");
	}

	leadsView() {
		this.action.doAction({
			type: "ir.actions.act_window",
			name: _t("Leads"),
			// target: "current", (point?)
			// res_id: crm_lead_all_leads_view_tree,
			// res_id: 'toto', (works also?)
			res_model: "crm.lead",
			views: [[false, "tree"], [false, "kanban"]],
		});
	}
}

registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);

