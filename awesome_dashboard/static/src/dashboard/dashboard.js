/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboardItem";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardItemsDialog } from "./dashboard_item_dialog/dashboard_item_dialog";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static props = {
    label: String,
    data: Object,
  };

  setup() {
    this.action = useService("action");
    const removedItems = localStorage.getItem("removedItems")?.split(",") ?? [];
    this.statistics = useState(useService("awesome_dashboard.statistics"));
    this.dialog = useService("dialog");
    this.items = useState(
      registry
        .category("awesome_dashboard")
        .getAll()
        .map((item) => ({
          ...item,
          isSelected: !removedItems.find((i) => item.id == i),
        }))
    );
  }
  // Open the Customers view (Kanban)
  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  async openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "Leads",
      target: "current",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  openDialog() {
    this.dialog.add(DashboardItemsDialog, {
      items: this.items.map((item) => ({
        id: item.id,
        description: item.description,
        isSelected: item.isSelected,
      })),
      apply: (removedIds) => {
        localStorage.setItem("removedItems", removedIds?.join(","));
        this.items.forEach((item) => {
          if (removedIds.includes(item.id)) item.isSelected = false;
          else item.isSelected = true;
        });
      },
    });
  }
  static components = { DashboardItem, Layout, PieChart };
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
