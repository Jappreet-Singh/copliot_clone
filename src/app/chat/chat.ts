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
  public selectedFile!: File | null;
  public uploading: boolean = false;

  // Store the entire conversation as an array of message pairs
  conversation: { role: 'user'|'assistant'; content: string;
  type?: 'chat'|'summary'
   }[] = [];

  constructor(private http: HttpClient) {}

  sendMessage() {
    if (!this.userMessage.trim()) return;

    // Push user message
    this.conversation.push({
      role: 'user',
      content: this.userMessage,
    });

    const msg = this.userMessage;
    this.userMessage = '';

    // Temporary loading message
    this.conversation.push({
      role: 'assistant',
      content: 'thinking...',
    });

    const assistantIndex = this.conversation.length - 1;

    // STREAMING API CALL
    fetch('http://127.0.0.1:8000/message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg }),
    })
      .then(async (response) => {
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        let fullReply = '';

        while (true) {
          const { value, done } = await reader!.read();
          if (done) break;

          // Convert streamed bytes → text
          const chunk = decoder.decode(value, { stream: true });
          fullReply += chunk;

          // Update assistant message LIVE
          this.conversation[assistantIndex].content = fullReply;
        }
      })
      .catch(() => {
        this.conversation[assistantIndex].content = 'Error: AI not responding';
      });
  }
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0] || null;
  }

  uploadFile(){
    if (!this.selectedFile) return;
    
    // Temporary loading message
    this.conversation.push({
      role: 'assistant',
      content: 'Summarizing file...',
      type:'summary'
    });

    this.uploading = true;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post<any>('http://127.0.0.1:8000/uploadfile', formData)
    .subscribe({
      next: (res) => {
        // replacing temporary message with actual summary
        const assistantIndex = this.conversation.length - 1;
        this.conversation[assistantIndex].content = `📄 Summary of ${res.filename}:\n\n${res.summary}`;

        this.uploading = false;
        this.selectedFile = undefined!;
      },
      error: () => {
        this.conversation.push({
          role: 'assistant',
          content: 'Error: Failed to summarize file'
        });
        this.uploading = false;
      }
    });
  }
}
