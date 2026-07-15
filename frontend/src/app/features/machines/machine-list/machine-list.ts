import { DatePipe, DecimalPipe } from '@angular/common';
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
import { MatTableModule } from '@angular/material/table';
import { RouterLink } from '@angular/router';
import { debounceTime, finalize, merge } from 'rxjs';

import { Machine, MachineStatus } from '../../../core/models/api.models';
import { MachineService } from '../../../core/services/machine.service';
import { EmptyState } from '../../../shared/components/empty-state/empty-state';
import { LoadingState } from '../../../shared/components/loading-state/loading-state';
import { PageHeader } from '../../../shared/components/page-header/page-header';
import { StatusBadge } from '../../../shared/components/status-badge/status-badge';

@Component({
  selector: 'app-machine-list',
  imports: [
    DatePipe,
    DecimalPipe,
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
    RouterLink,
    StatusBadge,
  ],
  templateUrl: './machine-list.html',
  styleUrl: './machine-list.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MachineList implements OnInit {
  private readonly machinesService = inject(MachineService);
  private readonly destroyRef = inject(DestroyRef);

  protected readonly displayedColumns = [
    'machine',
    'location',
    'status',
    'temperature',
    'efficiency',
    'lastSeen',
  ];
  protected readonly machines = signal<Machine[]>([]);
  protected readonly total = signal(0);
  protected readonly pageIndex = signal(0);
  protected readonly pageSize = signal(10);
  protected readonly loading = signal(true);
  protected readonly error = signal<string | null>(null);
  protected readonly searchControl = new FormControl('', { nonNullable: true });
  protected readonly statusControl = new FormControl<MachineStatus | ''>('', {
    nonNullable: true,
  });

  ngOnInit(): void {
    merge(this.searchControl.valueChanges, this.statusControl.valueChanges)
      .pipe(debounceTime(300), takeUntilDestroyed(this.destroyRef))
      .subscribe(() => this.load(0));
    this.load();
  }

  protected load(pageIndex = this.pageIndex()): void {
    this.pageIndex.set(pageIndex);
    this.loading.set(true);
    this.error.set(null);
    this.machinesService
      .list({
        page: pageIndex + 1,
        pageSize: this.pageSize(),
        search: this.searchControl.value.trim() || undefined,
        status: this.statusControl.value || undefined,
      })
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (response) => {
          this.machines.set(response.items);
          this.total.set(response.total);
        },
        error: () => this.error.set('Machine data could not be loaded.'),
      });
  }

  protected pageChanged(event: PageEvent): void {
    this.pageSize.set(event.pageSize);
    this.load(event.pageIndex);
  }

  protected clearFilters(): void {
    this.searchControl.setValue('', { emitEvent: false });
    this.statusControl.setValue('', { emitEvent: false });
    this.load(0);
  }
}
