import { Routes } from '@angular/router';
import { CopilotUi } from './copilot-ui/copilot-ui';

export const routes: Routes = [
{
    path: '',
    component: CopilotUi,
    pathMatch: 'full'
}

];
