import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { SalespersonListPopup } from "../salesperson_dialog/salesperson_dialog";

export class SelectSalesPersonButton extends Component {
  static template = "salesperson_pos.SelectSalesPersonButton";
  static components = { SalespersonListPopup };
  static props = {};
  setup() {
    this.pos = usePos();
    this.dialog = useService("dialog");
    this.orm = useService("orm");
    this.state = useState({
      selectedSalesperson: null,
    });
  }

  async SelectSalesPerson() {
    const currentOrder = this.pos.get_order();

    if (!currentOrder) {
      return false;
    }

    try {
      const salespersonList = await this.orm.searchRead(
        "hr.employee",
        [],
        ["id", "name", "work_email"]
      );

      if (salespersonList.length === 0) {
        this.dialog.add(AlertDialog, {
          title: "No Salesperson",
          body: "No salesperson found in the system.",
        });
        return;
      }
      this.dialog.add(SalespersonListPopup, {
        title: "Select Salesperson",
        salespersonList,
        confirm: (salesperson) => {
          this.state.selectedSalesperson = salesperson;
          if (salesperson) {
            currentOrder.set_salesperson(salesperson?.id);
          }
        },
      });
    } catch (error) {
      console.log(error);
    }
  }
}
