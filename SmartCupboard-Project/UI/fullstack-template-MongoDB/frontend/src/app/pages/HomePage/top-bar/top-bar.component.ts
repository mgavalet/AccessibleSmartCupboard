import { Component,OnInit,Output,EventEmitter } from '@angular/core';

@Component({
  selector: 'ami-fullstack-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.scss']
})


export class TopBarComponent implements OnInit {
  
  @Output() newFilterButtonEvent = new EventEmitter<number>();

  sendInfoEvent(value: number) {
    this.newFilterButtonEvent.emit(value); // send info to parent component
  }

  constructor() {
    
  }

  ngOnInit() {}

  pressState = [true,false,false,false,false] ; 
  startButton = 0 ;
  
  public pressButtonFunc(buttonId : number){
    this.pressState[this.startButton] = false;
    this.startButton = buttonId;
    
    this.pressState[buttonId] = true;
    
    this.sendInfoEvent(buttonId) ; // give info into parent component

  }
}
