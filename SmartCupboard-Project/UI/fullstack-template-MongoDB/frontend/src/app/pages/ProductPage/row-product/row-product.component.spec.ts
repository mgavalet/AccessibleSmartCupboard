import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RowProductComponent } from './row-product.component';

describe('RowProductComponent', () => {
  let component: RowProductComponent;
  let fixture: ComponentFixture<RowProductComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RowProductComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RowProductComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
