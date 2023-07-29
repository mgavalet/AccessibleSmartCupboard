import { Component, OnInit } from '@angular/core';
import { SocketsService, TasksService } from './global/services';
import { GetData } from 'src/app/global/services/getData/getData'; 

@Component({
  selector: 'ami-fullstack-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  constructor(private socketsService: SocketsService, public getDataService : GetData) {
    // Connect to sockets server on startup
    this.socketsService.initAndConnect();

    //How to consume an event
    this.socketsService.syncMessages('eventName').subscribe((data)=>{
      console.log('The message i received for this event is: ', data);
    });
  }

  public onRightClick(){ // disable right click 
    return false ;
  }

}
