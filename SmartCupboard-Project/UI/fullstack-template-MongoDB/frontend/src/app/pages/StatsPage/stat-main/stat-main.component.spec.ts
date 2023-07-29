import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StatMainComponent } from './stat-main.component';

describe('StatMainComponent', () => {
  let component: StatMainComponent;
  let fixture: ComponentFixture<StatMainComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StatMainComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StatMainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
