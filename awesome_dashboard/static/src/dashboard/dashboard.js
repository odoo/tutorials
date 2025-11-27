import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./DashboardItem/dashboard_item";
import { PieChart } from "./PieChart/pie_chart";

class AwesomeDashboard extends Component {
	static template = "awesome_dashboard.AwesomeDashboard";
	static components = { Layout, DashboardItem, PieChart };

	setup() {
		this.action = useService("action");
		const statisticsService = useService("awesome_dashboard.statistics");
		this.statistics = useState(statisticsService.state);
		this.modalState = useState({ isOpen: false });
		this.hiddenItems = useState({ ids: JSON.parse(localStorage.getItem("hidden_dashboard_items") || "[]"), });
		this.items = useState(registry.category("awesome_dashboard").getAll().filter((item) => !this.hiddenItems.ids.includes(item.id)));
		this.allItems = useState(registry.category("awesome_dashboard").getAll());
	}

	openCustomers() {
		this.action.doAction({
			type: "ir.actions.act_window",
			name: "Customers",
			res_model: "res.partner",
			views: [
				[false, "kanban"],
				[false, "form"],
				[false, "list"],
			],
		});
	}

	openLeads() {
		this.action.doAction({
			type: "ir.actions.act_window",
			name: "Leads",
			res_model: "crm.lead",
			views: [
				[false, "list"],
				[false, "form"],
			],
		});
	}

	toggleModal() {
		this.modalState.isOpen = !this.modalState.isOpen
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

	applySettings() {
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

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
