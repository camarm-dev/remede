import { registerPlugin } from '@capacitor/core';

export interface SetResultPlugin {
    sendActiveRemedeResult(options: { value: string }): Promise<void>;
}

const SetResult = registerPlugin<SetResultPlugin>('SetResult');

export default SetResult;
