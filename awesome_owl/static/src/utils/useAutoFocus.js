import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(refName) {
  const elRef = useRef(refName);
  onMounted(() => {
    if (elRef.el && typeof elRef.el.focus === 'function') {
      elRef.el.focus();
    } else {
        console.error("The component you try to focus does not have a focus method")
    }
  });
  return elRef;
}
