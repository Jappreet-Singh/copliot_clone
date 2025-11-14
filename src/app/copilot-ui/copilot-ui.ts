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
  // Bindings for user input and copilot response
  public userMessage: string = '';
  public copilotMessage: string = '';
  public isLoading: boolean = false;

  // Store the entire conversation as an array of message pairs
  conversation: { user: string; copilot: string }[] = [];

  constructor(private http: HttpClient) {}
  
  sendMessage() {
    if (!this.userMessage.trim()) return;

    // Add user message to conversation immediately
    const userMsg = this.userMessage;
    this.conversation.push({ user: userMsg, copilot: 'Loading...' });
    this.userMessage = '';
    this.isLoading = true;

    // Send message as query parameter
    this.http
      .post<{ sent_message: string }>(
        `http://127.0.0.1:8000/message?message=${encodeURIComponent(userMsg)}`,
        {
          sent_message: userMsg,
        }
      )
      .subscribe({
        next: (response) => {
          console.log('Message sent to API:', response.sent_message);
        }
      });

    // Get response from API
    this.http.get('http://127.0.0.1:8000/').subscribe({
      next: (response: any) => {
        this.copilotMessage = response.message;
        // Update the last conversation entry with actual response
        this.conversation[this.conversation.length - 1].copilot = this.copilotMessage;
        this.isLoading = false;
        console.log('Response from API:', this.copilotMessage);
      },
      error: (err) => {
        this.conversation[this.conversation.length - 1].copilot = 'Error: Could not get response';
        this.isLoading = false;
      }
    });
  }
}