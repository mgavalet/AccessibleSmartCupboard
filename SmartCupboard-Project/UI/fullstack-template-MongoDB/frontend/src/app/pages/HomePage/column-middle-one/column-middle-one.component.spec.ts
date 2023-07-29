import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ColumnMiddleOneComponent } from './column-middle-one.component';

describe('ColumnMiddleOneComponent', () => {
  let component: ColumnMiddleOneComponent;
  let fixture: ComponentFixture<ColumnMiddleOneComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ColumnMiddleOneComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ColumnMiddleOneComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
