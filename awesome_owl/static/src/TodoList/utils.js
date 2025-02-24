import { onMounted, useRef } from "@odoo/owl";
 
export function useAutofocus(name) {
    const inputref = useRef(name)
    onMounted(() => {
        if (inputref.el) {
            inputref.el.focus();
        }
    });
  }