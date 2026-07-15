import { HttpClient } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';

import { environment } from '../../../environments/environment';
import { AuthResponse, User } from '../models/api.models';

const TOKEN_KEY = 'factory-monitor.access-token';
const USER_KEY = 'factory-monitor.user';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly currentUser = signal<User | null>(this.readUser());

  readonly user = this.currentUser.asReadonly();
  readonly isAuthenticated = computed(() => Boolean(this.token && this.currentUser()));

  get token(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  login(email: string, password: string): Observable<AuthResponse> {
    return this.http
      .post<AuthResponse>(`${environment.apiUrl}/auth/login`, { email, password })
      .pipe(tap((response) => this.saveSession(response)));
  }

  logout(redirect = true): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    this.currentUser.set(null);
    if (redirect) {
      void this.router.navigate(['/login']);
    }
  }

  private saveSession(response: AuthResponse): void {
    localStorage.setItem(TOKEN_KEY, response.access_token);
    localStorage.setItem(USER_KEY, JSON.stringify(response.user));
    this.currentUser.set(response.user);
  }

  private readUser(): User | null {
    const value = localStorage.getItem(USER_KEY);
    if (!value) {
      return null;
    }
    try {
      return JSON.parse(value) as User;
    } catch {
      localStorage.removeItem(USER_KEY);
      localStorage.removeItem(TOKEN_KEY);
      return null;
    }
  }
}
