import { Component, useState, onMounted } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class SelectSalesAgentButton extends Component {
    static template = "pos.sales_agent.SelectSalesAgentButton";

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.salesAgent = useState({ name: "Select Agent", id: null });

        onMounted(() => {
            // Check if current order already has a sales agent
            const currentOrder = this.pos.get_order();
            if (currentOrder && currentOrder.get_sales_agent) {
                const salesAgentId = currentOrder.get_sales_agent();
                if (salesAgentId) {
                    this.updateSalesAgentDisplay(salesAgentId);
                }
            }
        });
    }

    /**
     * Updates the display with the selected sales agent's name
     * @param {Number} agentId - The ID of the selected sales agent
     */
    updateSalesAgentDisplay(agentId) {
        const employees = this.getEmployees();
        const agent = employees.find(emp => emp.id === agentId);
        if (agent) {
            this.salesAgent.id = agent.id;
            this.salesAgent.name = agent.name;
        }
    }

    /**
     * Gets the list of employees from POS data
     * @returns {Array} List of employee records
     */
    getEmployees() {
        return this.pos.models['hr.employee'] || [];
    }

    async selectSalesAgent() {
        try {
            const currentOrder = this.pos.get_order();
            if (!currentOrder) {
                this.dialog.add(AlertDialog, {
                    title: "No Active Order",
                    body: "Please create an order first.",
                    confirmLabel: "OK",
                });
                return;
            }

            const employees = this.getEmployees();
            if (!employees.length) {
                this.dialog.add(AlertDialog, {
                    title: "No Sales Agents Found",
                    body: "No sales agent records are available. Please make sure employees are configured in the system.",
                    confirmLabel: "OK",
                });
                return;
            }

            // Get current sales agent if exists
            const currentAgentId = currentOrder.get_sales_agent?.() || null;

            const selectionList = employees.map((emp) => ({
                id: emp.id,
                item: emp,
                label: emp.name + (emp.job_title ? ` (${emp.job_title})` : ''),
                isSelected: emp.id === currentAgentId,
            }));

            const payload = await makeAwaitable(this.dialog, SelectionPopup, {
                title: "Select Sales Agent",
                list: selectionList,
                confirmButtonText: "Select",
                cancelButtonText: "Cancel"
            });

            if (payload) {
                this.salesAgent.id = payload.id;
                this.salesAgent.name = payload.name;
                currentOrder.set_sales_agent(payload.id);
            }
        } catch (error) {
            console.error("Error selecting sales agent:", error);
            this.dialog.add(AlertDialog, {
                title: "Error",
                body: "An error occurred while selecting a sales agent: " + (error.message || 'Unknown error'),
                confirmLabel: "OK",
            });
        }
    }
}
