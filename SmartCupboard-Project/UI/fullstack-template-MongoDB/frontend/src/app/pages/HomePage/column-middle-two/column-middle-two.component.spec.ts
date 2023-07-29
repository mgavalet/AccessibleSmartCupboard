import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ColumnMiddleTwoComponent } from './column-middle-two.component';

describe('ColumnMiddleTwoComponent', () => {
  let component: ColumnMiddleTwoComponent;
  let fixture: ComponentFixture<ColumnMiddleTwoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ColumnMiddleTwoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ColumnMiddleTwoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
