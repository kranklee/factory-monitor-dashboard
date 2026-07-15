import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Alert, AlertSeverity, AlertStatus, PageResponse } from '../models/api.models';

export interface AlertFilters {
  page: number;
  pageSize: number;
  search?: string;
  status?: AlertStatus;
  severity?: AlertSeverity;
}

@Injectable({ providedIn: 'root' })
export class AlertService {
  private readonly http = inject(HttpClient);

  list(filters: AlertFilters): Observable<PageResponse<Alert>> {
    let params = new HttpParams().set('page', filters.page).set('page_size', filters.pageSize);
    if (filters.search) {
      params = params.set('search', filters.search);
    }
    if (filters.status) {
      params = params.set('status', filters.status);
    }
    if (filters.severity) {
      params = params.set('severity', filters.severity);
    }
    return this.http.get<PageResponse<Alert>>(`${environment.apiUrl}/alerts`, { params });
  }

  updateStatus(alertId: number, status: AlertStatus): Observable<Alert> {
    return this.http.patch<Alert>(`${environment.apiUrl}/alerts/${alertId}/status`, { status });
  }
}
