/** @odoo-module **/

import { onMounted } from "@odoo/owl";

export const useAutofocus = (ref) => {
  onMounted(() => {
    ref.el?.focus();
  });
};
