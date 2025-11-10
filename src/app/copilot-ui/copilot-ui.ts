import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-copilot-ui',
  imports: [FormsModule],
  templateUrl: './copilot-ui.html',
  styleUrls: ['./copilot-ui.css'],
})
export class CopilotUi {
  public userMessage: string = '';
  public copilotMessage: string = '';

  constructor(private http: HttpClient) {}
  sendMessage() {
    this.http.get('http://127.0.0.1:8000/').subscribe((response: any) => {
      this.copilotMessage = response.message;
      console.log('Response from API:', this.copilotMessage, this.userMessage);
    });
  }
}
