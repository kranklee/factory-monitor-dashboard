import { DatePipe } from '@angular/common';
import {
  ChangeDetectionStrategy,
  Component,
  DestroyRef,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { debounceTime, finalize, merge } from 'rxjs';

import { Alert, AlertSeverity, AlertStatus } from '../../core/models/api.models';
import { AlertService } from '../../core/services/alert.service';
import { EmptyState } from '../../shared/components/empty-state/empty-state';
import { LoadingState } from '../../shared/components/loading-state/loading-state';
import { PageHeader } from '../../shared/components/page-header/page-header';
import { StatusBadge } from '../../shared/components/status-badge/status-badge';

@Component({
  selector: 'app-alerts',
  imports: [
    DatePipe,
    EmptyState,
    LoadingState,
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatPaginatorModule,
    MatSelectModule,
    MatTableModule,
    PageHeader,
    ReactiveFormsModule,
    StatusBadge,
  ],
  templateUrl: './alerts.html',
  styleUrl: './alerts.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Alerts implements OnInit {
  private readonly alertService = inject(AlertService);
  private readonly snackBar = inject(MatSnackBar);
  private readonly destroyRef = inject(DestroyRef);

  protected readonly displayedColumns = [
    'severity',
    'alert',
    'machine',
    'detected',
    'status',
    'actions',
  ];
  protected readonly alerts = signal<Alert[]>([]);
  protected readonly total = signal(0);
  protected readonly pageIndex = signal(0);
  protected readonly pageSize = signal(10);
  protected readonly loading = signal(true);
  protected readonly updating = signal<Set<number>>(new Set());
  protected readonly error = signal<string | null>(null);
  protected readonly searchControl = new FormControl('', { nonNullable: true });
  protected readonly statusControl = new FormControl<AlertStatus | ''>('', { nonNullable: true });
  protected readonly severityControl = new FormControl<AlertSeverity | ''>('', {
    nonNullable: true,
  });

  ngOnInit(): void {
    merge(
      this.searchControl.valueChanges,
      this.statusControl.valueChanges,
      this.severityControl.valueChanges,
    )
      .pipe(debounceTime(300), takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.load(0));
    this.load();
  }

  protected load(pageIndex = this.pageIndex()): void {
    this.pageIndex.set(pageIndex);
    this.loading.set(true);
    this.error.set(null);
    this.alertService
      .list({
        page: pageIndex + 1,
        pageSize: this.pageSize(),
        search: this.searchControl.value.trim() || undefined,
        status: this.statusControl.value || undefined,
        severity: this.severityControl.value || undefined,
      })
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (response) => {
          this.alerts.set(response.items);
          this.total.set(response.total);
        },
        error: () => this.error.set('Alert data could not be loaded.'),
      });
  }

  protected updateStatus(alert: Alert, status: AlertStatus): void {
    this.setUpdating(alert.id, true);
    this.alertService
      .updateStatus(alert.id, status)
      .pipe(finalize(() => this.setUpdating(alert.id, false)))
      .subscribe({
        next: (updated) => {
          this.alerts.update((items) =>
            items.map((item) => (item.id === updated.id ? updated : item)),
          );
          this.snackBar.open(`Alert ${status}.`, 'Dismiss', { duration: 3000 });
        },
        error: () =>
          this.snackBar.open('The alert could not be updated.', 'Dismiss', { duration: 4000 }),
      });
  }

  protected pageChanged(event: PageEvent): void {
    this.pageSize.set(event.pageSize);
    this.load(event.pageIndex);
  }

  protected clearFilters(): void {
    this.searchControl.setValue('', { emitEvent: false });
    this.statusControl.setValue('', { emitEvent: false });
    this.severityControl.setValue('', { emitEvent: false });
    this.load(0);
  }

  private setUpdating(alertId: number, isUpdating: boolean): void {
    this.updating.update((current) => {
      const next = new Set(current);
      if (isUpdating) {
        next.add(alertId);
      } else {
        next.delete(alertId);
      }
      return next;
    });
  }
}
