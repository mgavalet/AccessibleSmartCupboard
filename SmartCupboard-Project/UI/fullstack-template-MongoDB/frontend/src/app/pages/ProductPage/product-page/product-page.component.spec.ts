import { async, ComponentFixture, TestBed } from '@angular/core/testing';

// import { ProductPageComponent } from './product-page.component';
import { ProductPageComponent } from '/home/marios/Desktop/smart_git/SmartCupboard_569/SmartCupboard_ThesisProject/code_in_Course_template_RPI-UI-MongoDB/frontend/src/app/pages/ProductPage/product-page/product-page.component.ts';

describe('ProductPageComponent', () => {
  let component: ProductPageComponent;
  let fixture: ComponentFixture<ProductPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProductPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProductPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
