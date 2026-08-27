import { registry, reactive } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { memoize } from "@web/core/utils/functions"


export async function _loadStatistics() {
    // console.log("loading statistics")
    const result = await rpc("/awesome_dashboard/statistics")
    // console.log(result)
    return result
}

export const myCaching = {
        start(env) {
            return { 
                loadStatistics() {
                    let memoLoadStatistics = memoize(_loadStatistics)
                    return memoLoadStatistics
                }
            }
        },
    }

registry.category("services").add("myCaching", myCaching);