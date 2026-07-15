import { Routes } from '@angular/router';

import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login/login').then((m) => m.Login),
  },
  {
    path: '',
    canActivate: [authGuard],
    loadComponent: () => import('./layout/shell').then((m) => m.Shell),
    children: [
      {
        path: 'dashboard',
        title: 'Dashboard | Factory Monitor',
        loadComponent: () => import('./features/dashboard/dashboard').then((m) => m.Dashboard),
      },
      {
        path: 'machines',
        title: 'Machines | Factory Monitor',
        loadComponent: () =>
          import('./features/machines/machine-list/machine-list').then((m) => m.MachineList),
      },
      {
        path: 'machines/:id',
        title: 'Machine Details | Factory Monitor',
        loadComponent: () =>
          import('./features/machines/machine-detail/machine-detail').then((m) => m.MachineDetail),
      },
      {
        path: 'alerts',
        title: 'Alerts | Factory Monitor',
        canActivate: [roleGuard],
        data: { roles: ['admin', 'operator'] },
        loadComponent: () => import('./features/alerts/alerts').then((m) => m.Alerts),
      },
      { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
    ],
  },
  {
    path: 'forbidden',
    title: 'Access denied | Factory Monitor',
    loadComponent: () => import('./features/errors/error-pages').then((m) => m.ForbiddenPage),
  },
  {
    path: '**',
    title: 'Page not found | Factory Monitor',
    loadComponent: () => import('./features/errors/error-pages').then((m) => m.NotFoundPage),
  },
];
