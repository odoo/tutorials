/** @odoo-module */

import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(name) {
  const ref = useRef(name);

  onMounted(() => {
    ref.el.focus();
  });
}
