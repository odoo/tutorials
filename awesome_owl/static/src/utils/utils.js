import { useRef, onMounted } from "@odoo/owl"

export function useInputFocus(ref) {
    const input_field = useRef(ref);
    onMounted(() => input_field.el.focus())
}
