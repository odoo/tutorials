import { useRef, onMounted } from "@odoo/owl";

export function useAutofocus(name) {
  const inputRef = useRef(name);
  onMounted(() => {
    inputRef.el.focus();
  });
}
