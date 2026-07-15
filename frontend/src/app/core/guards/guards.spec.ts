import { signal } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import {
  ActivatedRouteSnapshot,
  provideRouter,
  Router,
  RouterStateSnapshot,
  UrlTree,
} from '@angular/router';

import { User } from '../models/api.models';
import { AuthService } from '../services/auth.service';
import { authGuard } from './auth.guard';
import { roleGuard } from './role.guard';

describe('route guards', () => {
  const user = signal<User | null>(null);
  const isAuthenticated = signal(false);

  beforeEach(() => {
    user.set(null);
    isAuthenticated.set(false);
    TestBed.configureTestingModule({
      providers: [
        provideRouter([]),
        {
          provide: AuthService,
          useValue: { user, isAuthenticated },
        },
      ],
    });
  });

  it('preserves the requested URL when authentication is required', () => {
    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as ActivatedRouteSnapshot, { url: '/machines/42' } as RouterStateSnapshot),
    ) as UrlTree;

    expect(TestBed.inject(Router).serializeUrl(result)).toBe('/login?returnUrl=%2Fmachines%2F42');
  });

  it('prevents a viewer from opening an operator route', () => {
    user.set({ role: 'viewer' } as User);
    const route = { data: { roles: ['admin', 'operator'] } } as unknown as ActivatedRouteSnapshot;

    const result = TestBed.runInInjectionContext(() =>
      roleGuard(route, {} as RouterStateSnapshot),
    ) as UrlTree;

    expect(TestBed.inject(Router).serializeUrl(result)).toBe('/forbidden');
  });
});
