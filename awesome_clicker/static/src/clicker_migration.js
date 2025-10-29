export const CURRENT_VERSION = 2.0;
export const migrations = [
    {
        fromVersion: 1.0,
        toVersion: 1.5,
        apply: (state) => {
            console.log("Nothing to do, you are uptodate dude!");
        }
    },
    {
        fromVersion: 1.5,
        toVersion: 2.0,
        apply: (state) => {
            console.log("New tree available: peach tree!");
            state.trees.peachTree = {
                price: 1000000,
                number: 0,
                level: 4,
                fruit: "peaches"
            }
            state.fruits.peaches = 0;
        }
    }
];

export function migrate(localState) {
    if (localState?.version_number < CURRENT_VERSION) {
        for (const migration of migrations) {
            if (localState.version_number === migration.fromVersion) {
                migration.apply(localState);
                localState.version_number = migration.toVersion
            }
        }
        localState.version_number = CURRENT_VERSION;
    }
    return localState;
}
