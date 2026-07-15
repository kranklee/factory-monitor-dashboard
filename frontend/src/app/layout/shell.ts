import { BreakpointObserver } from '@angular/cdk/layout';
import { ChangeDetectionStrategy, Component, computed, inject, viewChild } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenav, MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { map } from 'rxjs';

import { AuthService } from '../core/services/auth.service';

interface NavigationItem {
  label: string;
  icon: string;
  route: string;
}

@Component({
  selector: 'app-shell',
  imports: [
    MatButtonModule,
    MatDividerModule,
    MatIconModule,
    MatListModule,
    MatMenuModule,
    MatSidenavModule,
    MatToolbarModule,
    RouterLink,
    RouterLinkActive,
    RouterOutlet,
  ],
  templateUrl: './shell.html',
  styleUrl: './shell.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Shell {
  private readonly breakpoints = inject(BreakpointObserver);
  protected readonly auth = inject(AuthService);
  protected readonly sidenav = viewChild(MatSidenav);
  protected readonly isHandset = toSignal(
    this.breakpoints.observe('(max-width: 768px)').pipe(map((result) => result.matches)),
    { initialValue: false },
  );
  protected readonly navigation = computed<NavigationItem[]>(() => {
    const items: NavigationItem[] = [
      { label: 'Dashboard', icon: 'space_dashboard', route: '/dashboard' },
      { label: 'Machines', icon: 'precision_manufacturing', route: '/machines' },
    ];
    if (this.auth.user()?.role !== 'viewer') {
      items.push({ label: 'Alerts', icon: 'notification_important', route: '/alerts' });
    }
    return items;
  });

  protected closeNavigation(): void {
    if (this.isHandset()) {
      void this.sidenav()?.close();
    }
  }
}
