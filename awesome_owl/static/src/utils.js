import { onMounted } from "@odoo/owl";

export function useAutofocus(ref) {
    onMounted(() => {
        if(ref.el)
            ref.el.focus();
    });
}
