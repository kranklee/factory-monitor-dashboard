import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';

@Component({
  selector: 'app-status-badge',
  template: `<span class="badge" [class]="'badge badge--' + status()">{{ label() }}</span>`,
  styleUrl: './status-badge.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StatusBadge {
  readonly status = input.required<string>();
  readonly label = computed(() => this.status().replaceAll('_', ' '));
}
