import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component } from "@odoo/owl";

export class DashboardLoader extends Component {
	static components = { LazyComponent };
	static template = "awesome_dashboard.DashboardLoader";
}

registry
	.category("actions")
	.add("awesome_dashboard.dashboard", DashboardLoader);
