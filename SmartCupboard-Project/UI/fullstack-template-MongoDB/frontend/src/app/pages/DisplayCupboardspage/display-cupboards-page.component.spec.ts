import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DisplayCupboardsPageComponent } from './display-cupboards-page.component';

describe('DisplayCupboardsPageComponent', () => {
  let component: DisplayCupboardsPageComponent;
  let fixture: ComponentFixture<DisplayCupboardsPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DisplayCupboardsPageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DisplayCupboardsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
