import { registry } from "@web/core/registry";
import { Base } from "@point_of_sale/app/models/related_models";

export class HrEmployee extends Base {
  static pythonModel = "hr.employee";

  get searchString() {
    const fields = ["name"];
    return fields
      .map((field) => {
        return this[field] || "";
      })
      .filter(Boolean)
      .join(" ");
  }
}

registry
  .category("pos_available_models")
  .add(HrEmployee.pythonModel, HrEmployee);
