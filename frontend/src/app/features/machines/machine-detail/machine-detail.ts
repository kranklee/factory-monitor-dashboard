import { DatePipe, DecimalPipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { finalize } from 'rxjs';

import { Machine } from '../../../core/models/api.models';
import { MachineService } from '../../../core/services/machine.service';
import { LoadingState } from '../../../shared/components/loading-state/loading-state';
import { PageHeader } from '../../../shared/components/page-header/page-header';
import { StatusBadge } from '../../../shared/components/status-badge/status-badge';

@Component({
  selector: 'app-machine-detail',
  imports: [
    DatePipe,
    DecimalPipe,
    LoadingState,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    PageHeader,
    RouterLink,
    StatusBadge,
  ],
  templateUrl: './machine-detail.html',
  styleUrl: './machine-detail.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MachineDetail implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly machineService = inject(MachineService);

  protected readonly machine = signal<Machine | null>(null);
  protected readonly loading = signal(true);
  protected readonly error = signal<string | null>(null);

  ngOnInit(): void {
    this.load();
  }

  protected load(): void {
    const machineId = Number(this.route.snapshot.paramMap.get('id'));
    if (!Number.isInteger(machineId) || machineId < 1) {
      this.error.set('The machine identifier is invalid.');
      this.loading.set(false);
      return;
    }
    this.loading.set(true);
    this.machineService
      .get(machineId)
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (machine) => this.machine.set(machine),
        error: (error: HttpErrorResponse) =>
          this.error.set(
            error.status === 404 ? 'Machine not found.' : 'Machine data is unavailable.',
          ),
      });
  }
}
