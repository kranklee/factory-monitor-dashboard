import { ChangeDetectionStrategy, Component, input } from '@angular/core';

@Component({
  selector: 'app-empty-state',
  template: `
    <section class="empty">
      <h2>{{ title() }}</h2>
      <p>{{ message() }}</p>
    </section>
  `,
  styles: `
    .empty {
      padding: 3.5rem 1.5rem;
      text-align: center;
      color: var(--app-text-secondary);
    }
    h2 {
      margin: 0 0 0.5rem;
      color: var(--app-text-primary);
      font-size: 1.1rem;
    }
    p {
      margin: 0;
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class EmptyState {
  readonly title = input.required<string>();
  readonly message = input.required<string>();
}
