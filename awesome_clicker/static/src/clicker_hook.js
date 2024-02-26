/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { useState } from "@odoo/owl";

export const useClicker = () =>
  useState(useService("awesome_clicker.clickerService"));
