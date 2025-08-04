import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "@awesome_dashboard/dashboard/components/dashboard_item/dashboard_item";
import { PieChart } from "@awesome_dashboard/dashboard/components/piechart/piechart";
import { useState } from "@odoo/owl";
import { SettingsDialog } from "@awesome_dashboard/dashboard/components/settings_dialog/settings_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart}

    setup() {
      this.dialog = useService("dialog");
      this.action = useService("action");
      this.display = { controlPanel: {} };
      this.statisticsService = useService("awesome_dashboard.statistics");
      this.statistics = useState(this.statisticsService.statistics);
      this.allItems = registry.category('awesome_dashboard').getAll() || [];
      this.removedIds = JSON.parse(localStorage.getItem("awesome_dashboard_hidden_items") || "[]");
      this.dashboardItems = this.allItems.filter(
        item => !this.removedIds.includes(item.id)
      );
    }

    openCustomers() {
      this.action.doAction('base.action_partner_form');
    }
    
    openLeads() {
      this.action.doAction({
        type: "ir.actions.act_window",
        name: "Leads",
        res_model: "crm.lead",
        views: [[false, "list"], [false, "form"]],
        target: "current",
      });
    }

    openSettings() {
      this.dialog.add(SettingsDialog, {
        items: this.allItems,
        removedIds: this.removedIds || [],
        onSave: (removed) => {
          localStorage.setItem("awesome_dashboard_hidden_items", JSON.stringify(removed));
          this.removedIds = removed;  
          this.dashboardItems = this.allItems.filter(item => !removed.includes(item.id));
          this.render();
        }
      });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
