import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { Machine, MachineStatus, PageResponse } from '../models/api.models';

export interface MachineFilters {
  page: number;
  pageSize: number;
  search?: string;
  status?: MachineStatus;
}

@Injectable({ providedIn: 'root' })
export class MachineService {
  private readonly http = inject(HttpClient);

  list(filters: MachineFilters): Observable<PageResponse<Machine>> {
    let params = new HttpParams().set('page', filters.page).set('page_size', filters.pageSize);
    if (filters.search) {
      params = params.set('search', filters.search);
    }
    if (filters.status) {
      params = params.set('status', filters.status);
    }
    return this.http.get<PageResponse<Machine>>(`${environment.apiUrl}/machines`, { params });
  }

  get(machineId: number): Observable<Machine> {
    return this.http.get<Machine>(`${environment.apiUrl}/machines/${machineId}`);
  }
}
