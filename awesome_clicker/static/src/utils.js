import { rewards } from "./click_rewards";


export function chooseReward(current_level) {
    let available_rewards = rewards.filter(reward =>
        (!reward.minLevel || reward.minLevel <= current_level) &&
        (!reward.maxLevel || reward.maxLevel >= current_level)
    );
    let reward_index = Math.ceil(Math.random() * available_rewards.length) - 1
    return available_rewards[reward_index];
}
