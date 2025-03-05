import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectSalespersonDialog } from "@salesperson_pos/select_salesperson_dialog/select_salesperson_dialog";

export class SelectSalespersonButton extends Component {
    static template = "salesperson_pos.SelectSalespersonButton";
    static components = { SelectSalespersonDialog };
    static props = {};

    setup() {
        this.pos = usePos();
        this.orm = useService("orm");
        this.dialog = useService("dialog");
        this.state = useState({ selectedSalesperson: null });
    }

    async selectSalesperson() {
        // Get the current POS order
        const currentOrder = this.pos.get_order();
        if (!currentOrder) return;

        try {
            // Fetch Salesperson List
            const salespersonList = await this.getSalespersonList();
            // Converting salespersonList object to array
            const salespersonArray = salespersonList.map((employee) => ({
                id: employee?.id || null,
                name: employee?.name || "Unknown",
                email: employee?.work_contact_id?.email || "no email",
                role: employee?._role || "",
            }));

            if (!salespersonArray || salespersonArray.length === 0) {
                this.dialog.add(AlertDialog, {
                    title: "No Salespersons Available",
                    body: "There are no active salespersons in this company.",
                });
                return;
            }

            // Open Selector Dialog
            const selectedSalesperson = await this.openSalespersonSelector(
                salespersonArray
            );
            Object.assign(this.state, { selectedSalesperson });

            if (this.state.selectedSalesperson) {
                currentOrder.set_salesperson(this.state.selectedSalesperson);
            }
        } catch (error) {
            this.dialog.add(AlertDialog, {
                title: "Error",
                body: "An error occurred while fetching salespersons. Please try again later.",
            });
        }
    }

    async getSalespersonList() {
        return this.pos.models["hr.employee"] || [];
    }

    async openSalespersonSelector(salespersonArray) {
        try {
            const payload = await makeAwaitable(
                this.dialog,
                SelectSalespersonDialog,
                { employees: salespersonArray, title: "Select a Salesperson" },
                {}
            );
            return payload;
        } catch (error) {
            throw Error("Error in Salesperson Selector:", error);
        }
    }
}
