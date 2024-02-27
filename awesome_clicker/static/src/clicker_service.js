/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Clicker } from "./model/clicker_model";

const clickerService = {
  dependencies: [],
  start: () => new Clicker(),
};

registry
  .category("services")
  .add("awesome_clicker.clickerService", clickerService);
