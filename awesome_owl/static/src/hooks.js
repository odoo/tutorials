import { onMounted, useRef } from "@odoo/owl";
export function useAutoFocus(ref_name) {
    const ref = useRef(ref_name);
    onMounted(() => ref.el.focus())
}
