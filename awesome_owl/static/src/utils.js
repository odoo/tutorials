import { useRef, onMounted } from "@odoo/owl";

export const useAutofocus = (element) => {
  const elementRef = useRef(element);
  onMounted(() => elementRef.el && elementRef.el.focus());
};
