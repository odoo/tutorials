/** @odoo-module **/
import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(refName) {
  const ref = useRef(refName);
  onMounted(() => {
    if (ref.el) {
      ref.el.focus();
    }
  });
  return ref;
}
