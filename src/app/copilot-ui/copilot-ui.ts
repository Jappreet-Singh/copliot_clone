import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-copilot-ui',
  imports: [],
  templateUrl: './copilot-ui.html',
  styleUrl: './copilot-ui.css',
})
export class CopilotUi {

   sendMessage(message: string) {
    HttpClient
    
  }

}
