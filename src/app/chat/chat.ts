import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chat',
  imports: [FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class Chat {

  // Bindings for user input and copilot response
  public userMessage: string = '';
  public copilotMessage: string = '';
  public isLoading: boolean = false;

  // Store the entire conversation as an array of message pairs
  conversation: { role: string; content: string }[] = [];

  constructor(private http: HttpClient) {}
  
  sendMessage() {
  if (!this.userMessage.trim()) return;

  // Push user message
  this.conversation.push({
    role: "user",
    content: this.userMessage
  });

  const msg = this.userMessage;
  this.userMessage = "";

  // Temporary loading message
  this.conversation.push({
    role: "assistant",
    content: "Typing..."
  });

  // Send full conversation to backend
  this.http.post<{ response: string }>(
    "http://127.0.0.1:8000/chat",
    { messages: this.conversation }
  ).subscribe({
    next: (res) => {
      // Replace the last "Typing..." placeholder
      this.conversation[this.conversation.length - 1].content = res.response;
    },
    error: () => {
      this.conversation[this.conversation.length - 1].content = "Error: AI not responding";
    }
  });
}


}
