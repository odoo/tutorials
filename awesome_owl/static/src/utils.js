import { onMounted } from "@odoo/owl";

export function useAutoFocus(ref) {
    onMounted(() => {
        if (ref.el) {
            ref.el.focus();
        }
    });
}
