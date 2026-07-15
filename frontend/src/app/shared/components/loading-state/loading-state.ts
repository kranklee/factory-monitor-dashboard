import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-loading-state',
  imports: [MatProgressSpinnerModule],
  template: `
    <div class="loading" role="status" aria-live="polite">
      <mat-spinner diameter="36" />
      <span>{{ message() }}</span>
    </div>
  `,
  styles: `
    .loading {
      display: flex;
      min-height: 15rem;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      gap: 1rem;
      color: var(--app-text-secondary);
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoadingState {
  readonly message = input('Loading data…');
}
