import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./DashboardItem/DashboardItem";
import { PieChart } from "./PieChart/PieChart";

class AwesomeDashboard extends Component {
	static components = { Layout, DashboardItem, PieChart };
	static template = "awesome_dashboard.AwesomeDashboard";

	setup() {
		this.action = useService("action");
		this.statistics = useState(useService("awesome_dashboard.statistics"));
		this.modalState = useState({ isOpen: false });

		this.temp = useState({ ids: ["a", "b"] });

		this.hiddenItems = useState({
			ids: JSON.parse(
				localStorage.getItem("hidden_dashboard_items") || "[]"
			),
		});
		console.log(this.hiddenItems.ids);

		this.items = useState(
			registry
				.category("awesome_dashboard")
				.getAll()
				.filter((item) => !this.hiddenItems.ids.includes(item.id))
		);

		this.allItems = useState(
			registry.category("awesome_dashboard").getAll()
		);
	}

	openCustomersKanban() {
		this.action.doAction("base.action_partner_form");
	}

	openLeads() {
		this.action.doAction({
			type: "ir.actions.act_window",
			name: "CRM Leads",
			res_model: "crm.lead",
			views: [[false, "list", "form"]],
		});
	}

	toggleModal() {
		this.modalState.isOpen = !this.modalState.isOpen;
	}

	toggleItem(event) {
		const itemId = event.target.value;

		if (event.target.checked) {
			this.hiddenItems.ids = this.hiddenItems.ids.filter(
				(id) => id !== itemId
			);
		} else {
			this.hiddenItems.ids.push(itemId);
		}
	}

	saveSettings() {
		localStorage.setItem(
			"hidden_dashboard_items",
			JSON.stringify(this.hiddenItems.ids)
		);

		this.items = registry
			.category("awesome_dashboard")
			.getAll()
			.filter((item) => !this.hiddenItems.ids.includes(item.id));

		this.toggleModal();
	}
}

registry
	.category("lazy_components")
	.add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
