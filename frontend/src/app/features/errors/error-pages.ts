import { ChangeDetectionStrategy, Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { RouterLink } from '@angular/router';

const errorPageStyles = `
  .error-page {
    display: flex;
    min-height: 100dvh;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    box-sizing: border-box;
    flex-direction: column;
    background: var(--app-background);
    color: var(--app-text-secondary);
    text-align: center;
  }
  mat-icon {
    width: 4rem;
    height: 4rem;
    color: #78909c;
    font-size: 4rem;
  }
  .code {
    margin: 1rem 0 0;
    color: #52778a;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.15em;
  }
  h1 {
    margin: 0.5rem 0;
    color: var(--app-text-primary);
    font-size: 2rem;
  }
  p:not(.code) {
    margin: 0 0 1.5rem;
  }
`;

@Component({
  selector: 'app-forbidden-page',
  imports: [MatButtonModule, MatIconModule, RouterLink],
  template: `
    <main class="error-page">
      <mat-icon>lock</mat-icon>
      <p class="code">403</p>
      <h1>Access denied</h1>
      <p>Your account does not have permission to open this area.</p>
      <a mat-flat-button routerLink="/dashboard">Return to dashboard</a>
    </main>
  `,
  styles: [errorPageStyles],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ForbiddenPage {}

@Component({
  selector: 'app-not-found-page',
  imports: [MatButtonModule, MatIconModule, RouterLink],
  template: `
    <main class="error-page">
      <mat-icon>search_off</mat-icon>
      <p class="code">404</p>
      <h1>Page not found</h1>
      <p>The requested page does not exist or may have moved.</p>
      <a mat-flat-button routerLink="/dashboard">Return to dashboard</a>
    </main>
  `,
  styles: [errorPageStyles],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class NotFoundPage {}
