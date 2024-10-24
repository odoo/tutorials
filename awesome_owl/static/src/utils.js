
import { useRef, onMounted } from "@odoo/owl";

export function useAutoFocus(elRefName) {
    let ref = useRef(elRefName);
    onMounted(() => {
        ref.el.focus();
    })
    return ref;
}
