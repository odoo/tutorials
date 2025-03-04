import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { registry } from "@web/core/registry";

export class SalespersonPosOrder extends PosOrder {
    setSalesPerson(sales_person) {
        this.update({ sales_person_id: sales_person })
    }
}

registry.category("pos_available_models").add(PosOrder.pythonModel, SalespersonPosOrder, { force: true });
