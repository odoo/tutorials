import {useRef, onMounted, useEffect} from "@odoo/owl";

export function useCustomAutofocus(inputRefName) {
    const ref = useRef(inputRefName);
    /*
     onMounted(() => {
       ref.el.focus();
     })
    */

    useEffect(
        (el) => el && el.focus(),
        () => [ref.el]
    );


}
