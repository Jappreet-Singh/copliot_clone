import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CopilotUi } from './copilot-ui';

describe('CopilotUi', () => {
  let component: CopilotUi;
  let fixture: ComponentFixture<CopilotUi>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CopilotUi]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CopilotUi);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
