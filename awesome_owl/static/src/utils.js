import { onMounted, useRef } from "@odoo/owl";

export function useAutofocus(ref) {
  if (typeof ref === "string") {
    ref = useRef(ref)
  }

  onMounted(() => ref.el.focus())
}
