import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus() {
  const inputRef = useRef("input");
  onMounted(() => {
    inputRef.el.focus();
  });
}
