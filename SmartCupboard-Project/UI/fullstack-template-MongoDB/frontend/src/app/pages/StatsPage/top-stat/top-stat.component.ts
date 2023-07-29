import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ami-fullstack-top-stat',
  templateUrl: './top-stat.component.html',
  styleUrls: ['./top-stat.component.scss']
})
export class TopStatComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  pressState = [true,false] ; 
  startButton = 0 ;

  public pressButtonFunc(buttonId : number){
    this.pressState[this.startButton] = false;
    this.startButton = buttonId;
    
    this.pressState[buttonId] = true;
  
  }

}