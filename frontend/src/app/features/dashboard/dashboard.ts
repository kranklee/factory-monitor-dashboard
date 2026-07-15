import { DatePipe, DecimalPipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { finalize } from 'rxjs';

import { DashboardSummary } from '../../core/models/api.models';
import { DashboardService } from '../../core/services/dashboard.service';
import { LoadingState } from '../../shared/components/loading-state/loading-state';
import { PageHeader } from '../../shared/components/page-header/page-header';
import { StatusBadge } from '../../shared/components/status-badge/status-badge';

@Component({
  selector: 'app-dashboard',
  imports: [
    DatePipe,
    DecimalPipe,
    LoadingState,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    PageHeader,
    StatusBadge,
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Dashboard implements OnInit {
  private readonly dashboardService = inject(DashboardService);

  protected readonly summary = signal<DashboardSummary | null>(null);
  protected readonly loading = signal(true);
  protected readonly error = signal<string | null>(null);

  ngOnInit(): void {
    this.load();
  }

  protected load(): void {
    this.loading.set(true);
    this.error.set(null);
    this.dashboardService
      .getSummary()
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (summary) => this.summary.set(summary),
        error: () => this.error.set('Dashboard data is unavailable. Try again in a moment.'),
      });
  }

  protected statusPercent(count: number, total: number): number {
    return total ? Math.round((count / total) * 100) : 0;
  }
}
