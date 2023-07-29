import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopStatComponent } from './top-stat.component';

describe('TopStatComponent', () => {
  let component: TopStatComponent;
  let fixture: ComponentFixture<TopStatComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopStatComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopStatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
