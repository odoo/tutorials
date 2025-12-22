import { useRef, onMounted } from "@odoo/owl"

export function useAutoFocus(ref_name) {
    const ref = useRef(ref_name)

    onMounted(() => {
        if (ref.el) {
            ref.el.focus()
        }
    })

    return ref;
}