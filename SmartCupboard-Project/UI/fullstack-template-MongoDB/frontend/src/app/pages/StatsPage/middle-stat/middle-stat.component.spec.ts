import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MiddleStatComponent } from './middle-stat.component';

describe('MiddleStatComponent', () => {
  let component: MiddleStatComponent;
  let fixture: ComponentFixture<MiddleStatComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MiddleStatComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MiddleStatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
