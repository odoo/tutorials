import { Base } from "@point_of_sale/app/models/related_models";
import { registry } from "@web/core/registry";

export class HrEmployee extends Base {
    static pythonModel = "hr.employee";
}

registry.category("pos_available_models").add(HrEmployee.pythonModel, HrEmployee);
