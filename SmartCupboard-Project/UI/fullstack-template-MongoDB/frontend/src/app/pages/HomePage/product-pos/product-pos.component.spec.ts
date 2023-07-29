import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductPosComponent } from './product-pos.component';

describe('ProductPosComponent', () => {
  let component: ProductPosComponent;
  let fixture: ComponentFixture<ProductPosComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProductPosComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductPosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
