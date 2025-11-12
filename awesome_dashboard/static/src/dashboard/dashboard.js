/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

import { Layout } from "@web/search/layout";
import { DashboardItem } from "../dashboard/dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { DashboardItemsDialog } from "./dashboard_items_dialog/dashboard_items_dialog";

export class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };

  setup() {
    this.action = useService("action");
    this.statistics = useState(useService("awesome_dashboard.statistics"));
    const removedItems = localStorage.getItem("removedItems")?.split(",") ?? [];
    this.items = useState(
      registry
        .category("awesome_dashboard")
        .getAll()
        .map((item) => ({
          ...item,
          isSelected: !removedItems.find((x) => item.id == x),
        }))
    );
    this.dialog = useService("dialog");
  }

  openCustomerKanban() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: _t("Leads"),
      target: "current",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }

  openDashboardItemsDialog() {
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
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
