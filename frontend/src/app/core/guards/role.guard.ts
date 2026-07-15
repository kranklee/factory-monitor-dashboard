import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { UserRole } from '../models/api.models';
import { AuthService } from '../services/auth.service';

export const roleGuard: CanActivateFn = (route) => {
  const role = inject(AuthService).user()?.role;
  const allowedRoles = (route.data['roles'] as UserRole[] | undefined) ?? [];
  return role && allowedRoles.includes(role) ? true : inject(Router).createUrlTree(['/forbidden']);
};
