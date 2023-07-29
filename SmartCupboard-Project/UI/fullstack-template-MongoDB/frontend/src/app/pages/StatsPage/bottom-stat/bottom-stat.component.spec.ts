import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BottomStatComponent } from './bottom-stat.component';

describe('BottomStatComponent', () => {
  let component: BottomStatComponent;
  let fixture: ComponentFixture<BottomStatComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BottomStatComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BottomStatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
