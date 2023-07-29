import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AmiPageComponent } from './ami-page.component';

describe('AmiPageComponent', () => {
  let component: AmiPageComponent;
  let fixture: ComponentFixture<AmiPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AmiPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AmiPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
