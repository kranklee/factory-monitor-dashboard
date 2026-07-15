import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ActivatedRoute, Router } from '@angular/router';
import { finalize } from 'rxjs';

import { ApiErrorResponse } from '../../../core/models/api.models';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  imports: [
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatProgressSpinnerModule,
    ReactiveFormsModule,
  ],
  templateUrl: './login.html',
  styleUrl: './login.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Login {
  private readonly formBuilder = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  protected readonly loading = signal(false);
  protected readonly error = signal<string | null>(null);
  protected readonly hidePassword = signal(true);
  protected readonly form = this.formBuilder.nonNullable.group({
    email: ['operator@factorymonitor.io', [Validators.required, Validators.email]],
    password: ['Operator123!', [Validators.required, Validators.minLength(8)]],
  });

  protected submit(event: Event): void {
    event.preventDefault();
    if (this.form.invalid || this.loading()) {
      this.form.markAllAsTouched();
      return;
    }
    this.loading.set(true);
    this.error.set(null);
    const { email, password } = this.form.getRawValue();
    this.auth
      .login(email, password)
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: () => void this.router.navigateByUrl(this.returnUrl()),
        error: (error: HttpErrorResponse) => this.error.set(this.errorMessage(error)),
      });
  }

  private returnUrl(): string {
    const value = this.route.snapshot.queryParamMap.get('returnUrl');
    return value?.startsWith('/') && !value.startsWith('//') ? value : '/dashboard';
  }

  private errorMessage(error: HttpErrorResponse): string {
    const response = error.error as ApiErrorResponse | undefined;
    return response?.error?.message ?? 'Unable to sign in. Check your connection and try again.';
  }
}
