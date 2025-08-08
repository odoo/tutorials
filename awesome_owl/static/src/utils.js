import {onMounted, useRef} from "@odoo/owl";
export function useAutofocus(name) {
  let myRef = useRef(name);
          
   onMounted(() => {
        myRef.el.focus();
   });
}
